import cv2 as cv
import dlib
import os
from rmn import RMN
import pandas as pd
from time import perf_counter

img_folder = "ExpW\data\image\origin"
labels = "ExpW\data\label\label.lst"
modelo_opencv = "haarcascade_frontalface_default.xml"
modelo_dlib = "shape_predictor_5_face_landmarks.dat"

opencv_detec_facial = cv.CascadeClassifier(modelo_opencv)
previsor_formato = dlib.shape_predictor(modelo_dlib)
detector_facial = dlib.get_frontal_face_detector()
rmn = RMN()

benchmark_df = pd.DataFrame(columns = ["Imagem", "FEX-esperada", "FEX-detectada" ])
usable_img_list = []

num2fer = {
    0: "angry",
    1: "disgust",
    2: "fear",
    3: "happy",
    4: "sad",
    5: "surprise",
    6: "neutral"
}

def detect_fex(filepath):
    try:
        imagem_colorida = cv.imread(filepath)
        imagem_cinza = cv.cvtColor(imagem_colorida, cv.COLOR_BGR2GRAY)

        faces = opencv_detec_facial.detectMultiScale (imagem_cinza, scaleFactor=1.1, minNeighbors=4, minSize=(50,50))

        for (x, y, w, h) in faces: #Recortar imagens detectadas
            imagem_recortada = imagem_colorida[y:y+h, x:x+w]
            img = cv.cvtColor(imagem_recortada, cv.COLOR_BGR2RGB)

            dets = detector_facial(img, 1) #Detectar rostos:
            faces = dlib.full_object_detections()  #Prever formato facial:

            for detection in dets:
                faces.append(previsor_formato(img, detection))

            images = dlib.get_face_chips(img, faces, size=1000)
            for image in images:
                result = rmn.detect_emotion_for_single_face_image(img)
                fex = result[0]
                return fex              
    except:
        return None

tempo_inicial = perf_counter()
with open(labels) as f:
            labeled_list = f.readlines()
            strip_list = [item.strip("\n") for item in labeled_list]
            for label in strip_list:
                label_confidence = float(label.split(sep=" ")[-2])
                if label_confidence >= 100:
                    name = label.split()[0]
                    fex_esperada = num2fer[int(label.split()[-1])]
                    img_path = os.path.join(img_folder, name)
                    fex_detectada = detect_fex(img_path)

                    if fex_detectada != None:
                        benchmark_df.loc[benchmark_df.shape[0]] = [name, fex_esperada, fex_detectada]
                        print(name, fex_esperada, fex_detectada)

tempo_final = perf_counter()
tempo = tempo_final-tempo_inicial
with open('time-log.txt', 'w') as f: #Exportar tempo em arquivo de txt
    f.write(str(tempo))

benchmark_df.to_csv(path_or_buf="fex.csv")