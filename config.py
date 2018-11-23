## @file config.py
#  @author Mark Vecsernyes
#
#  @brief This loads the database configurations
#  @{ 

## Import modules
from configparser import ConfigParser

## Database configuration from file
#  @param filename string the name of the config file
#  @param section string used service name
#  @return Dictionary with the configuration values
def config(filename='database.ini', section='postgresql'):
    #print(TEST: config config() called)
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