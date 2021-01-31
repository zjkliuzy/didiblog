import datetime
import hashlib
import json
import base64
import requests


class YunTongxin:
    base_url = "https://app.cloopen.com:8883"

    def __init__(self, accountSid, accountToken, appId, templateId):
        self.accountSid = accountSid
        self.accountToken = accountToken
        self.appId = appId
        self.templateId = templateId

    def get_request_url(self, sig):
        self.url = self.base_url + "/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s" % (self.accountSid, sig)
        return self.url

    def get_timestamp(self):
        now = datetime.datetime.now()
        now_str = now.strftime("%Y%m%d%H%M%S")
        return now_str

    def get_sig(self, timestamp):
        data = self.accountSid + self.accountToken + timestamp
        md5 = hashlib.md5()
        md5.update(data.encode())
        hash_value = md5.hexdigest()
        return hash_value.upper()

    def get_request_header(self, timestamp):
        """
        构建请求头
        :param timestamp:
        :return:
        """
        data = self.accountSid + ":" + timestamp
        data_bs = base64.b64encode(data.encode())
        data_bs = data_bs.decode()
        return {
            "Accept": "application/json",
            "Content-Type": "application/json;charset=utf-8",
            "Authorization": data_bs
        }

    def get_request_body(self, phone, code):
        """
        构建请求体
        :param phone:
        :param code:
        :return:
        """
        data = {
            "to": phone,
            "appId": self.appId,
            "templateId": self.templateId,
            "datas": [code, 3]
        }
        return data

    def do_request(self, url, header, body):
        res = requests.post(url, headers=header, data=json.dumps(body))
        return res.text

    def run(self, phone, code):
        timestamp = self.get_timestamp()
        sig = self.get_sig(timestamp)
        url = self.get_request_url(sig)

        header = self.get_request_header(timestamp)
        body = self.get_request_body(phone, code)
        res = self.do_request(url, header, body)
        return res


if __name__ == '__main__':
    asid = "8aaf0708773733a8017741b5e99704c0"
    atoken = "06dadebda10d4e4db6e4ecef6c117616"
    appid = "8aaf0708773733a8017741b5ea2004c7"
    templateId = "1"
    yun = YunTongxin(asid, atoken, appid, templateId)
    res = yun.run("13146650318", "123456")
    print(res)
