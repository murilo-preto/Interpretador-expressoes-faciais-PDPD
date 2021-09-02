

import cv2 as cv
import os

#Definindo função para o recorte de imagens:
def Recortar_faces(caminho_imagem, caminho_cascata, caminho_output):
    """
    Recorta rostos de imagens por meio de uma ai em cascata:

    Variáveis:
    caminho_imagem = r"diretório + nome da imagem"
    caminho_cascata = r"diretório + nome do arquivo"
    caminho_output = r"diretório de saída"
    """
   
    #Ler IA para reconhecimento facial
    ia_detec_facial = cv.CascadeClassifier(caminho_cascata)

    #Ler arquivo de imagem:
    imagem = cv.imread(caminho_imagem)

    #Converter imagem em tons de cinza:
    imagem_cinza = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)

    #Detectar faces:
    faces = ia_detec_facial.detectMultiScale (imagem_cinza, scaleFactor=1.1, minNeighbors=15, minSize=(100,100))
    #Exportar face
    contador = 0
    name = caminho_imagem.split("\\")
    name = name[-1].split(".")[-2]
    ext = caminho_imagem.split(".")[-1]

    for (x, y, w, h) in faces:
        contador = contador+1
        Recortar_imagem = imagem[y:y+h, x:x+w]
        cv.imwrite(os.path.join(caminho_output, f"Recortada_{name}_{contador}.{ext}"), Recortar_imagem)