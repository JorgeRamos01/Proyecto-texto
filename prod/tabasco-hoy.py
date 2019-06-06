#Tabasco hoy secciones region, centro, justicia
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
from mesANumero import mNumero
import datetime
from pgdbqueries import send_data_to_db  # module to connect data base
from scraputils import *           #Funcion para cambiar el formato de la fecha
from custom_printing import CustomWrite  # new class (for printing logs)

cw = CustomWrite("Tabasco hoy")  # instance class CW
cw.header()  # Header

# Settings
storedata = True  # send data to PostgresDB?
now = datetime.datetime.now() - datetime.timedelta(days = 2)

secciones=["justicia", "centro", "region"]

for i in secciones:

	site = "http://www.tabascohoy.com/noticias/"+i
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = Request(site,headers=hdr)
	data = urlopen(req)

	urls = []
	soup = BeautifulSoup(data,"html5lib")
	for a in soup.find_all('a', href=True):
		if "tabascohoy.com/nota" in str(a['href']):
			urls.append(str(a['href'])[:str(a['href']).find("#")-1])

	cw.init_counter(len(urls))  # initialize counter of the object CW

	for j in urls:
		site = j
		hdr = {'User-Agent': 'Mozilla/5.0'}
		req = Request(site,headers=hdr)
		data = urlopen(req)

		soup = BeautifulSoup(data,"html5lib")
		title = soup.find('title').get_text()
		if "-" in title:                           #Conseguimos el titulo
			title=title[:title.find("-")-1]
		temp = soup.find('section', {'class', 'container margin-section'}).find('div', {'class', 'row'}).find_all('span')  #Conseguimos el texto
		texto = ""

		for k in temp:
			if 'span style=' in str(k):
				texto=str(k)
		texto = re.sub('<[^>]+>', '', texto).strip()
		temp2 = soup.find('section', {'class', 'container margin-section'}).find('div', {'class', 'row'}).find_all('p')    #Conseguimos la fecha de publicacion

		# if cw.counter < 3:
		# 	cw.debug("Cuerpo del texto:\n" + texto + "\n")	

		fecha_pub = ""

		for l in temp2:
			if 'p style' in str(l):
				fecha_pub=str(l)

		fecha_pub = re.sub('<[^>]+>', '', fecha_pub).strip()
		lugar = fecha_pub[fecha_pub.find("/ ")+2:fecha_pub.find(",")].lower()
		fecha_pub = fecha_pub[:fecha_pub.find(str(now.year))+4].strip()
		fecha_pub = isodate(fecha_pub)  # from %d/%m/%Y to %Y-%m-%d (ISO format)

		fecha_scrap = now
		periodico = "Tabasco HOY"

		# cw.debug("Lugar: " + lugar)

		if i != "justicia":
			seccion = "Local"
		else:
			seccion = "Policiaca"

		# Send data to db
		if storedata is True:
			send_data_to_db(news_title = title, scrapping_date = fecha_scrap, 
	        section_name = seccion, 
	        news_content = texto, importance_level = "Local",
	        news_link = j, 
	        newspaper_name = periodico, news_name_place_reported = lugar,
	                                    
	        news_date_reported = fecha_scrap)  # send data

		# cw.debug("Formato de fecha: " + str(fecha_pub))  # debugging
		cw.status_insert()  # from class CustomWrite: Status

	if cw.counter == 0:
		print("No hay noticias nuevas en seccion", i)
	

cw.footer()  # Footer