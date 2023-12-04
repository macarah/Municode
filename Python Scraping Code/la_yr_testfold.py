import requests
import time
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


url_list = [
     "https://library.municode.com/ca/los_angeles_county/codes/code_of_ordinances/189447", #10-08-2012
     "https://library.municode.com/ca/los_angeles_county/codes/code_of_ordinances/208697", #09-27-2013
     "https://library.municode.com/ca/los_angeles_county/codes/code_of_ordinances/229682", #09-11-2014
     "https://library.municode.com/ca/los_angeles_county/codes/code_of_ordinances/253976", #10-05-2015
     "https://library.municode.com/ca/los_angeles_county/codes/code_of_ordinances/278482", #10-05-2016
     "https://library.municode.com/ca/los_angeles_county/codes/code_of_ordinances/304298", #09-27-2017
     "https://library.municode.com/ca/los_angeles_county/codes/code_of_ordinances/328365", #09-18-2018
     "https://library.municode.com/ca/los_angeles_county/codes/code_of_ordinances/349596", #09-19-2019
     "https://library.municode.com/ca/los_angeles_county/codes/code_of_ordinances/370506", #09-28-2020
     "https://library.municode.com/ca/los_angeles_county/codes/code_of_ordinances/391668", #09-29-2021
     "https://library.municode.com/ca/los_angeles_county/codes/code_of_ordinances/410890", #10-10-2022
     "https://library.municode.com/ca/los_angeles_county/codes/code_of_ordinances/418767", #10-09-2023
]

names = ["10-08-2012_Codes", "09-27-2013_Codes", "09-11-2014_Codes", "10-05-2015_Codes", "10-05-2016_Codes", "09-27-2017_Codes", "09-18-2018_Codes", "09-19-2019_Codes", "09-28-2020_Codes", "09-29-2021_Codes", "10-10-2022_Codes", "10-09-2023_Codes"]
# Use Selenium to open the webpage
driver = webdriver.Chrome()  # You'll need to download the appropriate WebDriver for your browser


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
        
        # Wait for <li> elements with nodedepth="2"
        wait = WebDriverWait(driver, 5)
        click_load_more_button(driver)
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

base_directory = "/Users/macarahmorgan/Guldi-Lab/Sample/LosAngeles_Overtime"

try:
    for index, url in enumerate(url_list):
        driver.get(url)

        # Wait for the page to load completely (you might need to adjust the wait time)
        driver.implicitly_wait(10)

        # Get the page source after JavaScript execution
        page_source = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")
        city_link = url

        # Find the parent container by class (if applicable)
        parent_container = soup.find('div', class_='parent-container')

        folder_name = names[index]

        # Create city directory inside the state directory
        year_directory = os.path.join(base_directory, folder_name)
        os.makedirs(year_directory, exist_ok=True)


        driver.get(city_link) 

        driver.implicitly_wait(5)

        try:
                    # Use explicit wait to wait for the elements to be present
                        wait = WebDriverWait(driver, 5)
                        
                        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li[ng-repeat="node in toc.topLevelNodes track by node.Id"]')))
                        
                        # Get the page source after JavaScript execution
                        page_source = driver.page_source

                        # Parse the page source with BeautifulSoup
                        soup = BeautifulSoup(page_source, "html.parser")
                        click_load_more_button(driver)
                        

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
                                
                                click_load_more_button(driver)
                                #while a link is returned call again
                                extract_sub_links(href_link, year_directory, heading_text)
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
                                        
                                        click_load_more_button(driver)
                                        #while a link is returned call again
                                        extract_sub_links(href_link, year_directory, heading_text)
                            except Exception as e:
                                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li[ng-repeat="node in toc.topLevelNodes track by node.Id"]')))
                        
                                # Get the page source after JavaScript execution
                                page_source = driver.page_source

                                # Parse the page source with BeautifulSoup
                                soup = BeautifulSoup(page_source, "html.parser")
                                click_load_more_button(driver)
                                

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
                                        
                                        click_load_more_button(driver)
                                        #while a link is returned call again
                                        extract_sub_links(href_link, year_directory, heading_text)

finally:
    # Close the browser after extraction
    driver.quit()