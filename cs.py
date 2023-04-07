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


class Rdxk():
    def __init__(self, ck, pwd):
        self.msg = ''
        self.ck = ck

    def sign(self):
        time.sleep(1)
        headers = {
            "authori-zation": "Bearer " + authorization,
            "User-Agent": "Mozilla/5.0 (Linux; Android 11;Redmi Note 8 Pro Build/RP1A.200720.011;wv)AppleWebKit/537.36(KHTML./like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4435 MMWEBSDK/20230202 Mobile Safari/537.36 MMWEBID/9516MicroMessenger/8.0.33.2320(0x28002151) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android",
        }
        sgin_url = 'https://m.reduxingke.com/api/usersign/sign'
        sign_rsp = requests.post(url, headers=headers)
        time.sleep(1)
        info_url = 'https://m.reduxingke.com/api/userinfo'
        info_rsp = requests.get(infourl, headers=headers)
        tx_url = 'https://m.reduxingke.com/api/user/applyExtract'
        tx_info = requests.post(txurl, headers=txheaders, json=txdata).json()

        if sign_rsp.status_code == 200 and info_rsp.status_code == 200:
            if sign_rsp.json()['msg'] == '请登录':
                xx = f"[用户]{info_rsp.json()['data']['nickname']}\n[签到]{sign_rsp.json()['msg']}\nck可能无效:{self.ck}\n\n"
                self.msg += xx
                return self.msg
            else:
                xx = f"[用户]{info_rsp.json()['data']['nickname']}\n[签到]{sign_rsp.json()['msg']}\n[余额]{info_rsp.json()['data']['brokerage_price']}\n[提现]\n\n"
                self.msg += xx
                return self.msg
        else:
            xx = f"[账号]{a}\n[签到]请检查网络或者ck有效性：{self.ck}\n\n"
            self.msg += xx
            return self.msg

    def get_sign_msg(self):
        return self.sign()


if __name__ == '__main__':
    token = get_environ("Rdxkck")
    if not token:
        print("未获取到Rdxkck环境变量，请检查配置")
        exit(0)
    msg = ''
    cks = token.split("&")
    print("检测到{}个ck记录\n".format(len(cks)))
    a = 0
    for ck in cks:
        a += 1
        run = Rdxk(ck)
        msg += run.get_sign_msg()
    if send:
        send("Rdxk签到通知", msg)
    else:
        print(f"Rdxk签到通知\n{msg}")
