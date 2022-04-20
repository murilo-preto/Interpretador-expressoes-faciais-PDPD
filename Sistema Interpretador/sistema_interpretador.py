import tkinter as tk
import socket
from pickle import dumps
from tkinter import ttk
from matplotlib.pyplot import fill
import cv2 as cv
import dlib
from rmn import RMN
import threading


#### CAMINHOS ####
opencv_path = "haarcascade_frontalface_default.xml"
opencv_modelo = cv.CascadeClassifier(opencv_path)

dlib_path = "shape_predictor_5_face_landmarks.dat"
dlib_previsor_formato = dlib.shape_predictor(dlib_path) #Importa o previsor de formato dlib
dlib_detector_facial = dlib.get_frontal_face_detector()

rmn = RMN()


#### SOCKET CONFIG ####
header_len = 10
ip = "127.0.0.1"
port = 1500

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#### DEF ####
def conect_server(): #Conectar ao servidor
    try:
        client_socket. connect((ip, port))
        send_type("interpretador")

        l_conect_status['text'] = "Status: Conectado"
        l_conect_status['foreground'] = 'green'
        b_init_envio_dados['state'] = tk.ACTIVE
        
    except:
        print("Não foi possível conectar ao servidor.")


def send_dict(header_len, dict): #Converter dict e enviar
    data = dumps(dict)

    header = bytes(f"{len(data):<{header_len}}", "utf-8")
    msg = header+data

    client_socket.send(msg)


def send_type(type): #Enviar tipo de api
    data = bytes(type, "utf-8")

    header = bytes(f"{len(data):<{header_len}}", "utf-8")
    msg = header+data

    client_socket.send(msg)


def init_enviar_dados(): #Detectar fex e enviar
    l_fex['background'] = 'black'
    l_fex['foreground'] = 'yellow'
    l_fex['text'] = 'Preparando detecção, aguarde'
    b_parar_fex['state'] = tk.ACTIVE

    user = str(e_user.get())
    fex_dict = {}

    webcam = cv.VideoCapture(0)
    
    while True:
        global stop_fex
        if stop_fex:
            break

        emotion_dict = fex_detection(user, fex_dict, webcam)
        if emotion_dict != None:
            send_dict(header_len, emotion_dict)


def fex_detection(user, fex_dict, webcam):
    ret, imagem_colorida = webcam.read()

    imagem_cinza = cv.cvtColor(imagem_colorida, cv.COLOR_BGR2GRAY)

    faces = opencv_modelo.detectMultiScale (imagem_cinza, scaleFactor=1.1, minNeighbors=4)
    
    for (x, y, w, h) in faces: #Recortar imagens detectadas
            imagem_recortada = imagem_colorida[y:y+h, x:x+w]
            img = cv.cvtColor(imagem_recortada, cv.COLOR_BGR2RGB)
            try:
                dets = dlib_detector_facial(img, 1) #Detectar rostos:
                faces = dlib.full_object_detections()  #Prever formato facial:

                for detection in dets:
                    faces.append(dlib_previsor_formato(img, detection))
                    images = dlib.get_face_chips(img, faces, size=500)

                    for image in images:
                        preprocessed_image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

                        result = rmn.detect_emotion_for_single_face_image(preprocessed_image)
                        fex = result[0]
                        fex_dict[user] = fex  

                        l_fex['background'] = 'white'
                        l_fex['foreground'] = 'green'
                        l_fex['text'] = (user,":",fex)

                        return fex_dict
            except:
                None    


def start_tfex():
    t_fex.start()

def end_tfex():
    global stop_fex
    stop_fex = True


def retrieve_user():
    user = str(e_user.get())
    
    if user == "":
        b_conectar_servidor['state'] = tk.DISABLED
    else:
        b_conectar_servidor['state'] = tk.ACTIVE

        e_user['state'] = tk.DISABLED
        b_registrar_user['state'] = tk.DISABLED


def closing_protocol():
    end_tfex()
    root.destroy()


#### INTERFACE ####
## Root ##
root = tk.Tk()
root.geometry("400x400")
root.resizable(False, False)
root.title('Sistema interpretador')


## Frame ##
frame_interp = ttk.Frame(root)
frame_interp.pack(padx=10, fill='x', expand=True)


## Title ##
l_title = tk.Label(frame_interp, text="Sistema Interpretador",font=("Times 20"))
l_title.pack(fill='x', expand=True, pady=(0,25))


## Username entry ##
l_user_entry = tk.Label(frame_interp, text="Insira seu nome de usuário:")
l_user_entry.pack(fill='x', expand=True)

e_user = ttk.Entry(frame_interp)
e_user.pack(fill='x', expand=True)

b_registrar_user = ttk.Button(frame_interp, text="Registrar nome", command=retrieve_user)
b_registrar_user.pack(fill='x', expand=True, pady=(0,25))


## Conectar / Status ##
b_conectar_servidor = ttk.Button(frame_interp, text="Conectar ao servidor", command=conect_server, state=tk.DISABLED)
b_conectar_servidor.pack(fill='x', expand=True)

l_conect_status = tk.Label(frame_interp, text="Status: Não conectado", foreground='red')
l_conect_status.pack(fill='x', expand=True, pady=(0,25))


## Iniciar fex / Parar fex / Status ##
b_init_envio_dados = ttk.Button(frame_interp, text="Iniciar detecção de expressão facial", command=start_tfex, state=tk.DISABLED)
b_init_envio_dados.pack(fill='x', expand=True)

stop_fex = False
b_parar_fex = ttk.Button(frame_interp, text="Parar detecção de expressão facial", command=end_tfex, state=tk.DISABLED)
b_parar_fex.pack(fill='x', expand=True)

l_fex = tk.Label(frame_interp, text="Aguardando início de detecção")
l_fex.pack(fill='x', expand=True)

## Loop settings // Threading ##
t_fex = threading.Thread(target=init_enviar_dados, args=())

root.protocol("WM_DELETE_WINDOW", closing_protocol)

root.mainloop()