"""
Filename: web_search_tool.py

Author: Szymon Manduk

Company: Szymon Manduk AI, manduk.ai

Description: Defines a class that represents a tool for searching the web for documents that may help to answer a given question.

Copyright (c) 2024 Szymon Manduk AI.
"""
from langchain_community.tools.tavily_search import TavilySearchResults

class WebSearchTool:
    """
    A class representing a tool for searching the web for documents that may help to answer a given question.

    Attributes:
        max_results (int): The maximum number of results to return. Default is 3.
        web_search_tool (TavilySearchResults): The tool for searching the web.

    Methods:
        search(self, query): Searches the web for documents that may help to answer a given question.
    """
    
    def __init__(self, max_results = 3):
        self.max_results = max_results
        self.web_search_tool = TavilySearchResults(max_results=self.max_results, include_images=False)
    
    def search(self, query):
        return self.web_search_tool.invoke({"query": query})
