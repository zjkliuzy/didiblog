import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from message.models import Message
from tools.login_dec import login_check
from topic.models import Topic


@login_check
def message_view(request, topic_id):
    # 限定post请求
    if request.method == "POST":
        json_str = request.body
        json_obj = json.loads(json_str)
        content = json_obj["content"]
        parent_id = json_obj.get("parent_id", 0)
        try:
            topic = Topic.objects.get(id=topic_id)
        except:
            result = {"code":10401,"error":"文章id有误"}
            return JsonResponse(result)
        user = request.myuser
        Message.objects.create(content=content, topic=topic, user_profile=user, parent_message=parent_id)
        return JsonResponse({"code": 200})
    else:
        result = {"code":10400,"error":"发送post请求"}
        return JsonResponse(result)
