from mongoengine import Document, StringField, DateTimeField, ObjectIdField
from bson import ObjectId
from datetime import datetime

class DB_Message(Document):
    _id = ObjectIdField(default=ObjectId)  # MongoDB ObjectId
    ChatId = ObjectIdField(required=True)  # Foreign key for chat
    User = StringField(required=True)
    System = StringField()
    CreateAt = DateTimeField(default=datetime.utcnow)  # Store as DateTimeField

    def __str__(self):
        return f"{self.User}: {self.System[:50]}"

    meta = {
        'db_alias': 'core',  # MongoDB alias (optional, but useful for multiple databases)
        'collection': 'MESSAGES',  # Collection name in MongoDB
    }
