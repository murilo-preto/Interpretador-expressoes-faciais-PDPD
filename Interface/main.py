import tkinter as tk
from time import sleep

window = tk.Tk()
window.geometry("600x300")

l_title = tk.Label(text="Sistema Interpretador",font=("Times 20",16))
l_title.pack()

def Hello():
    print("Hello")

b_hello = tk.Button(text="Hello", command=Hello, font=("Arial",14))
b_hello.pack()

window.mainloop()