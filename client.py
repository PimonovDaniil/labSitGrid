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

addr = (myHost, myPort)

# socket - функция создания сокета
# первый параметр socket_family может быть AF_INET или AF_UNIX
# второй параметр socket_type может быть SOCK_STREAM(для TCP) или SOCK_DGRAM(для UDP)
udp_socket = socket(AF_INET, SOCK_DGRAM)
# bind - связывает адрес и порт с сокетом
udp_socket.bind(addr)


# Бесконечный цикл работы программы
while True:
    print('wait data...')
    # recvfrom - получает UDP сообщения
    conn, addr = udp_socket.recvfrom(1024)
    data = json.loads(conn.decode())
    md5 = hashlib.md5()
    md5.update(data[1].encode())
    if md5.hexdigest() == data[0]:
        # print("Контрольная сумма совпадает")
        data = json.loads(data[1])
        print(data)
        res = []
        for i in range(len(data[0])):
            sum = 0
            for j in range(len(data)):
                sum += data[j][i]
            res.append(sum)
        md5 = hashlib.md5()
        md5.update(json.dumps(res).encode())
        # sendto - передача сообщения UDP
        udp_socket.sendto(json.dumps([md5.hexdigest(), json.dumps(res)]).encode(), addr)
    else:
        md5 = hashlib.md5()
        md5.update(b'False')
        # sendto - передача сообщения UDP
        udp_socket.sendto(json.dumps([md5.hexdigest(), 'False']).encode(), addr)
udp_socket.close()