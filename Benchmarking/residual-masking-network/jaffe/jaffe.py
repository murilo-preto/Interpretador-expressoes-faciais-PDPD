import cv2 as cv
import dlib
import os
from rmn import RMN
import pandas as pd
from time import perf_counter


all_image_folder = "images"
modelo_opencv = "haarcascade_frontalface_default.xml"
modelo_dlib = "shape_predictor_5_face_landmarks.dat"

opencv_detec_facial = cv.CascadeClassifier(modelo_opencv)
previsor_formato = dlib.shape_predictor(modelo_dlib)
detector_facial = dlib.get_frontal_face_detector()
rmn = RMN()


benchmark_df = pd.DataFrame(columns = ["Imagem", "FEX-esperada", "FEX-detectada" ])


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


fex_normalize_dict = {
    "happines":"happy",
    "neutrality":"neutral"
    }

folder_list = os.listdir(all_image_folder)
folder_list.remove("jaffedbase.curious")
print(folder_list)

tempo_inicial = perf_counter()
for folder in folder_list:
    fex_esperada = folder.split(".")[1]

    if fex_esperada in fex_normalize_dict.keys():
        fex_esperada = fex_normalize_dict[fex_esperada]

    dir_path = os.path.join(all_image_folder, folder)

    for diretorio, _, arquivos in os.walk(dir_path): #Identifica todos os arquivos no diretorio
        for arquivo in arquivos:
            filepath = os.path.join(dir_path, arquivo)

            fex_detectada = detect_fex(filepath)

            if fex_detectada in ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]:
                name = arquivo.replace(".", "_")

                benchmark_df.loc[benchmark_df.shape[0]] = [name, fex_esperada, fex_detectada]
                print(name, fex_esperada, fex_detectada)

tempo_final = perf_counter()
tempo = tempo_final-tempo_inicial
with open('time-log.txt', 'w') as f: #Exportar tempo em arquivo de txt
    f.write(str(tempo))

benchmark_df.to_csv(path_or_buf="fex.csv")