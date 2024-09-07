from retriever import Retriever
from main_chain import MainChain
from eval_chain import EvalChain
from web_search_tool import WebSearchTool
from graph_builder import build_graph
from graph_operations import GraphOperations
from langchain_core.tracers.context import tracing_v2_enabled
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
PROVIDER = "ollama" # PROVIDER = "openai"

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
