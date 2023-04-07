import time
import requests
from os import environ, path


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
            print(
                '''加载通知服务失败~\n请使用以下拉库地址\nql repo https://github.com/Bidepanlong/ql.git "bd_" "README" "SendNotify"''')
    else:
        send = False
        print(
            '''加载通知服务失败~\n请使用以下拉库地址\nql repo https://github.com/Bidepanlong/ql.git "bd_" "README" "SendNotify"''')


load_send()


# 获取环境变量
def get_environ(key, default="", output=True):
    def no_read():
        if output:
            print(f"未填写环境变量 {key} 请添加")
            exit(0)
        return default

    return environ.get(key) if environ.get(key) else no_read()


class Qdzs():
    def __init__(self, ck):
        self.msg = ''
        self.ck = ck

    def sign(self):
        time.sleep(1)
        sign_url = 'https://z1.yyyy.run/api/sign/userSignIn'
        list_url = 'https://z1.yyyy.run/api/sign/userSignList'
        headers = {

            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/6762',
            'token': self.ck,

        }

        while True:
            sign_rsp = requests.post(sign_url, headers=headers)
            time.sleep(1)
            list_rsp = requests.post(list_url, headers=headers)
            if sign_rsp.status_code == 200:
                if sign_rsp.json()['msg'] == '请登录后操作':
                    xx = f"[账号]：{a}\n[签到]：{sign_rsp.json()['msg']}，ck可能无效:{self.ck}\n\n"
                    self.msg += xx
                    break
                    return self.msg
                elif sign_rsp.json()['msg'] == '已超过今日签到次数上限':
                    jfye = 0
                    for jf in list_rsp.json()['data']:
                        jfye += float(jf['num'])
                    xx = f"[账号]：{a}\n[签到]：{sign_rsp.json()['msg']}\n[积分]：{jfye}\n\n"
                    print(xx)
                    self.msg += xx
                    return self.msg
                    break
                elif sign_rsp.json()['msg'] == '签到完成~':
                    jfye = 0
                    for jf in list_rsp.json()['data']:
                        jfye += float(jf['num'])
                    xx = f"[账号]：{a}\n[签到]：{sign_rsp.json()['msg']}\n[积分]：{jfye}\n\n"
                    print(xx)
                    self.msg += xx
                    return self.msg
                    continue
                else:
                    xx = f"[账号]：{a}\n[签到]：签到异常：{self.ck}\n\n"
                    print(xx)
                    self.msg += xx
                    return self.msg
                    break
            else:
                xx = f"[账号]：{a}\n[签到]：请检查网络或者ck有效性：{self.ck}\n\n"
                print(xx)
                self.msg += xx
                return self.msg
                break

    def get_sign_msg(self):
        return self.sign()


if __name__ == '__main__':
    token = get_environ("qdzsck")
    msg = ''
    cks = token.split("&")
    print("检测到{}个ck记录\n开始奇点知识签到\n".format(len(cks)))
    a = 0
    for ck in cks:
        a += 1
        run = Qdzs(ck)
        msg += run.get_sign_msg()
    if send:
        send("glados签到通知", msg)

