import os
import cv2 as cv
import dlib
import pandas as pd
import time

#Variaveis
vizinhos_minimos = 4
fator_escala = 1.1
base_de_dados = "input-base-de-dados"
output_recortada = "output-1-faces-recortadas"
output_alinhada = "output-2-faces-alinhadas"
modelo_opencv = "haarcascade_frontalface_default.xml"
modelo_dlib = "shape_predictor_5_face_landmarks.dat"
lst = [] #Lista para log de excecoes

tempo_inicial = time.perf_counter() #Tempo inicial

#OPENCV
opencv_detec_facial = cv.CascadeClassifier(modelo_opencv) #Importa o modelo de detecção opencv
for diretorio, _, arquivos in os.walk(base_de_dados): #Identifica todos os arquivos no diretorio
    for arquivo in arquivos:
        caminho_imagem = (os.path.join(diretorio, arquivo))
        print("Detec facial OpenCV", caminho_imagem)
        
        img = cv.imread(caminho_imagem)
        img_cinza = cv.imread(caminho_imagem,0)
        
        #Detectar faces:
        faces = opencv_detec_facial.detectMultiScale (img_cinza, scaleFactor=fator_escala, minNeighbors=vizinhos_minimos, minSize=(500,500))

        #Configurar nome:
        contador = 0
        name = caminho_imagem.split("\\")
        name = name[-1].split(".")[-2]
        ext = caminho_imagem.split(".")[-1]
        
        for (x, y, w, h) in faces: #Recortar imagens detectadas
            contador = contador+1
            imagem_recortada = img[y:y+h, x:x+w]

            #Escrever imagem para diretório
            caminho_recortada_output = os.path.join(output_recortada, f"{name}_{contador}.{ext}")
            cv.imwrite(filename=caminho_recortada_output, img=imagem_recortada)

#DLIB
previsor_formato = dlib.shape_predictor(modelo_dlib) #Importa o previsor de formato dlib
detector_facial = dlib.get_frontal_face_detector()

for diretorio, _, arquivos in os.walk(output_recortada): #Identifica todos os arquivos no diretorio
    for arquivo in arquivos:
        caminho_imagem = (os.path.join(diretorio, arquivo))
        print("Alinhamento facial DLIB", caminho_imagem)

        #Configurar nome:
        name = caminho_imagem.split("\\")
        name = name[-1].split(".")[-2]
        ext = caminho_imagem.split(".")[-1]

        try:
            #Importar detector facial
            img = dlib.load_rgb_image(caminho_imagem)
            dets = detector_facial(img, 1) #Detectar rostos:

            faces = dlib.full_object_detections()  #Prever formato facial:
            for detection in dets:
                faces.append(previsor_formato(img, detection))

            caminho_imagem_alinhada_saida = os.path.join(output_alinhada, arquivo) #Exportar imagem alinhada
            images = dlib.get_face_chips(img, faces, size=1000)

            for image in images:
                img_cinza = cv.cvtColor(image, cv.COLOR_BGR2GRAY) #Converter imagem em tons de cinza
                eq = cv.equalizeHist(img_cinza)
                cv.imwrite(caminho_imagem_alinhada_saida, eq)

        except:
            print(f"Exceção: {name}")
            lst.append(arquivo)

tempo_final = time.perf_counter() #Tempo final
variacao_tempo = tempo_final-tempo_inicial #Calcular tempo de execução

with open('time-log.txt', 'w') as f: #Exportar tempo em arquivo de txt
    f.write(str(variacao_tempo))

df = pd.DataFrame(lst, columns=["Excecoes"]) #Exportar exceções em tabela
df.to_csv(path_or_buf="excecoes.csv")