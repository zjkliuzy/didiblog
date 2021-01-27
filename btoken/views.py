import hashlib
import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from user.models import UserProfile
from user.views import make_token


class TokenView(View):
    def post(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj["username"]
        password = json_obj["password"]
        try:
            user = UserProfile.objects.get(username=username)
        except:
            result = {"code": 10200, "error": "用户名或密码错误"}
            return JsonResponse(result)

        md5 = hashlib.md5()
        md5.update(password.encode())
        pass_h = md5.hexdigest()
        if pass_h != user.password:
            result = {"code": 10201, "error": "用户名或密码错误"}
            return JsonResponse(result)
        token = make_token(username)
        token = token.decode()
        return JsonResponse({"code": 200, "username": username, "data": {"token": token}})
