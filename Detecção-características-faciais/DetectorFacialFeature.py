"""
Detecção de facial features via DLIB
Modificado pela última vez em 07/09/2021, por Murilo Preto

"""

import cv2 as cv
import dlib

#Importar previsor de formato:
previsor_caminho = "shape_predictor_5_face_landmarks.dat"
previsor_formato = dlib.shape_predictor(previsor_caminho)

#Importar detector facial
detector_facial = dlib.get_frontal_face_detector()

#Carregar imagem:
imagem_caminho = "Dataset\Recortada_00072_1.png"
img = dlib.load_rgb_image(imagem_caminho)

#Detectar rostos:
dets = detector_facial(img, 1)

#Prever formato facial:
faces = dlib.full_object_detections()
for detection in dets:
    faces.append(previsor_formato(img, detection))

#Exibir imagem
nome_imagem = (imagem_caminho.split("\\")[-1]).split(".")[-2]
formato_imagem = imagem_caminho.split(".")[-1]
filename = f"{nome_imagem}_alinhada.{formato_imagem}"

window = dlib.image_window()
images = dlib.get_face_chips(img, faces, size=500)
for image in images:
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    cv.imwrite(filename, image_rgb)
