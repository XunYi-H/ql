import time
import requests
from os import environ, system, path


# 读取通知
def load_send():
    global send, mg
    cur_path = path.abspath(path.dirname(__file__))
    if path.exists(cur_path + "/SendNotify.py"):
        try:
            from SendNotify import send
            print("加载通知服务成功！")
        except:
            send = False
            print("加载通知服务失败~")
    else:
        send = False
        print("加载通知服务失败~")


load_send()


# 获取环境变量
def get_environ(key, default="", output=True):
    def no_read():
        if output:
            print(f"未填写环境变量 {key} 请添加")
            exit(0)
        return default

    return environ.get(key) if environ.get(key) else no_read()


class Glados():
    def __init__(self, ck):
        self.msg = ''
        self.ck = ck

    def sign(self):
        time.sleep(1)
        url = "https://glados.rocks/api/user/checkin"
        headers = {
            'Cookie': self.ck,
            'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        }

        data = {
            "token": "glados.network"
        }
        r = requests.post(url, headers=headers, json=data)
        if r.status_code == 200:
            if r.json()['message'] == '没有权限':
                xx = f"[账号]{a}\n[签到]{r.json()['message']}，ck可能无效:{self.ck}\n\n"
                self.msg += xx
                return self.msg
            else:
                xx = f"[账号]{a}\n[签到]{r.json()['message']}\n\n"
                self.msg += xx
                return self.msg
        else:
            xx = f"[账号]{a}\n[签到]请检查网络或者ck有效性：{self.ck}\n\n"
            self.msg += xx
            return self.msg

    def get_sign_msg(self):
        return self.sign()


if __name__ == '__main__':
    token = get_environ("gladosck")
    if not token:
        print("未获取到gladosck环境变量，请检查配置")
        exit(0)
    msg = ''
    cks = token.split("&")
    print("检测到{}个ck记录\n".format(len(cks)))
    a = 0
    for ck in cks:
        a += 1
        run = Glados(ck)
        msg += run.get_sign_msg()
    if send:
        send("glados签到通知", msg)
    else:
        print(f"glados签到通知\n{msg}")
