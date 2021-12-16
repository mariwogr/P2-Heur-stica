import sys

class Problema:
    """
    Clase que modela el problema CSP a resolver definiendo el conjunto de variables y el conjunto de restricciones
    """
    def __init__(self):
        """
        Constructor de la clase problema, define su estado inicial
        """
        # Comprobamos que el número de argumentos pasado sea correcto (5 ya que la pos 0 es el propio programa)
        if len(sys.argv) != 5:
            print("Error: número de argumentos incorrecto")
            return

        # Comprobamos que todos los argumentos son strings, ya que no podremos operar con ellos si no lo son
        if (type(sys.argv[1]) != str or type(sys.argv[2]) != str or type(sys.argv[3]) != str or type(sys.argv[4]) != str):
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

        self.heuristic = sys.argv[4]

        # Leemos el contenido de los dos ficheros obtenidos por las rutas combinadas respectivas
        map = map_file.read()
        cont = cont_file.read()

        # Definimos la tupla que representará el estado inicial

        cont = cont.split("\n")
        self.content = []
        for i in cont:
            all_content = i.split(" ")
            self.content.append(tuple(all_content[1:]))
        
        initial_state = []
        for i in range(len(cont)):
            container = [0, None]    
            initial_state.append(container)

        # Añadimos el estado inicial del barco

        initial_state.append(0)
    
        # Creamos el nodo inicial que no tendrá padre

        start_node = Node(initial_state)

        # Resolvemos el problema utlizando A*

        self.astar(start_node)

    def astar(self, start_node, end_node):
        """
        Operador cargar, carga los containers en el barco
        """
        
        # Inicializamos las listas de abiertos y cerrados

        open_list = []
        closed_list = []

        # Añadimos el nodo inicial

        open_list.append(start_node)

        # Bucle hasta que no queden nodos por abrir

        while len(open_list) > 0:

            # Guardamos el nodo actual

            current_node = open_list[0]
            current_index = 0

            # Obtenemos el nodo de la lista de abiertos con menor f

            for cont, i in enumerate(open_list):
                if i.f < current_node.f:
                    current_node = i
                    current_index = cont

        # Eliminamos el nodo actual de la lista de abiertos y lo añadimos a la lista de cerrados

        open_list.pop(current_index)
        closed_list.append(current_node)

        # Comprobamos si hemos encontrado la meta

        if self.is_goal(current_node):
            path = []
            current = current_node
            while current is not None:
                path.append(current.state)
                current = current.parent
            return path[::-1] 
            
        # Generamos los sucesores

        children = []
        
        for cont, i in enumerate(current_node.state[:-1]):
            if i[0] == current_node.state[-1]:
                self.cargar(i)
            


        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.state[0] - end_node.state[0]) ** 2) + ((child.state[1] - end_node.state[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

        

    def is_goal(self, node):
        """
        Método para obtener el nodo final del problema
        """
        
        for cont, i in enumerate(node.state):
            if cont != len(node.state) - 1 and (i[1] != None or i[0] != self.content[cont]):
                return False
        return True

    def cargar(self, i):
        """
        Operador cargar, carga los containers en el barco
        """
        pass
    
    def descargar_destinadosP1_P1(self):
        """
        Operador descargar contenedores destinados a P1 en P1,
        descarga los containers del barco que cumplen esa condición
        """
        pass

    def descargar_destinadosP2_P1(self):
        """
        Operador descargar contenedores destinados a P2 en P1,
        descarga los containers del barco que cumplen esa condición
        """
        pass

    def navegar_bahia_P1(self):
        """
        Operador navegar desde la bahía a puerto 2
        """
        pass

    def navegar_P1_P2(self):
        """
        Operador navegar desde puerto 1 a puerto 2
        """
        pass

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, state, parent=None):
        self.parent = parent
        self.state = state

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.state == other.state
