from django.http import HttpResponseRedirect, JsonResponse


def hello(request):
    return JsonResponse({"status": "00"})
