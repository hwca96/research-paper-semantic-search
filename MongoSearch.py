from pymongo import MongoClient
from dotenv import load_dotenv
import requests
import os
import pandas as pd

load_dotenv()

class MongoSearch:
    def __init__(self, database = "arxiv_data", collection = "cs_sample"):
        self.client = MongoClient(os.getenv("MONGODB_URI"))
        self.db = self.client[database]
        self.collection = self.db[collection]
        self.embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

    def generate_embedding(self, text):
        response = requests.post(
            self.embedding_url,
            headers={"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"},
            json={"inputs": text, "options": {"wait_for_model": True}})

        if response.status_code != 200:
            raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")

        return response.json()

    def search(self, query):
        results = self.collection.aggregate([
        {"$vectorSearch": {
            "queryVector": self.generate_embedding(query),
            "path": "embedding",
            "numCandidates": 100,
            "limit": 5,
            "index": "EmbeddingSemanticSearch",
            }}
        ])
        keys = ["title", "abstract", "authors", "id", "categories", "update_date"]
        return pd.DataFrame([dict((k, result[k]) for k in keys) for result in results])
