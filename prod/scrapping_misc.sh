# Set local Time Zone

TZ=America/Monterrey
export TZ  # and export it

# Create directories and file names

# CWD=$( cd "$( dirname ${BASH_SOURCE[0]} )" && pwd )
CWD="/opt/notebook/"
cd $CWD  # set parent directory

mkdir -p logs  # create directory for log files
LOGFILE="logs/scrap_misc_$(date +%Y-%m-%d)".log  # Name for log file


# Execute each python script for scrapping

python /opt/notebook/excelsior.py            >> $LOGFILE
python /opt/notebook/la-jornada-opinion.py  >> $LOGFILE
python /opt/notebook/tabasco-hoy.py         >> $LOGFILE
# python /opt/notebook/abc-noticias.py        #>> $LOGFILE
python /opt/notebook/al-calor-politico.py   >> $LOGFILE
python /opt/notebook/diario-chiapas.py      >> $LOGFILE
# python /opt/notebook/el-imparcial-sonora.py #>> $LOGFILE
# python /opt/notebook/impacto_beta.py             #>> $LOGFILE
python /opt/notebook/milenio.py             #>> $LOGFILE
# python /opt/notebook/universal_beta.py           #>> $LOGFILE

echo "\nAll miscellaneuos scrapping segment has finalized." >> $LOGFILE
