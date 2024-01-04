"""
This script will create a database, vector store and index from the data file.
"""
from dotenv import load_dotenv
load_dotenv()
import json
import os
from pymongo.mongo_client import MongoClient
from pymongo.collection import Collection
from pymongo.server_api import ServerApi
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.indices.vector_store.base import VectorStoreIndex
from llama_index.storage.storage_context import StorageContext
from llama_index import Document

def get_field_names_from_data(data: list[dict]) -> list[str]:
    field_names = set(data[0].keys())
    for obj in data[1:]:
        field_names.update(obj.keys())
    return list(field_names)

def mongo_docs_to_llamaindex_docs(collection: Collection, field_names):
    llamaindex_documents = []
    for mongo_doc in collection.find():
        text = ",\n".join([f"{name}: {mongo_doc[name]}" for name in field_names if name in mongo_doc])
        metadata = {name: mongo_doc[name] for name in field_names if name in mongo_doc}
        llamaindex_documents.append(Document(text=text, metadata=metadata))
    return llamaindex_documents

client = MongoClient(os.getenv('MONGODB_URI'), server_api=ServerApi('1'))
db = client[os.getenv("MONGODB_DATABASE")]
collection = db[os.getenv("MONGODB_COLLECTION")]

with open('../scrapers/data.json', 'r') as file:
    scrapers_data = json.load(file)

field_names = get_field_names_from_data(scrapers_data)
collection.insert_many(scrapers_data)
documents = mongo_docs_to_llamaindex_docs(collection, field_names)

# create Atlas as a vector store
store = MongoDBAtlasVectorSearch(
    client,
    db_name=os.getenv('MONGODB_DATABASE'),
    collection_name=os.getenv('MONGODB_VECTORS'), # this is where our embeddings will be stored
    index_name=os.getenv('MONGODB_VECTOR_INDEX') # this is the name of the index we create in Mongo console
)

# create an index from all the Documents and store them in Atlas
storage_context = StorageContext.from_defaults(vector_store=store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context,
    show_progress=True,
)