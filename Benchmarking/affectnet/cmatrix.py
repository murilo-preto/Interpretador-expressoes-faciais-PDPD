from sklearn.metrics import confusion_matrix
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np

df = pd.read_csv("fex.csv")

fex_esperada = df["FEX-esperada"]
fex_detectada = df["FEX-detectada"]

cf_matrix = confusion_matrix(fex_esperada, fex_detectada, labels=["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"])

print(cf_matrix)

fig, ax = plt.subplots(figsize=(7,7))

color = sns.cubehelix_palette(start=2.7, rot=0, dark=.02, light=.98, reverse=False, as_cmap=True)
ax = sns.heatmap(cf_matrix, annot=True, cmap=color, fmt='d', cbar=False)

ax.set_title('Método: OpenCV + DLIB + RMN\nDataset: Affect NET\n');
ax.set_xlabel('\nExpressões detectadas')
ax.set_ylabel('Expressões reais\n');

ptbr_fex = ["Raiva", "Desgosto", "Medo", "Felicidade", "Tristeza", "Surpresa", "Neutro"]

ax.xaxis.set_ticklabels(ptbr_fex)
ax.yaxis.set_ticklabels(ptbr_fex)

plt.savefig('cmatrix-affectnet.png')