from django.http import JsonResponse
from django.views import View
from utils.mongodb_service import get_by_id
from models.account import DB_Account
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
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
        dicts = DB_Account.queryset_to_json(result)

        if not result:
            # If no existing account, create a new one
            new_account = DB_Account(
                Username=username,
            )
            new_account.save()

            return JsonResponse(new_account, safe=isinstance(result, dict))

        return JsonResponse(dicts, safe=isinstance(result, dict))
