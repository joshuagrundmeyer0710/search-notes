"""
Filename: create_empty_index.py

Author: Szymon Manduk

Company: Szymon Manduk AI, manduk.ai

Description: This file contains the code to create an empty custom index in Azure AI Search.

Copyright (c) 2024 Szymon Manduk AI.
"""

import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import OpenAIEmbeddings
from index_fields import fields

# Load the environment variables
_ = load_dotenv(find_dotenv(filename='.env'))

# OpenAI API data (for embeddings)
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_version = "2023-05-15"
model = "text-embedding-ada-002"

# Ask a user if they want to create the index
create_index = input("Do you want to create the index? (y/n): ")
if create_index.lower() != "y":
    print("Index creation aborted.")
    exit()

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

vector_store = AzureSearch(
    azure_search_endpoint=vector_store_address,
    azure_search_key=vector_store_password,
    index_name=vector_store_index,
    embedding_function=embedding_function,
    fields=fields,
)

print("Index created successfully.")