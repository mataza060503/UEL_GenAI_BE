from mongoengine import Document, StringField, DateTimeField, ObjectIdField
from bson import ObjectId
from datetime import datetime
import json

class DB_Account(Document):
    _id = ObjectIdField(default=ObjectId)  # MongoDB ObjectId
    Username = StringField(required=True)
    Password = StringField()
    Birth = StringField()
    Email = StringField()
    Name = StringField()
    Phone = StringField()


    def __str__(self):
        return f"{self.User}: {self.System[:50]}"
    
    @classmethod
    def queryset_to_json(cls, queryset):
        # Helper function to recursively convert fields
        def convert_fields(doc):
            if isinstance(doc, dict):
                return {key: convert_fields(value) for key, value in doc.items()}
            elif isinstance(doc, list):
                return [convert_fields(item) for item in doc]
            elif isinstance(doc, ObjectId):
                return str(doc)  # Convert ObjectId to string
            elif isinstance(doc, datetime):
                return doc.isoformat()  # Convert datetime to ISO format
            else:
                return doc  # Return other types as is

        # Process each document in the queryset
        result = []
        for doc in queryset:
            doc_dict = doc.to_mongo().to_dict()  # Convert each document to a MongoDB document
            result.append(convert_fields(doc_dict))  # Recursively process fields

        return result

    meta = {
        'db_alias': 'core',  # MongoDB alias (optional, but useful for multiple databases)
        'collection': 'ACCOUNT',  # Collection name in MongoDB
    }
