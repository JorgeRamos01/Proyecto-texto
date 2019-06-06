# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 18:21:50 2018

@author: jonef
"""
from joblib import load
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

#funcion para recategorizar de números a categorias de complejidad
def renombre_complejidad(x,modelo,ruta):
    #imagenes asocadas con la complejidad
    with cbook.get_sample_data(ruta+'facil.jpg') as facil_image_file:
        facil = plt.imread(facil_image_file)
    with cbook.get_sample_data(ruta+'dificil.jpg') as dificil_image_file:
        dificil = plt.imread(dificil_image_file)
    with cbook.get_sample_data(ruta+'normal.jpg') as normal_image_file:
        normal = plt.imread(normal_image_file)
    
    fig, ax = plt.subplots()
    
    #arreglo donde se guardan las recategorizaciones
    arreglo_final=[]
    for i in modelo.predict(x):
        #arreglo_final.append(renombre(i))
            #categorias
        if int(i)==0:
            x="Facil"
            ax.imshow(facil)
            ax.axis('off')
        elif int(i)==1:
            x="Normal"
            ax.imshow(normal)
            ax.axis('off')
        else:
            x="Dificil"
            ax.imshow(dificil)
            ax.axis('off')
        arreglo_final.append(x)
    print(arreglo_final)

#cargando el modelo probado
clf = load('filename.joblib') 
#datos de prueba
x = {'Silabas' : pd.Series([3024,3008,1487,2008]),'Palabras': pd.Series([924,1473,707,1006]),'Frases': pd.Series([44,73,42,61]),'PROPN': pd.Series([24,134,88,54]),'VERB': pd.Series([34,136,55,96]),'ADJ': pd.Series([40,96,48,82])}
x=pd.DataFrame(x)

#renombre_complejidad(x=x,modelo=clf,ruta='C:/Users/jonef/Documents/Maestría/Tercer Semestre/Datos Complejos/Proyecto/')

#prueba del primero dificil
renombre_complejidad(x=x[:1],modelo=clf,ruta='C:/Users/jonef/Documents/Maestría/Tercer Semestre/Datos Complejos/Proyecto/')

#prueba del primero normal
renombre_complejidad(x=x[:2],modelo=clf,ruta='C:/Users/jonef/Documents/Maestría/Tercer Semestre/Datos Complejos/Proyecto/')

#prueba del primero facil
renombre_complejidad(x=x[:4],modelo=clf,ruta='C:/Users/jonef/Documents/Maestría/Tercer Semestre/Datos Complejos/Proyecto/')



