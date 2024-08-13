# for all files in this directory remove "Q: " and "A: " prefixes
# and save them in the same directory with the name "cleaned-<filename>"
import os
import re

# change directory to raw-data/QnAs%20-%20txt
os.chdir("raw-data/QnAs - txt")

# print current directory
print(os.getcwd())

def remove_prefixes(file):
    print("Cleaning file: ", file)
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open("cleaned-"+file, 'w', encoding='utf-8') as f:
        for line in lines:
            if not line.strip(): # every line that is empty replace with "\n####\n"
                f.write("####\n\n")
            else: # remove "Q: " and "A: " prefixes
                f.write(re.sub(r'^(Q|A): ', '', line))


for file in os.listdir():
    if file.endswith(".txt") and not file.startswith("cleaned-"):
        remove_prefixes(file)

