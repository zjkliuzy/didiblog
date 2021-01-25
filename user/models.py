from django.db import models
import random


def default_sign():
    """
    随机个人签名
    :return:
    """
    sign = ["IT精英", "创业者", "健身达人"]
    return random.choice(sign)


# Create your models here.
class UserProfile(models.Model):
    username = models.CharField("用户名", max_length=20, primary_key=True)
    nickname = models.CharField("昵称", max_length=30)
    email = models.EmailField("邮箱")
    password = models.CharField("密码", max_length=32)
    sign = models.CharField("个人签名", max_length=50, default=default_sign)
    info = models.CharField("个人简介", max_length=150, default="")
    avatar = models.ImageField(upload_to="avatar", null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    phone = models.CharField("手机号", max_length=11, default="")
