from crewai.tools import BaseTool
from pymongo import MongoClient
from pydantic import BaseModel, Field, PrivateAttr
from typing import Type, Dict, Any
import os

# MongoDB URI string (replace with your actual URI)
MONGO_URI ="mongodb+srv://Suvanshh:bB632221010@cluster0.pkiya.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "mydb"  # Replace with your actual database name

class FindInput(BaseModel):
    collection: str = Field(..., description="MongoDB collection name")
    query: Dict[str, Any] = Field(..., description="MongoDB query")

class MongoDBTool(BaseTool):
    name: str = "MongoDB Tool"
    description: str = "Query MongoDB collections using a filter."
    args_schema: Type[BaseModel] = FindInput

    _client: MongoClient = PrivateAttr()
    _db: Any = PrivateAttr()

    def __init__(self, uri: str = MONGO_URI, db_name: str = DB_NAME):
        super().__init__()
        object.__setattr__(self, "_client", MongoClient(uri))
        object.__setattr__(self, "_db", self._client[db_name])

    # For agent direct use
    def find(self, collection: str, query: dict):
        return list(self._db[collection].find(query))

    def aggregate(self, collection: str, pipeline: list):
        return list(self._db[collection].aggregate(pipeline))

    # For CrewAI tool interface
    def _run(self, collection: str, query: dict):
        return self.find(collection, query)
