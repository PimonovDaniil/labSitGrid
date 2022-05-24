from socket import *
import sys
from thr import Thr


@Thr.thread
def getRequest(data, host, port):
    addr = (host, port)

    udp_socket = socket(AF_INET, SOCK_DGRAM)

    if not data:
        udp_socket.close()
        sys.exit(1)

    # encode - перекодирует введенные данные в байты, decode - обратно
    data = str.encode(data)
    udp_socket.sendto(data, addr)
    data = udp_socket.recvfrom(1024)
    udp_socket.close()
    print(data)
    return data


print(getRequest("test1", 'localhost', 777))
print(getRequest("test2", 'localhost', 778))
