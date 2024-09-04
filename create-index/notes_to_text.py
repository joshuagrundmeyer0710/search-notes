"""
Filename: notes_to_text.py

Author: Szymon Manduk

Company: Szymon Manduk AI, manduk.ai

Description: 
This script reads Google Notes exported as HTMLs and extracts the title, content, and label of each note. 
The extracted information is then saved to a text file.

Copyright (c) 2024 Szymon Manduk AI.
"""

import glob
from bs4 import BeautifulSoup
import os

# Directory containing the HTML files
input_directory = 'data/Notes'
output_directory = 'data/Notes/txt'
encoding = 'utf-8'
length_threshold = 100  # Minimum number of characters in the content of a note

# Get a list of all HTML files in the input directory
html_files = glob.glob(input_directory + '/*.html')

# Process each HTML file
correct = 0
incorrect = 0
for file in html_files:
    with open(file, 'r', encoding=encoding) as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        body = soup.find('body')
        if body:
            title = body.find('div', class_='title')
            v_title = title.text if title else ''
            
            content = body.find('div', class_='content')
            v_content = content.text if content else ''
            
            # if content is less than a samll number of characters, then skip it
            if len(v_content) < length_threshold:
                continue

            label = body.find('span', class_='label-name')
            v_label = label.text if label else ''
            
            # append information to a file
            try:
                with open(output_directory + "/" + os.path.splitext(os.path.basename(file))[0] + ".txt", 'w', encoding=encoding) as output_file:
                    output_file.write(f'Title: {v_title}\n')
                    output_file.write(f'Content: {v_title}\n{v_content}\n')
                    output_file.write(f'Label: {v_label}\n')
                correct += 1
            except UnicodeEncodeError as e:
                incorrect += 1
                # print(f"Encoding error occurred: {e}. Skipping this entry.")
                # delete the file
                os.remove(output_directory + "/" + os.path.splitext(os.path.basename(file))[0] + ".txt")

print(f'Processed {correct} notes. {incorrect} notes were skipped due to encoding errors.')
