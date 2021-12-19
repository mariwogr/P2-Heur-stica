from constraint import *
import sys
import constraint

class Problema:
    """
    Clase que modela el problema CSP a resolver definiendo el conjunto de variables y el conjunto de restricciones
    """
    def __init__(self):
        """
        Constructor de la clase problema, define su estado inicial
        """
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
        self.content = []
        for i in cont:
            all_content = i.split(" ")
            self.vars.append(all_content[0])
            self.content.append(tuple(all_content[1:]))
        
        # Definición del problema

        self.problem = constraint.Problem()

        # Reducimos los posibles dominios para las variables S y R

        dom_S = self.standar_map()
        dom_R = self.energy_map()

        # Obtención de la profundidad real (no X) de cada columna

        self.lengths = self.obtain_lengths()
        
        # Asignamos los dominios correspondientes a cada contenedor

        for i in range(len(self.vars)):
            if "S" in self.content[i]:
                self.problem.addVariable(self.vars[i], tuple(dom_S))
            else:
                self.problem.addVariable(self.vars[i], tuple(dom_R))

        # Añadimos las restricciones al problema
        self.problem.addConstraint(constraint.AllDifferentConstraint())
        self.problem.addConstraint(self.base, tuple(self.vars))
        self.problem.addConstraint(self.ports_order, tuple(self.vars))

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

        # Calculamos el número de soluciones

        if sol == None:
            length = 0
        
        else:
            length = len(sol)

        # Adecuamos el formato de la solución

        sols=[]
        for i in sol:
            dic = {}
            for j in i.keys():
                dic[int(j)] = i[j]
            sols.append(dic)

        output = f"Numero de soluciones: {length} \n"

        for i in sols:
            output += str(i)+"\n"

        # Escribimos el fichero solución            
        
        output_file = open(sys.argv[1] + "/" + sys.argv[2] + "-" + sys.argv[3] + ".output", "w")
        output_file.write(output)
    
    def obtain_lengths(self)->list:
        """
        Devuelve la longitud real de cada columna
        """
        lengths = []
        
        # Inicializa la longitud de la lista con el número de columnas
        
        for i in range(len(self.dom[0])):
            lengths.append(len(self.dom))

        # Rellena cada posición de la lista con la longitud real de esa columna indexada

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
                # Definirá el dominio como toda celda no X
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
                # Definirá el dominio como toda celda no X y no N
                if self.dom[i][j] != "X" and self.dom[i][j] != "N":
                    valid_positions.append((j,i))
        
        return valid_positions

    def base(self, *args)->bool:
        """
        Restricción: un contenedor debe tener a otro debajo o una casilla X en su lugar
        """
        
        # Iteramos sobre los posibles valores.
        
        for i in range (len(args)):

            # Inicializamos una variable base a False para actualizarla si hay algún posible valor del contenedor i teniendo otro contenedor
            # debajo o estar encima de una casilla X.
            
            base = False
            for j in range (len(args)):

                # Iremos añadiendo True ó 1 cada vez que se cumpla esta condición:
                #   - No son el mismo elemento (i != j)
                #   - Están en la misma columna (args[i][0] == args[j][0])
                #   - El elemento j está justo debajo de i (args[i][1] + 1 == args[j][1])
                #   Ó si el elemento se encuentra en el último elemento posible de la profundidad de cada pila (args[i][1] + 1 == self.lengths[args[i][0]]-1)

                base += (i != j and args[i][1] + 1 == args[j][1] and args[i][0] == args[j][0] or args[i][1] + 1 == self.lengths[args[i][0]])

            # Si la variable base sigue siendo False, no hay ningún posible valor que cumpla esta restricción => False

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
                # Comprobaciones:
                #   - No son el mismo elemento (i != j)
                #   - Están en la misma columna (args[i][0] == args[j][0])
                #   - El puerto de i debe ser menor en índice que el de j (self.vars[i][2] < self.vars[j][2])
                #   - La profundidad de i es mayor que la de j (args[i][1] > args[j][1])
                if i != j and args[i][0] == args[j][0] and self.content[i][1] < self.content[j][1] and args[i][1] > args[j][1]:
                    return False
        return True

if __name__=="__main__":
    a = Problema()
    a.write_solution()





















