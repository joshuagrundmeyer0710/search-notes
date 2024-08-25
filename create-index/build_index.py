"""
Filename: build_index.py

Author: Szymon Manduk

Company: Szymon Manduk AI, manduk.ai

Description: 

Copyright (c) 2024 Szymon Manduk AI.
"""

from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
import re
import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import OpenAIEmbeddings

# Load the environment variables
_ = load_dotenv(find_dotenv(filename='.env'))

# OpenAI API data (for embeddings)
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_version = "2023-05-15"
model = "text-embedding-ada-002"

# Initialize the embeddings
embeddings = OpenAIEmbeddings(
    openai_api_key=openai_api_key, 
    openai_api_version=openai_api_version, 
    model=model
)
embedding_function = embeddings.embed_query

# Azure AI Search data (for vector store)
vector_store_address = os.getenv("AZURESEARCH_ENDPOINT") 
vector_store_password = os.getenv("AZURESEARCH_ADMIN_KEY")
# The name of the index will be stored in the environment variables, but for now, we will hardcode it here
print("Change where the index name is stored in the code to use the environment variable")
# vector_store_index = os.getenv("AZURESEARCH_INDEX_NAME")
vector_store_index = "google-notes-index"

# Initialize the vector store
vector_store = AzureSearch(
    azure_search_endpoint=vector_store_address,
    azure_search_key=vector_store_password,
    index_name=vector_store_index,
    embedding_function=embedding_function,
)

# Function to parse the text file
def parse_text_file(file_content):
    entries = re.split(r'\n####\n', file_content)
    documents = []
    for entry in entries:
        if entry.strip():
            lines = entry.strip().split('\n')
            title = content = label = ""
            for line in lines:
                if line.startswith("Title:"):
                    title = line.replace("Title:", "").strip()
                elif line.startswith("Content:"):
                    content = line.replace("Content:", "").strip()
                elif line.startswith("Label:"):
                    label = line.replace("Label:", "").strip()
            documents.append(Document(page_content=content, metadata={"title": title, "label": label}))
    return documents

# Load and parse the text file
with open("raw-data/Notes/joined_notes.txt", "r", encoding="utf-8") as file:
    file_content = file.read()
documents = parse_text_file(file_content)

print(f"Read {len(documents)} documents from the file.")
# Sort the documents by length in ascending order
sorted_documents = sorted(documents, key=lambda doc: len(doc.page_content))

# Print the 10 shortest documents
for i in range(200):
    print(f"Document {i+1} (length {len(sorted_documents[i].page_content)}): {sorted_documents[i].page_content}")


# Create text splitter
text_splitter = CharacterTextSplitter(chunk_size=1, chunk_overlap=0)

# Split the documents
split_docs = text_splitter.split_documents(documents)

print(f"Split the documents into {len(split_docs)} chunks.")

# # Ask a user if they want to build the index
# create_index = input("Do you want to build the index? (y/n): ")
# if create_index.lower() != "y":
#     print("Index build aborted.")
#     exit()

# # Add documents to the vector store
# vector_store.add_documents(documents=split_docs)
