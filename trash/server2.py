# Модуль socket для сетевого программирования
import time
from socket import *

# данные сервера
host = 'localhost'
port = 778
addr = (host, port)

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
    print('client addr: ', addr)
    print('client conn: ', conn)
    time.sleep(5)
    # sendto - передача сообщения UDP
    udp_socket.sendto(b'message received by the server2', addr)

udp_socket.close()
