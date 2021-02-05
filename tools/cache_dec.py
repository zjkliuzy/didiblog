from django.core.cache import cache

from tools.login_dec import get_user_by_request


def topic_cache(expire):
    def _topic_cache(func):
        def warp(request, *args, **kwargs):
            if "t_id" in request.GET.keys():
                return func(request, *args, **kwargs)
            visitor_name = get_user_by_request(request)
            author_name = kwargs["author_id"]

            if visitor_name == author_name:
                # 访问自己
                # get_full_path()返回带查询字符串的完整路径
                cache_key = "topic_cache_self_%s" % request.get_full_path()
            else:
                cache_key = "topic_cache_%s" % request.get_full_path()

            res = cache.get(cache_key)
            if res:
                print("-------------cache in----")
                return res
            else:
                res = func(request, *args, **kwargs)
                cache.set(cache_key, res, expire)
                return res

        return warp

    return _topic_cache
