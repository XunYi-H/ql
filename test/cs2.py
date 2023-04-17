from os import environ


a = '112#12@33'

c = a.split("@")
for b in c:
    print(b)
    print()
    c = b.split('#')
    print(c)
    if len(c) == 2:
        print("交易密码为：" + c[1])
    else:
        print("没有交易密码")
    print()