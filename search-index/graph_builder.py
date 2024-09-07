"""
Filename: graph_builder.py

Author: Szymon Manduk

Company: Szymon Manduk AI, manduk.ai

Description: This module defines the build_graph function, which builds a graph structure for the search-index module.

Copyright (c) 2024 Szymon Manduk AI.
"""

from langgraph.graph import START, END, StateGraph
from graph_state import GraphState

def build_graph(graph_ops):
    graph_structure = StateGraph(GraphState)

    graph_structure.add_node("retrieve", graph_ops.retrieve)
    graph_structure.add_node("generate", graph_ops.generate)
    graph_structure.add_node("evaluate", graph_ops.evaluate)
    graph_structure.add_node("web_search", graph_ops.web_search)

    graph_structure.add_edge(START, "retrieve")
    graph_structure.add_edge("retrieve", "evaluate")
    graph_structure.add_conditional_edges(
        "evaluate", 
        graph_ops.determine_next_node,
        {
            "web_search": "web_search",
            "generate": "generate",
        },
    )
    graph_structure.add_edge("web_search", "generate")
    graph_structure.add_edge("generate", END)

    return graph_structure.compile()
