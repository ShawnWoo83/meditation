from functools import wraps
from django.http import HttpResponseRedirect, JsonResponse
import logging
from meditation.utils import utils


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            request.session["user"]
            return view_func(request, *args, **kwargs)
        except KeyError as e:
            logging.exception(str(e))
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({
                    'login_required': True,
                    'redirect_url': '/hello/'
                })
            else:
                return HttpResponseRedirect('/direct/user/login')

    return wrapper
