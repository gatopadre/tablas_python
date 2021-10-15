# from datasource import connection
from datasource import sybase_connection_pyodbc as connection

import os
import configparser

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

root_path = config['LOCAL']['ROOT_PATH']

# Obtiene el nombre de los archivos y su ubicacion
def get_files_names():
    counter_files = 0
    result = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        if filenames:
            for file_name in filenames:
                item = {}
                if file_name.find('.parametros') > 0 and file_name.find('.parametros') + len('.parametros') == len(
                        file_name):
                    dirpath_encode = dirpath.encode('utf-8', 'surrogateescape').decode('utf-8', 'replace')
                    filepath_encode = file_name.encode('utf-8', 'surrogateescape').decode('utf-8', 'replace')
                    counter_files += 1
                    item['ruta'] = dirpath_encode.replace('\\','/')
                    item['archivo'] = filepath_encode
                result.append(item)
    return result


def check_if_exist_file_name(file_info):
    connection.connect()
    query = 'select 1 from archivo_parametros where ruta = "{}" and nombre_archivo = "{}"'.format(file_info['ruta'] + '/', file_info['archivo'])
    # query = 'select 1 from archivo_parametros where ruta = "pepita" and nombre_archivo = "juenita"'
    result = connection.executeQuery(query)
    connection.disconnect()
    if len(result) > 0:
        return True
    else:
        return False


def save_file_name(file_info):
    connection.connect()
    query = 'insert into archivo_parametros(ruta, nombre_archivo)  values ("{}","{}")'.format(file_info['ruta'] + '/', file_info['archivo'])
    result = connection.executeUpdate(query)
    connection.disconnect()
    return result


def save_all_file_names(files_info):
    for file_info in files_info:
        if not check_if_exist_file_name(file_info): # evita que se repitan los archivos en la bd
            save_file_name(file_info)
    return True


def get_all_files_paths():
    result = False
    connection.connect()
    query = 'select id, ruta, nombre_archivo from archivo_parametros'
    result = connection.executeQuery(query)
    connection.disconnect()
    return result


# trae el contenido del archivo en bruto
def get_file_content(file_path):
    file = open(file_path, "r")
    return file.read()


# entrega el contenido del archivo separado en clave con sus tipos y valores
def prepare_file_content(file_content):
    arr_lineas = file_content.split('\n')
    result = []
    for index in range(0, len(arr_lineas)):
        item = {}
        arr_lineas_separadas = arr_lineas[index].split(';')
        # arr_lineas_separadas[0] --> contiene las claves
        if not arr_lineas_separadas[0] or len(arr_lineas_separadas) == 1:  # si la linea es vacia o el tipo es vacio
            continue
        item['clave'] = arr_lineas_separadas[0]
        ar_types = []
        for index2 in range(0, len(arr_lineas_separadas) - 1):
            item_types = {}
            if index2 != 0:
                ar_row_types = arr_lineas_separadas[index2].split('=')
                item_types['titulo'] = ar_row_types[0]
                item_types['valor'] = ar_row_types[1]
                ar_types.append(item_types)
                # print('ar_types: {}'.format(arr_lineas_separadas[index2]))
        item['tipos'] = ar_types
        result.append(item)
    return result


def check_if_exist_data(clave, tipo, valor, id_archivo):
    connection.connect()
    query = 'select 1 from datos_archivo_parametros where clave = "{}" and tipo = "{}"' \
            'and valor = "{}" and fk_id_archivo_parametros = {}'.format(clave, tipo, valor, id_archivo)
    result = connection.executeQuery(query)
    connection.disconnect()
    if len(result) > 0:
        return True
    else:
        return False


# guarda el contenido de los archivos
def save_file_data(clave, tipo, valor, id_archivo):
    connection.connect()
    # print('clave: {} / tipo: {} / valor: {} / id_archivo: {}'.format(clave, tipo, valor, id_archivo)) # aqui presenta los datos
    query = 'insert into datos_archivo_parametros (clave, tipo, valor, fk_id_archivo_parametros) values ("{}", "{}", "{}", {})'.format(clave, tipo, valor, id_archivo)
    result = connection.executeUpdate(query)
    connection.disconnect()
    return result


def prepare_file_data_and_save(file_info):
    id_file_path = file_info[0]
    file_path = file_info[1]
    file_name = file_info[2]
    file_url = file_path + '/' + file_name
    file_content = get_file_content(file_url)
    data_in_file = prepare_file_content(file_content)
    for item in data_in_file:
        for tipo in item['tipos']:
            if not check_if_exist_data(item['clave'], tipo['titulo'], tipo['valor'], id_file_path):
                save_file_data(item['clave'], tipo['titulo'], tipo['valor'], id_file_path)
    return True


def save_all_files_content(files):
    print('[INFO] cantidad de archivos a revisar: {}'.format(len(files)))
    for file in files:
        prepare_file_data_and_save(file)
    return True




