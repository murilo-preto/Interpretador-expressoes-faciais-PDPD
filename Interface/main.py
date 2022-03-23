import tkinter as tk
import socket
from pickle import dumps
from tkinter.font import NORMAL
from tkinter import ttk
from matplotlib.pyplot import fill
import cv2 as cv
import dlib
from rmn import RMN


#### SOCKET CONFIG ####
header_len = 10
ip = "127.0.0.1"
port = 1500

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#### SOCKET CONFIG ####


#### DEF ####
def conect_server(): #Conectar ao servidor
    try:
        client_socket. connect((ip, port))

        l_conect_status['text'] = "Status: Conectado"
        l_conect_status['foreground'] = 'green'
        
    except:
        None


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
    send_type("interpretador")
    
    ## Caminhos ##
    opencv_path = "haarcascade_frontalface_default.xml"
    opencv_modelo = cv.CascadeClassifier(opencv_path)

    dlib_path = "shape_predictor_5_face_landmarks.dat"
    dlib_previsor_formato = dlib.shape_predictor(dlib_path) #Importa o previsor de formato dlib
    dlib_detector_facial = dlib.get_frontal_face_detector()

    rmn = RMN()
    #---------------------#

    user = str(e_user.get())
    fex_dict = {}
    s_end_detection = True

    webcam = cv.VideoCapture(0)

    while True:
        ret, imagem_colorida = webcam.read()

        if ret == True:
            if s_end_detection == False:
                webcam.release()
                cv.destroyAllWindows()
                break

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

                                cv.imshow("img", preprocessed_image)

                                result = rmn.detect_emotion_for_single_face_image(preprocessed_image)
                                fex = result[0]
                                fex_dict[user] = fex  

                                l_fex['text'] = fex_dict
                                send_dict(header_len, fex_dict)
                    except:
                        None        


def retrieve_user():
    user = str(e_user.get())
    
    if user == "":
        b_conectar_servidor['state'] = tk.DISABLED
    else:
        b_conectar_servidor['state'] = tk.ACTIVE

        e_user['state'] = tk.DISABLED
        b_registrar_user['state'] = tk.DISABLED


def return_false(var):
    var = False
    return var


#### DEF ####


#### INTERFACE ####
root = tk.Tk()
root.geometry("300x300")
root.resizable(False, False)
root.title('Sistema interpretador')


## Frame ##
frame_interp = ttk.Frame(root)
frame_interp.pack(padx=10, fill='x', expand=True)
#---------------------#


## Title ##
l_title = tk.Label(frame_interp, text="Sistema Interpretador",font=("Times 20"))
l_title.pack(fill='x', expand=True, pady=(0,25))
#---------------------#


## Username entry ##
l_user_entry = tk.Label(frame_interp, text="Insira seu nome de usuário:")
l_user_entry.pack(fill='x', expand=True)

e_user = tk.Entry(frame_interp)
e_user.pack(fill='x', expand=True)

b_registrar_user = tk.Button(frame_interp, text="Registrar nome", command=retrieve_user)
b_registrar_user.pack(fill='x', expand=True, pady=(0,25))
#---------------------#


## Conectar / Status ##
b_conectar_servidor = tk.Button(frame_interp, text="Conectar ao servidor", command=conect_server, state=tk.DISABLED)
b_conectar_servidor.pack(fill='x', expand=True)

l_conect_status = tk.Label(frame_interp, text="Status: Não conectado", foreground='red')
l_conect_status.pack(fill='x', expand=True, pady=(0,25))
#---------------------#


## Iniciar envio de dados / Status ##
b_init_envio_dados = tk.Button(frame_interp, text="Iniciar envio de dados", command=init_enviar_dados, state=tk.DISABLED)
b_init_envio_dados.pack(fill='x', expand=True)

l_fex = tk.Label(frame_interp, text="Aguardando detecção")
l_fex.pack(fill='x', expand=True)
#---------------------#


## Parar detecção ##
s_end_detection = True
b_stop_detec = tk.Button(frame_interp, text="Parar detecção", command=return_false(s_end_detection), state=tk.DISABLED)
b_stop_detec.pack(fill='x', expand=True)
#---------------------#


root.mainloop()
#### INTERFACE ####