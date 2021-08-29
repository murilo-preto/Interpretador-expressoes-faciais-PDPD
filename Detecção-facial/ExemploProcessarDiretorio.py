
import DetectorCascata
import os

#Inserir variáveis:
caminho_diretorio = r"exemplo"
caminho_cascata = r"exemplo"
caminho_output = r"exemplo"

#Identifica todos os arquivos no diretorio:
for diretorio, _, arquivos in os.walk(caminho_diretorio):
    for arquivo in arquivos:
        imagem = (os.path.join(diretorio, arquivo))

        DetectorCascata.Recortar_faces(imagem, caminho_cascata, caminho_output)



