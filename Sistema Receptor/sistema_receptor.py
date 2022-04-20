#### IMPORTS ####
import tkinter as tk
from tkinter import ttk

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
matplotlib.use('TkAgg')

import matplotlib.animation as animation

from matplotlib import style
style.use('ggplot')

from collections import Counter

import socket
import pickle


#### SOCKET CONFIG ####
header_len = 10
ip = "127.0.0.1"
port = 1500
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#### INIT GRAPH ####
f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)
fex = {}
emotions_counter = {'neutral': 0, 'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'sad': 0, 'surprise': 0}
clear_counter=0


#### DEF ####
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

    except:
        print("Não foi possível conectar ao servidor.")


def animate(i): #Animar gráfico
    global clear_counter
    global fex

    clear_counter += 1
    if clear_counter > 10:
        fex = {}
        clear_counter=0

    fex_dict = recv_dict(client_socket)
    if fex_dict != False:
        emotions_counter.update({'neutral': 0, 'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'sad': 0, 'surprise': 0})
        fex.update(fex_dict)

    emotions = fex.values()
    emotions_counter.update(Counter(emotions))

    keys = emotions_counter.keys()
    values = emotions_counter.values()

    a.clear()
    a.bar(keys, values)

#### GUI ####
LARGE_FONT = ('Times New Roman', 20) #Fonte para títulos

class SistemaReceptor(tk.Tk): #Root
    def __init__(self, *args, **krwags):
        tk.Tk.__init__(self, *args, **krwags)

        tk.Tk.wm_title(self, 'Sistema Receptor')
        tk.Tk.wm_geometry(self, '525x525')
        tk.Tk.wm_resizable(self, False, False)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Page_start, Page_1):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(Page_start)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Page_start(tk.Frame): #Página inicial
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title = tk.Label(self, text='Tela Inicial', font=LARGE_FONT)
        title.pack(expand=True, padx=(10,10), pady=(10,10))

        b_conectar_servidor = ttk.Button(self, text="Conectar ao servidor", command=conect_server)
        b_conectar_servidor.pack(fill=tk.BOTH, expand=True, padx=(10,10), pady=(10,50))

        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill='x', padx=(10,10))

        navegar = tk.Label(self, text='Telas:', font=('Times New Roman', 16))
        navegar.pack(expand=True, padx=(10,10), pady=(10,10))

        button1 = ttk.Button(self, text="Gráfico em barra", command=lambda: controller.show_frame(Page_1))
        button1.pack(fill=tk.BOTH, expand=True, padx=(10,10), pady=(0,10))


class Page_1(tk.Frame): #Gráfico em barra
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title = tk.Label(self, text='Gráfico em barra', font=LARGE_FONT)
        title.pack(padx=(10,10), pady=(10,10))

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=(10,10), pady=(10,10))

        button1 = ttk.Button(self, text="Retornar: Tela Inicial", command=lambda: controller.show_frame(Page_start))
        button1.pack(fill=tk.BOTH, expand=True, padx=(10,10), pady=(10,10))

app = SistemaReceptor()
ani = animation.FuncAnimation(f,animate, interval=1000) #Intervalo de atualização do gráfico
app.mainloop()