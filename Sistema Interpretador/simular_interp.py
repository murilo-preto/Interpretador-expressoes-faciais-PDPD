import socket
from pickle import dumps
from random import randrange
from time import sleep


################################ Socket config ################################
header_len = 10
ip = "127.0.0.1"
port = 1500

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket. connect((ip, port))


################################ Functions ################################
def send_dict(header_len, dict):
    data = dumps(dict)

    header = bytes(f"{len(data):<{header_len}}", "utf-8")
    msg = header+data

    client_socket.send(msg)


def send_type(type):
    data = bytes(type, "utf-8")

    header = bytes(f"{len(data):<{header_len}}", "utf-8")
    msg = header+data

    client_socket.send(msg)


def sim_fex(user, emotions):
    fex = emotions[randrange(len(emotions))]
    return {user:fex}


################################# Logic ################################
emotions = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
user = str(input("User: "))


send_type("interpretador")
while True:
    dict = sim_fex(user=user, emotions=emotions)
    print(dict)

    send_dict(header_len, dict)
    
    sleep(3)