# UDP 编程

## Purpose
----------
实现一个UDP进行通信的客户端和服务器端的程序

## Description
----------
* **udp_client.py ** - UDP 客户端，接收用户输入，发送给服务端（代理） 
* **udp_server.py ** - UDP 服务端，接收客户端数据，稍作处理返回，若数据为 'wc', 则返回所用数据的词频信息
* **udp_proxy.py**   - UDP 代理，接收客户端数据，发送给客户端，然后返回数据给客户端
* **udp_multicast_chatroom.py** - UDP 多播聊天室

## Requirement
----------
* Python 2.7


## Usage
----------
### 客户端和服务器端的程序

``` bash
python udp_client.py 
python udp_server.py 
python udp_proxy.py 
```
#### Example
##### client
``` bash
Hello world!
Hello, ('127.0.0.1', 53709), you send Hello world!
Hello Google!
Hello, ('127.0.0.1', 53709), you send Hello Google!
World
Hello, ('127.0.0.1', 53709), you send World
wc
Counter({'Hello': 2, 'world': 1, 'Google': 1, 'World': 1})
```

##### proxy
``` bash
Start proxy server
Proxy receive from ('127.0.0.1', 51168)
Proxy send data to server: ('127.0.0.1', 8080)
Proxy get data from server
Proxy send the data received from server to client
--------------------------
Proxy receive from ('127.0.0.1', 51168)
Proxy send data to server: ('127.0.0.1', 8080)
Proxy get data from server
Proxy send the data received from server to client
--------------------------
Proxy receive from ('127.0.0.1', 51168)
Proxy send data to server: ('127.0.0.1', 8080)
Proxy get data from server
Proxy send the data received from server to client
--------------------------
Proxy receive from ('127.0.0.1', 51168)
Proxy send data to server: ('127.0.0.1', 8080)
Proxy get data from server
Proxy send the data received from server to client
--------------------------
```

##### server
``` bash
Start server
Receive from ('127.0.0.1', 53709):Hello world!
Receive from ('127.0.0.1', 53709):Hello Google!
Receive from ('127.0.0.1', 53709):World
Receive from ('127.0.0.1', 53709):wc
```

### 聊天室
可多个终端开启多次 

``` bash
python udp_multicast_chatroom.py
```

#### Example

``` bash
Please enter your name: Nero
Hello world
12:45:19 Nero> Hello world

12:45:27 Google> Hi, Nero

12:45:38 Google> Hi, Trump

12:45:52 Trump> Hello, guys!
```