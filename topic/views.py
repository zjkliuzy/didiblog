import json

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page

from message.models import Message
from tools.cache_dec import topic_cache
from tools.login_dec import *
from topic.models import Topic
from user.models import UserProfile


class TopicView(View):
    # 清除缓存的方法
    def clear_topic_caches(self, request, limit, category):
        """
        清除缓存
        :return:
        """
        if limit == "public":
            key_perfix = "topic_cache_self_"
        else:
            key_perfix = "topic_cache_"
        key_middle = request.path_info
        if category == "tec":
            key_last = "?category=tec"
        else:
            key_last = "?category=no-tec"

        list_key = []
        list_key.append(key_perfix + key_middle)
        list_key.append(key_perfix + key_middle + key_last)
        cache.delete_many(list_key)

    @method_decorator(login_check)
    def post(self, request, author_id):
        user = request.myuser
        json_str = request.body
        json_obj = json.loads(json_str)
        content = json_obj["content"]
        content_text = json_obj["content_text"]
        limit = json_obj["limit"]
        title = json_obj["title"]
        category = json_obj["category"]
        if limit not in ["public", "private"]:
            result = {"code": 10300, "error": "权限错误"}
            return JsonResponse(result)
        if category not in ["tec", "no-tec"]:
            result = {"code": 10301, "error": "分类错误"}
            return JsonResponse(result)
        Topic.objects.create(
            title=title,
            category=category,
            limit=limit,
            introduce=content_text[:30],
            content=content,
            user_profile=user
        )
        # 如果对文章列表使用了缓存，清理缓存
        self.clear_topic_caches(request, limit, category)
        return JsonResponse({"code": 200, "username": author_id})

    @method_decorator(topic_cache(100))
    def get(self, request, author_id):
        print("###############进入函数#################")
        try:
            author = UserProfile.objects.get(username=author_id)
        except:
            result = {"code": 10305, "error": "用户名错误"}
            return JsonResponse(result)
        # 获取访问者username
        visitor_name = get_user_by_request(request)

        t_id = request.GET.get("t_id")
        is_self = False
        if t_id:
            # 文章详情页
            if visitor_name == author_id:
                is_self = True
                try:
                    author_topic = Topic.objects.get(id=t_id, user_profile_id=author_id)
                except:
                    result = {"code": 10310, "error": "topic id 有误"}
                    return JsonResponse(result)
            else:
                # 非博主访问
                try:
                    author_topic = Topic.objects.get(id=t_id, user_profile_id=author_id, limit="public")
                except:
                    result = {"code": 10311, "error": "非公开博文"}
                    return JsonResponse(result)

            res = self.make_topic_json_single(author, author_topic, is_self)
            return JsonResponse(res)
        else:
            # 列表页
            filter_category = False
            category = request.GET.get("category")
            if category in ["tec", "no-tec"]:
                filter_category = True
            if visitor_name == author_id:
                if filter_category:
                    author_topics = Topic.objects.filter(user_profile_id=author_id, category=category)
                else:
                    author_topics = Topic.objects.filter(user_profile_id=author_id)

            else:

                if filter_category:
                    author_topics = Topic.objects.filter(user_profile_id=author_id, category=category, limit="public")
                else:
                    author_topics = Topic.objects.filter(user_profile_id=author_id, limit="public")

            res = self.make_topic_json(author, author_topics)

            return JsonResponse(res)

    def make_topic_json(self, author, topics):
        """
        构建json
        :param author:作者对象
        :param topics: 博文列表
        :return: json
        """
        topics_res = []
        for topic in topics:
            d = {}
            d["id"] = topic.id
            d["title"] = topic.title
            d["category"] = topic.category
            d["introduce"] = topic.introduce
            d["created_time"] = topic.created_time.strftime("%Y-%m-%d %H:%M:%S")
            d["author"] = author.nickname
            topics_res.append(d)
        res = {"code": 200, "data": {}}
        res["data"]["nickname"] = author.nickname
        res["data"]['topics'] = topics_res
        return res

    def make_topic_json_single(self, author, author_topic, is_self):
        result = {"code": 200, "data": {}}
        # 1文章详情
        result["data"]["nickname"] = author.nickname
        result["data"]["title"] = author_topic.title
        result["data"]["category"] = author_topic.category
        result["data"]["content"] = author_topic.content
        result["data"]["introduce"] = author_topic.introduce
        result["data"]["author"] = author.nickname
        result["data"]["created_time"] = author_topic.created_time
        # 2上一篇
        if is_self:
            next_topic = Topic.objects.filter(id__gt=author_topic.id, user_profile_id=author.username).first()
            last_topic = Topic.objects.filter(id__lt=author_topic.id, user_profile_id=author.username).last()
        else:
            next_topic = Topic.objects.filter(id__gt=author_topic.id, user_profile_id=author.username,
                                              limit="public").first()
            last_topic = Topic.objects.filter(id__lt=author_topic.id, user_profile_id=author.username,
                                              limit="public").last()
        if next_topic:
            next_id = next_topic.id
            next_title = next_topic.title
        else:
            next_id = None
            next_title = None
        if last_topic:
            last_id = last_topic.id
            last_title = last_topic.title
        else:
            last_id = None
            last_title = None

        result["data"]["last_id"] = last_id
        result["data"]["last_title"] = last_title
        result["data"]["next_id"] = next_id
        result["data"]["next_title"] = next_title
        # 3评论
        messages = Message.objects.filter(topic=author_topic).order_by("-created_time")
        msf_lis = []
        r_dict = {}
        msg_count = 0
        for item in messages:
            if item.parent_message:
                # 回复
                r_dict.setdefault(item.parent_message, [])
                r_dict[item.parent_message].append({
                    "msg_id": item.id,
                    "content": item.content,
                    "publisher": item.user_profile.nickname,
                    "publisher_avatar": str(item.user_profile.avatar),
                    "created_time": item.created_time.strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                # 评论
                msg_count += 1

                msf_lis.append({"id": item.id, "content": item.content, "publisher": item.user_profile.nickname,
                                "publisher_avatar": str(item.user_profile.avatar),
                                "created_time": item.created_time.strftime("%Y-%m-%d %H:%M:%S"), "reply": []})

        for m in msf_lis:
            if m["id"] in r_dict:
                m["reply"] = r_dict[m["id"]]

        result["data"]["messages"] = msf_lis
        result["data"]["messages_count"] = msg_count
        return result
