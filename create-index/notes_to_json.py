"""
Filename: notes_to_json.py

Author: Szymon Manduk

Company: Szymon Manduk AI, manduk.ai

Description: 
This script reads Google Notes exported as HTMLs and extracts the title, content, and label of each note. 
The extracted information is then saved to a correspoding json file.

Copyright (c) 2024 Szymon Manduk AI.
"""
import glob
import json
from bs4 import BeautifulSoup
import os

# Directory containing the HTML files
input_directory = 'raw-data/Notes'
output_directory = 'raw-data/Notes/json'
encoding = 'utf-8'
length_threshold = 100  # Minimum number of characters in the content of a note

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Get a list of all HTML files in the input directory
html_files = glob.glob(os.path.join(input_directory, '*.html'))

# Process each HTML file
correct = 0
incorrect = 0
for file in html_files:
    try:
        with open(file, 'r', encoding=encoding) as f:
            soup = BeautifulSoup(f, 'html.parser')
            body = soup.find('body')
            if body:
                v_title = body.find('div', class_='title').text.strip() if body.find('div', class_='title') else ''

                v_content = body.find('div', class_='content').text.strip() if body.find('div', class_='content') else ''
                # Skip if content is less than the threshold
                if len(v_content) < length_threshold:
                    continue

                v_label = body.find('span', class_='label-name').text.strip() if body.find('span', class_='label-name') else ''

                # Prepare data for JSON
                data = {
                    "title": v_title,
                    "content": f"{v_title}\n{v_content}",
                    "label": v_label
                }

                # Write the information to a JSON file
                output_filename = os.path.splitext(os.path.basename(file))[0] + ".json"
                output_path = os.path.join(output_directory, output_filename)
                with open(output_path, 'w', encoding=encoding) as output_file:
                    json.dump(data, output_file, ensure_ascii=False, indent=2)
                correct += 1
    except Exception as e:
        incorrect += 1
        print(f"Error processing {file}: {str(e)}. File skipped.")
        # delete the file
        os.remove(output_path)

print(f'Processed {correct} notes. {incorrect} notes were skipped due to errors.')
