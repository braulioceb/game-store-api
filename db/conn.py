from dotenv import dotenv_values
import pyodbc


def open_connection(path_env = '.env'):
    config = dotenv_values(path_env)
    driver = config['DRIVER']
    server = config['SERVER']
    database = config['DATABASE']
    user = config['USER']
    port = config['PORT']
    pwd = config['PWD']
    data_infile = 1 

    '''This function let us establish a connection to the database.'''
    try: 
        connection_string = f'DRIVER={{{driver}}};' \
                            f'SERVER={server};' \
                            f'PORT={port};' \
                            f'DATABASE={database};' \
                            f'UID={user};' \
                            f'PWD={pwd};' \
                            f'ENABLE_LOCAL_INFILE={data_infile}'
        connection = pyodbc.connect(connection_string)
        conn = connection
        return conn
    except Exception as e:
        print(f'something get Error while conecting to tha database: {e}')
