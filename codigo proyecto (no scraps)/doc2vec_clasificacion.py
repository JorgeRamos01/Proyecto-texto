#### Doc2Vec similaridades ####


import psycopg2
import sys
import pandas as pd
import spacy
from gensim import corpora
import numpy as np

### consultar base de datos  ####

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

#mostrar data frame
my_df.head


#cargar stop words extras
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

#crear modelo LDA
lista_documentos = []

for d in range(np.shape(my_df)[0]):
    doc = nlp(my_df.loc[d,'news_content'])
    lda_tokens = [] # lista de tokens limpios
    #print(doc.text)
    for token in doc:
        #if token.pos_ =="VERB":
        temp_token = (token.lemma_).lower()
        if not(token.is_stop or token.is_punct or token.is_space):
            #print(token.text, token.pos_,token.lemma_, token.dep_)
            lda_tokens.append(temp_token)
    lista_documentos.append(lda_tokens)
#     for ent in doc.ents:
#         print(ent.text, ent.start_char, ent.end_char, ent.label_)


import pickle

from gensim import corpora
from gensim import models
dictionary = corpora.Dictionary(lista_documentos)

dictionary.filter_extremes(no_below=5, no_above=0.25)#agregado
corpus = [dictionary.doc2bow(text) for text in lista_documentos]
#corpus =models.TfidfModel(corpus)

import pickle
pickle.dump(corpus, open('corpus_policia.pkl', 'wb'))
dictionary.save('dictionary_policia.gensim')

### Crear modelo LDA 5 topicos ##
import gensim
NUM_TOPICS = 7
#ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=65,eval_every=None,iterations=600,eta=0.60)
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=65,eval_every=None,iterations=500,alpha='asymmetric',eta=40)
ldamodel.save('model_policia.gensim')

topics = ldamodel.print_topics(num_words=8)
for topic in topics:
    print(topic)

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

