"""
Filename: build_index.py

Author: Szymon Manduk

Company: Szymon Manduk AI, manduk.ai

Description: This script reads documents from a directory, splits them into chunks, and adds them to the Azure Search index.

Copyright (c) 2024 Szymon Manduk AI.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import json
import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import OpenAIEmbeddings
from uuid import uuid4
from index_fields import fields

# Load the environment variables
_ = load_dotenv(find_dotenv(filename='.env'))

directory = 'data/Notes/json'

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
vector_store_index = os.getenv("AZURESEARCH_INDEX_NAME")

# Initialize the vector store
vector_store = AzureSearch(
    azure_search_endpoint=vector_store_address,
    azure_search_key=vector_store_password,
    index_name=vector_store_index,
    embedding_function=embedding_function,
    fields=fields,
)

# for each json file in the directory we append the content to the documents list
documents = []
for file in os.listdir(directory):
    # if the file is not a json file we skip it
    if not file.endswith(".json"):
        continue

    # Load and parse the json file
    with open(directory + "/" + file, "r", encoding="utf-8") as file:
        data = json.load(file)
        documents.append(Document(page_content=data["content"], metadata={"title": data["title"], "label": data["label"]}))

print(f"Read {len(documents)} documents from the file.")

# Sort the documents by length in ascending order
sorted_documents = sorted(documents, key=lambda doc: len(doc.page_content))

# # Print few shortest documents
# for i in range(8):
#     print(sorted_documents[i])
#     #print(f"Document {i+1} (length {len(sorted_documents[i].page_content)}): {sorted_documents[i].page_content} - {sorted_documents[i].metadata}")

# Generate a unique ID for the split
def generate_id():
    return str(uuid4())

# Create text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, 
    chunk_overlap=100,
    separators=["\n\n", ".", "!", "?", "\n"],
    # add_start_index=True,  # Optionally - it adds the starting position for each chunk within the split (0 for the first chunk) 
)

# Split the documents
split_docs = text_splitter.split_documents(documents)
print(f"Split the documents into {len(split_docs)} chunks.")

# Let's add IDs for each chunk ina separate list
ids = [generate_id() for split in split_docs]

# Print the content of the first few chunks
for i in range(10):
    print(f"Content for [{i}]: {split_docs[i]}")
    print(f"ID for [{i}]: {ids[i]}\n\n")

# Ask a user if they want to build the index
create_index = input("Do you want to build the index? (y/n): ")
if create_index.lower() != "y":
    print("Index build aborted.")
    exit()

# Add documents to the vector store
results = vector_store.add_documents(documents=split_docs, ids=ids)

print(results[:5])
