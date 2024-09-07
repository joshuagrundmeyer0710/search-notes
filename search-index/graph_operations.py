"""
Filename: graph_operations.py

Author: Szymon Manduk

Company: Szymon Manduk AI, manduk.ai

Description: This module defines the GraphOperations class, which contains nodes operations of the graph: retrieve, evaluate, generate and search-web.

Copyright (c) 2024 Szymon Manduk AI.
"""

from langchain.schema import Document

class GraphOperations:
    def __init__(self, retriever, main_chain, eval_chain, web_search_tool):
        self.retriever = retriever
        self.main_chain = main_chain
        self.eval_chain = eval_chain
        self.web_search_tool = web_search_tool


    # Retrieves documents using previously defined retriever. Consumes a state with a question.
    # Returns a new state with documents added and appended step
    def retrieve(self, state):
        question = state["question"]

        documents = self.retriever.retrieve(question)
        
        steps = state["steps"] if state["steps"] is not None else []
        steps.append("retrieve_documents")
        
        return {
            "documents": documents, 
            "question": question, 
            "steps": steps
        }


    # Generates an answer using previously defined main_chain. Consumes a state with a question and documents. 
    # Returns a new state with answer added and appended step
    def generate(self, state):
        question = state["question"]
        documents = state["documents"]
        search_required = state["search_required"]
        search_results = state["search_results"]
        
        # if search was required and results are available, we use them instead of retrieved documents
        if search_required and search_results:
            documents = search_results

        answer = self.main_chain.generate(question, documents)

        steps = state["steps"]
        steps.append("generate_answer")
        
        return {
            "documents": documents,
            "question": question,
            "answer": answer,
            "search_required": search_required,
            "search_results": search_results,
            "steps": steps,
        }


    # Evaluates if the documents are relevant to the question. Consumes a state with a question and documents.
    # Returns a new state with search_required added and appended step
    def evaluate(self, state):
        question = state["question"]
        documents = state["documents"]
        steps = state["steps"]
        steps.append("evaluate_retrieval")

        # Evaluate if the documents are relevant to the question
        evaluation = self.eval_chain.evaluate(question, documents)

        # if the evaluation is negative we set search_required to True
        search_required = False
        search_required = evaluation["Evaluation"] == "no"

        return {
            "documents": documents,
            "question": question,
            "search_required": search_required,
            "steps": steps,
        }


    # Searches the web for documents that may help to answer the question. Consumes the question.
    # Returns the search results.
    def web_search(self, state):
        question = state["question"]
        documents = state["documents"]
        search_required = state["search_required"]
        steps = state["steps"]
        steps.append("web_search")
        
        # results = web_search_tool.invoke({"query": question})
        results = self.web_search_tool.search(question)

        search_results = [
            Document(page_content=doc["content"], metadata={"url": doc["url"]})
            for doc in results
        ]

        return {
            "documents": documents, 
            "question": question,
            "search_required": search_required,
            "search_results": search_results,
            "steps": steps
        }
    

    def determine_next_node(self, state):
        return "web_search" if state["search_required"] else "generate"
