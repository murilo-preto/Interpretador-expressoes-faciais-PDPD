
import DetectorCascata
import os

#Variáveis
path_diretorio = r"caminho_diretorio"
path_cascata = "caminho_cascata"
path_output = "caminho_saida"

#Identifica todos os arquivos no diretorio:
for diretorio, _, arquivos in os.walk(path_diretorio):
    for arquivo in arquivos:
        path_imagem = (os.path.join(diretorio, arquivo))

        DetectorCascata.Recortar_faces(
            caminho_imagem=path_imagem,\
            caminho_cascata=path_cascata,\
            caminho_output=path_output)



