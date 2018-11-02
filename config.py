## @file config.py
#  @author Mark Vecsernyes
#
#  @brief Ez a fájl indítja el a backend szolgáltatásokat
#  @{ 

## A szükséges könyvtárak importálása
from configparser import ConfigParser

## Adatbázis konfigurálása a fájlból
#  @param filename string a konfigurációs fájl neve
#  @param section string a használt szolgáltatás neve
#  @return Dictionary a konfigurációs paraméterekkel
def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
 
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db
## @}