#### Doc2Vec similaridades ####


import psycopg2
import sys
import pandas as pd
import spacy
from gensim import corpora
import numpy as np

### consultar base de datos  ####

#con = psycopg2.connect("host='192.168.1.70' dbname='newspapers_oem1' user='kenny' password='secr3tp455' port = 5433")   
con = psycopg2.connect("host='127.0.0.1' dbname='newspapers_oem1' user='kenny' password='secr3tp455' port = 5433")   
cur = con.cursor()
#cur.execute("SELECT * FROM information_schema.sql_packages")
#Select * from public.news_content1  WHERE newspaper_name = 'Periódico ABC' AND news_date_reported < '2018-01-01'
cur.execute("SELECT id, news_title, scrapping_date, section_name, news_content FROM public.news_content1 WHERE section_name = 'policia' AND news_date_reported > '2018-11-22' LIMIT 100")

### Guardar en un dataframe pandas resultado de consulta

col_names =  ['news_title', 'scrapping_date','section_name','news_content']
my_df  = pd.DataFrame(columns = col_names)
#my_df = my_df.append({'news_title': row[1], 'scrapping_date': row[2], 'section_name': row[3],'news_content': row[4]}, ignore_index=True)

while True:
    row = cur.fetchone()

    if row == None:
        break
    my_df = my_df.append({'news_title': row[1], 'scrapping_date': row[2], 'section_name': row[3],'news_content': row[4]}, ignore_index=True)

    #print("\n id: " + str(row[0]) + "\t title: " + str(row[1])+"\t scrapping_date "+str(row[2])+"\t section_name "+row[3]+"\n Contenido\n "+row[4])
con.close()

#mostrar data frame
my_df.head



#cargar stop words extras
#nlp = spacy.load('es')
#nlp.vocab["a"].is_stop = True
#nlp.vocab["y"].is_stop = True
#nlp.vocab["El"].is_stop = True
#nlp.vocab["La"].is_stop = True
#nlp.vocab["en"].is_stop = True
#nlp.vocab["En"].is_stop = True
#nlp.vocab["o"].is_stop = True
#nlp.vocab["O"].is_stop = True
##nlp.vocab[""].is_stop = True


#my_df.loc[:,'news_content']

#### Modelo doc2vec buscar noticias similares ####
#Import all the dependencies
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

import nltk
#nltk.download('punkt')
tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(my_df.loc[:,'news_content'])]


max_epochs = 100
vec_size = 200
alpha = 0.025

model = Doc2Vec(size=vec_size,
                alpha=alpha, 
                min_alpha=0.00025,
                min_count=1,
                dm =1)

model.build_vocab(tagged_data)

for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(tagged_data,
                total_examples=model.corpus_count,
                epochs=model.iter)
    # decrease the learning rate
    model.alpha -= 0.00002
    # fix the learning rate, no decay
    model.min_alpha = model.alpha

model.save("d2v.model")
print("Model Saved")


from gensim.models.doc2vec import Doc2Vec
import scipy

model= Doc2Vec.load("d2v.model")

for i in range(90):
    print(scipy.spatial.distance.cosine(model.docvecs['2'],model.docvecs[str(i)]))



numero_noticia_a_comparar = 2
similaridades = [ [i,scipy.spatial.distance.cosine(model.docvecs[str(numero_noticia_a_comparar)],model.docvecs[str(i)]) ] for i in range(90)]

## Obtener las 5 noticias mas similares
print(sorted(similaridades, key=lambda x: x[1])[1:6])
## Obtener las 5 noticias menos similares
print(sorted(similaridades, key=lambda x: x[1])[-5:])

#obtener solo los indices
[x[0] for x in sorted(similaridades, key=lambda x: x[1])[-5:]]



### Doc2Vec noticias iszquierda derechga    

import os

lista_archivos = []

for i in os.listdir("/home/adrianrdzv/MEGAsync/prdc/26nov/Derecha/"):
    with open('/home/adrianrdzv/MEGAsync/prdc/Derecha/der_1.txt', 'r') as myfile:
        data=myfile.read().replace('\n', '')
        lista_archivos.append(data)

for i in os.listdir("/home/adrianrdzv/MEGAsync/prdc/26nov/Izquierda/"):
    with open('/home/adrianrdzv/MEGAsync/prdc/Derecha/der_1.txt', 'r') as myfile:
        data=myfile.read().replace('\n', '')
        lista_archivos.append(data)

    
len(lista_archivos)

lista_archivos[0]

tagged_data_new = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(lista_archivos)]

tagged_data_new[1]

    

max_epochs = 100
vec_size = 400
alpha = 0.025

model = Doc2Vec(size=vec_size,
                alpha=alpha, 
                min_alpha=0.00025,
                min_count=1,
                sample=0,
                negative=8,
                hs=0,
                dm =0)

model.build_vocab(tagged_data_new)

for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(tagged_data_new,
                total_examples=model.corpus_count,
                epochs=model.iter)
    # decrease the learning rate
    model.alpha -= 0.00002
    # fix the learning rate, no decay
    model.min_alpha = model.alpha

model.save("d2v.model_izq_der")
print("Model Saved")


from gensim.models.doc2vec import Doc2Vec
import scipy

model= Doc2Vec.load("d2v.model_izq_der")

len(lista_archivos)

for i in range(len(lista_archivos)):
    print(scipy.spatial.distance.cosine(model.docvecs['100'],model.docvecs[str(i)]))
    
labels = np.concatenate( [np.zeros(60), np.ones(64) ])


izqder_features = np.zeros((len(lista_archivos),400))

for i in range(len(lista_archivos)):
    izqder_features[i] = model.docvecs[str(i)]

np.shape(izqder_features)
np.shape(labels)
matriz_final = np.concatenate([izqder_features,labels.reshape(-1,1)],axis=1)

from sklearn import svm

clf = svm.SVC(gamma='scale')
clf.fit(izqder_features, labels.ravel().astype(int))

pd.wr

np.savetxt("izqder.csv", matriz_final, delimiter=",")

numero_noticia_a_comparar = 2
similaridades = [ [i,scipy.spatial.distance.cosine(model.docvecs[str(numero_noticia_a_comparar)],model.docvecs[str(i)]) ] for i in range(90)]

## Obtener las 5 noticias mas similares
print(sorted(similaridades, key=lambda x: x[1])[1:6])
## Obtener las 5 noticias menos similares
print(sorted(similaridades, key=lambda x: x[1])[-5:])





#####################33

from gensim import corpora
from gensim import models
dictionary = corpora.Dictionary(tagged_data_new)

dictionary.filter_extremes(no_below=5, no_above=0.4)#agregado

corpus = [dictionary.doc2bow(text) for text in lista_archivos]