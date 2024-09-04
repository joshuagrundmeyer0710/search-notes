# Google Keep Notes Search Engine

This project implements a simple search engine for Google Keep notes using Azure AI Search and various AI technologies. It combines vector search with semantic search (hybrid mode) to provide high-quality search results and uses LangGraph to create an intelligent workflow for answering queries.

## Project Overview

The search engine is built on a dataset of hundreds of Google Keep notes collected over years. It leverages Azure AI Search for indexing and searching, with the index created programmatically through Langchain Azure integration.

The project uses LangGraph to build and run a workflow that:
1. Retrieves relevant information from the notes
2. Evaluates if a query can be answered with the retrieved information
3. If sufficient information is found, passes it to the main LLM for answering
4. If not, performs an additional web search using Tavily Search API or Azure Bing Search API
5. Passes the extended information to the LLM for a comprehensive answer

## Key Features

- Azure AI hybrid search combining vector and semantic search for improved results
- Flexible deployment options, including full Azure cloud compatibility
- Integration with various AI and search APIs
- Intelligent query processing workflow

## Technology Stack

- **Programming Language**: Python
- **Orchestrator**: Langchain and LangGraph
- **Observability**: LangSmith
- **Search Engine**: Azure AI Search
- **Web Search API**: Tavily Search API or Azure Bing Search API
- **Models**: 
  - GPT-4-turbo (OpenAI or Azure OpenAI)
  - Llama 3.1 8B (locally through Ollama)
- **Cloud Platform**: Azure

## Deployment

The project is designed to be deployed on Azure cloud and can be configured to run exclusively within the Azure ecosystem:

- All OpenAI API calls can be replaced by Azure OpenAI API calls
- Local LLM calls can be replaced by Azure OpenAI API calls
- Tavily Search API can be replaced by Azure Bing Search API

1. Create an Azure AI Search service in Azure Portal

2. Configure environment variables:
The following environment variables need to be set in .env file:
- AZURESEARCH_ENDPOINT="address of the Azure Search endpoint"
- AZURESEARCH_ADMIN_KEY=admin key for the Azure Search service
- OPENAI_API_KEY=openai api key, if used
- AZURESEARCH_INDEX_NAME=name of the Azure Search index
- TAVILY_API_KEY=api key for Tavily Search API, if used
- LANGCHAIN_TRACING_V2=false # if we don't want to trace every request then set it to false and use 'with tracing_v2_enabled():' in the code to trace specific requests
- LANGCHAIN_API_KEY=langchain api key
- LANGCHAIN_PROJECT=name of the Langchain project

3. Prepare data
- Export Google Keep notes using Google Takeout. Notes examples are provided in the `raw-data/Notes examples` directory.
- Convert the notes from html to json using notes_to_json.py script.
- Create a new Azure Search index using create_empty_index.py script.
- Build index using build_index.py script.

4. 

## License

GNU GENERAL PUBLIC LICENSE - see LICENSE file for details.
