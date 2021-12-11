from constraint import *
import sys
import constraint

def main():

    # Comprobamos que el número de argumentos pasado sea correcto (4 ya que la pos 0 es el propio programa)
    if len(sys.argv) != 4:
        print("Error: número de argumentos incorrecto")
        return

    # Comprobamos que todos los argumentos son strings, ya que no podremos operar con ellos si no lo son
    if (type(sys.argv[0]) != str or type(sys.argv[0]) != str or type(sys.argv[0]) != str):
        print("Error: los argumentos no son correctos")
        return


    # Controlamos la excepción de que la ruta combinada por los diferentes argumentos sea correcta
    try:
        map_file = open(sys.argv[1] + "/" + sys.argv[2])
        cont_file = open(sys.argv[1] + "/" + sys.argv[3])

    # Si no existe, salimos de la ejecución
    except Exception:
        print("Error: los ficheros no existen, la ruta está mal y/o los nombres de los ficheros son incorrectos")
        return

    # Leemos el contenido de los dos ficheros obtenidos por las rutas combinadas respectivas
    map = map_file.read()
    cont = cont_file.read()

    # Obtenemos una lista de las posiciones en el mapa
    map = map.split("\n")
    dom = []

    for i in map:
        dom.append(i.split(" "))

    # Gracias al contenido del fichero de contenedores podemos obtener un array de arrays con los atributos de cada contenedor (org, id, dest)
    cont = cont.split("\n")
    vars = []
    for i in cont:
        vars.append(i.split(" "))

    # print(map_index(dom))
    # print("------------------------")
    # print(x_positions(dom))

    problem = constraint.Problem()

    # Reducimos los posibles dominios para las variables S y R

    dom_S = standar_map(dom)
    dom_R = energy_map(dom)
    x_map = x_positions(dom)

    for i in range(len(vars)):
        vars[i] = tuple(vars[i])    
    
    for i in vars:
        if "S" in i:
            problem.addVariable(i, tuple(dom_S))
        else:
            problem.addVariable(i, tuple(dom_R))

    problem.addConstraint(not_equal, tuple(vars))
    problem.addConstraint(base, tuple(vars))

    salida = problem.getSolution()

    print(salida)

    write(salida)
        

def standar_map(dom):
    valid_positions=[]
    for i in range(len(dom)):
        for j in range(len(dom[i])):
            if dom[i][j] != "X":
                valid_positions.append((j,i))

    return valid_positions

def energy_map(dom):
    valid_positions=[]
    for i in range(len(dom)):
        for j in range(len(dom[i])):
            if dom[i][j] != "X" and dom[i][j] != "N":
                valid_positions.append((j,i))
    
    return valid_positions

def x_positions(dom):
    x_positions=[]
    for i in range(len(dom)):
        for j in range(len(dom[i])):
            if dom[i][j] == "X":
                x_positions.append((j,i))

    return x_positions

def map_index(dom):
    map_index=[]
    for i in range(len(dom)):
        for j in range(len(dom[i])):
            map_index.append((j, i))  
        
    return map_index

def not_equal(*args):
    for i in range (len(args)):
        for j in range (i + 1, len(args)):
            if i != j and args[i] == args[j]:
                return False
    return True

def base(*args):
    for i in range (len(args)):
        for j in range (i + 1, len(args)):
            if i != j and args[i][1] + 1 == args[j][1] and args[i][0] == args[j][0]:
                return True
        return False

def write(salida):

    for i in salida.keys():
        num = i[0]
        t = (num,salida[i])

    with open("sol.txt","w") as sol:
        sol.write(str(t))

if __name__=="__main__":
    main()  





















