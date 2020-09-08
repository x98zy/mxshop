import json
import requests

class Yunpian():
    def __init__(self,api_key):
        self.api_key=api_key
        self.single_send_url="https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self,mobile,code):
        params={
            "apikey":self.api_key,
            "mobile":mobile,
            "text":"生鲜商城：您的验证码是%s。如非本人操作请忽略"%(code)
        }
        reponse=requests.post(self.single_send_url,data=params)
        re_dict=json.loads(reponse.text)
        return re_dict

if __name__=="__main__":
    yunpian=Yunpian("505f81879dd07052c1122f32225984a4")
    yunpian.send_sms("18870558696",4352)