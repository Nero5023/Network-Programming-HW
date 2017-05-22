#coding:utf-8

import socket
import select
import sys
import hashlib
import json

HOST = '127.0.0.1'
PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

userName = ""

printColorStrDic = {}
nextColorNum = 91

def colorName(name):
    global nextColorNum
    if printColorStrDic.get(name) is None:
        printColorStrDic[name] = '\x1b[%sm%s\x1b[0m' % (str(nextColorNum), name)
        if nextColorNum != 98:
            nextColorNum+=1
    return printColorStrDic[name]

def onRecvFromStdin(data, sock):
    if data == "exit":
        sock.close()
        sys.exit(0)
    # data = userName + ": " + data
    sock.send(data)

def onRecvFromSock(data):
    data = json.loads(data)
    print colorName(data['username']) + ": " + data['data']

def register(sock):
    try:
        name = raw_input("Please enter your name: ")
        password = ""
        while True:
            password = raw_input("Plase enter your password: ")
            passwordCheck = raw_input("Plase enter the password again: ")
            if password == passwordCheck and password != "":
                break
            elif password != passwordCheck:
                print "Password is not same!"
            else:
                print "Password is empty"
        passwordMd5 = hashlib.md5(password)
        passwordMd5 = passwordMd5.hexdigest()
        dataToSend = {"username": name, "password": passwordMd5}
        sock.sendall(json.dumps(dataToSend))
        reponse = sock.recv(1024)
        reponse = json.loads(reponse)
        if reponse['res'] == 0:
            print "Username and password do not compare! or This user haved login!" 
            return register(sock)
        else:
            print "Success!"
            print "Start chat..."
    except:
        sock.close()
        sys.exit(0)
    return name


sock.connect((HOST, PORT))
userName = register(sock)




while True:
    infs, outfs, excs = select.select([sock, sys.stdin],[],[])
    for inputFS in infs:
        if inputFS is sys.stdin:
            data = sys.stdin.readline()
            if data[-1] == '\n':
                data = data[:len(data)-1]
            onRecvFromStdin(data, sock)
        if inputFS is sock:
            newdata = sock.recv(1024)
            onRecvFromSock(newdata)

# def onRecvFromStdin(data, sock):
#     if data == "exit":
#         sock.close()
#         sys.exit(0)
#     data = userName + ": " + data
#     sock.send(data)
