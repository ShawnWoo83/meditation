from django.http import JsonResponse
from meditation.models import UserInfo
from meditation.wrapper.wraps import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.utils import timezone
from meditation.utils import utils
from meditation.bus import business


def login(request):
    """
    登录。根据登录ID + 登录密码查找用户：
        1、未查得：返回登录页（login.html），提示错误信息。
        2、查得：
            a）用户信息放入Session，进入首页（index.html）
            b）用户状态异常（申请中/禁用），进入提示页（tips.html）
    :param request:
    :return:
    """
    context = {
    }
    login_id = request.POST['login_id']
    login_pwd = request.POST['login_pwd']
    try:
        user_info = UserInfo.objects.get(login_id=login_id, login_pwd=login_pwd)
        if user_info.user_stat != UserInfo.UserStat.NORMAL:
            context["status"] = "99"
            match user_info.user_stat:
                case UserInfo.UserStat.APPLYING:
                    context["msg"] = "申请正在审批中，请稍后再试"
                case UserInfo.UserStat.DISABLE:
                    context["msg"] = "用户已被禁用，无法登陆"
            return JsonResponse(context)
        user_info.last_login_date = timezone.now()
        user_info.save()
        request.session['user'] = user_info
        context["status"] = "00"
        context["data"] = utils.obj_to_json(user_info)
    except UserInfo.DoesNotExist:
        context["status"] = "99"
        context["msg"] = "用户不存在或密码错误，请重试"
    return JsonResponse(context)


def register(request):
    """
    注册。
        1、根据登录ID查找用户。如查得：提示用户ID已存在；
        2、未查得，保存用户信息。用户此时的状态为”申请中“；需要教练确认后，方可正常登陆。
    :param request:
    :return:
    """
    context = {}
    login_id = request.POST['login_id']
    login_pwd = request.POST['login_pwd']
    user_nm = request.POST['user_nm']
    try:
        UserInfo.objects.get(login_id=login_id)
        context["status"] = "99"
        context["msg"] = business.resMsgDic.USER_IS_EXIST
    except UserInfo.DoesNotExist:
        user_info = UserInfo()
        user_info.login_id = login_id
        user_info.login_pwd = login_pwd
        user_info.user_nm = user_nm
        user_info.register_dt = timezone.now()
        user_info.last_login_dt = timezone.now()
        user_info.save()
        context["status"] = "00"
        context["msg"] = "注册成功，请提醒教练激活"
    return JsonResponse(context)


def logout(request):
    try:
        request.session.pop("user")
    except KeyError:
        pass
    return HttpResponseRedirect('/hello/')
