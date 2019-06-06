# #Scrapepr impacto.mx, seccion de opinion
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import datetime
from mesANumero import mNumero
from pgdbqueries import send_data_to_db  # module to connect data base
from custom_printing import CustomWrite  # new class (for printing logs)

cw = CustomWrite("Impacto")  # instance class CW
cw.header()  # Header

now = datetime.datetime.now()

site= "http://impacto.mx/seccion-opinion"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
data = urlopen(req)

soup=BeautifulSoup(data,"html5lib")
urls=[]
for a in soup.find_all('a', href=True):
	if "/opinion" in str(a['href']):
		urls.append(a['href'])

urls=list(set(urls)) #Quitamos las direcciones repetidas

num_url=0

cw.init_counter(len(urls))  # initialize counter of the object CW

for i in urls:
	sites= i
	hdr1 = {'User-Agent': 'Mozilla/5.0'}
	req1 = Request(sites,headers=hdr1)
	data1 = urlopen(req1)

	soup1=BeautifulSoup(data1,"html5lib")
	fecha_pub=soup1.find('time').get_text() #Fecha de publicacion
	fecha_pub=mNumero(fecha_pub[fecha_pub.find(" ")+1:fecha_pub.find(",")]+"/"+fecha_pub[:fecha_pub.find(" ")]+"/"+fecha_pub[-4:]) #Arreglamos formato de la fecha de publicacion
	if fecha_pub==str(now.day)+"/"+str(now.month)+"/"+str(now.year):
		title=soup1.find('h1', {'class','entry-title'}).get_text()
		texto=str(soup1.find('div',attrs={'class',"td-post-content"}).get_text())
		texto=texto[texto.find("scrollIntoView"):]
		texto=texto[texto.find("}")+1:]
		texto=texto.replace("\n\n\n","")
		texto=texto.replace("\n\n","")
		texto=texto.replace(".\n",".\n\n")
		texto=text.strip()
		periodico="Impacto"
		seccion="opinion"
		fecha_scrap=now
				# Send content to data base in PostgreSQL
		send_data_to_db(news_title = title, scrapping_date = fecha_scrap, 
			section_name = seccion, 
			news_content = texto, importance_level = "Nacional",
			news_link = i, 
			newspaper_name = periodico, news_name_place_reported = None,
			news_date_reported = fecha_scrap)  # send data
		print("Register of",  num_url + 1, " of ", len(urls), "  inserted successfully.")

		num_url += 1

		cw.debug("Formato de fecha: " + fecha_pub)  # debugging
		cw.status_insert()  # from class CustomWrite: Status

if num_url==0:
	print("No hay noticias nuevas")	


cw.footer()  # Footer