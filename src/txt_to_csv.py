import csv
import pandas as pd
import os

filelocation = "/Users/macarahmorgan/Guldi-Lab/txt to csv"
output_csv_path = "/Users/macarahmorgan/Guldi-Lab/out csv/out_csv_data.csv"

files = [f for f in os.listdir(filelocation) if f.endswith(".txt")]

filenames = []
content = []
dates = []
chapters = []

for file in files:
    file_name, _ = os.path.splitext(file)  # Remove the ".txt" extension
    parts = file_name.split("_")
    
    # Extracting Date and Chapter from the filename parts
    date = parts[0] if len(parts) >= 1 else None
    chapter = "_".join(parts[1:]) if len(parts) > 1 else None
    
    file_path = os.path.join(filelocation, file)
    with open(file_path, 'r', newline='', encoding='utf-8') as source_file:
        filenames.append(file_name)
        dates.append(date)
        chapters.append(chapter)
        
        lines = source_file.read()
        content.append(lines)

data = {'Filename': filenames, 'Date': dates, 'Chapter': chapters, 'Content': content}

df = pd.DataFrame(data)
print(df)

df.to_csv(output_csv_path, index=False)