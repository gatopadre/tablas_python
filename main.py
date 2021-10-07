from datasource import mysql
import sys
import os
import tablas

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
# Anotaciones
# TODO: la tabla de contenidos de los archivos va a crecer a la csm, definir indices
# TODO: considerar reutilizar la conexion con la bd o usar por separado como esta ahora

print('Inicio...')

'''
Pasos:
Primera parte:
1.- Recorrer el arbol rescatando los nombres de los archivos
2.- Guardar el nombre de los archivos en la tabla correspondiente
'''

# listado_tablas = tablas.get_files_names()
# tablas.save_all_file_names(listado_tablas)


'''
Segunda parte:
1.- traer el listado de archivos que existen en la bd
2.- con cada archivo existente ir a buscar su contenido
3.- guardar el contenido de cada archivo, contemplar relacion contenido archivo
'''
listado_ruta_archivos = tablas.get_all_files_paths()
tablas.save_all_files_content(listado_ruta_archivos)
print('Fin...')


