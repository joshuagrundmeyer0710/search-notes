"""
Filename: main_chain.py

Author: Szymon Manduk

Company: Szymon Manduk AI, manduk.ai

Description: Defines a class that represents a main chain for question-answering tasks.

Copyright (c) 2024 Szymon Manduk AI.
"""

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class MainChain:
    """
    A class representing a main chain for question-answering tasks.

    Attributes:
        provider (str): The provider for the question-answering model. Default is "ollama", other option is "openai".
        temperature (int): The temperature parameter for generating responses. Default is 0.
        prompt (PromptTemplate): The template for generating prompts.
        llm (ChatOllama or ChatOpenAI): The language model for generating responses.
        chain (Chain): The chain for generating responses

    Methods:
        generate(self, question, documents): Generates a response for the given question and documents.

    """
    def __init__(self, provider = "ollama", temperature = 0):
        self.provider = provider
        self.temperature = temperature
        self.prompt = PromptTemplate(
            template="""You are an assistant for question-answering tasks. 
            Analyze carefully and use the following documents to answer the user question. 
            If you don't know the answer, just say that you don't know. Do not make up an answer. 
            Keep your answer short and to the point.
            Question: {question} 
            Documents: {documents} 
            Answer: 
            """,
            input_variables=["question", "documents"],
        )
        
        if self.provider == "openai":
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=self.temperature)
        elif self.provider == "ollama":
            self.llm = ChatOllama(model="llama3.1", temperature=self.temperature)
        else:
            raise ValueError("Invalid provider. Please choose 'openai' or 'ollama'.")
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def generate(self, question, documents):
        return self.chain.invoke({"documents": documents, "question": question})
