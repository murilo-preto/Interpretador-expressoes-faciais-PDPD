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
ax = sns.heatmap(cf_matrix, annot=True, cmap='Blues', fmt='d', vmin=0, vmax=80, cbar=False)

ax.set_title('Método: OpenCV + DLIB + RMN\nDataset: CK+\n');
ax.set_xlabel('\nExpressões detectadas')
ax.set_ylabel('Expressões reais\n');

ax.xaxis.set_ticklabels(["Raiva", "Desgosto", "Medo", "Felicidade", "Tristeza", "Surpresa", "Neutro"])
ax.yaxis.set_ticklabels(["Raiva", "Desgosto", "Medo", "Felicidade", "Tristeza", "Surpresa", "Neutro"])

#plt.show()

plt.savefig('cmatrix.png')