import os
import cv2 as cv
import dlib
import pandas as pd
import time

vizinhos_minimos = int(input())
base_de_dados = "input-base-de-dados"
output_recortada = "output-1-faces-recortadas"
output_alinhada = "output-2-faces-alinhadas"
modelo_opencv = "haarcascade_frontalface_default.xml"
modelo_dlib = "shape_predictor_5_face_landmarks.dat"
lst = []

#OPENCV
for diretorio, _, arquivos in os.walk(base_de_dados): #Identifica todos os arquivos no diretorio
    for arquivo in arquivos:
        caminho_imagem = (os.path.join(diretorio, arquivo))
        print(caminho_imagem)
        
        ia_detec_facial = cv.CascadeClassifier(modelo_opencv) #Ler modelo de detec opencv
        imagem = cv.imread(caminho_imagem) #Ler arquivo de imagem
        imagem_cinza = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY) #Converter imagem em tons de cinza
        
        #Detectar faces:
        faces = ia_detec_facial.detectMultiScale (imagem_cinza, scaleFactor=1.1, minNeighbors=vizinhos_minimos, minSize=(500,500))

        #Configurar nome:
        contador = 0
        name = caminho_imagem.split("\\")
        name = name[-1].split(".")[-2]
        ext = caminho_imagem.split(".")[-1]
        
        for (x, y, w, h) in faces: #Recortar imagens detectadas
            contador = contador+1
            imagem_recortada = imagem[y:y+h, x:x+w]

            #Escrever imagem para diretório
            caminho_recortada_output = os.path.join(output_recortada, f"{name}_{contador}.{ext}")
            cv.imwrite(filename=caminho_recortada_output, img=imagem_recortada)

#DLIB
for diretorio, _, arquivos in os.walk(output_recortada): #Identifica todos os arquivos no diretorio
    for arquivo in arquivos:
        caminho_imagem = (os.path.join(diretorio, arquivo))
        print(caminho_imagem)

        #Configurar nome:
        name = caminho_imagem.split("\\")
        name = name[-1].split(".")[-2]
        ext = caminho_imagem.split(".")[-1]

        try:
            previsor_formato = dlib.shape_predictor(modelo_dlib)
                
            detector_facial = dlib.get_frontal_face_detector() #Importar detector facial
            img = dlib.load_rgb_image(caminho_imagem)

            dets = detector_facial(img, 1) #Detectar rostos:

            faces = dlib.full_object_detections()  #Prever formato facial:
            for detection in dets:
                faces.append(previsor_formato(img, detection))

            caminho_imagem_alinhada_saida = os.path.join(output_alinhada, f"{name}.{ext}") #Exportar imagem alinhada
            images = dlib.get_face_chips(img, faces, size=1000)
            for image in images:
                image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                cv.imwrite(caminho_imagem_alinhada_saida, image_rgb)

        except:
            print(f"Exceção: {name}")
            lst.append(arquivo)

df = pd.DataFrame(lst, columns=["Excecoes"]) #Anotar exceções
df.to_csv(path_or_buf="excecoes.csv")

time = time.perf_counter()
with open('time-log.txt', 'w') as f:
    f.write(str(time))