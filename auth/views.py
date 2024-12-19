from django.http import JsonResponse
from django.views import View
from utils.mongodb_service import get_by_id

class AuthView(View):
    async def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        """
        # Retrieve account_id from query parameters
        account_id = request.GET.get("accountId")  # Use 'accountId' as the parameter name

        if not account_id:
            # If account_id is not provided, return an error response
            return JsonResponse({"error": "Missing accountId parameter"}, status=400)

        # Fetch the account data from MongoDB
        result = await get_by_id("ACCOUNT", account_id)
        return JsonResponse(result, safe=isinstance(result, dict))
