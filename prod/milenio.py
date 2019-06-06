# #Scrapepr milenio, seccion de opinion
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import datetime
from pgdbqueries import send_data_to_db  # module to connect data base
from custom_printing import CustomWrite  # new class (for printing logs)
from scraputils import *  # Utility functions of date, validations, etc

cw = CustomWrite("Milenio")  # instance class CW
cw.header()  # Header

# Settings
cw.storedata = True  # send data to PostgresDB?
now = datetime.datetime.now()# - datetime.timedelta(days = 1)

# Notifications
cw.notifications()

site= "http://www.milenio.com/opinion"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
data = urlopen(req)

soup=BeautifulSoup(data,"html5lib")
urls = []
match = str(soup.find_all('div',attrs={'class', 'title'})) #Sacamos las urls parciales
match = re.findall(r'href=[\'"]?([^\'" >]+)', match)

for i in match: #Le damos formato a las URLS
	urls.append("http://www.milenio.com" + i)

urls = list(set(urls)) #Quitamos las direcciones repetidas

cw.init_counter(len(urls))  # initialize counter of the object CW

for j in urls:

	site1= j
	hdr1 = {'User-Agent': 'Mozilla/5.0'}
	req1 = Request(site1,headers=hdr1)
	data1 = urlopen(req1)
	soup1 = BeautifulSoup(data1,"html5lib")
	title = soup1.find('title').get_text()   #Consigue el titulo
	
	if soup1.find('time',{'class','date'}) is not None:

		fecha_pub = soup1.find('time',{'class','date'}).get_text()   #Fecha de publicacion y de scrapeo
		fecha_pub = fecha_pub[0:fecha_pub.find("/")]
		fecha_pub = fecha_pub.replace(".","/")
		fecha_pub = isodate(fecha_pub)  # from dd/mm/yyyy string to isodate

		# cw.debug("Formato de fecha: " + str(fecha_pub))  # debugging

		#if fecha_pub == str(now.day)+"/"+str(now.month)+"/"+str(now.year):
		if is_same_day(fecha_pub, now):

			texto = str(soup1.find('div', {'class', 'nd-content-body'}).find_all('p'))        #Todo esto arregla el texto
			texto = texto.replace("<br/><br/>","\n")
			texto = texto.replace("<b>:","")
			texto = re.sub('<[^>]+>', '', texto)
			texto = texto[1:len(texto)-1]
			texto = texto.replace(" , ", "")
			texto = texto.replace(",,", "")
			texto = texto.replace(" , ", "")
			texto = texto.replace(".\n", ".\n\n")
			fecha_scrap = datetime.datetime.now()
	
			periodico = "Milenio"   #Nombre del periodico y seccion
			seccion = "Opinion"

			# Send content to data base in PostgreSQL
			if cw.storedata is True:

				send_data_to_db(news_title = title, scrapping_date = fecha_scrap, 
					section_name = seccion, 
					news_content = texto, importance_level = "Nacional",
					news_link = j, 
					newspaper_name = periodico, news_name_place_reported = None,
					news_date_reported = fecha_pub)  # send data

				# cw.debug("Formato de fecha: " + fecha_pub)  # debugging
				cw.status_insert()  # from class CustomWrite: Status

if cw.counter == 0:
	print("No hay noticias nuevas")	


cw.footer()  # Footer