#El imparcial de Sonora, secciones Hermosillo, Obregon, Nogales, Policiaca
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
from mesANumero import mNumero
import datetime
from pgdbqueries import send_data_to_db  # module to connect data base
from custom_printing import CustomWrite  # new class (for printing logs)

cw = CustomWrite("El imparcial de Sonora")  # instance class CW
cw.header()  # Header

now = datetime.datetime.now()

secciones=["Hermosillo", "Obregon", "Nogales", "Policiaca"]
for indice in secciones:
	site= "https://www.elimparcial.com/Policiaca/"
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = Request(site,headers=hdr)
	data = urlopen(req)

	urls=[]               #Obtenemos las URLs
	temp3=[]
	soup=BeautifulSoup(data,"html5lib")
	temp=soup.find_all('article')
	for i in temp:
		if "data-url=" in str(i):
			temp3.append([m.start() for m in re.finditer('data-url=', str(i))])


	for i in temp3:           #Filtramos las URLs
		temp2=""
		for j in i:
			for k in temp:
				if "data-url=" in str(k)[int(j):int(j)+25]:
					temp2=str(k)[int(j)+10:]
					if len(temp2[:temp2.find('"')])>30:
						urls.append(temp2[:temp2.find('"')])

	urls=list(set(urls))
	num_url=0

	cw.init_counter(len(urls))  # initialize counter of the object CW

	for m in urls:

		site= m
		hdr = {'User-Agent': 'Mozilla/5.0'}
		req = Request(site,headers=hdr)
		data = urlopen(req)

		title=soup.find('title').get_text()       #Obtenemos el titulo
		temp=soup.find_all('time')
		fecha_pub=""                             #Obtenemos la fecha de publicacion
		for i in temp:
			if "datePublished" in str(i):
				fecha_pub=str(i)
		fecha_pub=re.sub('<[^>]+>', '', fecha_pub)
		fecha_pub=fecha_pub[:fecha_pub.find(" ")]
		texto=soup.find('div',{'class', 'notecontent'}).get_text()  #Obtenemos el texto y le damos formato
		temp2=""
		if "VER MÁS" in texto:
			temp2=texto[texto.find("VER MÁS"):]
			temp2=temp2[:temp2.find(".")]
			texto=texto.replace(temp2,"")
		texto=texto.strip()
		lugar=soup.find('span', {'class','nota-procedencia'}).get_text()
		if "," in lugar:
			lugar=lugar[:lugar.find(",")].lower()
		else:
			if len(lugar)<5:
				if index!="Policiaca":
					lugar=indice
					lugar=lugar.lower()
				else:
					lugar="Hermosillo"
			else:
				lugar=lugar[:lugar.find("(")].lower()
		fecha_scrap=now
		periodico="EL IMPARCIAL.COM"
		if indice!="Policiaca":
			seccion="Local"
		else:
			seccion="Policiaca"

		# send_data_to_db(news_title = title, scrapping_date = fecha_scrap, 
  #           section_name = seccion, 
  #           news_content = texto, importance_level = "Local",
  #           news_link = m, 
  #           newspaper_name = periodico, news_name_place_reported = lugar,
  #           news_date_reported = fecha_scrap)  # send data
		# print("Register of",  num_url + 1, " of ", len(urls), "  inserted successfully.")

		num_url += 1
		cw.debug("Formato de fecha: " + fecha_pub)  # debugging
		cw.status_insert()  # from class CustomWrite: Status

if num_url==0:
	print("No hay noticias nuevas en seccion", index)

cw.footer()  # Footer