#Scrapea abcnoticias secciones policia y mty
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from html.parser import HTMLParser
import re
import json
import datetime
from pgdbqueries import send_data_to_db  # module to connect data base
from custom_printing import CustomWrite  # new class (for printing logs)

cw = CustomWrite("ABC Noticias")  # instance class CW
cw.header()  # Header

#### BORRRAR PREVIOS 2018
#DELETE from public.news_content1  WHERE newspaper_name = 'Periódico ABC' AND news_date_reported < '2018-01-01'
###

now = datetime.datetime.now()
proxies = {'http': 'http://www.someproxy.com:3128'}


secciones=["mty","policia"]
for i in secciones:
	site= "https://www.abcnoticias.mx/seccion/"+i   #Solo sirve para la seccion de Mty y policiaca
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = Request(site,headers=hdr)
	data = urlopen(req)

	urls=[]
	soup=BeautifulSoup(data,"html5lib")
	for a in soup.find_all('a', href=True):
		if (str(a['href']))[-1].isdigit():
			urls.append("https://www.abcnoticias.mx"+a['href'])

	urls=list(set(urls)) #Aqui estan todas las urls de noticias

	for k in urls:   #Removemos paginas innecesarias
		if "epsilon" in k:
			urls.remove(k)

	num_url = 0
	cw.init_counter(len(urls))  # initialize counter of the object CW

	for j in urls:
		sites= j  #Scrapea bien secciones Mty y policiaca
		hdr1 = {'User-Agent': 'Mozilla/5.0'}
		req1 = Request(sites,headers=hdr1)
		data1 = urlopen(req1)
		p=HTMLParser()   #Para quitar entidades HTML

		soup1=BeautifulSoup(data1,"html5lib")
		if None!=soup1.find('script', type='application/ld+json'):
			datos = json.loads(soup1.find('script', type='application/ld+json').text)
			texto=p.unescape(str(datos["articleBody"]))
			fecha_pub=p.unescape(str(datos["datePublished"]))[:10]                  #Obtenemos fecha de publicacion
			fecha_pub=fecha_pub[-2:]+"/"+fecha_pub[5:7]+"/"+fecha_pub[:4]    		#Le damos el formato a la fecha de publicacion
			periodico=p.unescape(str(datos["publisher"]["name"]))
			title=p.unescape(str(datos["headline"]))
			fecha_scrap=datetime.datetime.now()
			seccion=i
			lugar=texto[:texto.find(".-")]
			if "," in lugar:
				lugar=lugar[:lugar.find(",")]
			lugar=str(lugar).strip()	#Aparece Ciudad de Mexico y tambien mal escritos
			#print(lugar, "\n")

			send_data_to_db(news_title = title, scrapping_date = fecha_scrap, 
		section_name = seccion, 
		news_content = texto, importance_level = "Local",
		news_link = j, 
		newspaper_name = periodico, news_name_place_reported = lugar,
		news_date_reported = fecha_pub)  # send data
			#print("Register of",  num_url + 1, " of ", len(urls), "  inserted successfully.")

			cw.status_insert()  # from class CustomWrite: Status

			num_url += 1

	cw.footer()  # Footer