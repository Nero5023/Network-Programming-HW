## 进程和线程的基本概念* 进程是处于运行过程中的程序实例,是操作系统调度和分 配资源的基本单位。* 一个进程实体由程序代码、数据和进程控制块三部分构成。* 各种计算机应用程序在运行时,都以进程的形式存在。网络应用程序也不例外。

## 	实现网间进程通信必须解决哪些问题？
* 网间进程的标识问题；
* 如何与网络协议栈连接的问题；
* 协议的识别
* 不同的通信服务的问题

## 套接字
网络应用程序通过网络协议栈进行通信时所使用的接口,即应用程序与协议栈软件之间的接口,简称套接字编程 接口(Socket API)。 它定义了应用程序与协议栈软件进行交互时可以使用的一组操作,决定了应用程序使用协议栈的方式、应用程序所能实现的功能、以及开发具有这些功能的程序的难度。

## 端口
应用层进程与传输层协议实体间的通信接口。

## 什么是阻塞阻塞是指一个进程执行了一个函数或者系统调用,该函数由于某种原因不能立即完成,因而不能返回调用它的进程,导致进程受控于这个函数而处于等待的状态,进程的这种状态称为阻塞。

## ICMP
ICMP是(Internet Control Message Protocol)Internet控制报文协议。它是TCP/IP协议族的一个子协议,用于在IP主机、路由器之间传递控制消息。控制消息是指网络通不通、主机是否可达、 路由是否可用等网络本身的消息。这些控制消息虽然并不传输用户数据,但是对于用户数据的传递起着重要的作用。

## UDP协议UDP是User Datagram Protocol的简称,中文名是用户数据报协议,是OSI(Open System Interconnection,开放式系统互联)参考模型中一种无连接的传输层协议,提供面向事务的简单不可靠信息传送服务。UDP在IP报文的协议号是17。

* User Datagram Protocol
* 无连接的传输层协议
* 简单不可靠信息传送服务
* 在第四层——传输层,处于IP协议的上一层。
* 不提供数据包分组、组装和不能对数据包进行排序的缺点

### 特点
* UDP是一个无连接协议,传输数据之前源端和终端不建立连接
*  由于传输数据不建立连接
*  UDP信息包的头很短
*   吞吐量不受拥挤控制算法的调节,只受应用软件生成数据的速率、传输带宽、源端和终端主 机性能的限制。
*   UDP使用尽最大努力交付
*   UDP是面向报文的

## TCP 协议
传输控制协议 (Transmission Control Protocol,TCP)提供一个面向连接的、端到端的、 完全可靠的(无差错、无丢失、无重复或失序) 全双工的流传输服务。


* TCP是面向连接的传输层协议。 
* 面向字节流。* TCP提供可靠交付的服务。

### 可靠性保证
* 每个信息包都包含一个校验码
* 了防止信息包丢失,TCP会要求接收方每收到一个信息包都反馈一下
* 为了防止信息包重复或顺序错误TCP每传送一个信息包都会传送一个序号



## 多线程
* 适合采用多线程的任务特点: 本质上是异步的,需要有多个并发事务; 
* 各个事务的运行顺序可以是不确定的,随机的,不可预测的; 
* 非CPU密集型任务


## 常用函数

### S.getsockname() 和 S.getpeername()
#### getpeername
返回所连接的远程socket的地址和端口 

#### getsockname
返回关于本地socket的地址和端口


## 实例
### UPD

#### Server
```
import socket

BUF_SIZE = 1024
serverAddr = ('127.0.0.1', 8080)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(serverAddr)

while True:
    print "Waiting for data"
    data, client_addr = sock.recvfrom(BUF_SIZE)
    print "Connected by ", client_addr, " Receive Data: ", data
    sock.sendto(data, client_addr)

sock.close()
```

#### Client
```
import socket

BUF_SIZE = 1024
serverAddr = ('127.0.0.1', 8080)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    data = raw_input()
    sock.sendto(data, serverAddr)
    data, addr = sock.recvfrom(BUF_SIZE)
    print "Data: ", data
sock.close()
```