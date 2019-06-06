# #Scrapepr la jornada, seccion de opinion
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import datetime
from pgdbqueries import send_data_to_db  # module to connect data base
from mesANumero import mNumero           #Funcion para cambiar el formato de la fecha
from custom_printing import CustomWrite  # new class (for printing logs)

cw = CustomWrite("La Jornada")
cw.header()  # Header

now = datetime.datetime.now()   - datetime.timedelta(days = 2)
print(now)

site = "https://www.jornada.com.mx/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day).zfill(2)+"/opinion"
print(site)
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
data = urlopen(req)

soup=BeautifulSoup(data,"html5lib")
urls=[]
for a in soup.find_all('a', href=True):
	if "opinion/" in str(a['href']):
		#urls.append("https://www.jornada.com.mx/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day)+"/"+a['href'])
		urls.append("https://www.jornada.com.mx/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day).zfill(2)+"/"+a['href'])

urls = list(set(urls))
num_url = 0


cw.init_counter(len(urls))  # initialize counter of the object CW

for i in urls:
	sites = i 
	hdr1 = {'User-Agent': 'Mozilla/5.0'}
	req1 = Request(sites,headers=hdr1)
	data1 = urlopen(req1)

	soup1 = BeautifulSoup(data1,"html5lib")
	fecha_pub = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
	print("La fecha de pub: " + fecha_pub)  # debug
	
	fecha_pub = mNumero(fecha_pub)  # cast to datetime class (update 2018-11-07)

	if fecha_pub == str(now.day)+"/"+str(now.month)+"/"+str(now.year):
		title=soup1.find('div',attrs={'id','cabeza'}).get_text()
		texto=str(soup1.find('div',attrs={'class','col'}).get_text())
		texto=re.sub(r'\([^)]*\)', '', texto) #eliminar links en el texto
		texto=texto.replace(".\n", ".\n\n")
	
		periodico = "La Jornada"
		seccion = "opinion"
		fecha_scrap = now
		# Send content to data base in PostgreSQL
		send_data_to_db(news_title = title, scrapping_date = fecha_scrap, 
			section_name = seccion, 
			news_content = texto, importance_level = "Nacional",
			news_link = i, 
			newspaper_name = periodico, news_name_place_reported = None,
			news_date_reported = fecha_scrap)  # send data
		#print("Register of",  num_url + 1, " of ", len(urls), "  inserted successfully.")
		
		cw.status_insert()  # from class CustomWrite: Status

		num_url += 1

if num_url == 0:
	print("No hay noticias nuevas")	

cw.footer()  # Footer
