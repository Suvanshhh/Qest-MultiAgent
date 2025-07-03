from pymongo import MongoClient, errors

MONGO_URI = "mongodb+srv://Suvanshh:bB632221010@cluster0.pkiya.mongodb.net/mydb?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # 5 seconds timeout
    client.server_info()  # Will raise exception if cannot connect
    print("MongoDB connection successful!")
except errors.ServerSelectionTimeoutError as err:
    print("MongoDB connection failed:", err)
