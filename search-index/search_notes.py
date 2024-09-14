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
- api-mode: to start the FastAPI server that serves the API for answering questions. The API can be accessed locally at on http://localhost:8000 
    The example command for local execution: 
    python search-index\search_notes.py --mode api-mode-local (uses Uvicorn)
    or
    python search-index\search_notes.py --mode api-mode-azure (uses Gunicorn)

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the script in different modes")
    parser.add_argument('--mode', type=str, required=True, choices=['test-mode', 'api-mode-local', 'api-mode-azure'], help="Mode of operation: 'test-mode', 'api-mode-local' or 'api-mode-azure'")
    args = parser.parse_args()
    print(f"Arguments parsed - mode: {args.mode}")

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

    else:
        #### Define fastAPI App (used in both local and Azure) ####
        app = FastAPI()

        class Question(BaseModel):
            question: str

        @app.post("/answer")
        async def get_answer(question: Question):
            result = search_graph.invoke({"question": question.question})
            return {"answer": result['answer'], "steps": result['steps']}
        
        print("FastAPI app created")

        if args.mode == 'api-mode-local':
            print("Starting FastAPI server via Uvicorn")
            #### Local API Mode: Start FastAPI server via Uvicorn ####
            import uvicorn
            uvicorn.run(app, host="0.0.0.0", port=8000)
        elif args.mode == 'api-mode-azure':
            print("Starting FastAPI server via gunicorn")
            #### Azure API Mode: Start FastAPI server via gunicorn ####
                        #### Azure API Mode: Start FastAPI server via gunicorn ####
            from gunicorn.app.base import BaseApplication

            class StandaloneApplication(BaseApplication):
                def __init__(self, app, options=None):
                    self.options = options or {}
                    self.application = app
                    super().__init__()

                def load_config(self):
                    config = {key: value for key, value in self.options.items()
                              if key in self.cfg.settings and value is not None}
                    for key, value in config.items():
                        self.cfg.set(key.lower(), value)

                def load(self):
                    return self.application

            options = {
                'bind': '0.0.0.0:8000',
                'workers': 4,
                'worker_class': 'uvicorn.workers.UvicornWorker'
            }
            StandaloneApplication(app, options).run()
        else:
            raise ValueError("Invalid mode. Please choose 'test-mode' or 'api-mode-local' or 'api-mode-azure'")
