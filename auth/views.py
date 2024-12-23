from django.http import JsonResponse
from django.views import View
from utils.mongodb_service import get_by_id
from models.account import DB_Account

class View(View):
    async def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        """
        # Retrieve account_id from query parameters
        username = request.GET.get("username")  # Use 'accountId' as the parameter name

        if not username:
            # If account_id is not provided, return an error response
            return JsonResponse({"error": "Missing accountId parameter"}, status=400)

        # Fetch the account data from MongoDB
        result = DB_Account.objects(Username=username)
        return JsonResponse(result, safe=isinstance(result, dict))
