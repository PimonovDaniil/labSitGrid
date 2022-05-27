import time
from socket import *
import sys
import hashlib
import json
import numpy as np
from thr import Thr

global raschetchiki
global sumMatrix
global kol_ras


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
    flagKrSum = True
    while flagKrSum:
        flagKrSum = False
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
        global sumMatrix, kol_ras
        if md5.hexdigest() == data[0]:
            print("Контрольная сумма совпадает")
            k = 0
            data[1] = json.loads(data[1])
            for i in range(a, b):
                sumMatrix[i] = data[1][k]
                k += 1
            kol_ras -= 1
        else:
            flagKrSum = True
            print("Контрольная сумма полученного сообщения не совпадает!")

        udp_socket.close()


@Thr.thread
def check_size(data, host, port, a, b):
    print(port)
    maxSize = 60000  # размер датаграммы
    massData = [json.loads(data)]
    massData[0].append(a)
    massData[0].append(b)
    #print(massData)
    flag = True
    while flag:
        flag = False
        for i in range(len(massData)):
            #print(sys.getsizeof(json.dumps(massData[i])))
            if sys.getsizeof(json.dumps(massData[i])) > maxSize:
                flag = True
                m1 = [massData[i][0][0: len(massData[i][0]) // 2], massData[i][1][0: len(massData[i][0]) // 2],
                      massData[i][2], (massData[i][2] + massData[i][3]) // 2]
                m2 = [massData[i][0][len(massData[i][0]) // 2: len(massData[i][0])], massData[i][1][len(massData[i][0]) // 2: len(massData[i][0])],
                      (massData[i][2] + massData[i][3]) // 2, massData[i][3]]
                massData.append(m1)
                massData.append(m2)
                del massData[i]
                break
    print(massData)
    for i in range(len(massData)):
        getSum(json.dumps([list(massData[i][0]), list(massData[i][1])]), host, port, massData[i][2], massData[i][3])





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
l1 = len(m1)
l2 = len(m1[0])
sumMatrix = [0] * (l1 * l2)
l_raschetchiki = len(raschetchiki)
if l_raschetchiki > 0:
    m1.shape = (1, l1 * l2)
    m2.shape = (1, l1 * l2)
    m1 = list(m1)[0]
    m2 = list(m2)[0]

    #check_size(json.dumps([list(m1), list(m2)]), raschetchiki[0][0], raschetchiki[0][1], 0, 12)
    k = 0
    kol_ras = 0
    for i in range(0, l1 * l2, (l1 * l2) // l_raschetchiki):
        if i + l_raschetchiki >= l1 * l2:
            print(m1[i:l1 * l2])
            kol_ras += 1
            check_size(json.dumps([list(m1[i:l1 * l2]), list(m2[i:l1 * l2])]), raschetchiki[k][0], raschetchiki[k][1], i,
                   l1 * l2)
            break
        else:
            kol_ras += 1
            print(m1[i:i + ((l1 * l2) // l_raschetchiki)])
            check_size(json.dumps(
                [list(m1[i:i + ((l1 * l2) // l_raschetchiki)]), list(m2[i:i + ((l1 * l2) // l_raschetchiki)])]),
                   raschetchiki[k][0], raschetchiki[k][1], i,
                   i + ((l1 * l2) // l_raschetchiki))
        k += 1
    while kol_ras != 0:
        print("Ждём " + str(kol_ras) + " расчётчиклв")
    result = np.array([sumMatrix])
    result.shape = (l1, l2)
    print("\n\nРезультат сложения матриц:")
    print(result)
else:
    print("А нет у нас расчётчиков :(")
