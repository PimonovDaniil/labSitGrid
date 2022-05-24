import time
from socket import *
import sys
import hashlib
import json

# данные сервера
myHost = 'localhost'
myPort = 778


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
        if data[1] == "True":
            print("Расчётчик зарегистрирован на сервере")
        else:
            print("Ошибка на сервере! (мб сообщение побилось по пути к серваку)")
            raise Exception('Ошибка на сервере! (мб сообщение побилось по пути к серваку)')
    else:
        print("Контрольная сумма полученного сообщения не совпадает!")
        raise Exception('Контрольная сумма полученного сообщения не совпадает!')

    udp_socket.close()


# говорим серверу, что мы расчётчик
while True:
    # «Нет большей неудачи, чем перестать пытаться».
    # — Элберт Хаббард
    try:
        try:
            getRequest(json.dumps([1, myHost, myPort]), 'localhost', 777)
            break
        except timeout:
            print("timeout")
            time.sleep(1)
    except:
        pass
