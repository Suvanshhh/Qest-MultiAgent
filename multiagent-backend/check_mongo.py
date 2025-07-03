from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=3000)
    client.admin.command('ping')
    print("You are connected to MongoDB!")
except Exception as e:
    print("MongoDB connection error:", e)
