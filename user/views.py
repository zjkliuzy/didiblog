import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from user.models import UserProfile
import hashlib


class UserView(View):
    def get(self, request):
        return HttpResponse("user get")

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

        return JsonResponse({"code": 200})
