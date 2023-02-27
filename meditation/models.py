from django.db import models


class UserInfo(models.Model):
    def __str__(self):
        return str(self.user_id)

    class UserType(models.TextChoices):
        TRAINER = '01', 'Trainer'
        TRAINEE = '02', 'Trainee'

    class UserSex(models.TextChoices):
        UNKNOWN = '09', 'Unknown'
        MALE = '01', 'Male'
        FEMALE = '02', 'Female'

    class UserStat(models.TextChoices):
        NORMAL = '00', 'Normal'
        APPLYING = '09', 'Applying'
        DISABLE = '10', 'Disable'

    user_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    login_id = models.TextField(max_length=100)
    login_pwd = models.TextField(max_length=100)
    user_nm = models.TextField(max_length=100, null=True)
    user_type = models.CharField(max_length=2, choices=UserType.choices, default=UserType.TRAINEE)
    user_sex = models.CharField(max_length=2, choices=UserSex.choices, default=UserSex.UNKNOWN)
    user_stat = models.CharField(max_length=2, choices=UserStat.choices, default=UserStat.APPLYING)
    register_dt = models.DateTimeField()
    last_login_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_user_info'


class ScheduleInfo(models.Model):
    def __str__(self):
        return str(self.schedule_id)

    class ScheduleStat(models.TextChoices):
        NORMAL = '00', 'Normal'
        INITIAL = '09', 'Initial'
        CLOSE = '10', 'Close'

    schedule_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    trainer = models.ForeignKey(UserInfo, on_delete=models.DO_NOTHING, db_column='trainer_id')
    begin_dt = models.DateField()
    end_dt = models.DateField()
    disable_time = models.JSONField(null=True)
    schedule_stat = models.CharField(max_length=2, choices=ScheduleStat.choices)
    last_upd_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_schedule_info'


class AppointInfo(models.Model):
    class AppointStat(models.TextChoices):
        NORMAL = '00', 'Normal'
        SELF_CANCEL = '10', 'Self Cancel'
        TRAINER_CANCEL = '11', 'Trainer Cancel'
        DONE = '01', 'Train Finished'

    appoint_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    trainee = models.ForeignKey(UserInfo, on_delete=models.DO_NOTHING, db_column='trainee_id')
    schedule = models.ForeignKey(ScheduleInfo, on_delete=models.DO_NOTHING, db_column='schedule_id')
    appoint_time = models.JSONField()
    appoint_dt = models.DateField()
    appoint_stat = models.CharField(max_length=2, choices=AppointStat.choices)
    preview_work = models.JSONField()
    review_work = models.JSONField()
    last_upd_dt = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_appoint_info'
