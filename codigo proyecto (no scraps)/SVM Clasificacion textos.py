# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 13:32:37 2018

@author: jonef
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
import pandas as pd
from matplotlib import style
style.use("ggplot")
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from joblib import dump, load

#extraccion de datos
features = ["Silabas","Palabras","Frases","PROPN","VERB","ADJ"]
data_df = pd.DataFrame.from_csv("Clasificacion Textos.csv",index_col=None)

data_df1 = data_df[:169]

X = np.array(data_df1[features].values)
#print(X)
#categorias de la variable respuesta
y = (data_df1["Escala Inflesz"]
     .replace("Facil",0)
     .replace("Normal",1)
     .replace("Dificil",2)
     .values.tolist())


# Split the data into a training set and a test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

clf = svm.SVC(kernel="linear", C= 1.0)
clf.fit(X_train,y_train)
#guardar modelo
dump(clf, 'filename.joblib') 

#matriz de confusion
y_pred = clf.fit(X_train, y_train).predict(X_train)
mat_conf=confusion_matrix(y_train,y_pred)
print(mat_conf)
precision=sum(np.diag(mat_conf))/sum(sum(mat_conf))
print("%.2f" % (precision*100))






#matriz de confusion
y_pred_test = clf.predict(X_test)
mat_conf_test=confusion_matrix(y_test,y_pred_test)
print(mat_conf_test)
precision_test=sum(np.diag(mat_conf_test))/sum(sum(mat_conf_test))
print("%.2f" % (precision_test*100))


#PCA en todos los datos
from sklearn.decomposition import PCA

pca = PCA(n_components=4)

#todos los datos
Componentes = pca.fit_transform(X)

principalDf = pd.DataFrame(data = Componentes
             , columns = ['principal component 1', 'principal component 2','principal component 3','principal component 4'])
finalDf = pd.concat([principalDf, data_df1[['Escala Inflesz']]], axis = 1)
#print(finalDf)
#visualizacion
fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Componente Principal 1', fontsize = 15)
ax.set_ylabel('Componente Principal 4', fontsize = 15)
ax.set_title('Entrenamiento', fontsize = 20)

targets = ['Facil', 'Normal', 'Dificil']
colors = ['r', 'g', 'b']
for target, color in zip(targets,colors):
    indicesToKeep = finalDf['Escala Inflesz'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 4']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()
#
