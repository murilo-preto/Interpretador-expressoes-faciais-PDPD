import cv2 as cv
import dlib
from time import perf_counter
import os

#Caminhos
input = "input"
output = "output"
modelo_opencv = "haarcascade_frontalface_default.xml"
modelo_dlib = "shape_predictor_5_face_landmarks.dat"

#Modelos de deteccao
opencv_detec_facial = cv.CascadeClassifier(modelo_opencv) #Importa o modelo de detecção opencv
previsor_formato = dlib.shape_predictor(modelo_dlib) #Importa o previsor de formato dlib
detector_facial = dlib.get_frontal_face_detector()

for diretorio, _, arquivos in os.walk(input): #Identifica todos os arquivos no diretorio
    for arquivo in arquivos:
        caminho_imagem = (os.path.join(diretorio, arquivo))

        imagem_colorida = cv.imread(caminho_imagem)
        imagem_cinza = cv.cvtColor(imagem_colorida, cv.COLOR_BGR2GRAY)
        
        #Detectar faces:
        faces = opencv_detec_facial.detectMultiScale (imagem_cinza, scaleFactor=1.1, minNeighbors=4, minSize=(500,500))

        #Configurar nome:
        contador = 0
        name = caminho_imagem.split("\\")
        name = name[-1].split(".")[-2]
        ext = caminho_imagem.split(".")[-1]
        
        for (x, y, w, h) in faces: #Recortar imagens detectadas
            contador = contador+1
            imagem_recortada = imagem_colorida[y:y+h, x:x+w]
            img = cv.cvtColor(imagem_recortada, cv.COLOR_BGR2RGB)

            caminho_output = os.path.join(output, f"{name}_{contador}.{ext}")

            try:
                dets = detector_facial(img, 1) #Detectar rostos:
                faces = dlib.full_object_detections()  #Prever formato facial:

                for detection in dets:
                    faces.append(previsor_formato(img, detection))

                images = dlib.get_face_chips(img, faces, size=1000)

                for image in images:
                    image_cvt = cv.cvtColor(image, cv.COLOR_RGB2BGR)
                    cv.imwrite(caminho_output, image_cvt)
            except:
                print(f"Nenhuma face detectada em {name}")

tempo = perf_counter()
with open('time-log.txt', 'w') as f: #Exportar tempo em arquivo de txt
    f.write(str(tempo))