import psycopg2
import sys
from datetime import datetime 

# Function to make the connection and insertion to PostgreSQL DB
def insert_data_to_pg(news_title = None, scrapping_date = None, 
	section_name = None, news_content = None, importance_level = None,
	news_link = None, newspaper_name = None, news_name_place_reported = None, 
	news_date_reported = None):
	
	try:
		con = psycopg2.connect("host='192.168.1.70' dbname='newspapers_oem1' \
			user='kenny' password='secr3tp455' port = 5432") # ip changed 
		cur = con.cursor()  # cursor
		
		cur.execute(""" INSERT INTO news_content1 (news_title, scrapping_date, \
		section_name, news_content, importance_level, news_link, newspaper_name, \
		news_name_place_reported, news_date_reported) VALUES (%s, %s, %s, %s,
		%s, %s, %s, %s, %s) """, (news_title, scrapping_date, section_name,
			news_content, importance_level, news_link, newspaper_name, 
			news_name_place_reported, 
			news_date_reported))  # make the query (insert data)

		con.commit()
		cur.close()  # close cursor

	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if con is not None:
			con.close()

# Function to prepare data and send to postgres function
def send_data_to_db(news_title = None, scrapping_date = None, 
	section_name = None, news_content = None, importance_level = None,
	news_link = None, newspaper_name = None, news_name_place_reported = None, 
	news_date_reported = None):

	# Define the arguments to be passed to the query
	news_title = news_title  # Title
	scrapping_date = str(scrapping_date)  # Scrapping date
	section_name = section_name  # Section name
	news_content = str(news_content)
	importance_level = importance_level  # Category of the news
	news_link = news_link # web page
	newspaper_name = newspaper_name  # Newspaper name
	news_name_place_reported = news_name_place_reported  # Place
	news_date_reported = str(news_date_reported)  # News date

	insert_data_to_pg(news_title, scrapping_date, section_name, news_content,
		importance_level, news_link, newspaper_name, news_name_place_reported,
		news_date_reported)  # make connection and insert in to Postgres DB

	print("\n:: SENT ::\n")  # if there no was an error



