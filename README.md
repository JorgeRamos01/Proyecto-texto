# Proyecto-texto
Scapping de noticias de varios periódicos nacionales.

Con las noticias recolectadas se hicieron varios análisis:

- En el caso de noticias de opinión (se consideraron noticias de índole política) y se procedió a una clasificación de izquierda-derecha usando una red LSTM y Doc2Vec ambos algoritmos estan basados en técnicas de Deep Learning.

- Se generó un clasificador de textos para establecer la complejidad de la lectura, mejorando el índice Flesch-Szigriszt que actualmente se usa para las investigaciones en ciencias sociales.

- Se consideraron noticias en la secciones policiaca, local y de opinión y se extrajeron los tópicos para clasificarlas de acuerdo a ellas usando LDA.

Para la implementación del sistema se estableció una instancia de docker que permitiría la instancia de una base de datos PostgreSQL, Python, R, sin que las diferencias de versiones entre los sistemas utilizados causara conflicto.
