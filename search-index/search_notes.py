"""
Filename: search_notes.py

Author: Szymon Manduk

Company: Szymon Manduk AI, manduk.ai

Description: Main script for the search engine. It defines:
- The retriever class that retrieves documents from Azure AI Search based on a given question.
- The main chain class that generates an answer based on the retrieved documents.
- The evaluation chain class that evaluates if the retrieved documents are sufficient to answer the question.
- The web search tool class that performs a web search for additional information.
- The graph builder that builds the graph of operations.
- The graph operations that define the operations in the graph.
- The FastAPI app that serves the API for answering questions.

it can be run in two modes:
- test-mode: to test the graph - this will print the answer and steps for a few hardcoded questions: python search-index\search_notes.py --mode test-mode
- api-mode: to start the FastAPI server that serves the API for answering questions. The API can be accessed locally at on http://127.0.0.1:8000 by default or on the Azure App Service URL. 
    The example command for Azure: az webapp up --name your-api-name --resource-group your-resource-group --runtime "PYTHON:3.9" --sku F1 # or B1
    The example command for local execution: python search-index\search_notes.py --mode api-mode

Copyright (c) 2024 Szymon Manduk AI.
"""

import argparse
from retriever import Retriever
from main_chain import MainChain
from eval_chain import EvalChain
from web_search_tool import WebSearchTool
from graph_builder import build_graph
from graph_operations import GraphOperations
from langchain_core.tracers.context import tracing_v2_enabled
from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv(filename='.env'))
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_version = "2023-05-15"
model = "text-embedding-ada-002"
vector_store_address = os.getenv("AZURESEARCH_ENDPOINT") 
vector_store_password = os.getenv("AZURESEARCH_ADMIN_KEY")
vector_store_index = os.getenv("AZURESEARCH_INDEX_NAME")

# We may choose the provider of intelligence: Ollama (llama3.1) or OpenAI (gpt-4o-mini)
# PROVIDER = "ollama" 
PROVIDER = "openai"

# Define the retriever - it will retrieve documents from the vector store
retriever = Retriever(
    openai_api_key=openai_api_key,
    open_ai_api_version=openai_api_version,
    embedding_model_name=model,
    embedding_provider="openai",
    vector_store_address=vector_store_address,
    vector_store_password=vector_store_password,
    vector_store_index=vector_store_index,
    retrieved_documents=3,
    search_type="hybrid"
)

# Define the main chain - it will generate an answer based on the retrieved documents
main_chain = MainChain(provider=PROVIDER)

# Define the evaluation chain - it will evaluate if the retrieved documents are sufficient to answer the question
eval_chain = EvalChain(provider=PROVIDER)

# Define websearch tool - we use Tavily Search for this
# ToDo: extend to Azure Bing Search
web_search_tool = WebSearchTool()

 # Create graph operations
graph_ops = GraphOperations(retriever, main_chain, eval_chain, web_search_tool)

# Build the graph
search_graph = build_graph(graph_ops)

#### Define fastAPI App (used in both local and Azure) ####
app = FastAPI()

class Question(BaseModel):
    question: str

@app.post("/answer")
async def get_answer(question: Question):
    result = search_graph.invoke({"question": question.question})
    return {"answer": result['answer']}

#### Command-line argument parsing for local execution ####
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the script in different modes")
    parser.add_argument('--mode', type=str, required=True, choices=['test-mode', 'api-mode'], help="Mode of operation: 'test-mode' or 'api-mode'")
    args = parser.parse_args()

    if args.mode == 'test-mode':
        #### Testing the graph ####
        # Let's make some simple tests and also add tracing in LangSmith.
        with tracing_v2_enabled():
            result = search_graph.invoke({"question": "What is a generator function?"})
            print(result['answer'])
            print(result['steps'])

        # This one will not be traced  
        result = search_graph.invoke({"question": "Who is Harry Potter?"})
        print(result['answer'])
        print(result['steps'])

        with tracing_v2_enabled():
            result = search_graph.invoke({"question": "What is LangSmith?"})
            print(result['answer'])
            print(result['steps'])

    elif args.mode == 'api-mode':
        #### Local API Mode: Start FastAPI server via Uvicorn ####
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
