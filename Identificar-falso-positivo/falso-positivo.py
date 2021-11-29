import pandas as pd
import os
import cv2 as cv
import keyboard

diretorio = "inserir_caminho_diretorio"

df = pd.DataFrame(columns = ["Imagem", "Situação"])

for diretorio, _, arquivos in os.walk(diretorio):
    for arquivo in arquivos:
        imagem = (os.path.join(diretorio, arquivo))

        img = cv.imread(imagem)        
        imS = cv.resize(img, (960, 540))

        cv.imshow(imagem, imS)
        cv.waitKey(0)
        cv.destroyAllWindows()

        while True:
            try:
                if keyboard.is_pressed('c'):
                    print(f'Imagem correta: {arquivo}')
                    break
                elif keyboard.is_pressed('f'):
                    print(f'Falso positivo: {arquivo}')
                    df.loc[df.shape[0]] = [arquivo, 'Falso positivo']
                    break
            except:
                break

df.to_csv(path_or_buf=f"falso_positivos.csv")