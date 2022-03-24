import socket
import pickle
import tkinter as tk
from PIL import ImageTk, Image
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#### SOCKET CONFIG ####
header_len = 10
ip = "127.0.0.1"
port = 1500

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#### SOCKET CONFIG ####


#### DEF  ####
def send_type(type):
    data = bytes(type, "utf-8")

    header = bytes(f"{len(data):<{header_len}}", "utf-8")
    msg = header+data

    client_socket.send(msg)


def recv_dict(client_socket):
    try:
        msg_header = client_socket.recv(header_len)

        if not len(msg_header):
            return False

        msg_len = int((msg_header).decode("utf-8").strip())

        msg = client_socket.recv(msg_len)
        return pickle.loads(msg)
        
    except:
        return False


def conect_server():
    try:
        client_socket.connect((ip, port))
        client_socket.setblocking(False)
        send_type("receptor")

        l_conect_status['text'] = "Status: Conectado"
        l_conect_status['foreground'] = 'green'

    except:
        print("Não foi possível conectar ao servidor.")


def graph():
    y= np.random.normal(100, 50, 100)
    x = 25

    plt.hist(y, x)

#### DEF  ####


#### INTERFACE ####
## Root ##
root = tk.Tk()
root.geometry("400x400")
root.resizable(False, False)
root.title('Sistema Receptor')
#---------------------#


## Frame ##
frame_recep = tk.Frame(root)
frame_recep.pack(padx=10, fill='x', expand=True)
#---------------------#


## Title ##
l_title = tk.Label(frame_recep, text="Sistema Receptor",font=("Times 20"))
l_title.pack(fill='x', expand=True, pady=(0,25))
#---------------------#

## Conectar / Status ##
b_conectar_servidor = tk.Button(frame_recep, text="Conectar ao servidor", command=conect_server)
b_conectar_servidor.pack(fill='x', expand=True)

l_conect_status = tk.Label(frame_recep, text="Status: Não conectado", foreground='red')
l_conect_status.pack(fill='x', expand=True, pady=(0,25))
#---------------------#

## Exibição de dados ##
fig_vbar = plt.figure()
graph_vbar = fig_vbar.add_subplot(111)
canva = FigureCanvasTkAgg(fig_vbar, frame_recep)
canva.get_tk_widget().pack()
graph()
#---------------------#



root.mainloop()
#### INTERFACE ####