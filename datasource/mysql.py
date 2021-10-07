import configparser
import pymysql
import os


obj_connection = None


def connect():
    result = False
    try:
        config = configparser.ConfigParser()
        config.read(os.path.join(os.getcwd(), 'config.ini'))
        db = pymysql.connect(
            host=config['LOCAL']['MYSQL_HOST'],
            user=config['LOCAL']['MYSQL_USER'], 
            password=config['LOCAL']['MYSQL_PASSWORD'], 
            database=config['LOCAL']['MYSQL_DATABASE'],
            port=int(config['LOCAL']['MYSQL_PORT'])
            ) 
        global obj_connection
        obj_connection = db
        result = True
    except pymysql.Error as identifier:
        print('[ERROR] ocurrio un error conectando la base de datos: {}'.format(identifier))
    return result


def disconnect():
    result = False
    try:
        db = obj_connection
        if db is None:
            print('no se recibe la conexion')
            return result
            db.close()                    
        result = True
    except pymysql.Error as identifier:
        print('[ERROR] ocurrio un error desconectando la base de datos: {}'.format(identifier))
    return result


def executeQuery(query):
    result = False
    try:
        db = obj_connection
        if db is False:
            return result
        cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
    except pymysql.Error as identifier:
        print('[ERROR] ocurrio un error ejecutando la query: {}'.format(query))
    return result


def executeUpdate(query):
    result = False
    try:
        db = obj_connection
        if db is False:
            return result
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        cursor.close()
        result = True
    except pymysql.Error as identifier:
        print('[ERROR] ocurrio un error ejecutando la query: {}'.format(query))
    return result