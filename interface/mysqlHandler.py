import os
import configparser
import pymysql
# from interface import Constants

configFile = os.path.dirname(__file__) + '/database.ini'
print(configFile)
config = configparser.ConfigParser()
config.read(configFile)
config.sections()

DATABASE_HOST = config['prod_database']['host']
DATABASE_USER = config['prod_database']['username']
DATABASE_PASSWORD = config['prod_database']['password']
DATABASE = config['prod_database']['database']
DATABASE_CHARSET = config['prod_database']['characterset']

def dbConnect():
    try:
        db_connection = pymysql.connect(host=DATABASE_HOST,
                                        user=DATABASE_USER,
                                        password=DATABASE_PASSWORD,
                                        db=DATABASE,
                                        charset=DATABASE_CHARSET)
    except Exception as e:
        print(e)
    return db_connection

def dbCursor(db_connection):
    cursor = db_connection.cursor()
    return cursor

def dbDictCursor(db_connection):
    cursor = db_connection.cursor(pymysql.cursors.DictCursor)
    return cursor