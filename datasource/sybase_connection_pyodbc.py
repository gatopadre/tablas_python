import pyodbc

obj_connection = None

def connect():
    result = False
    try:
        db = pyodbc.connect(
            driver='FreeTDS',
            server='161.131.232.225',
            user='everistdm',
            password='chi08le!',
            database='tdm',
            conn_properties='',
            port='7850'
        )
        global obj_connection
        obj_connection = db
        result = True
    except pyodbc.Error as identifier:
        print(
            '[ERROR] ocurrio un error conectando la base de datos: {}'.format(identifier))
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
    except pyodbc.Error as identifier:
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
    except pyodbc.Error as identifier:
        print('[ERROR] ocurrio un error ejecutando la query: {}'.format(query))
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
    except pyodbc.Error as identifier:
        print('[ERROR] ocurrio un error desconectando la base de datos: {}'.format(identifier))
    return result
