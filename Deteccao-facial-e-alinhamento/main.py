import os
import cv2 as cv
import dlib
import pandas as pd

caminho_entrada = "input"
caminho_cascata = "haarcascade_frontalface_default.xml"
caminho_saida = "output"
lst = []

for diretorio, _, arquivos in os.walk(caminho_entrada): #Identifica todos os arquivos no diretorio:
    for arquivo in arquivos:
        caminho_imagem = (os.path.join(diretorio, arquivo))
        print(caminho_imagem)
        
        ia_detec_facial = cv.CascadeClassifier(caminho_cascata) #Ler IA para reconhecimento facial
        imagem = cv.imread(caminho_imagem) #Ler arquivo de imagem:
        imagem_cinza = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY) #Converter imagem em tons de cinza:
        
        try: #Detectar faces:
            faces = ia_detec_facial.detectMultiScale (imagem_cinza, scaleFactor=1.1, minNeighbors=5, minSize=(500,500))

            #Configurar nome:
            contador = 0
            name = caminho_imagem.split("\\")
            name = name[-1].split(".")[-2]
            ext = caminho_imagem.split(".")[-1]
            
            for (x, y, w, h) in faces: #Recortar imagens detectadas
                contador = contador+1
                imagem_recortada = imagem[y:y+h, x:x+w]

                #Escrever imagem para diretório
                caminho_imagem_recortada_saida = os.path.join(caminho_saida, f"{name}_{contador}_Recortada.{ext}")
                cv.imwrite(caminho_imagem_recortada_saida, imagem_recortada)

                previsor_caminho = "shape_predictor_5_face_landmarks.dat" #Importar previsor de formato:
                previsor_formato = dlib.shape_predictor(previsor_caminho)
                
                detector_facial = dlib.get_frontal_face_detector() #Importar detector facial
                img = dlib.load_rgb_image(caminho_imagem_recortada_saida)

                dets = detector_facial(img, 1) #Detectar rostos:

                faces = dlib.full_object_detections()  #Prever formato facial:
                for detection in dets:
                    faces.append(previsor_formato(img, detection))

                caminho_imagem_alinhada_saida = os.path.join(caminho_saida, f"{name}.{ext}") #Exportar imagem alinhada
                images = dlib.get_face_chips(img, faces, size=1000)
                for image in images:
                    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                    cv.imwrite(caminho_imagem_alinhada_saida, image_rgb)

                os.remove(caminho_imagem_recortada_saida) #Remover imagem recortada
        except:
            print(f"Exceção: {name}")
            lst.append(arquivo)

df = pd.DataFrame(lst, columns=["Excecoes"]) #Anotar exceções
df.to_csv(path_or_buf="excecoes.csv")