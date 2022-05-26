import time
from socket import *
import sys
import hashlib
import json
import numpy as np

global raschetchiki
global sumMatrix


def getRequest(data, host, port):
    md5 = hashlib.md5()
    md5.update(data.encode())
    addr = (host, port)
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    if not data:
        udp_socket.close()
        sys.exit(1)
    udp_socket.settimeout(1)
    data = json.dumps([md5.hexdigest(), data])
    data = str.encode(data)
    udp_socket.sendto(data, addr)
    data = udp_socket.recvfrom(1024)
    data = json.loads(data[0].decode())
    md5 = hashlib.md5()
    md5.update(data[1].encode())
    if md5.hexdigest() == data[0]:
        # print("Контрольная сумма совпадает")
        global raschetchiki
        raschetchiki = json.loads(data[1])
    else:
        print("Контрольная сумма полученного сообщения не совпадает!")
        raise Exception('Контрольная сумма полученного сообщения не совпадает!')
    udp_socket.close()


def getSum(data, host, port, a, b):
    md5 = hashlib.md5()
    md5.update(data.encode())
    addr = (host, port)
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    if not data:
        udp_socket.close()
        sys.exit(1)
    udp_socket.settimeout(1)
    data = json.dumps([md5.hexdigest(), data])
    data = str.encode(data)
    udp_socket.sendto(data, addr)
    data = udp_socket.recvfrom(1024)
    data = json.loads(data[0].decode())
    md5 = hashlib.md5()
    md5.update(data[1].encode())
    if md5.hexdigest() == data[0]:
        print("Контрольная сумма совпадает")
        print(data[1])
    #     global raschetchiki
    #     raschetchiki = json.loads(data[1])
    # else:
    #     print("Контрольная сумма полученного сообщения не совпадает!")
    #     raise Exception('Контрольная сумма полученного сообщения не совпадает!')
    udp_socket.close()


# говорим серверу, что мы расчётчик
while True:
    # «Нет большей неудачи, чем перестать пытаться».
    # — Элберт Хаббард
    try:
        try:
            getRequest(json.dumps([2]), 'localhost', 777)
            break
        except timeout:
            print("timeout")
            time.sleep(1)
    except:
        pass
print("Получили данные о доступных расчётчиках " + str(raschetchiki))

# читаем данные
readData = ""
with open("data.txt", "r") as f:
    for line in f:
        readData += line
m1, m2 = readData.split("\n\n")
m1 = np.array(list(map(lambda x: list(map(float, x)), list(map(lambda x: x.split(" "), m1.split("\n"))))))
m2 = np.array(list(map(lambda x: list(map(float, x)), list(map(lambda x: x.split(" "), m2.split("\n"))))))
# m1.shape = (1, 12)
# m1.shape = (3, 4)
l1 = len(m1)
l2 = len(m1[0])
sumMatrix = [0] * (l1 * l2)
l_raschetchiki = len(raschetchiki)
if l_raschetchiki > 0:
    m1.shape = (1, l1 * l2)
    m2.shape = (1, l1 * l2)
    m1 = list(m1)[0]
    m2 = list(m2)[0]

    getSum(json.dumps([list(m1), list(m2)]), raschetchiki[0][0], raschetchiki[0][1], 0, 12)
    # for i in range(0, l1 * l2, (l1 * l2) // l_raschetchiki):
    #     if i + l_raschetchiki >= l1 * l2:
    #         print(m1[i:l1 * l2])
    #         break
    #     else:
    #         print(m1[i:i + ((l1 * l2) // l_raschetchiki)])

else:
    print("А нет у нас расчётчиков :(")
