"""meditation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from meditation.views import common_views, user_views, trainee_views, trainer_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 首页
    path('hello/', common_views.hello),

    # 以下为特殊的调用，包括直接调用页面及ajax调用
    path('direct/<path:url>', common_views.direct),

    # 用户类路径
    path('login/', user_views.login),
    path('register/', user_views.register),
    path('logout/', user_views.logout),

    # 学员类路径
    path('getTraineeScheduleList/', trainee_views.get_trainee_schedule_list),
    path('getScheduleDetail/', trainee_views.get_schedule_detail),
    path('cancelAppoint/', trainee_views.cancel_appoint),
    path('traineeAppoint/', trainee_views.trainee_appoint),
    path('getTraineeAppointList/', trainee_views.get_trainee_appoint_list),
    path('getAppointWork/', trainee_views.get_appoint_work),
    path('saveWork/', trainee_views.save_work),

    # 教练类路径
    path('getScheduleList/', trainer_views.get_schedule_list),
    path('createSchedule/', trainer_views.create_schedule),
    path('getTrainerAppointList/', trainer_views.get_trainer_appoint_list),
    path('getApplyUserList/', trainer_views.get_apply_user_list),
    path('applyVerify/', trainer_views.apply_verify),
    path('saveScheduleDetail/', trainer_views.save_schedule_detail),
]

handler404 = common_views.res_404
