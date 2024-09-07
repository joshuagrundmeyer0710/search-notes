"""
Filename: eval_chain.py

Author: Szymon Manduk

Company: Szymon Manduk AI, manduk.ai

Description: Defines a class that represents a chain for evaluating if retrieved documents are sufficient to answer a given query.

Copyright (c) 2024 Szymon Manduk AI.
"""

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class EvalChain:
    """
    A class representing a chain for evaluating if retrieved documents are sufficient to answer a given query.

    Attributes:
        provider (str): The provider for the evaluator model. Default is "ollama", other option is "openai".
        temperature (int): The temperature parameter for generating responses. Default is 0.
        prompt (PromptTemplate): The template for generating prompts.
        llm (ChatOllama or ChatOpenAI): The language model for generating responses.
        eval_chain (Chain): The chain for generating responses

    Methods:
        evaluate(self, question, documents): Evaluates if the documents are sufficient to answer the question.

    """

    def __init__(self, provider = "ollama", temperature = 0):
        self.provider = provider
        self.temperature = temperature
        self.prompt = PromptTemplate(
            template="""Your task is to carefully evaluate if information in Documents provided below is sufficient for answering User Question.  
            User Question: {question} 
            Documents: {documents} 
            Return your Evaluation in JSON format with a single key 'Evaluation' and binary score 'yes' or 'no'. No other keys, values or preambles are allowed.
            
            Evaluation: 
            """,
            input_variables=["question", "documents"],
        )
        
        if self.provider == "openai":
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, model_kwargs={"response_format": {"type": "json_object"}},
            )
        elif self.provider == "ollama":
            self.llm = ChatOllama(model="llama3.1", temperature=0, format="json")
        else:
            raise ValueError("Invalid provider. Please choose 'openai' or 'ollama'.")
        
        self.eval_chain = self.prompt | self.llm | JsonOutputParser()
    
    def evaluate(self, question, documents):
        return self.eval_chain.invoke({"documents": documents, "question": question})
    