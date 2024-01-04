"""
This module contains all database interfacing methods for the application. 
"""
from llama_index.retrievers import VectorIndexRetriever

from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.indices.vector_store.base import VectorStoreIndex
import pandas as pd
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))
db = client[os.getenv("MONGODB_DATABASE")]
store = MongoDBAtlasVectorSearch(
    client,
    db_name=os.getenv('MONGODB_DATABASE'), # this is the database where we stored our embeddings
    collection_name=os.getenv('MONGODB_VECTORS'), # this is where our embeddings were stored
    index_name=os.getenv('MONGODB_VECTOR_INDEX') # this is the name of the index we created
)
index = VectorStoreIndex.from_vector_store(store)


def get_all_products():
    """
    Return all products in the database
    """
    collection = db[os.getenv("MONGODB_COLLECTION")]
    return pd.DataFrame(list(collection.find()))

def query_products(query):
    """
    Given a query, return a list of products that match the query
    """
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=10,
    )
    nodes = retriever.retrieve(query)
    return [node.metadata for node in nodes]