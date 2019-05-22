"""
    聊天室客户端
"""

import os, sys
from socket import *

HOST = '176.215.155.161'
PORT = 9317
ADDR = (HOST, PORT)


# 发送消息
def send_msg(s, name):
    while True:
        try:
            text = input()
        except KeyboardInterrupt:
            # 当有异常时直接赋值为quit退出
            text = 'quit'
        # 退出聊天室
        if text == "quit":
            msg = "Q "+name
            s.sendto(msg.encode(),ADDR)
            sys.exit("退出聊天室")
        msg = "C %s %s" % (name, text)
        s.sendto(msg.encode(), ADDR)


# 接收消息
def recv_msg(s):
    while True:
        data, addr = s.recvfrom(1024)
        # 因为进程不相互影响,所以通过服务端反馈的消息退出客户端
        if data == "EXIT":
            sys.exit()
        print(data.decode()+ '\n发言:',end = "")


def main():
    s = socket(AF_INET, SOCK_DGRAM)
    while True:
        name = input("请输入姓名:")
        # 自定义一个协议内容
        msg = "L " + name
        s.sendto(msg.encode(), ADDR)
        # 等待回应
        data, addr = s.recvfrom(1024)
        if data.decode() == "OK":
            print("您已进入聊天室")
            break
        else:
            print(data.decode())

    # 创建新的进程
    pid = os.fork()
    if pid < 0:
        sys.exit("Error")
    elif pid == 0:
        send_msg(s, name)
    else:
        recv_msg(s)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        sys.exit()
