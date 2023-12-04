import requests
import time
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


url = "https://library.municode.com/#G"

# Use Selenium to open the webpage
driver = webdriver.Chrome()  # You'll need to download the appropriate WebDriver for your browser
driver.get(url)

# Wait for the page to load completely (you might need to adjust the wait time)
driver.implicitly_wait(10)

# Get the page source after JavaScript execution
page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")


#defining text conversion function
def extract_and_save_text(url, output_folder, file_name):
    driver = None
    try:
        # Check if the output folder exists, if not, create it
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Concatenate .txt extension to the file name if it's not already there
        file_name = file_name.replace(" - ", "-")
        file_name = file_name.replace(" ", "_")
        if not file_name.endswith('.txt'):
            file_name += '.txt'
        
        # Limit the file path to the specified folder and file name
        output_file_path = os.path.join(output_folder, file_name)
        
        # Check if the file already exists, if yes, don't append
        if os.path.exists(output_file_path):
            print(f"File '{output_file_path}' already exists. Not appending the extracted text.")
            return
        
        # Use Selenium to open the webpage
        driver = webdriver.Chrome()
        driver.get(url)
        
        # Wait for the page to load completely (you might need to adjust the wait time)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'chunks')))
        
        # Remove elements with class "btn-group action-bar text-primary hidden-xs pull-right" using JavaScript
        script = """
        var elements = document.querySelectorAll('.btn-group.action-bar.text-primary.hidden-xs.pull-right');
        elements.forEach(function(element) {
            element.remove();
        });
        """
        driver.execute_script(script)
        
        # Find elements with class "chunks"
        chunk_elements = driver.find_elements(By.CLASS_NAME, 'chunks')
        
        # Extract text from chunk elements
        text_content = ""
        for chunk in chunk_elements:
            text_content += chunk.text.strip() + '\n'
        
        # Save the extracted text to a text file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(text_content)
        
        print(f"Text extracted and saved to {output_file_path}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Make sure to close the browser after extraction
        if driver:
            driver.quit()

old_link = ''
def extract_sub_links(link, directory, heading_text):
    global old_link
    # Initialize the WebDriver
    driver = webdriver.Chrome()

    try:
        # Head to the provided link
        driver.get(link)
        click_load_more_button(driver)
        # Wait for <li> elements with nodedepth="2"
        wait = WebDriverWait(driver, 5)
        if(link==old_link):
            li_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[nodedepth="3"]')))
        else:
            li_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[nodedepth="2"]')))

        # Traverse through <li> elements and extract heading text and href links from <a> tags
        for li_element in li_elements:
            a_element = li_element.find_element(By.TAG_NAME, "a")
            head_text = a_element.text.strip()
            href_link = a_element.get_attribute('href')
            print(f"Sub-Chapter: {head_text}")
            print(f"Sub-Link: {href_link}")
            result_string = heading_text + "-" + head_text
            old_link = href_link
            extract_sub_links(href_link, directory, result_string)
            print("---")
        
    except Exception as e:
        print(f"No elements with nodedepth='2' found. Error: {str(e)}")
        
        # Call the function to extract and save text to a file (you need to provide this function)
        extract_and_save_text(link, directory, heading_text)
        print("---")

def click_load_more_button(driver):
    while True:
        try:
            # Wait for the button to be clickable
            load_more_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Load more')]"))
            )
            
            if load_more_button:
                # If the button is found, click it
                load_more_button.click()
                print("Clicked the 'Load more' button.")
        except TimeoutException:
            # If the button is not found within the given time, print a message and break the loop
            print("No more 'Load more' buttons found or not clickable.")
            break

# Find state links
state_links_elements = soup.find_all("li", {"ng-repeat": "state in stateGroup.states"}, class_="col-xs-12 col-md-6 col-lg-4 text-center")

# Extract state links and names
state_data = []
for state_element in state_links_elements:
    state_name = state_element.text.strip()
    state_link = state_element.find("a")["href"]
    state_data.append({"name": state_name, "link": state_link})

# Directory where you want to store the folders
print(os.getcwd())
base_directory = "/Users/macarahmorgan/Guldi-Lab/Municode-Data"


# Iterate through state links and names
for state in state_data:
    state_link = state["link"]
    state_name = state["name"]
    state_directory = os.path.join(base_directory, state_name)
    os.makedirs(state_directory, exist_ok=True)  # Create state folder if not exists

    # Visit the state page
    driver.get(state_link)
    
    # Wait for the state page to load
    driver.implicitly_wait(10)
    
    # Get the page source after JavaScript execution
    state_page_source = driver.page_source
    
    # Parse the state page with BeautifulSoup
    state_soup = BeautifulSoup(state_page_source, "html.parser")

    try:
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[ng-repeat="letterGroup in letterGroups"]')))
    except TimeoutException as ex:
        print(f"Timed out waiting for elements: {ex}")
    
    # Find city elements for the current state
    city_elements = state_soup.find_all("li", {"ng-repeat": "client in letterGroup.clients"}, class_="col-xs-12 col-sm-6 col-md-4 col-lg-3 text-center")
    
    # Extract city names and links for the current state
    city_data = []
    for city_element in city_elements:
        city_name = city_element.text.strip()
        city_link = city_element.find("a")["href"]
        city_data.append({"name": city_name, "link": city_link})
        # Create city directory inside the state directory
        city_directory = os.path.join(state_directory, city_name)
        os.makedirs(city_directory, exist_ok=True)
        print(state_name + ", " + city_name)

        #we only want ordinances from Georgia cities
        if state_name == "Georgia" and city_name=="Atlanta":
            print(city_data)
            driver.get(city_link) #visit the city page of ordinances
            #scrape textual data of ordinances
            #convert to txt file
            #add to city directory folder
            # Wait for the page to load completely (you might need to adjust the wait time)
            driver.implicitly_wait(5)

            try:
            # Use explicit wait to wait for the elements to be present
                wait = WebDriverWait(driver, 5)
                
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li[ng-repeat="node in toc.topLevelNodes track by node.Id"]')))
                
                # Get the page source after JavaScript execution
                page_source = driver.page_source

                # Parse the page source with BeautifulSoup
                soup = BeautifulSoup(page_source, "html.parser")
                

                # Find <li> elements with ng-repeat="node in toc.topLevelNodes track by node.Id"
                chapters = soup.find_all("li", {"ng-repeat": "node in toc.topLevelNodes track by node.Id"})
            
                # Traverse through <li> elements and extract href links from <a> tags
                for li_element in chapters:
                    a_element = li_element.find("a", class_="toc-item-heading")
                    if a_element:
                        heading_text = a_element.text.strip()
                        href_link = a_element["href"]
                        print(f"Section Name: {heading_text}")
                        print(f"Link: {href_link}")
                        print()
                        
                        #while a link is returned call again
                        extract_sub_links(href_link, city_directory, heading_text)
            except Exception as e:
                print(f"An error occurred: {str(e)}") #a "browse" button exists
                #click browse button and try again
                #<a class="btn btn-primary btn-raised" aria-label="Browse Code of Ordinances" href="/ga/alpharetta/codes/code_of_ordinances" ng-href="/ga/alpharetta/codes/code_of_ordinances"><span class="">Browse</span> »</a>
                # Check if the "Browse" button exists
                browse_button = driver.find_element(By.CSS_SELECTOR, 'a.btn.btn-primary.btn-raised[aria-label="Browse Code of Ordinances"]')
                #get new link and assign it to city_link
                if browse_button:
                    browse_button.click()
                    # Wait for the page to load completely
                    try:
                        wait = WebDriverWait(driver, 10)
                        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li[nodedepth="2"]')))

                        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li[ng-repeat="node in toc.topLevelNodes track by node.Id"]')))
                
                        # Get the page source after JavaScript execution
                        page_source = driver.page_source

                        # Parse the page source with BeautifulSoup
                        soup = BeautifulSoup(page_source, "html.parser")
                        

                        # Find <li> elements with ng-repeat="node in toc.topLevelNodes track by node.Id"
                        chapters = soup.find_all("li", {"ng-repeat": "node in toc.topLevelNodes track by node.Id"})
                    
                        # Traverse through <li> elements and extract href links from <a> tags
                        for li_element in chapters:
                            a_element = li_element.find("a", class_="toc-item-heading")
                            if a_element:
                                heading_text = a_element.text.strip()
                                href_link = a_element["href"]
                                print(f"Section Name: {heading_text}")
                                print(f"Link: {href_link}")
                                print()
                                
                                #while a link is returned call again
                                extract_sub_links(href_link, city_directory, heading_text)
                    except Exception as e:
                        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li[ng-repeat="node in toc.topLevelNodes track by node.Id"]')))
                
                        # Get the page source after JavaScript execution
                        page_source = driver.page_source

                        # Parse the page source with BeautifulSoup
                        soup = BeautifulSoup(page_source, "html.parser")
                        

                        # Find <li> elements with ng-repeat="node in toc.topLevelNodes track by node.Id"
                        chapters = soup.find_all("li", {"ng-repeat": "node in toc.topLevelNodes track by node.Id"})
                    
                        # Traverse through <li> elements and extract href links from <a> tags
                        for li_element in chapters:
                            a_element = li_element.find("a", class_="toc-item-heading")
                            if a_element:
                                heading_text = a_element.text.strip()
                                href_link = a_element["href"]
                                print(f"Section Name: {heading_text}")
                                print(f"Link: {href_link}")
                                print()
                                
                                #while a link is returned call again
                                extract_sub_links(href_link, city_directory, heading_text)
                        continue
                    

            
        
    
# Close the WebDriver
driver.quit()
