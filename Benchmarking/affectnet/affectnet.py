import numpy as np
import os
import cv2 as cv
import dlib
from rmn import RMN
import pandas as pd
from time import perf_counter

label_folder = 'val_set\\annotations'
image_folder = 'val_set\\images'
modelo_opencv = 'haarcascade_frontalface_default.xml'
modelo_dlib = 'shape_predictor_5_face_landmarks.dat'

num2fex = {
    0 : 'neutral',
    1 : 'happy',
    2 : 'sad',
    3 : 'surprise',
    4 : 'fear',
    5 : 'disgust',
    6 : 'angry'
}

benchmark_df = pd.DataFrame(columns = ["Imagem", "FEX-esperada", "FEX-detectada" ])

def detect_fex(filepath):
    try:
        imagem_colorida = cv.imread(filepath)
        imagem_cinza = cv.cvtColor(imagem_colorida, cv.COLOR_BGR2GRAY)

        faces_cv = opencv_detec_facial.detectMultiScale (imagem_cinza, scaleFactor=1.1, minNeighbors=2)

        if isinstance(faces_cv, (np.ndarray, np.generic)):
            for (x, y, w, h) in faces_cv:
                imagem_recortada = imagem_colorida[y:y+h, x:x+w]
                img = cv.cvtColor(imagem_recortada, cv.COLOR_BGR2RGB)

                dets = detector_facial(img, 1)
                faces_dlib = dlib.full_object_detections()

                if str(dets) != "rectangles[]":
                    for detection in dets:
                        faces_dlib.append(previsor_formato(img, detection))

                    images = dlib.get_face_chips(img, faces_dlib)
                    for image in images:
                        result = rmn.detect_emotion_for_single_face_image(image)
                        fex = result[0]
                        return fex              
    except Exception as e:
        print(e)
        return None

opencv_detec_facial = cv.CascadeClassifier(modelo_opencv)
previsor_formato = dlib.shape_predictor(modelo_dlib)
detector_facial = dlib.get_frontal_face_detector()
rmn = RMN()

img_and_fex = []
label_list = os.listdir(label_folder)
for label in label_list:
    prefix = (((label.split(sep="_"))[1]).split(sep="."))[0]
    if prefix == 'exp':
        num_fex = int(np.load(os.path.join(label_folder, label)))
        if num_fex in num2fex.keys():
            fex_esperada = num2fex[num_fex]
            img_and_fex.append([label.split('_')[0], fex_esperada])

img_and_fex.sort(key=lambda x:x[1])

all_images = os.listdir(image_folder)
numbered_item_list = [item.split(".")[0] for item in all_images]

tempo_inicial = perf_counter()
for sublist in img_and_fex:
    file_num = sublist[0]
    fex_esperada = sublist[1]  

    if file_num in numbered_item_list:
        img_path = (os.path.join(image_folder, file_num)+'.jpg')
        fex_detectada = detect_fex(img_path)

        if fex_detectada != None:
            benchmark_df.loc[benchmark_df.shape[0]] = [file_num, fex_esperada, fex_detectada]
            print(file_num, fex_esperada, fex_detectada)
tempo_final = perf_counter()

tempo = tempo_final-tempo_inicial
with open('time-log.txt', 'w') as f:
    f.write(str(tempo))

benchmark_df.to_csv(path_or_buf="fex.csv")