"""
Filename: graph_state.py

Author: Szymon Manduk

Company: Szymon Manduk AI, manduk.ai

Description: This module defines the GraphState class, which represents the state of the graph. 

Copyright (c) 2024 Szymon Manduk AI.
"""

from typing_extensions import TypedDict, List

class GraphState(TypedDict):
    """
    Represents the state of the graph.

    Attributes:
        question: question
        documents: list of retrieved documents
        answer: LLM generated answer
        search_required: whether to search web
        search_results: results of web search
        steps: steps of the graph execution
        
    """

    question: str
    documents: List[str]
    answer: str
    search_required: bool
    search_results: List[str]
    steps: List[str]