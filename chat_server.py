"""
    聊天室
"""

import os, sys
from socket import *

HOST = '176.215.155.161'
PORT = 9317
ADDR = (HOST, PORT)

# 存储
user = {}


def do_login(s, name, addr):
    if ("管理员" in name ) or (name in user) :
        s.sendto("\n该用户已存在".encode(), addr)
        return
    s.sendto(b"OK", addr)

    # 通知其他人
    msg = "欢迎%s进入聊天室" % name
    for i in user:
        s.sendto(msg.encode(), user[i])

    # 将用户加入
    user[name] = addr
    print(user)


def do_chat(s,name,text):
    msg = "%s发言 : %s"%(name,text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])

def do_quit(s,name):
    msg = "%s退出了聊天室"%name
    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])
        else:
            s.sendto(b"EXIT",user[i])
    # 将用户删除
    del user[name]


# 接收各种客户端请求
def do_request(s):
    while True:
        data, addr = s.recvfrom(1024)
        # 如何判断收到的是姓名登录信息,自建协议
        msg = data.decode().split(' ')
        # 区分请求类型
        if msg[0] == 'L':
            do_login(s, msg[1], addr)
        elif msg[0] == 'C':
            #将切割后的信息拼接起来
            text = ' '.join(msg[2:])
            do_chat(s,msg[1],text)
        elif msg[0] == 'Q':
            do_quit(s,msg[1])


# 创建网络连接
def main():
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)
    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        while True:
            msg = input("管理员消息:")
            # 子进程中的user一直为空,故而将管理员消息发送给自身服务器
            msg = "C 管理员消息 " + msg
            s.sendto(msg.encode(),ADDR)
    else:
        # 请求处理
        do_request(s)  # 处理客户端请求


if __name__ == "__main__":
    main()
