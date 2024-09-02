"""
Filename: index_fields.py

Author: Szymon Manduk

Company: Szymon Manduk AI, manduk.ai

Description: Contains definition of vector index for Azure AI Search.

Copyright (c) 2024 Szymon Manduk AI.
"""

from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)

# Define the index schema with default field names: id, content, content_vector, metadata 
# or provide alternative field names in the env variables and change fields below accordingly.
# See also: https://python.langchain.com/v0.2/docs/integrations/vectorstores/azuresearch/#install-azure-ai-search-sdk
# See also: definition of AzureSearch class.
# Default vector configuration is also in AzureSearch class.
fields = [
    SimpleField(
        name="id",
        type=SearchFieldDataType.String,
        key=True,
        filterable=True,
    ),
    SearchableField(
        name="content", 
        type=SearchFieldDataType.String,
        searchable=True,
    ),
    SearchField(
        name="content_vector",  
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=1536,  # for text-embedding-ada-002
        vector_search_profile_name="myHnswProfile",
    ),
    SearchableField(
        name="metadata",
        type=SearchFieldDataType.String,
        searchable=True,
    ),
    SearchableField(
        name="title",
        type=SearchFieldDataType.String,
        searchable=True,
    ),
    SimpleField(
        name="label",
        type=SearchFieldDataType.String,
        filterable=True,
    ),
]