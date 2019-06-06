import re  # regular expressions
import datetime

def mNumero(string):   #Funcion para arreglar el formato de la fecha
    m = {
        'enero': "01",
        'febrero': "02",
        'marzo': "03",
        'abril': "04",
        'mayo': "05",
        'junio': "06",
        'julio': "07",
        'agosto': "08",
        'septiembre': "09",
        'octubre': "10",
        'noviembre': "11",
        'diciembre': "12"
        }

    fecha = string.split("/")
    dia =  fecha[0]
    mes =  fecha[1]
    anio = fecha[2]
    out = str(m[mes.lower()])

    return(dia + "/" +  out + "/" + anio)



def str_to_date(text):   #Funcion para arreglar el formato de la fecha
    m = {
        'enero': "01",
        'febrero': "02",
        'marzo': "03",
        'abril': "04",
        'mayo': "05",
        'junio': "06",
        'julio': "07",
        'agosto': "08",
        'septiembre': "09",
        'octubre': "10",
        'noviembre': "11",
        'diciembre': "12"
        }

    spt_str = text
    temp_date = text.split("/")

    dd =  temp_date[0] # day
    mm = str(m[temp_date[1].lower()])  # month
    yy = temp_date[2]  # year

    return(datetime.date(int(yy), int(mm), int(dd)))

# Extract the sentence of rawdate
def extract_rawdate(text):

    ans_patt = re.findall(r"\d+ de+ \w+ de \d+", text)

    return(ans_patt[0])

# Transform the raw date to an datetime object
def trans_rawdate(patt):

    res_temp = str(patt).replace("de", "/")
    res_temp = res_temp.replace(" ", "")  # remove blank spaces

    return(str_to_date(res_temp))