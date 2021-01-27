import json
import time

import jwt
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from user.models import UserProfile
import hashlib
from tools.login_dec import login_check

class UserView(View):
    def get(self, request, username=None):
        if username:
            # 返回指定用户信息
            try:
                user = UserProfile.objects.get(username=username)
            except:
                result = {"code": 10104, "error": "用户名称有误"}
                return JsonResponse(result)

            if request.GET.keys():
                #     获取指定信息
                data = {}
                for k in request.GET.keys():
                    if k == "password":
                        continue
                    elif hasattr(user, k):
                        data[k] = getattr(user, k)
                result = {"code": 200, "username": username, "data": data}
            else:
                # 全量信息
                result = {"code": 200, "username": username,
                          "data": {
                              "info": user.info, "sign": user.sign, "nickname": user.nickname,
                              "avatar": str(user.avatar)
                          }}
            return JsonResponse(result)
        else:
            return HttpResponse("返回所有用户信息")

    def post(self, request):
        json_str = request.body
        # json饭序列化
        json_obj = json.loads(json_str)
        username = json_obj["username"]
        email = json_obj["email"]
        phone = json_obj["phone"]
        password_1 = json_obj["password1"]
        password_2 = json_obj["password2"]
        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {"code": 10100, "error": "用户名已占用"}
            return JsonResponse(result)
        if password_1 != password_2:
            result = {"code": 10101, "error": "两次密码不一致"}
            return JsonResponse(result)
        # TODO 密码hash
        md5 = hashlib.md5()
        md5.update(password_1.encode())
        passHash = md5.hexdigest()
        try:
            UserProfile.objects.create(username=username, password=passHash, phone=phone, email=email,
                                       nickname=username)
        except:
            result = {"code": 10102, "error": "保存出错"}
            return JsonResponse(result)
        token = make_token(username)
        token = token.decode()
        return JsonResponse({"code": 200, "username": username, "data": {"token": token}})


def make_token(username, expire=3600 * 24):
    key = settings.JWT_TOKEN_KEY
    now = time.time()
    payload = {"username": username, "exp": now + expire}
    return jwt.encode(payload, key, algorithm="HS256")


@login_check
def user_avatar(request, username):
    if request.method != "POST":
        result = {"code": 10105, "error": "只接受post请求"}
        return JsonResponse(result)
    # 从request里面拿到user
    user = request.myuser
    # 修改用户头像
    user.avatar = request.FILES["avatar"]
    user.save()
    result = {"code": 200, "username": user.username}
    return JsonResponse(result)
