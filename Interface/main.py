import tkinter as tk
import socket
from pickle import dumps
from random import randrange


## SOCKET CONFIG ##
header_len = 10
ip = "127.0.0.1"
port = 1500

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
## SOCKET CONFIG ##


def conect_server():
    client_socket. connect((ip, port))


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


## TEMP ##
emotions = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
user = str(input("User: "))

def sim_fex(user, emotions):
    fex = emotions[randrange(len(emotions))]
    return {user:fex}
## TEMP ##


def init_enviar_dados():
    send_type("interpretador")
    while True:
        dict = sim_fex(user=user, emotions=emotions)
        print(dict)

        send_dict(header_len, dict)





## INTERFACE ##
window = tk.Tk()
window.geometry("600x300")

l_title = tk.Label(text="Sistema Interpretador",font=("Times 20",16))
l_title.pack()

b_conectar_servidor = tk.Button(text="Conectar ao servidor", command=conect_server, font=("Arial",14))
b_conectar_servidor.pack()

status_txt = ""
l_conect_status = tk.Label(text=status_txt,font=("Arial",14))
l_conect_status.pack()


window.mainloop()
## INTERFACE ##