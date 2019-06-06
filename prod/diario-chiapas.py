#diario de Chiapas seccion region
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
from mesANumero import mNumero
import datetime
from pgdbqueries import send_data_to_db  # module to connect data base
from custom_printing import CustomWrite  # new class (for printing logs)
from scraputils import *  # Utility functions of date, validations, etc

cw = CustomWrite("Diario Chiapas")  # instance class CW
cw.header()  # Header

# Settings
cw.storedata = True  # send data to PostgresDB?
now = datetime.datetime.now()#- datetime.timedelta(days = 2)


# Notifications
cw.notifications()

# Define the sections to be scrapped
seccion = ["la-roja", "opinion-dia", "region"]

for j in seccion:
        site = "http://www.diariodechiapas.com/landing/"+j+"/"
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site, headers = hdr)
        data = urlopen(req)

        urls = []
        soup = BeautifulSoup(data,"html5lib")
        for i in soup.find('main', {'class', 'page__main'}).find_all('a', href=True):
                if "/landing" in str(i['href']):
                        if j=="region":
                                if "/region/page" not in str(i['href']):
                                        urls.append(i['href'])
                        elif j=="opinion-dia":
                                if '/columna' not in str(i['href']):
                                        if '/opiniones/' not in str(i['href']):
                                                urls.append(i['href'])
                        else:
                                if "/la-roja/page" not in str(i['href']):
                                        urls.append(i['href'])

        urls = list(set(urls))
        num_url = 0

        cw.init_counter(len(urls))  # initialize counter of the object CW

        for k in urls:
                site = k
                hdr = {'User-Agent': 'Mozilla/5.0'}
                req = Request(site,headers=hdr)
                data = urlopen(req)
                soup = BeautifulSoup(data,"html5lib")
                fecha_pub = soup.find('main', {'class', 'single__main'}).find('em').get_text()
                fecha_pub = fecha_pub.replace(" ","/")
                fecha_pub = fecha_pub.replace(",","")  # get some like 26/noviembre/2018

                # fecha_pub = mNumero(fecha_pub)
                fecha_pub = str_to_date(fecha_pub)  # cast to isodate

                if is_same_day(fecha_pub, now):

                        if j == "region" or j == "la-roja":
                                texto = soup.find('main', {'class', 'single__main'}).find('p').get_text()
                                if len(str(texto))>200:                                       
                                        lugar = texto[texto.find('/')+1:texto.find('\n\n')].lower().strip()
                                        texto = texto[texto.find('\n\n'):]
                                        texto = texto.strip()
                                        title = soup.find('main', {'class', 'single__main'}).find('h1',{'class', 'single__title'}).get_text()
                                        periodico = "Diario de Chiapas"
                                        seccion = "Opinion"
                                        fecha_scrap = now
                                        #print(title, "\n", lugar, "\n\n")
                                        #Send data to db
                                        # send_data_to_db(news_title = title, scrapping_date = fecha_scrap, 
                                        #         section_name = seccion, 
                                        #         news_content = texto, importance_level = "Local",
                                        #         news_link = k, 
                                        #         newspaper_name = periodico, news_name_place_reported = None,
                                        #         news_date_reported = fecha_scrap)  # send data
                                        #  print("Register of",  num_url + 1, " of ", len(urls), "  inserted successfully.")


                                        # cw.debug("Formato de fecha: " + str(fecha_pub))  # debugging
                                        cw.status_insert()  # from class CustomWrite: Status
                                else:
                                        title = soup.find('main', {'class', 'single__main'}).find('h1',{'class', 'single__title'}).get_text()
                                        texto = soup.find('main', {'class', 'single__main'}).find_all('p')
                                        texto = re.sub('<[^>]+>', '\n', str(texto))
                                        texto = texto[1:-1]
                                        if title in texto:
                                                texto = texto[texto.find(title)+len(title):]

                                        texto = re.sub('\n,', "\n",texto)
                                        texto = texto.strip()
                                        lugar = None
                                        periodico = "Diario de Chiapas"
                                        seccion = "Opinion"
                                        fecha_scrap = now

                                        # Send data to db
                                        if cw.storedata is True:
                                                send_data_to_db(news_title = title, 
                                                        scrapping_date = fecha_scrap, 
                                                        section_name = seccion, 
                                                        news_content = texto, importance_level = "Local",
                                                        news_link = k, 
                                                        newspaper_name = periodico, 
                                                        news_name_place_reported = None,
                                                        news_date_reported = fecha_pub)  # send data



                                        # cw.debug("Formato de fecha: " + str(fecha_pub))  # debugging
                                        cw.status_insert()  # from class CustomWrite: Status
if cw.counter == 0:
        print("No hay noticias nuevas en seccion", j)

cw.footer()  # Footer