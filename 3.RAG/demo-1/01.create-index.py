from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    AzureOpenAIVectorizer,
    AzureOpenAIVectorizerParameters,
    SearchIndex
)
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_AI_SEARCH_API_KEY")

# Create a search index  
index_name = "nasa-py-rag-tutorial-idx"

# Use AzureKeyCredential instead of passing the raw key string to avoid AttributeError
# For production, prefer using Azure AD / DefaultAzureCredential with RBAC instead of key auth.
index_client = SearchIndexClient(endpoint=search_endpoint, credential=AzureKeyCredential(search_key))
fields = [
    SearchField(name="parent_id", type=SearchFieldDataType.String),  
    SearchField(name="title", type=SearchFieldDataType.String),
    SearchField(name="locations", type=SearchFieldDataType.Collection(SearchFieldDataType.String), filterable=True),
    SearchField(name="chunk_id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True, analyzer_name="keyword"),  
    SearchField(name="chunk", type=SearchFieldDataType.String, sortable=False, filterable=False, facetable=False),  
    SearchField(name="text_vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single), vector_search_dimensions=1536, vector_search_profile_name="myHnswProfile")
    ]  
  
# Configure the vector search configuration  
vector_search = VectorSearch(  
    algorithms=[  
        HnswAlgorithmConfiguration(name="myHnsw"),
    ],  
    profiles=[  
        VectorSearchProfile(  
            name="myHnswProfile",  
            algorithm_configuration_name="myHnsw",  
            vectorizer_name="myOpenAI",  
        )
    ],  
    vectorizers=[  
        AzureOpenAIVectorizer(  
            vectorizer_name="myOpenAI",  
            kind="azureOpenAI",  
            parameters=AzureOpenAIVectorizerParameters(  
                resource_url=endpoint,  
                deployment_name="text-embedding-ada-002",
                model_name="text-embedding-ada-002"
            ),
        ),  
    ], 
)  

  
# Create the search index
index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)  
result = index_client.create_or_update_index(index)  
print(f"{result.name} created")  