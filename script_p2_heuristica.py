from constraint import *
import sys
import constraint

class Problema():

    def __init__(self):
        """
        Constructor de la clase, inicializa el problema
        """

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
        self.dom = []

        for i in map:
            self.dom.append(i.split(" "))

        # Gracias al contenido del fichero de contenedores podemos obtener un array de arrays con los atributos de cada contenedor (org, id, dest)
        cont = cont.split("\n")
        self.vars = []
        for i in cont:
            self.vars.append(i.split(" "))

        # print(map_index(dom))
        # print("------------------------")
        # print(x_positions(dom))

        self.problem = constraint.Problem()

        # Reducimos los posibles dominios para las variables S y R

        self.dom_R = self.standar_map(self.dom)
        self.dom_S = self.energy_map(self.dom)
        
        # Obtenemos la profundidad real de cada columna, sin contar las X

        self.lengths = self.obtain_lengths()
        print(self.lengths)

        print(self.dom_S)
        print(self.dom_R)
        x_map = self.x_positions(self.dom)

        for i in range(len(self.vars)):
            self.vars[i] = tuple(self.vars[i])    
        
        for i in self.vars:
            
            if "S" in i:
                self.problem.addVariable(i, tuple(self.dom_S))
            else:
                self.problem.addVariable(i, tuple(self.dom_R))
        

        print(vars)
        self.problem.addConstraint(self.not_equal, tuple(self.vars))
        self.problem.addConstraint(self.base, tuple(self.vars))


    def __str__(self) -> str:
        return self.problem.getSolution()

    def obtain_lengths(self):
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
    

    
    def standar_map(self,dom):
        """
        Elimina del dominio las posiciones que son X
        """
        dom_S=[]
        for i in range(len(dom)):
            for j in range(len(dom[i])):
                if dom[i][j] != "X":
                    dom_S.append((j,i))
        return dom_S
    
    def energy_map(self,dom):
        """
        Elimina del dominio las posiciones que son X y las que son N
        """
        dom_R=[]
        for i in range(len(dom)):
            for j in range(len(dom[i])):
                if dom[i][j] != "X" and dom[i][j] != "N":
                    dom_R.append((j,i))
        return dom_R

    def x_positions(self,dom):
        x_positions=[]
        for i in range(len(dom)):
            for j in range(len(dom[i])):
                if dom[i][j] == "X":
                    x_positions.append((j,i))

        return x_positions

    def not_equal(self,*args):
        """
        Restricción: dos contenedores no pueden ocupar la misma celda
        """
        for i in range (len(args)):
            for j in range (i + 1, len(args)):
                if i != j and args[i] == args[j]:
                    return False
        return True

    def base(self,*args):
        """Voy a intentar ejecutar esta"""
        for i in range (len(args)):
            base = False
            for j in range (len(args)):   
                base += (i != j and args[i][1] + 1 == args[j][1] and args[i][0] == args[j][0] or args[i][1] == self.lengths) 
                print("base: ", base)
            if not base:
                return False
        return True


    def map_index(self,dom):
        map_index=[]
        for i in range(len(dom)):
            for j in range(len(dom[i])):
                map_index.append((j, i))  
            
        return map_index

if __name__=="__main__":
    Problema()
    print(Problema) 



















