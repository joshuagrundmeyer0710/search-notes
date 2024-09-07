"""
Filename: retriever.py

Author: Szymon Manduk

Company: Szymon Manduk AI, manduk.ai

Description: Defines a class that retrieves documents from Azure AI Seearch based on a given question.

Copyright (c) 2024 Szymon Manduk AI.
"""

from langchain_openai import OpenAIEmbeddings
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores.azuresearch import AzureSearch

class Retriever:
    """
    A class that retrieves documents from Azure AI Search based on a given question.

    Args:
        openai_api_key (str): The API key for OpenAI.
        open_ai_api_version (str): The version of the OpenAI API.
        embedding_model_name (str): The name of the embedding model.
        embedding_provider (str): The provider of the embedding model: openai or azure.
        vector_store_address (str): The address of the vector store.
        vector_store_password (str): The password for the vector store.
        vector_store_index (str): The index name of the vector store.
        retrieved_documents (int, optional): The number of documents to retrieve. Defaults to 3.
        search_type (str, optional): The type of search to perform. Defaults to "hybrid". Other option is "similarity".

    Attributes:
        embeddings (Embeddings): The embedding function used for querying.
        vector_store (AzureSearch): The vector store interface for document search.
        retriever (Retriever): The retriever object for invoking searches.

    Methods:
        retrieve(question: str) -> List[Document]:
            Retrieves documents based on the given question.
    """

    def __init__(self, openai_api_key, open_ai_api_version, embedding_model_name, embedding_provider, vector_store_address, vector_store_password, vector_store_index, retrieved_documents=3, search_type="hybrid"):
        self.openai_api_key = openai_api_key
        self.openai_api_version = open_ai_api_version
        self.model = embedding_model_name
        self.vector_store_address = vector_store_address
        self.vector_store_password = vector_store_password
        self.vector_store_index = vector_store_index
        self.retrieved_documents = retrieved_documents
        self.search_type = search_type
        
        if embedding_provider == "openai":
            self.embeddings = OpenAIEmbeddings(
            openai_api_key=self.openai_api_key,
            openai_api_version=self.openai_api_version,
            model=self.model
            )
        elif embedding_provider == "azure":
            #ToDo: Add token provider
            print("Add token provider!")
            self.embeddings = AzureOpenAIEmbeddings(
            model=self.model,
            azure_endpoint=self.vector_store_address,
            azure_ad_token_provider=None
            )
        else:
            raise ValueError("Invalid embedding provider. Please choose 'openai' or 'azure'.")
        
        self.vector_store = AzureSearch(
            azure_search_endpoint=self.vector_store_address,
            azure_search_key=self.vector_store_password,
            index_name=self.vector_store_index,
            embedding_function=self.embeddings.embed_query,
        )
        
        self.retriever = self.vector_store.as_retriever(k=self.retrieved_documents, search_type=self.search_type)
    
    def retrieve(self, question):
        return self.retriever.invoke(question)
