#Scrappeador seccion opinion alcalorpolitico.com
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import datetime
from pgdbqueries import send_data_to_db  # module to connect data base
from scraputils import *  # Utility functions of date, validations, etc
from custom_printing import CustomWrite  # new class (for printing logs)

cw = CustomWrite("Al calor politico")  # instance class CW
cw.header()  # Header

# Settings
storedata = True  # send data to PostgresDB?
now = datetime.datetime.now()#- datetime.timedelta(days = 2)

# Notifications
if storedata is False:
	cw.storedata_is_false()  # notification when the data is not storing in DB!

base_url = "https://www.alcalorpolitico.com/"
site = base_url + "informacion/notasarchivo.php?"+"m="+str(now.month)+"&y="+str(now.year)+"&d="+str(now.day)
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site, headers = hdr)
data = urlopen(req)

urls = []     #Consigue todos los links de columnas de opinion del dia
soup = BeautifulSoup(data,"html5lib")

for a in soup.find_all('a', attrs={'href': re.compile("^columnas.php")}):
    urls.append(a.get('href'))

cw.init_counter(len(urls))  # initialize counter of the object CW

##########Scrapea el texto de los textos de opinion
for i in urls:

	site = base_url + "informacion/" + i
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = Request(site,headers=hdr)
	data = urlopen(req)

	# cw.debug("URL: "  + site)  # DEBUG

	soup = BeautifulSoup(data,"html5lib")
	title = soup.find('title').get_text()
	title = title[0:title.find("-")]
	texto = soup.find('div', {'class',"cuerponota"}).get_text()

	# Extract publication date
	rawdate = extract_rawdate(texto)  # search some date in the body
	fecha_pub = selectdate(rawdate, use_currdate = True,
	verbose = True)  # datetime object
	# fecha_pub = str(now.day)+"/"+str(now.month)+"/"+str(now.year)

	fecha_scrap = now
	periodico = "Al Calor Politico"
	seccion = "Opinion"

	# Send content to data base in PostgreSQL
	if storedata is True:
		send_data_to_db(news_title = title, scrapping_date = fecha_scrap, 
		section_name = seccion, 
		news_content = texto, importance_level = "nacional",
		news_link = i, 
		newspaper_name = periodico, news_name_place_reported = None,
		news_date_reported = fecha_pub)  # send data

	# cw.debug("Formato de fecha: " + str(fecha_pub))  # debugging
	cw.status_insert()  # from class CustomWrite: Status

cw.footer()  # Footer
