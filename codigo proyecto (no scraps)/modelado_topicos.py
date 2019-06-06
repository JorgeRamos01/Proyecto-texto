#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 19:46:18 2018

@author: adrianrdzv
"""

import psycopg2
import sys
import pandas as pd
import spacy
from gensim import corpora
import numpy as np

##-----###

con = psycopg2.connect("host='192.168.1.70' dbname='newspapers_oem1' user='kenny' password='secr3tp455' port = 5433")   
cur = con.cursor()
#cur.execute("SELECT * FROM information_schema.sql_packages")
#Select * from public.news_content1  WHERE newspaper_name = 'Periódico ABC' AND news_date_reported < '2018-01-01'
#cur.execute("SELECT * FROM public.news_content1 WHERE section_name = 'opinion' AND importance_level = 'Nacional' AND newspaper_name = 'La Jornada' AND news_date_reported > '2018-11-10' LIMIT 160")
cur.execute("SELECT * FROM public.news_content1 WHERE section_name = 'opinion' AND importance_level = 'Nacional' AND news_date_reported > '2018-11-10' LIMIT 250")

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

my_df.head

###--------------###

nlp = spacy.load('es')
nlp.vocab["a"].is_stop = True
nlp.vocab["y"].is_stop = True
nlp.vocab["El"].is_stop = True
nlp.vocab["La"].is_stop = True
nlp.vocab["en"].is_stop = True
nlp.vocab["En"].is_stop = True
nlp.vocab["o"].is_stop = True
nlp.vocab["O"].is_stop = True
#nlp.vocab[""].is_stop = True

lista_documentos = []

for d in range(np.shape(my_df)[0]):

    doc = nlp(my_df.loc[d,'news_content'])

    lda_tokens = [] # lista de tokens limpios
    #print(doc.text)
    print("\n\n Taggeo\n\n")
    i=0
    for token in doc:
        #if token.pos_ =="VERB":
        temp_token = (token.lemma_).lower()
        if not(token.is_stop or token.is_punct or token.is_space):
            #print(token.text, token.pos_,token.lemma_, token.dep_)
            i=i+1
            lda_tokens.append(temp_token)
    lista_documentos.append(lda_tokens)

    print("\n\n Entidades\n\n")

#     for ent in doc.ents:
#         print(ent.text, ent.start_char, ent.end_char, ent.label_)

print(i)


####----------------###

from gensim import corpora
from gensim import models
dictionary = corpora.Dictionary(lista_documentos)

dictionary.filter_extremes(no_below=5, no_above=0.4)#agregado

corpus = [dictionary.doc2bow(text) for text in lista_documentos]

#corpus =models.TfidfModel(corpus)

import pickle
pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')

####-----------------#####

import gensim
NUM_TOPICS = 5
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=45,eval_every=None,iterations=400,alpha=0.60)
ldamodel.save('model6.gensim')

topics = ldamodel.print_topics(num_words=6)
for topic in topics:
    print(topic)
        
###-------------------###
array_topicos= np.zeros(240)

for i in range(0,240):
    id_doc=i
    new_doc = lista_documentos[id_doc]
    new_doc_bow = dictionary.doc2bow(new_doc)
    most_prob_topic=ldamodel.get_document_topics(new_doc_bow)
    print("noticia "+str(i))
    print(topics[most_prob_topic[0][0]])
    array_topicos[i] = topics[most_prob_topic[0][0]][0]
    print(array_topicos[i])
    print(most_prob_topic)
  
    
array_topicos    
import matplotlib.pyplot as plt
#plt.pie(array_topicos)

    #print(my_df.loc[id_doc,'news_content'])
##-----------------###
    
#new_doc_bow

my_df.loc[3,'news_content']    

######### PRUEBAS POLICIACAS ############

con = psycopg2.connect("host='192.168.1.70' dbname='newspapers_oem1' user='kenny' password='secr3tp455' port = 5433")   
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

my_df.head

np.shape(my_df)

###-----------------------------------_##

nlp = spacy.load('es')
nlp.vocab["a"].is_stop = True
nlp.vocab["y"].is_stop = True
nlp.vocab["El"].is_stop = True
nlp.vocab["La"].is_stop = True
nlp.vocab["en"].is_stop = True
nlp.vocab["En"].is_stop = True
nlp.vocab["o"].is_stop = True
nlp.vocab["O"].is_stop = True
#nlp.vocab[""].is_stop = True

lista_documentos = []

for d in range(np.shape(my_df)[0]):

    doc = nlp(my_df.loc[d,'news_content'])

    lda_tokens = [] # lista de tokens limpios
    #print(doc.text)
    print("\n\n Taggeo\n\n")
    i=0
    for token in doc:
        #if token.pos_ =="VERB":
        temp_token = (token.lemma_).lower()
        if not(token.is_stop or token.is_punct or token.is_space):
            #print(token.text, token.pos_,token.lemma_, token.dep_)
            i=i+1
            lda_tokens.append(temp_token)
    lista_documentos.append(lda_tokens)

    print("\n\n Entidades\n\n")

#     for ent in doc.ents:
#         print(ent.text, ent.start_char, ent.end_char, ent.label_)


##-------------------------------------------###

from gensim import corpora
from gensim import models
dictionary = corpora.Dictionary(lista_documentos)

dictionary.filter_extremes(no_below=5, no_above=0.30)#agregado

corpus = [dictionary.doc2bow(text) for text in lista_documentos]

#corpus =models.TfidfModel(corpus)

import pickle
pickle.dump(corpus, open('corpus_policia.pkl', 'wb'))
dictionary.save('dictionary_policia.gensim')


###-------------------------------------------##

import gensim
NUM_TOPICS = 5
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=45,eval_every=None,iterations=400,eta=0.70)
#ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=65,eval_every=None,iterations=500,alpha='auto',eta='auto')
ldamodel.save('model_policia.gensim')

topics = ldamodel.print_topics(num_words=8)
for topic in topics:
    print(topic)