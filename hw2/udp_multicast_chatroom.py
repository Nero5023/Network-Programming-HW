#coding:utf-8

import socket
import time

import sys, select

def getLine():
    i, _, _ = select.select([sys.stdin], [], [], 0.0001)
    for s in i:
        if s == sys.stdin:
            userInput = sys.stdin.readline()
            return userInput
    return False

ANY = '0.0.0.0'
MCAST_ADDR = '224.1.1.1'
MCAST_PORT = 1600

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# 允许端口复用 mac 这里用了
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
# 绑定监听多播数据包的端口
sock.bind((ANY,MCAST_PORT))
# 设置为多播类型的socket
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
# 入指定的多播组，组地址由第三个参数指定
status = sock.setsockopt(socket.IPPROTO_IP,
socket.IP_ADD_MEMBERSHIP,
socket.inet_aton(MCAST_ADDR) + socket.inet_aton(ANY))

sock.setblocking(0)
ts = time.time()

name = raw_input("Please enter your name: ")
while True:
    try:
        data, addr = sock.recvfrom(1024)
        if data:
            timeNow = time.strftime("%H:%M:%S", time.localtime())
            print timeNow + " " + data
    except socket.error, e:
        pass
    except KeyboardInterrupt:
        sock.close()
        break

    userInput = getLine()
    if (userInput != False and userInput != "" and not userInput.isspace()):
        userInput = name + "> " + userInput
        sock.sendto(userInput, (MCAST_ADDR,MCAST_PORT))
