# #Scrapepr la jornada, seccion de opinion
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import datetime
from pgdbqueries import send_data_to_db  # module to connect data base
from scraputils import *           #Funcion para cambiar el formato de la fecha
from custom_printing import CustomWrite  # new class (for printing logs)


cw = CustomWrite("La Jornada")
cw.header()  # Header

# Settings
storedata = True  # send data to PostgresDB?
now = datetime.datetime.now()#- datetime.timedelta(days = 2)

base_url = "https://www.jornada.com.mx/"
site = base_url + fmtdate(now) + "/opinion"
# cw.debug("Site: " + site)

hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site, headers = hdr)
data = urlopen(req)

soup = BeautifulSoup(data,"html5lib")
urls = []
for a in soup.find_all('a', href=True):
	if "opinion/" in str(a['href']):
		urls.append(base_url + fmtdate(now) + "/" + a["href"])

urls = list(set(urls))

cw.init_counter(len(urls))  # initialize counter of the object CW

for i in urls:
	sites = i 
	hdr1 = {'User-Agent': 'Mozilla/5.0'}
	req1 = Request(sites, headers = hdr1)
	data1 = urlopen(req1)

	soup1 = BeautifulSoup(data1,"html5lib")

	title = soup1.find('div',attrs={'id','cabeza'}).get_text()
	texto = str(soup1.find('div',attrs={'class','col'}).get_text())
	texto = re.sub(r'\([^)]*\)', '', texto) #eliminar links en el texto
	texto = texto.replace(".\n", ".\n\n")
	
	# cw.debug("Url: " + str(i))

	# Extract publication date
	rawdate = extract_rawdate(texto)  # search some date in the body
	fecha_pub = selectdate(rawdate, use_currdate = True)  # datetime object

	#if fecha_pub == str(now.day)+"/"+str(now.month)+"/"+str(now.year):
	if True:

		periodico = "La Jornada"
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
		
		# cw.debug("Fecha pub: " + str(fecha_pub) + "\n")
		cw.status_insert()  # from class CustomWrite: Status

if cw.counter == 0:
	print("No hay noticias nuevas")	

cw.footer()  # Footer
