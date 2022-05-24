# Запросы к серверу
# 1 - сообщить свой адрес
# 2 - узнать вдреса расчётчиков

# Модуль socket для сетевого программирования
import time
from socket import *
import hashlib
import json

# данные сервера
host = 'localhost'
port = 777
addr = (host, port)

# socket - функция создания сокета
# первый параметр socket_family может быть AF_INET или AF_UNIX
# второй параметр socket_type может быть SOCK_STREAM(для TCP) или SOCK_DGRAM(для UDP)
udp_socket = socket(AF_INET, SOCK_DGRAM)
# bind - связывает адрес и порт с сокетом
udp_socket.bind(addr)

raschetchiki = []

# Бесконечный цикл работы программы
while True:
    print('wait data...')

    # recvfrom - получает UDP сообщения
    conn, addr = udp_socket.recvfrom(1024)
    # print('client addr: ', addr)
    data = json.loads(conn.decode())
    # print('client data: ', data)
    md5 = hashlib.md5()
    md5.update(data[1].encode())
    if md5.hexdigest() == data[0]:
        # print("Контрольная сумма совпадает")
        data = json.loads(data[1])
        if data[0] == 1:
            print("Получили данные о расчётчике " + str(data[1]) + " " + str(data[2]))
            raschetchiki.append([data[1], data[2]])
            md5 = hashlib.md5()
            md5.update(b'True')
            # sendto - передача сообщения UDP
            udp_socket.sendto(json.dumps([md5.hexdigest(), 'True']).encode(), addr)
        elif data[0] == 2:
            md5 = hashlib.md5()
            md5.update(json.dumps(raschetchiki).encode())
            # sendto - передача сообщения UDP
            udp_socket.sendto(json.dumps([md5.hexdigest(), json.dumps(raschetchiki)]).encode(), addr)
            print("Отправили данные о расчётчике основному клиенту")
    else:
        md5 = hashlib.md5()
        md5.update(b'False')
        # sendto - передача сообщения UDP
        udp_socket.sendto(json.dumps([md5.hexdigest(), 'False']).encode(), addr)
udp_socket.close()
