from constraint import *
import sys


def main():

    # Comprobamos que el número de argumentos pasado sea correcto (4 ya que la pos 0 es el propio programa)
    if len(sys.argv) != 4:
        print("Error: número de argumentos incorrecto")
        return

    # Comprobamos que todos los argumentos son strings, ya que no podremos operar con ellos si no lo son
    if (type(argv[0]) != str or type(argv[0]) != str or type(argv[0]) != str):
        print("Error: los argumentos no son correctos")
        return


    # Controlamos la excepción de que la ruta combinada por los diferentes argumentos sea correcta
    try:
        map_file = open(argv[0] + "/" + argv[2])
        cont_file = open(argv[0] + "/" + argv[3])

    # Si no existe, salimos de la ejecución
    except exception:
        print("Error: los ficheros no existen, la ruta está mal y/o los nombres de los ficheros son incorrectos")
        return

    # Leemos el contenido de los dos ficheros obtenidos por las rutas combinadas respectivas
    map = map_file.read()
    cont = cont_file.read()

    # Obtenemos una lista de las posiciones en el mapa
    map = map.replace("\n", " ")
    map = map.split(" ")

    # Gracias al contenido del fichero de contenedores podemos obtener un array de arrays con los atributos de cada contenedor (org, id, dest)
    cont = cont.split("\n")
    containers = []
    for i in cont:
        containers.append(i.split(" "))





















