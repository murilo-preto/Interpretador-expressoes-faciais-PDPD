import numpy as np
import cv2 as cv
import dlib
from rmn import RMN

modelo_opencv = 'haarcascade_frontalface_default.xml'
modelo_dlib = 'shape_predictor_5_face_landmarks.dat'

opencv_detec_facial = cv.CascadeClassifier(modelo_opencv)
previsor_formato = dlib.shape_predictor(modelo_dlib)
detector_facial = dlib.get_frontal_face_detector()
rmn = RMN()

def fex_modelo_rmn(filepath, pre_process=True):
    try:
        if pre_process == True:
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
        if pre_process == False:
            imagem_colorida = cv.imread(filepath)
            result = rmn.detect_emotion_for_single_face_image(imagem_colorida)
            fex = result[0]
            return fex              
    except Exception as e:
        print(e)
        return None