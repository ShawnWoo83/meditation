import logging
import time
import datetime
import json

from django.db.models import F
from django.http import JsonResponse
from django.utils import timezone

from meditation.models import UserInfo, ScheduleInfo, AppointInfo, SurveyInfo
from meditation.utils import utils
from meditation.wrapper.wraps import login_required
from meditation.bus import business

logger = logging.getLogger(__name__)


@login_required
def get_trainee_schedule_list(request):
    context = {}
    user_info = request.session["user"]
    if user_info.user_type == UserInfo.UserType.TRAINER:
        context["status"] = "99"
        context["msg"] = "错误的用户类型"
        return JsonResponse(context)

    schedule_set = ScheduleInfo.objects.filter(
        schedule_stat=ScheduleInfo.ScheduleStat.NORMAL,
        end_dt__gte=time.strftime("%Y-%m-%d", time.localtime()),
    ).annotate(
        trainer_nm=F('trainer__user_nm'),
    ).values(
        'schedule_id',
        'begin_dt',
        'end_dt',
        'trainer',
        'trainer_nm',
    )
    context["status"] = "00"
    context["data"] = utils.obj_set_to_json(schedule_set)
    return JsonResponse(context)


@login_required
def get_schedule_detail(request):
    logging.info("in get_schedule_detail")
    context = {}
    user_info = request.session["user"]
    try:
        schedule_id = request.POST["schedule_id"]

        # 获取日程表基本信息
        schedule_info = ScheduleInfo.objects.get(schedule_id=schedule_id)

        # 获取该日程表的预约信息
        appoint_set = AppointInfo.objects.filter(
            schedule_id=schedule_id,
            appoint_stat=AppointInfo.AppointStat.NORMAL,
        ).annotate(
            trainee_nm=F("trainee__user_nm"),
        ).values(
            "appoint_id",
            "trainee_id",
            "trainee_nm",
            "appoint_time",
            "appoint_stat",
        )

        appoint_list = []
        for obj in appoint_set:

            if obj["trainee_id"] == user_info.user_id:
                obj.update({"appoint_type": "self"})
            else:
                obj.update({"appoint_type": "others"})
            appoint_list.append(obj)

        context["data"] = utils.obj_to_json(schedule_info)
        context["data"].update({
            "appoint_set": utils.obj_set_to_json(appoint_list)
        })
        context["status"] = "00"
    except (KeyError, ScheduleInfo.DoesNotExist) as e:
        context["status"] = "99"
    return JsonResponse(context)


@login_required
def trainee_appoint(request):
    context = {}
    user_info = request.session["user"]

    try:
        schedule_id = request.POST["schedule_id"]
        appoint_time = request.POST["appoint_time"]

        occupy_time = []
        schedule_info = ScheduleInfo.objects.get(
            pk=schedule_id, schedule_stat=ScheduleInfo.ScheduleStat.NORMAL,
        )
        occupy_time.extend(schedule_info.disable_time)

        appoint_set = AppointInfo.objects.filter(
            schedule_id=schedule_id, appoint_stat=AppointInfo.AppointStat.NORMAL
        ).values(
            'appoint_time',
        )
        for obj in appoint_set:
            occupy_time.extend(obj["appoint_time"])

        if occupy_time.count(appoint_time) <= 0:
            days = int(appoint_time.split("|")[0])
            times = int(appoint_time.split("|")[1])
            appoint_date = schedule_info.begin_dt + datetime.timedelta(days=days - 1)
            new_appoint_time = [appoint_time, str(days) + "|" + str(times + 1)]
            appoint_info = AppointInfo.objects.create(
                schedule=schedule_info,
                trainee=user_info,
                appoint_dt=appoint_date,
                appoint_time=new_appoint_time,
                appoint_stat=AppointInfo.AppointStat.NORMAL,
                preview_work={},
                review_work={},
                last_upd_dt=timezone.now(),
            )
            context["status"] = "00"
        else:
            context["status"] = "99"
    except KeyError:
        context["status"] = "99"

    return JsonResponse(context)


@login_required
def cancel_appoint(request):
    context = {}
    user_info = request.session["user"]

    try:
        schedule_id = request.POST["schedule_id"],
        appoint_id = request.POST["appoint_id"]
        appoint_info = AppointInfo.objects.get(schedule_id=schedule_id, appoint_id=appoint_id)
        appoint_info.appoint_stat = AppointInfo.AppointStat.SELF_CANCEL
        appoint_info.save()
        context["status"] = "00"
    except KeyError:
        context["status"] = "99"
    return JsonResponse(context)


@login_required
def get_trainee_appoint_list(request):
    context = {}
    user_info = request.session["user"]

    appoint_set = AppointInfo.objects.filter(
        trainee=user_info,
        appoint_stat__in=[AppointInfo.AppointStat.NORMAL, AppointInfo.AppointStat.DONE]
    ).values(
        "appoint_id",
        "appoint_dt",
        "appoint_time",
        "appoint_stat",
    ).order_by(
        "-appoint_dt",
        "-appoint_time",
    )

    appoint_list = business.get_appoint_list_json(appoint_set)
    context["status"] = "00"
    context["data"] = appoint_list
    return JsonResponse(context)


@login_required
def get_appoint_work(request):
    logger.info("getAppointWork")
    context = {}
    try:
        appoint_id = request.POST["appoint_id"]
        work_type = request.POST["work_type"]
        user_info = request.session["user"]
    except KeyError as e:
        logger.error(e)
        context["status"] = "99"
        context["msg"] = "无效的请求参数"
        return JsonResponse(context)

    logger.info(work_type)
    match work_type:
        case SurveyInfo.SurveyType.PRE_CLASS:
            column_name = "preview_work"
        case SurveyInfo.SurveyType.END_CLASS:
            column_name = "review_work"
        case _:
            return JsonResponse({
                "status": "99",
                "msg": "无效的请求参数",
            })

    homework = AppointInfo.objects.filter(
        pk=appoint_id
    ).values(
        column_name
    ).first()[column_name]
    # homework: {survey_id:#survey_id#,answer_list:[#answer1#,#answer2#]}
    question_set = []
    if "survey_id" not in homework:
        result_set = SurveyInfo.objects.filter(
            survey_type=work_type,
            survey_stat=SurveyInfo.SurveyStat.NORMAL,
        ).values(
            "survey_id",
            "question_list",
        ).first()
        survey_id = result_set["survey_id"]
        question_set = result_set["question_list"]
    else:
        result_set = SurveyInfo.objects.filter(
            pk=homework["survey_id"]
        ).values(
            "survey_id",
            "question_list",
        ).first()
        survey_id = result_set["survey_id"]
        question_set = result_set["question_list"]
        for index in range(len(question_set)):
            question_set[index]["answer"] = homework["answer_list"][index]
    context["status"] = "00"
    context["data"] = {}
    context["data"]["work_list"] = utils.obj_set_to_json(question_set)
    context["data"]["user_type"] = user_info.user_type
    context["data"]["survey_id"] = survey_id
    logger.info(context)
    return JsonResponse(context)


@login_required
def save_work(request):
    context = {}
    try:
        appoint_id = request.POST["appoint_id"]
        survey_id = request.POST["survey_id"]
        work_type = request.POST["work_type"]
        answer_list = request.POST["answer_list"]
    except KeyError:
        context["status"] = "99"

    appoint_info = AppointInfo.objects.get(pk=appoint_id)
    match work_type:
        case SurveyInfo.SurveyType.PRE_CLASS:
            appoint_info.preview_work = {
                "survey_id": survey_id,
                "answer_list": json.loads(answer_list),
            }
        case SurveyInfo.SurveyType.END_CLASS:
            appoint_info.review_work = {
                "survey_id": survey_id,
                "answer_list": json.loads(answer_list),
            }
        case _:
            context["status"] = "99"
            return JsonResponse(context)

    appoint_info.last_upd_dt = timezone.now()
    appoint_info.save()
    context["status"] = "00"
    context["data"] = utils.obj_to_json(appoint_info)
    return JsonResponse(context)
