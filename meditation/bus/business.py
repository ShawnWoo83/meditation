from datetime import time

from meditation.models import UserInfo
from meditation.utils import utils

__OPEN_TIME = time(9, 30)


class transTypeDic:
    """
    业务流程的梳理：
        学员视角：
            用户类视角：
                注册；
                登陆；
            业务类视角：
                选择导师（本次默认一位导师，不需要选择，用户申请通过后，即默认为该位导师）；
                查看课表；
                预约；
                取消预约；
                填写课前问卷；
                填写课后问卷。
        教练视角：
            用户类视角：
                注册；
                登陆；
                成为导师（本次以数据订正的方式实现，不实现本功能）；
            业务类视角：
                制定课表；
                查看课表；
                发送通知；
                查看课前问卷；
                查看课后问卷；
                查看学员信息；
                确认/拒绝学员带教申请（本功能暂不实现）。
    """
    USER_LOGIN = 'USER_LOGIN'
    USER_REGISTER = 'USER_REGISTER'
    AJAX_IS_USER_EXIST = "AJAX_IS_USER_EXIST"
    GET_APPLYING_USER = 'GET_APPLYING_USER'
    TABLE_INIT = 'TABLE_INIT'
    TABLE_RENDER = 'TABLE_RENDER'


class resMsgDic:
    USER_REGISTER_SUCCESS = "用户注册成功"
    USER_DOES_NOT_EXIST = "用户不存在"
    USER_IS_DISABLED = "用户已被禁用"
    USER_IS_APPLYING = "用户申请审批中，请稍后再试"
    USER_IS_EXIST = "用户已存在，请更换账号或直接登陆"
    PROCESS_SUCCESS = "处理成功"


timeDic = {
    '1': '9:30',
    '2': '10:00',
    '3': '10:30',
    '4': '11:00',
    '5': '11:30',
    '6': '14:00',
    '7': '14:30',
    '8': '15:00',
    '9': '15:30',
    '10': '16:00',
    '11': '16:30',
    '12': '17:00',
    '13': '17:30',
}


def get_appoint_list_json(appoint_set):
    appoint_list = []
    for obj in appoint_set:
        begin_time_str = obj["appoint_time"][0]
        end_time_str = obj["appoint_time"][len(obj["appoint_time"]) - 1]
        begin_time = timeDic[begin_time_str.split("|")[1]]
        end_time = timeDic[str(int(end_time_str.split("|")[1]) + 1)]
        obj["full_date"] = str(obj["appoint_dt"]) + " " + begin_time + " ~ " + end_time
        appoint_list.append(utils.obj_to_json(obj))
    return appoint_list


def check_session(request):
    try:
        user_info = request.session["user"]
    except KeyError:
        user_info = UserInfo.objects.get(pk=6)  # 测试的替代做法，请在上线时删除
    finally:
        return user_info


def get_day_diff(begin_dt, end_dt):
    print(begin_dt)
    print(end_dt)
    return (end_dt - begin_dt).days


def get_time_diff(req_time):
    return int((req_time.hour * 60 + req_time.minute - __OPEN_TIME.hour * 60 - __OPEN_TIME.minute) / 30)
