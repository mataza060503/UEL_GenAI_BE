import motor.motor_asyncio
from bson.objectid import ObjectId
from mongoengine import connect

connect('UEL_GEN_AI', host='mongodb://localhost:27017/', alias='core')

def connect_mongoengine():
  # Connect to MongoDB using MongoEngine with alias 'core'
  connect('UEL_GEN_AI', host='mongodb://localhost:27017/', alias='core')

# Initialize MongoDB Async Client
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017/")
db = client["UEL_GEN_AI"]  # Replace with your database name

# Async CRUD Operations

# GET methods
async def get_by_id(collection_name, document_id):
    """
    Retrieve a document by its ObjectId (_id).
    Args:
        collection_name (str): Name of the MongoDB collection.
        document_id (str): The string representation of the ObjectId.
    Returns:
        dict: The document if found, or an error message.
    """
    collection = db[collection_name]
    try:
        # Validate and convert document_id to ObjectId
        object_id = ObjectId(document_id)
        # Find document by _id
        result = await collection.find_one({"_id": object_id})
        if result:
            result["_id"] = str(result["_id"])  # Convert ObjectId to string for JSON compatibility
        return result or {"error": "Document not found"}
    except Exception as e:
        return {"error": f"Invalid ID or query failed: {str(e)}"}


async def get_one_by_params(collection_name, param, value):
    """Retrieve a single document from the specified collection by a parameter."""
    collection = db[collection_name]
    try:
        result = await collection.find_one({param: value})
        return result
    except Exception as e:
        return {"error": str(e)}


async def get_all_by_params(collection_name, filter_query):
    """Retrieve all documents matching a specific filter query."""
    collection = db[collection_name]
    try:
        results = []
        async for document in collection.find(filter_query):
            results.append(document)
        return results
    except Exception as e:
        return {"error": str(e)}


async def get_all(collection_name):
    """Retrieve all documents from the specified collection."""
    collection = db[collection_name]
    try:
        results = []
        async for document in collection.find():
            results.append(document)
        return results
    except Exception as e:
        return {"error": str(e)}


# POST methods
async def insert_one(collection_name, data):
    """Insert a single document into the specified collection."""
    collection = db[collection_name]
    try:
        result = await collection.insert_one(data)
        return {"inserted_id": str(result.inserted_id)}
    except Exception as e:
        return {"error": str(e)}


async def insert_many(collection_name, data_list):
    """Insert multiple documents into the specified collection."""
    collection = db[collection_name]
    try:
        result = await collection.insert_many(data_list)
        return {"inserted_ids": [str(id) for id in result.inserted_ids]}
    except Exception as e:
        return {"error": str(e)}


# PUT & PATCH methods
async def update_one(collection_name, document_id, updated_data):
    """Update a single document by its ID."""
    collection = db[collection_name]
    try:
        result = await collection.update_one(
            {"_id": ObjectId(document_id)}, {"$set": updated_data}
        )
        return {"matched_count": result.matched_count, "modified_count": result.modified_count}
    except Exception as e:
        return {"error": str(e)}


async def update_many(collection_name, filter_query, updated_data):
    """Update multiple documents matching a filter query."""
    collection = db[collection_name]
    try:
        result = await collection.update_many(filter_query, {"$set": updated_data})
        return {"matched_count": result.matched_count, "modified_count": result.modified_count}
    except Exception as e:
        return {"error": str(e)}


# DELETE methods
async def delete_one(collection_name, document_id):
    """Delete a single document by its ID."""
    collection = db[collection_name]
    try:
        result = await collection.delete_one({"_id": ObjectId(document_id)})
        return {"deleted_count": result.deleted_count}
    except Exception as e:
        return {"error": str(e)}


async def delete_many(collection_name, filter_query):
    """Delete multiple documents matching a filter query."""
    collection = db[collection_name]
    try:
        result = await collection.delete_many(filter_query)
        return {"deleted_count": result.deleted_count}
    except Exception as e:
        return {"error": str(e)}
