import jwt
from django.conf import settings
from django.http import JsonResponse

from user.models import UserProfile


def login_check(func):
    """
    登录用户检查
    :param func:
    :return:
    """
    def wrap(request, *args, **kwargs):
        # 从request中拿到token
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            result = {"code": 403, "error": "请登录"}
            return JsonResponse(result)
        try:
            payload = jwt.decode(token, settings.JWT_TOKEN_KEY, algorithm="HS256")
        except:
            result = {"code": 403, "error": "请登录"}
            return JsonResponse(result)

        username = payload["username"]
        user = UserProfile.objects.get(username=username)
        request.myuser = user
        # 调用装饰的函数
        return func(request, *args, **kwargs)

    return wrap
