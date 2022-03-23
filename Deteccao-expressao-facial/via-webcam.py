import cv2 as cv
import dlib
from rmn import RMN

############# Iniciadores/ Modelos #############
opencv_path = "haarcascade_frontalface_default.xml"
opencv_modelo = cv.CascadeClassifier(opencv_path)

dlib_path = "shape_predictor_5_face_landmarks.dat"
dlib_previsor_formato = dlib.shape_predictor(dlib_path) #Importa o previsor de formato dlib
dlib_detector_facial = dlib.get_frontal_face_detector()

rmn = RMN()

fex_dict = {}

############# Logic #############
username = str(input("Username: ")).capitalize()

webcam = cv.VideoCapture(0)

while True:
    ret, imagem_colorida = webcam.read()

    if ret == True:
        if cv.waitKey(1) & 0xFF == ord("q"):
            webcam.release()
            cv.destroyAllWindows()
            break

        imagem_cinza = cv.cvtColor(imagem_colorida, cv.COLOR_BGR2GRAY)

        faces = opencv_modelo.detectMultiScale (imagem_cinza, scaleFactor=1.1, minNeighbors=4)
        
        for (x, y, w, h) in faces: #Recortar imagens detectadas
                imagem_recortada = imagem_colorida[y:y+h, x:x+w]
                img = cv.cvtColor(imagem_recortada, cv.COLOR_BGR2RGB)
                try:
                    dets = dlib_detector_facial(img, 1) #Detectar rostos:
                    faces = dlib.full_object_detections()  #Prever formato facial:

                    for detection in dets:
                        faces.append(dlib_previsor_formato(img, detection))
                        images = dlib.get_face_chips(img, faces, size=500)

                        for image in images:
                            preprocessed_image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

                            cv.imshow("img", preprocessed_image)

                            result = rmn.detect_emotion_for_single_face_image(preprocessed_image)
                            fex = result[0]
                            fex_dict[username] = fex  

                            print(fex_dict)
                except:
                    print("Nenhuma face detectada")