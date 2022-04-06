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


#### INIT GRAPH ####
f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)


#### DEF ####
def animate(i): #Animar gráfico
    fex_dict = {}
    emotions_counter = {}

    pullData = open('sampleText.txt','r').read()
    dataArray = pullData.split('\n')
    for eachLine in dataArray:
        user, emotion = eachLine.split(',')
        fex_dict[user] = emotion
    
    emotions = fex_dict.values()
    emotions_counter.update(Counter(emotions))

    keys = emotions_counter.keys()
    values = emotions_counter.values()

    a.clear()
    a.bar(keys, values)


#### GUI ####
LARGE_FONT = ('Verdana', 16) #Fonte para títulos

class SistemaReceptor(tk.Tk): #Root
    def __init__(self, *args, **krwags):
        tk.Tk.__init__(self, *args, **krwags)

        tk.Tk.wm_title(self, 'Sistema Receptor')

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Page_start, Page_1, Page_2):
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

        title = ttk.Label(self, text='Tela Inicial', font=LARGE_FONT)
        title.pack(padx=(10,10), pady=(10,10))

        button1 = ttk.Button(self, text="Gráfico em barra", command=lambda: controller.show_frame(Page_1))
        button1.pack()

        button2 = ttk.Button(self, text="Tela 2", command=lambda: controller.show_frame(Page_2))
        button2.pack()


class Page_1(tk.Frame): #Gráfico em barra
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title = ttk.Label(self, text='Gráfico em barra', font=LARGE_FONT)
        title.pack(padx=(10,10), pady=(10,10))

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=(10,10), pady=(10,10))

        button1 = ttk.Button(self, text="Retornar: Tela Inicial", command=lambda: controller.show_frame(Page_start))
        button1.pack()


class Page_2(tk.Frame): #Placeholder
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        title = ttk.Label(self, text='Tela 2', font=LARGE_FONT)
        title.pack(padx=(10,10), pady=(10,10))

        button1 = ttk.Button(self, text="Retornar: Tela Inicial", command=lambda: controller.show_frame(Page_start))
        button1.pack()



app = SistemaReceptor()
ani = animation.FuncAnimation(f,animate, interval=1000) #Intervalo de atualização do gráfico
app.mainloop()