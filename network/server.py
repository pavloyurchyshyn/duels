import socket
from _thread import *
import sys

server = "192.168.0.105"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


def read_pos(string):
    string = string.split(",")
    # print(string)
    return int(round(float(string[0]), 1)), int(round(float(string[1]), 1)), float(string[2])  # , float(string[3])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + ',' + str(tup[2]) + ','  # + str(tup[3])


pos = [(100, 100, 0, 0), (100, 100, 0, 0)]


def threaded_client(conn, player, addr):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        # try:
        data = read_pos(conn.recv(2048).decode())
        pos[player] = data
        # print(f'Player {player}, data {data}')
        if not data:
            print("Disconnected")
            break
        else:
            if player == 1:
                reply = pos[0]
            else:
                reply = pos[1]

            # print("Received: ", data)
            # print("Sending : ", reply)

        conn.sendall(str.encode(make_pos(reply)))
        # except Exception as e:
        #     print(e)
        #     break

    print("Lost connection")
    conn.close()


print(socket.gethostbyname(socket.gethostname()))

currentPlayer = 0
threads = {}
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idx = start_new_thread(threaded_client, (conn, currentPlayer, addr))
    threads[currentPlayer] = idx
    currentPlayer += 1
