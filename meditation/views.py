from django.http import JsonResponse
from .models import UserInfo


def hello(request):
    user_info = UserInfo.objects.get(pk=1)
    return JsonResponse({"user_nm": user_info.user_nm})
