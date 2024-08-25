"""
Filename: create_empty_index.py

Author: Szymon Manduk

Company: Szymon Manduk AI, manduk.ai

Description: This file contains the code to create an empty custom index in Azure AI Search.

Copyright (c) 2024 Szymon Manduk AI.
"""

from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)
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
# The name of the index will be stored in the environment variables, but for now, we will hardcode it here
print("Change where the index name is stored in the code to use the environment variable")
# vector_store_index = os.getenv("AZURESEARCH_INDEX_NAME")
vector_store_index = "google-notes-index"

# Define the index schema
fields = [
    SimpleField(
        name="chunk_id",  # This is the mandatory field
        type=SearchFieldDataType.String,
        key=True,
        filterable=True,
    ),
    SearchableField(
        name="chunk",  # This is the mandatory field
        type=SearchFieldDataType.String,
        searchable=True,
    ),
    SearchField(
        name="text_vector",  # This is the mandatory field
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=len(embedding_function("Text")),
        vector_search_profile_name="myHnswProfile",
    ),
    SearchableField(
        name="content",
        type=SearchFieldDataType.String,
        searchable=True,
    ),
    SearchableField(
        name="metadata",
        type=SearchFieldDataType.String,
        searchable=True,
    ),
    SearchableField(
        name="title",
        type=SearchFieldDataType.String,
        searchable=True,
    ),
    SimpleField(
        name="label",
        type=SearchFieldDataType.String,
        filterable=True,
    ),
]

vector_store = AzureSearch(
    azure_search_endpoint=vector_store_address,
    azure_search_key=vector_store_password,
    index_name=vector_store_index,
    embedding_function=embedding_function,
    fields=fields,
)
