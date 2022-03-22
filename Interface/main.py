import tkinter as tk
import socket
from pickle import dumps
from random import randrange
from tkinter.font import NORMAL
from tkinter import TOP, ttk

from matplotlib.pyplot import fill


## SOCKET CONFIG ##
header_len = 10
ip = "127.0.0.1"
port = 1500

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
## SOCKET CONFIG ##

"""
def conect_server():
    client_socket. connect((ip, port))
"""

def conect_server():
    print(e_user.get())


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

def sim_fex(user, emotions):
    fex = emotions[randrange(len(emotions))]
    return {user:fex}
## TEMP ##


def init_enviar_dados():
    send_type("interpretador")
    while True:
        dict = sim_fex(user=e_user.get(), emotions=emotions)
        print(dict)

        send_dict(header_len, dict)

def retrieve_user():
    user = e_user.get()
    
    if user == "":
        b_conectar_servidor['state'] = tk.DISABLED
    else:
        b_conectar_servidor['state'] = tk.ACTIVE
        e_user['state'] = tk.DISABLED
        b_registrar_user['state'] = tk.DISABLED



## INTERFACE ##
root = tk.Tk()
root.geometry("300x300")
root.resizable(False, False)
root.title('Sistema interpretador')


## Frame
frame_interp = ttk.Frame(root)
frame_interp.pack(padx=10, fill='x', expand=True)


## Title
l_title = tk.Label(frame_interp, text="Sistema Interpretador",font=("Times 20"))
l_title.pack(fill='x', expand=True, pady=(0,25))


## Username entry
l_user_entry = tk.Label(frame_interp, text="Insira seu nome de usuário:")
l_user_entry.pack(fill='x', expand=True)

e_user = tk.Entry(frame_interp)
e_user.pack(fill='x', expand=True)

b_registrar_user = tk.Button(frame_interp, text="Registrar nome", command=retrieve_user)
b_registrar_user.pack(fill='x', expand=True, pady=(0,50))


b_conectar_servidor = tk.Button(frame_interp, text="Conectar ao servidor", command=conect_server, state=tk.DISABLED)
b_conectar_servidor.pack(fill='x', expand=True)


l_conect_status = tk.Label(frame_interp, text="Status: Não conectado")
l_conect_status.pack(fill='x', expand=True)


root.mainloop()
## INTERFACE ##