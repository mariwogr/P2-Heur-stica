from constraint import *
import sys
import constraint

class Problema:
    """
    Clase que modela el problema a resolver definiendo
    """

    def __init__(self):

        # Comprobamos que el número de argumentos pasado sea correcto (4 ya que la pos 0 es el propio programa)
        if len(sys.argv) != 4:
            print("Error: número de argumentos incorrecto")
            return

        # Comprobamos que todos los argumentos son strings, ya que no podremos operar con ellos si no lo son
        if (type(sys.argv[1]) != str or type(sys.argv[2]) != str or type(sys.argv[3]) != str):
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
        self.dom = []

        for i in map:
            self.dom.append(i.split(" "))

        # Gracias al contenido del fichero de contenedores podemos obtener un array de arrays con los atributos de cada contenedor (org, id, dest)
        cont = cont.split("\n")
        self.vars = []
        for i in cont:
            self.vars.append(i.split(" "))
        
        self.problem = constraint.Problem()

        # Reducimos los posibles dominios para las variables S y R

        dom_S = self.standar_map()
        dom_R = self.energy_map()

        self.lengths = self.obtain_lengths()

        for i in range(len(self.vars)):
            self.vars[i] = tuple(self.vars[i])    
        
        for i in self.vars:
            if "S" in i:
                self.problem.addVariable(i, tuple(dom_S))
            else:
                self.problem.addVariable(i, tuple(dom_R))

        self.problem.addConstraint(self.not_equal, tuple(self.vars))
        self.problem.addConstraint(self.base, tuple(self.vars))
        self.problem.addConstraint(self.ports_order, tuple(self.vars))

        #salida = problem.getSolution()

        #print(salida)

    def __str__(self)->str:
        """
        Método str que devuelve todas las posibles soluciones del problema
        """
        return self.problem.getSolutions()

    def write_solution(self):
        """
        Escribe la solución de un par map.txt - cont.txt
        """
        sol = self.__str__()

        if sol == None:
            length = 0
        else:
            length = len(sol)

        sols=[]
        
        for i in sol:
            dic = {}
            values = i.values()
            for j in i.keys():
                new = int(j[0])
                dic[new] = i[j]
            sols.append(dic)

        output = f"Numero de soluciones: {length} \n"

        for i in sols:
            output += str(i)+"\n"
        
        output_file = open(sys.argv[1] + "/" + sys.argv[2] + "-" + sys.argv[3] + ".output", "w")
        output_file.write(output)
    
    def obtain_lengths(self)->list:
        """
        Devuelve la longitud real de cada columna
        """
        lengths = []
        
        for i in range(len(self.dom[0])):
            lengths.append(len(self.dom))

        for i in range(len(self.dom)):
            for j in range(len(self.dom[i])):
                if self.dom[i][j] == "X":
                    lengths[j] -= 1
        return lengths

    def standar_map(self)->list:
        """
        Reduce el dominio de los contenedores tipo S
        """
        valid_positions=[]
        for i in range(len(self.dom)):
            for j in range(len(self.dom[i])):
                if self.dom[i][j] != "X":
                    valid_positions.append((j,i))

        return valid_positions

    def energy_map(self)->list:
        """
        Reduce el dominio de los contenedores tipo R
        """
        valid_positions=[]
        for i in range(len(self.dom)):
            for j in range(len(self.dom[i])):
                if self.dom[i][j] != "X" and self.dom[i][j] != "N":
                    valid_positions.append((j,i))
        
        return valid_positions

    def not_equal(self, *args)->bool:
        """
        Restricción: dos contenedores no pueden ocupar la misma celda
        (IMPLÍCITAMENTE) Restricción: el número de contenedores debe ser menor que el de celdas
        """
        for i in range (len(args)):
            for j in range (i + 1, len(args)):
                if i != j and args[i] == args[j]:
                    return False
        return True

    def base(self, *args)->bool:
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
    
    def ports_order(self, *args)->bool:
        """
        Restricción: los containers destinados al puerto 2 siempre
        estarán a más profundidad que los destinados al puerto 1
        """
        for i in range(len(self.vars)):
            for j in range(len(self.vars)):
                if i != j and args[i][0] == args[j][0]:
                    if self.vars[i][2] < self.vars[j][2]:
                        if args[i][1] > args[j][1]:
                            return False
        return True

if __name__=="__main__":
    a = Problema() 
    a.write_solution()





















