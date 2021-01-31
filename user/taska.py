from didiblog.celery import app
from tools.sms import YunTongxin


@app.task
def send_sms(phone, code):
    """
    通过消费者去处理发送验证码服务
    :param phone:
    :param code:
    :return:
    """
    # TODO 写道配置文件里面
    asid = "8aaf0708773733a8017741b5e99704c0"
    atoken = "06dadebda10d4e4db6e4ecef6c117616"
    appid = "8aaf0708773733a8017741b5ea2004c7"
    templateId = "1"
    yun = YunTongxin(asid, atoken, appid, templateId)
    res = yun.run(phone, code)
    print(res)
