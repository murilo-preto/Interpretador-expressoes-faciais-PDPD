import os
import cv2 as cv
import dlib

#Variáveis
caminho_entrada = "input"
caminho_cascata = "haarcascade_frontalface_default.xml"
caminho_saida = "output"

#Identifica todos os arquivos no diretorio:
for diretorio, _, arquivos in os.walk(caminho_entrada):
    for arquivo in arquivos:
        caminho_imagem = (os.path.join(diretorio, arquivo))
        print(caminho_imagem)

        #Ler IA para reconhecimento facial
        ia_detec_facial = cv.CascadeClassifier(caminho_cascata)

        #Ler arquivo de imagem:
        imagem = cv.imread(caminho_imagem)

        #Converter imagem em tons de cinza:
        imagem_cinza = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)

        #Detectar faces:
        faces = ia_detec_facial.detectMultiScale (imagem_cinza, scaleFactor=1.1, minNeighbors=5, minSize=(500,500))

        #Configurar nome:
        contador = 0
        name = caminho_imagem.split("\\")
        name = name[-1].split(".")[-2]
        ext = caminho_imagem.split(".")[-1]

        #Recortar imagens detectadas
        for (x, y, w, h) in faces:
            contador = contador+1
            imagem_recortada = imagem[y:y+h, x:x+w]

            #Escrever imagem para diretório
            caminho_imagem_recortada_saida = os.path.join(caminho_saida, f"{name}_{contador}_Recortada.{ext}")
            cv.imwrite(caminho_imagem_recortada_saida, imagem_recortada)

            #Importar previsor de formato:
            previsor_caminho = "shape_predictor_5_face_landmarks.dat"
            previsor_formato = dlib.shape_predictor(previsor_caminho)

            #Importar detector facial
            detector_facial = dlib.get_frontal_face_detector()
            img = dlib.load_rgb_image(caminho_imagem_recortada_saida)

            #Detectar rostos:
            dets = detector_facial(img, 1)

            #Prever formato facial:
            faces = dlib.full_object_detections()
            for detection in dets:
                faces.append(previsor_formato(img, detection))

            #Exportar imagem alinhada
            caminho_imagem_alinhada_saida = os.path.join(caminho_saida, f"{name}_{contador}_Alinhada.{ext}")
            images = dlib.get_face_chips(img, faces, size=1000)
            for image in images:
                image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                cv.imwrite(caminho_imagem_alinhada_saida, image_rgb)

            #Remover imagem recortada
            os.remove(caminho_imagem_recortada_saida)