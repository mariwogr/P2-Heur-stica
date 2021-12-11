from constraint import *
import sys
import constraint

class Problema:


    def __init__(self):

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

        self.problem = constraint.Problem()

        # Reducimos los posibles dominios para las variables S y R

        dom_S = self.standar_map(dom)
        dom_R = self.energy_map(dom)

        self.lengths = self.obtain_lengths(dom)

        for i in range(len(vars)):
            vars[i] = tuple(vars[i])    
        
        for i in vars:
            if "S" in i:
                self.problem.addVariable(i, tuple(dom_S))
            else:
                self.problem.addVariable(i, tuple(dom_R))

        self.problem.addConstraint(self.not_equal, tuple(vars))
        self.problem.addConstraint(self.base, tuple(vars))

        #salida = problem.getSolution()

        #print(salida)

    def __str__(self):
        return str(self.problem.getSolution())

    def obtain_lengths(self, dom):
        """
        Devuelve la longitud real de cada columna
        """
        lengths = []
        
        for i in range(len(dom[0])):
            lengths.append(len(dom))

        for i in range(len(dom)):
            for j in range(len(dom[i])):
                if dom[i][j] == "X":
                    lengths[j] -= 1
        return lengths

    def standar_map(self, dom):
        """
        Reduce el dominio de los contenedores tipo S
        """
        valid_positions=[]
        for i in range(len(dom)):
            for j in range(len(dom[i])):
                if dom[i][j] != "X":
                    valid_positions.append((j,i))

        return valid_positions

    def energy_map(self, dom):
        """
        Reduce el dominio de los contenedores tipo R
        """
        valid_positions=[]
        for i in range(len(dom)):
            for j in range(len(dom[i])):
                if dom[i][j] != "X" and dom[i][j] != "N":
                    valid_positions.append((j,i))
        
        return valid_positions

    def not_equal(self, *args):
        """
        Restricción: dos contenedores no pueden ocupar la misma celda
        """
        for i in range (len(args)):
            for j in range (i + 1, len(args)):
                if i != j and args[i] == args[j]:
                    return False
        return True

    def base(self, *args):
        """
        Restricción: un contenedor debe tener a otro debajo o una casilla X en su lugar
        """
        for i in range (len(args)):
            base = False
            for j in range (len(args)):
                base += (i != j and args[i][1] + 1 == args[j][1] and args[i][0] == args[j][0] or args[i][1] == self.lengths[args[i][0]]-1) 
            if not base:
                return False
        return True

if __name__=="__main__":
    a = Problema() 
    print(a)





















