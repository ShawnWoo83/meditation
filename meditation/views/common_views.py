from django.http import JsonResponse
from meditation.models import UserInfo
from meditation.wrapper.wraps import login_required
from django.shortcuts import render


@login_required
def hello(request):
    """
    默认URL。这里会对用户Session做判：
        1、如果Session不存在，进入登录页（login.html）；
        2、如果Session存在，进入首页（index.html)。
    :param request:
    :return:
    """
    user = request.session["user"]

    if user.user_type == UserInfo.UserType.TRAINER:
        return render(request, 'trainer/index.html')
    else:
        return render(request, 'trainee/index.html')


def res_404(request, exception):
    """
    404的应答页面，需要在URL中配置
    :param request:
    :param exception:
    :return:
    """
    return JsonResponse({"404": "404"})


def direct(request, url):
    """
    直接跳转页面，不做任何处理
    :param request:
    :param url:
    :return:
    """
    return render(request, url + ".html")
