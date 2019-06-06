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



# This fuction takes an output from  extract_rawdate(). It's inside of
# trans_rawdate(). The date should be of type "dd/spanish_month_name/yyyy"
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

# Extract a possible date (in a raw format) from the all text
def extract_rawdate(text):

    datepatt = re.compile(r"\d+ de+ \w+ de \d+")
    
    ans_patt = None
    temp_ans = datepatt.findall(text)

    if len(temp_ans) > 0:
        ans_patt = temp_ans[0]

    return(ans_patt)

# Transform the raw date to an datetime object. It takes the output of
# extract_rawdate() function. Currently is used inside of selectdate()
def trans_rawdate(patt):

    if patt is None:
        res_temp = None
    else:
        res_temp = str(patt).replace("de", "/")
        res_temp = res_temp.replace(" ", "")  # remove blank spaces
        res_temp = str_to_date(res_temp)

    return(res_temp)


# This function receives a datetime object and formats
# to YYYY/MM/DD format.
def fmtdate(xdate):
    return(xdate.strftime("%Y/%m/%d"))


# This function takes the output of extract_rawdate() and return the
# output of trans_rawdate().
def selectdate(xdate, use_currdate = True, verbose = False):

    ans = xdate  # could be None
    now = datetime.datetime.now()  # current date

    if xdate is not None:
        ans = trans_rawdate(xdate)  # datetime object
    else:
        if use_currdate is True:
            print("\nNO date appears in raw text, setting CURRENT DATE...\n")
            ans = now
        else:
            print("\nNO date appears in raw text, setting 'date = None'\n")

    return(ans)  # datetime object or None datatype

def is_same_day(date1, date2):

    fmt = "%Y-%m-%d"  # iso format
    return (str(date1.strftime(fmt)) == str(date2.strftime(fmt)))

# This functions transform a string from the format dd/mm/yyyy to 
# datetime object (in isodate).
def isodate(text, fmt = "%d/%m/%Y"):
    return(datetime.datetime.strptime(text, fmt))

