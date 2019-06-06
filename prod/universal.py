# #Scrapepr el universal, seccion de opinion
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import datetime
from pgdbqueries import send_data_to_db  # module to connect data base
from custom_printing import CustomWrite  # new class (for printing logs)

cw = CustomWrite("El Universal")  # instance class CW
cw.header()  # Header

now = datetime.datetime.now()

site= "https://www.eluniversal.com.mx/opinion"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
data = urlopen(req)

soup=BeautifulSoup(data,"html5lib")
urls=[]
for a in soup.find_all('a', href=True):                                       #Conseguimos las urls de notas de opinion
		if "/articulo" in str(a['href']):
			urls.append("https://www.eluniversal.com.mx"+a['href'])

		if "/columna" in str(a['href']):
			urls.append("https://www.eluniversal.com.mx"+a['href'])

for i in range(len(urls)):
	if "https://www.eluniversal.com.mxh" in urls[i]:
		urls[i]=urls[i][len("https://www.eluniversal.com.mx"):]

num_url=0

cw.init_counter(len(urls))  # initialize counter of the object CW

for j in urls:                                                #Obtenemos el contenido de las notas de opinion
	site1= j
	hdr1 = {'User-Agent': 'Mozilla/5.0'}
	req1 = Request(site1,headers=hdr1)
	data1 = urlopen(req1)
	soup1=BeautifulSoup(data1,"html5lib")
	
	fecha_pub=soup1.find('div',{'class','fechap'}).get_text() #Consigue la fecha de publicacion en el formato deseado
	if fecha_pub==str(now.day)+"/"+str(now.month)+"/"+str(now.year):
		seccion="Opinion"
		periodico="El Universal"
		title=soup1.find('title').get_text()   #Consigue el titulo 
		texto=str(soup1.find('div', {'class', 'field field-name-body field-type-text-with-summary field-label-hidden'}).find_all('p'))
		texto=texto.replace("</p>, <p>","\n")
		texto=texto[4:texto.find('</p>, <p class')]
		texto=re.sub('<[^>]+>', '', texto)
		texto=texto.replace('Read in English',"")
	
		fecha_scrap=datetime.datetime.now()
		
		# Send content to data base in PostgreSQL
		# send_data_to_db(news_title = title, scrapping_date = fecha_scrap, 
		# 	section_name = seccion, 
		# 	news_content = texto, importance_level = "Nacional",
		# news_link = j, 
		# 	newspaper_name = periodico, news_name_place_reported = None,
		# 	news_date_reported = fecha_scrap)  # send data
		

		num_url += 1

		cw.debug("Formato de fecha: " + fecha_pub)  # debugging
		cw.status_insert()  # from class CustomWrite: Status


if num_url==0:
	print("No hay noticias nuevas")	

cw.footer()  # Footer