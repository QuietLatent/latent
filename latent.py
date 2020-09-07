from time import time
from urllib import parse

import requests
import random
import hashlib


class Function:
    def __init__(self, session, question):
        self.session = session
        self.question = question.replace(" ", "")
        self.time_stamp = str(int(time()))
        self.nonce_str = ''.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz', 10))
        self.params = {'app_id': '2156483958', 'session': self.session, 'question': self.question,
                       'time_stamp': self.time_stamp, 'nonce_str': self.nonce_str, 'sign': ''}
        self.appkey = "kuWh8x8RHwuWx3ZK"

    def getReqSign(self):
        t = []
        for key in sorted(self.params):
            value = parse.quote(str(self.params[key]))
            if value != "":
                t.append(key + "=" + value + "&")
        s = ''.join(t) + "app_key=" + self.appkey
        hash_md5 = hashlib.md5()
        hash_md5.update(s.encode())
        sign = hash_md5.hexdigest().upper()
        self.params['sign'] = sign

    def doHttpPost(self):
        url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"
        r = requests.post(url=url, data=self.params)
        r_content = eval(r.text)
        return r_content


if __name__ == "__main__":
    print("=====欢迎来到聊天机器人=====")
    session_ch = input("是否创建新的聊天会话？(y/n)\n>>>")
    if session_ch == 'y':
        session = ''.join(random.sample('0123456789', 5))
        while True:
            question = input(">>>")
            fuc = Function(session, question)

            fuc.getReqSign()
            #fuc.doHttpPost()
            r_session = fuc.doHttpPost().get('data').get('session')
            r_answer = fuc.doHttpPost().get('data').get('answer')
            if fuc.doHttpPost().get('ret') == 0 and fuc.doHttpPost().get('msg') == 'ok':
                print("会话ID：", r_session)
                print(r_answer)
            else:
                print("参数错误，请重试")
    else:
        exit()
