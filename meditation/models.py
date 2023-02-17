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