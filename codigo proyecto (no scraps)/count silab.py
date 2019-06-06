import pyphen   #Programa que calcula el numero de silabas en un texto
import re
dic = pyphen.Pyphen(lang='es')
texto='Hola, como; estas? yo estoy muy bien, y ¿tu vas? (sorpresa)'
texto1=re.sub(r'[\?\!\-\¿\;\%\$\#\"\'\,]', '', texto)
texto1=re.sub(r'[aeiou]y', 'oi', texto1)
print(texto1)
a=dic.inserted(texto1)
print(a.split("-"))
print(len(a.split("-")))

#Programa que calcula el numero de palabras en un texto
listaPalabras = texto.split()
print(listaPalabras)
print(len(listaPalabras))

texto2=re.sub(r'[\¿\¡\(]', '', texto)
texto2=re.sub(r'[\:\;\.\)\!\?]','.', texto2)
print(texto2.split("."))
print(len(texto2.split(".")))
