# #Scrapepr la razon de mexico, seccion de opinion
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import datetime
from scraputils import *           #Funcion para cambiar el formato de la fecha
from pgdbqueries import send_data_to_db  # module to connect data base
from custom_printing import CustomWrite  # new class (for printing logs)

cw = CustomWrite("Excelsior")  # instance class CW
cw.header()  # Header

# Settings
storedata = True  # send data to PostgresDB?
now = datetime.datetime.now() #- datetime.timedelta(days = 1)

site = "https://www.excelsior.com.mx/opinion"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
data = urlopen(req)

soup = BeautifulSoup(data,"html5lib")
urls = []

for a in soup.find('section').find_all('a', href=True):   # Obteniendo las urls
	if "//www.excelsior.com.mx/opinion/" in str(a['href']):
		urls.append("https:"+a['href'])

urls = list(set(urls))  # unique urls
cw.init_counter(len(urls))  # initialize counter of the object CW

for i in urls: # Obteniendo contenido de las noticias
	sites = i
	hdr1 = {'User-Agent': 'Mozilla/5.0'}
	req1 = Request(sites,headers=hdr1)
	data1 = urlopen(req1)
	
	soup1 = BeautifulSoup(data1,"html5lib")
	temp = str(soup1.find('title').get_text())   
	texto = soup1.find('div', {'class','mb2 clear'}).get_text()

	if "|" in temp:
		title = temp[:temp.find(str(now.year)) - 1]  # modify
	else:
		title = temp  # default

	# cw.debug("Url: " + str(i))
	# cw.debug("Cuerpo del texto:\n" + texto + "\n")

	# Extract publication date
	rawdate = extract_rawdate(texto)
	fecha_pub = selectdate(rawdate, use_currdate = False)  # datetime object

	# if str(now.day) + " de" in texto:  # Tener cuidado con el cambio de dia
	# 	fecha_pub = texto[texto.find(str(now.day)):texto.find(str(now.year)) + len(str(now.year))]   
	# 	fecha_pub = fecha_pub.replace(" de ","/")
	# 	fecha_pub = mNumero(fecha_pub)  # Fecha arreglada
	# 	texto = texto[texto.find(str(now.year)) + len(str(now.year)):]

	#if str(fecha_pub) == str(now.strftime("%Y-%m-%d")):
	if is_same_day(fecha_pub, now):

		texto = texto.replace(".\n",".\n\n")
		texto = texto.replace("?\n","?\n\n")
		texto = texto.replace("!\n","!\n\n")
		texto = texto.strip()
		periodico = "Excelsior"
		seccion = "opinion"
		fecha_scrap = now

		# Send content to data base in PostgreSQL
		if storedata is True:
			send_data_to_db(news_title = title, scrapping_date = fecha_scrap, 
			section_name = seccion, 
			news_content = texto, importance_level = "Nacional",
			news_link = i, 
			newspaper_name = periodico, news_name_place_reported = None,
			news_date_reported = fecha_pub)  # send data

		cw.status_insert()  # from class CustomWrite: Status

if cw.counter == 0:
	print("No hay noticias nuevas")			

cw.footer()  # Footer