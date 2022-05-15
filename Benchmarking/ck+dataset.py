"""
Nota: Código de emoções do CK+ dataset:
    0=neutral
    1=anger
    2=contempt
    3=disgust
    4=fear
    5=happy
    6=sadness
    7=surpise
"""

import cv2 as cv
import dlib
import os
from rmn import RMN
import pandas as pd

emotion_label_folder = "CK+\Emotion_labels\Emotion"
faces_folder = "CK+\extended-cohn-kanade-images\cohn-kanade-images"
modelo_opencv = "haarcascade_frontalface_default.xml"
modelo_dlib = "shape_predictor_5_face_landmarks.dat"

opencv_detec_facial = cv.CascadeClassifier(modelo_opencv) #Importa o modelo de detecção opencv
previsor_formato = dlib.shape_predictor(modelo_dlib) #Importa o previsor de formato dlib
detector_facial = dlib.get_frontal_face_detector()
rmn = RMN()

df = pd.DataFrame(columns = ["Imagem", "FEX-esperada", "FEX-detectada" ])

num2emotion = {
    "0": "neutral",
    "1": "angry",
    "2": "contempt",
    "3": "disgust",
    "4": "fear",
    "5": "happy",
    "6": "sad",
    "7": "surprise"
}

for dir_emotion, _, arquivos in os.walk(emotion_label_folder):
    if arquivos != []:
        emotion_txt = os.path.join(dir_emotion,arquivos[0])
        with open(emotion_txt) as f:
            lines = f.readlines()
            emotion_num = lines[0].strip()[0]
            emotion = num2emotion[emotion_num]
    
            if emotion_num != "2":
                header_emotion = dir_emotion.strip(emotion_label_folder)
                if "\\" in header_emotion:
                    for dir_face, _, arquivos in os.walk(faces_folder):
                        header_face = dir_face.strip(faces_folder)
                        if header_emotion == header_face:
                            face_path = os.path.join(faces_folder,header_face)
                            list = os.listdir(face_path)
                            if 'Thumbs.db' in list:
                                list.remove('Thumbs.db')

                            img_emotion = list[-1]
                            img_folder_1 = img_emotion.strip()[0:4]
                            img_folder_2 = img_emotion.strip()[5:8]

                            caminho_imagem = (os.path.join(faces_folder, img_folder_1, img_folder_2, img_emotion))

                            imagem_colorida = cv.imread(caminho_imagem)
                            imagem_cinza = imagem_colorida
                            #imagem_cinza = cv.cvtColor(imagem_colorida, cv.COLOR_BGR2GRAY)

                            #Detectar faces:
                            faces = opencv_detec_facial.detectMultiScale (imagem_cinza, scaleFactor=1.1, minNeighbors=4, minSize=(50,50))

                            #Configurar nome:
                            contador = 0
                            name = img_emotion
                            ext = caminho_imagem.split(".")[-1]
                            
                            for (x, y, w, h) in faces: #Recortar imagens detectadas
                                contador = contador+1
                                name = f"{name}_{contador}"
                                imagem_recortada = imagem_colorida[y:y+h, x:x+w]
                                img = cv.cvtColor(imagem_recortada, cv.COLOR_BGR2RGB)

                                try:
                                    dets = detector_facial(img, 1) #Detectar rostos:
                                    faces = dlib.full_object_detections()  #Prever formato facial:

                                    for detection in dets:
                                        faces.append(previsor_formato(img, detection))
                                    images = dlib.get_face_chips(img, faces, size=1000)

                                    for image in images:
                                        result = rmn.detect_emotion_for_single_face_image(img)
                                        fex = result[0]
                                        df.loc[df.shape[0]] = [name, emotion, fex]  

                                        print(name, emotion, fex)
                                except:
                                    None

df.to_csv(path_or_buf="fex.csv")