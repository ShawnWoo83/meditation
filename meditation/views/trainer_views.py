import logging
import time
import datetime
import json

from django.db.models import F
from django.http import JsonResponse
from django.utils import timezone

from meditation.models import UserInfo, ScheduleInfo, AppointInfo
from meditation.utils import utils
from meditation.wrapper.wraps import login_required
from meditation.bus import business


@login_required
def get_schedule_list(request):
    context = {}
    user_info = request.session["user"]
    schedule_set = ScheduleInfo.objects.filter(trainer=user_info)
    schedule_list = utils.obj_set_to_json(schedule_set)
    context["data"] = schedule_list
    return JsonResponse(context)


@login_required
def create_schedule(request):
    context = {}
    user_info = request.session["user"]

    try:
        begin_dt = request.POST["begin_dt"]
        end_dt = request.POST["end_dt"]

        # 判断该日程的begin_dt是否有小于该老师所有日程的end_date，如果有代表有交叉
        schedule_set = ScheduleInfo.objects.filter(end_dt__gte=begin_dt)
        if len(schedule_set) > 0:
            context["status"] = "99"
            context["msg"] = "新建日程与过往日程存在时间冲突"
            return JsonResponse(context)

        schedule_info = ScheduleInfo.objects.create(
            trainer=user_info,
            begin_dt=begin_dt,
            end_dt=end_dt,
            disable_time=[],
            schedule_stat=ScheduleInfo.ScheduleStat.INITIAL,
            last_upd_dt=timezone.now()
        )
        context["data"] = utils.obj_to_json(schedule_info)
        context["status"] = "00"
    except Exception as e:
        context["status"] = "99"

    return JsonResponse(context)


@login_required
def get_trainer_appoint_list(request):
    context = {}
    user_info = request.session["user"]

    if user_info.user_type != UserInfo.UserType.TRAINER:
        context["status"] = "99"
        context["msg"] = "用户类型错误"

    appoint_set = AppointInfo.objects.filter(
        schedule_id=request.POST["schedule_id"],
        appoint_stat=AppointInfo.AppointStat.NORMAL,
    ).annotate(
        trainee_nm=F("trainee__user_nm"),
    ).values(
        "appoint_id",
        "appoint_dt",
        "appoint_time",
        "trainee_nm",
    ).order_by(
        "-appoint_dt",
        "-appoint_time",
    )
    appoint_list = business.get_appoint_list_json(appoint_set)
    context["status"] = "00"
    context["data"] = appoint_list
    return JsonResponse(context)


@login_required
def save_schedule_detail(request):
    context = {}
    try:
        schedule_id = request.POST["schedule_id"]
        disable_time = request.POST["disable_time"]
        schedule_info = ScheduleInfo.objects.get(pk=schedule_id)
        schedule_info.disable_time = json.loads(disable_time)
        schedule_info.schedule_stat = ScheduleInfo.ScheduleStat.NORMAL
        schedule_info.last_upd_dt = timezone.now()
        schedule_info.save()
        context["status"] = "00"
        context["msg"] = "保存成功"
    except Exception as e:
        context["status"] = "99"
        context["msg"] = "处理失败，请稍后再试"
    finally:
        return JsonResponse(context)


@login_required
def get_apply_user_list(request):
    context = {}
    user_set = UserInfo.objects.filter(
        user_stat=UserInfo.UserStat.APPLYING,
        user_type=UserInfo.UserType.TRAINEE
    )
    context["status"] = "00"
    context["data"] = utils.obj_set_to_json(user_set)
    return JsonResponse(context)


@login_required
def apply_verify(request):
    user_id = request.POST["user_id"]
    verify_type = request.POST["verify_type"]
    user_info = UserInfo.objects.get(user_id=user_id)
    if verify_type == UserInfo.UserStat.NORMAL:
        user_info.user_stat = UserInfo.UserStat.NORMAL
    else:
        user_info.user_stat = UserInfo.UserStat.DISABLE
    user_info.save()
    context = {
        "status": "00",
    }
    return JsonResponse(context)
