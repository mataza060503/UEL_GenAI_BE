from django.http import JsonResponse
from django.views import View
from utils.mongodb_service import get_by_id
from models.chat import DB_Chat
from bson.json_util import dumps
from bson import ObjectId
import mongoengine
import json

class ChatView(View):
    async def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        """
        # Retrieve account_id from query parameters
        account_id_str = request.GET.get("accountId")  # Use 'accountId' as the parameter name

        if not account_id_str:
            # If account_id is not provided, return an error response
            return JsonResponse({"error": "Missing accountId parameter"}, status=400)
        
        account_id = ObjectId(account_id_str)

        # Fetch the account data from MongoDB
        data = DB_Chat.objects(AccountId=account_id).order_by('CreateAt')
        # result = data.to_json()
        # dicts = json.loads(result)

        dicts = DB_Chat.queryset_to_json(data)

        return JsonResponse(dicts, safe=isinstance(dicts, dict))
    
    # async def post(self, request, *args, **kwargs):
    #     """
    #     Handle POST requests to create a new document.
    #     """
    #     try:
    #         # Parse the JSON body
    #         data = json.loads(request.body)
    #         if not data:
    #             return JsonResponse({"error": "Request body is empty"}, status=400)

    #         # Create a new document in MongoDB
    #         result = await create_document("ACCOUNT", data)
    #         return JsonResponse({"message": "Account created successfully", "id": str(result.inserted_id)}, status=201)
    #     except Exception as e:
    #         return JsonResponse({"error": str(e)}, status=500)

    # async def put(self, request, *args, **kwargs):
    #     """
    #     Handle PUT requests to update an existing document.
    #     """
    #     try:
    #         account_id = request.GET.get("accountId")
    #         if not account_id:
    #             return JsonResponse({"error": "Missing accountId parameter"}, status=400)

    #         # Parse the JSON body
    #         data = json.loads(request.body)
    #         if not data:
    #             return JsonResponse({"error": "Request body is empty"}, status=400)

    #         # Update the document in MongoDB
    #         result = await update_document("ACCOUNT", account_id, data)
    #         if result.modified_count == 0:
    #             return JsonResponse({"message": "No changes made to the account"}, status=200)
    #         return JsonResponse({"message": "Account updated successfully"}, status=200)
    #     except Exception as e:
    #         return JsonResponse({"error": str(e)}, status=500)

    # async def delete(self, request, *args, **kwargs):
    #     """
    #     Handle DELETE requests to delete an existing document.
    #     """
    #     try:
    #         account_id = request.GET.get("accountId")
    #         if not account_id:
    #             return JsonResponse({"error": "Missing accountId parameter"}, status=400)

    #         # Delete the document in MongoDB
    #         result = await delete_by_id("ACCOUNT", account_id)
    #         if result.deleted_count == 0:
    #             return JsonResponse({"error": "Account not found"}, status=404)
    #         return JsonResponse({"message": "Account deleted successfully"}, status=200)
    #     except Exception as e:
    #         return JsonResponse({"error": str(e)}, status=500)


from django.http import JsonResponse
from django.views import View
from utils.mongodb_service import get_by_id
from models.chat import DB_Chat
from models.message import DB_Message
from bson.json_util import dumps
from bson import ObjectId
import mongoengine
import json

class MessageView(View):
    async def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        """
        # Retrieve account_id from query parameters
        chat_id_str = request.GET.get("chatId")  # Use 'accountId' as the parameter name

        if not chat_id_str:
            # If account_id is not provided, return an error response
            return JsonResponse({"error": "Missing accountId parameter"}, status=400)
        
        chat_id = ObjectId(chat_id_str)

        # Fetch the account data from MongoDB
        data = DB_Message.objects(ChatId=chat_id).order_by('CreateAt')
        # result = data.to_json()
        # dicts = json.loads(result)

        dicts = DB_Message.queryset_to_json(data)

        return JsonResponse(dicts, safe=isinstance(dicts, dict))
    
    # async def post(self, request, *args, **kwargs):
    #     """
    #     Handle POST requests to create a new document.
    #     """
    #     try:
    #         # Parse the JSON body
    #         data = json.loads(request.body)
    #         if not data:
    #             return JsonResponse({"error": "Request body is empty"}, status=400)

    #         # Create a new document in MongoDB
    #         result = await create_document("ACCOUNT", data)
    #         return JsonResponse({"message": "Account created successfully", "id": str(result.inserted_id)}, status=201)
    #     except Exception as e:
    #         return JsonResponse({"error": str(e)}, status=500)

    # async def put(self, request, *args, **kwargs):
    #     """
    #     Handle PUT requests to update an existing document.
    #     """
    #     try:
    #         account_id = request.GET.get("accountId")
    #         if not account_id:
    #             return JsonResponse({"error": "Missing accountId parameter"}, status=400)

    #         # Parse the JSON body
    #         data = json.loads(request.body)
    #         if not data:
    #             return JsonResponse({"error": "Request body is empty"}, status=400)

    #         # Update the document in MongoDB
    #         result = await update_document("ACCOUNT", account_id, data)
    #         if result.modified_count == 0:
    #             return JsonResponse({"message": "No changes made to the account"}, status=200)
    #         return JsonResponse({"message": "Account updated successfully"}, status=200)
    #     except Exception as e:
    #         return JsonResponse({"error": str(e)}, status=500)

    # async def delete(self, request, *args, **kwargs):
    #     """
    #     Handle DELETE requests to delete an existing document.
    #     """
    #     try:
    #         account_id = request.GET.get("accountId")
    #         if not account_id:
    #             return JsonResponse({"error": "Missing accountId parameter"}, status=400)

    #         # Delete the document in MongoDB
    #         result = await delete_by_id("ACCOUNT", account_id)
    #         if result.deleted_count == 0:
    #             return JsonResponse({"error": "Account not found"}, status=404)
    #         return JsonResponse({"message": "Account deleted successfully"}, status=200)
    #     except Exception as e:
    #         return JsonResponse({"error": str(e)}, status=500)