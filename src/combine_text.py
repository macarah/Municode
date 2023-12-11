import os

base_directory = "/Users/macarahmorgan/Guldi-Lab/Municode/Los Angeles Building Codes (2012-2018)--txt"
output_directory = "/Users/macarahmorgan/Guldi-Lab/txt to csv"

# Create the output directory if it does not exist
os.makedirs(output_directory, exist_ok=True)

def combine_txt_files(folder_path, output_directory):
    # Get the name of the current folder without the "_Codes" part
    folder_name = os.path.basename(folder_path)
    folder_name = folder_name.split("_Codes")[0]
    output_file_path = os.path.join(output_directory, f"{folder_name}.txt")

    # Create a dictionary to store text content based on the grouping key
    text_dict = {}

    # Iterate through files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)

                # Extract the grouping key from the file name
                if "-" in file:
                    key = file.split("-")[0]  # Get text before the first dash
                    if len(file.split("-")) > 1:  # Check if a second dash exists
                        key = file.split("-", 2)[1]  # Get text between the first and second dash
                else:
                    key = file.split(".txt")[0]  # If no dash, use the filename without extension

                # Combine text content for each key
                with open(file_path, 'r', encoding='utf-8') as input_file:
                    content = input_file.read()
                    if key in text_dict:
                        text_dict[key] += content
                    else:
                        text_dict[key] = content

    # Write combined text content to output files based on the keys
    for key, content in text_dict.items():
        combined_file_name = f"{folder_name}_{key}.txt" if not key.endswith('.txt') else f"{folder_name}_{key}"
        combined_file_path = os.path.join(output_directory, combined_file_name)
        with open(combined_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(content)

    print(f"All the text files from {folder_name} have been combined based on the key.")

# Call the function for each subfolder in the base directory
for subfolder in os.listdir(base_directory):
    subfolder_path = os.path.join(base_directory, subfolder)
    if os.path.isdir(subfolder_path):
        combine_txt_files(subfolder_path, output_directory)
