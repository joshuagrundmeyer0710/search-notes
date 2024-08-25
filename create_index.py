import glob
import glob
from bs4 import BeautifulSoup

# Directory containing the HTML files
directory = 'raw-data/Notes'

# Get a list of all HTML files in the directory
html_files = glob.glob(directory + '/*.html')

# Process each HTML file
cnt = 0
for file in html_files:
    cnt += 1
    if cnt > 5:
        break
    with open(file, 'r', encoding='utf-8') as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        body = soup.find('body')
        if body:
            title = body.find('div', class_='title')
            v_title = title.text if title else ''
            
            content = body.find('div', class_='content')
            v_content = content.text if content else ''
            
            label = body.find('span', class_='label-name')
            v_label = label.text if label else ''
            
            # append information to a file
            with open(directory + '/output.txt', 'a', encoding='utf-8') as output_file:
                output_file.write(f'Title: {v_title}\n')
                output_file.write(f'Content: {v_content}\n')
                output_file.write(f'Label: {v_label}\n')