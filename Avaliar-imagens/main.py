import pandas as pd
import os
import cv2 as cv
import keyboard

diretorio = "00000"

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
                if keyboard.is_pressed('k'):
                    print('Mantendo imagem')
                    df.loc[df.shape[0]] = [arquivo, 'Mantida']
                    break
                elif keyboard.is_pressed('r'):
                    print('Removendo imagem')
                    df.loc[df.shape[0]] = [arquivo, 'Removida']
                    os.remove(imagem)
                    break
            except:
                break

df.to_csv(path_or_buf="dataframe.csv")