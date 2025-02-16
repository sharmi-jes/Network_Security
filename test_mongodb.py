
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://sharmianyum:sharmi123@cluster0.fgdgk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)


# List all databases
print(client.list_database_names())

db = client["sample_mflix"]  # Connect to this database
print(db.list_collection_names()) 

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)