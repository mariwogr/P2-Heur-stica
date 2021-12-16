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
        self.map = map_file.read()
        self.cont = cont_file.read()

        self.map = self.map.split("\n")
        self.positions = []

        for i in map:
            self.positions.append(i.split(" "))

        # Definimos la tupla que representará el estado inicial

        self.cont = self.cont.split("\n")
        self.content = []
        for i in self.cont:
            all_content = i.split(" ")
            self.content.append(tuple(all_content[1:]))
        
        initial_state = []
        for i in range(len(self.cont)):
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

        self.get_children(current_node)
    

    def is_goal(self, node):
        """
        Método para obtener el nodo final del problema
        """
        
        for cont, i in enumerate(node.state):
            if cont != len(node.state) - 1 and (i[1] != None or i[0] != self.content[cont][1]):
                return False
        return True
    
    def get_children(self, node):
        """
        Devuelve los sucesores de un nodo dado
        """    

        children=[]
        
        # Iteramos sobre todos los contenedores

        for contador,i in enumerate(node.state[:-1]):

            # Si el contenedor i está en la misma posición del barco, se llama a la función cargar para generar los sucesores
            if node.state[-1] == i[0]:
                children.append(self.cargar(contador, node))

            # Si el barco tiene posición 1 (puerto 1), el contenteendor tiene posición 3 (barco) y el contenedor tiene como destino el puerto 1
            # entonces llamamos al operador descargar contenedor destinado a P1 estando en P1
            if node.state[-1] == 1 and i[0] == 3 and self.content[contador][1] == 1:
                children.append(self.descargar_destinadosP1_P1(contador, node))

            # Si el barco tiene posición 1 (puerto 1), el contenteendor tiene posición 3 (barco) y el contenedor tiene como destino el puerto 2
            # entonces llamamos al operador descargar contenedor destinado a P2 estando en P1
            if node.state[-1] == 1 and i[0] == 3 and self.content[contador][1] == 2:
                children.append(self.descargar_destinadosP2_P1(contador, node))
            
            # Si el barco tiene posición 2 (puerto 2), el contenteendor tiene posición 3 (barco) y el contenedor tiene como destino el puerto 2
            # entonces llamamos al operador descargar contenedor destinado a P2 estando en P2
            if node.state[-1] == 2 and i[0] == 3 and self.content[contador][1] == 2:
                children.append(self.descargar_destinadosP2_P2(contador, node))

            # Comprobaremos si todos los contenedores están en el barco, es decir, que su posición sea 3
            all_in = True
            if i[0] != 3:
                all_in = False

            all_p2_in = True
            if i[0] and self.content[contador][1] == 2:
                all_p2_in = False

        # Si el barco se encuentra en el puerto 0 y todos los contenedores se encuentran en el barco
        if node.state[-1] == 0 and all_in:
            children.append(self.navegar_bahia_P1(node))

        # Si el barco se encuentra en el puerto 0 y todos los contenedores destinados al puerto 2 se encuentran en el barco
        if node.state[-1] == 1 and all_p2_in:
            children.append(self.navegar_P1_P2(node))
        
        self.descargar_destinadosP2_P2()
            
    def opciones_colocar(self, state):
        """
        Identifica que celdas están vacías para colocar ahí un contenedor 
        """
        
        map = self.obtain_map()

        for i in state:
            if i[1] != None:
                map.remove(i)
                
        return map

    def obtain_map(self):
        """
        """
        positions=[]
        for i in range(len(self.positions)):
            for j in range(len(self.positions[i])):
                # Definirá el dominio como toda celda no X
                if self.positions[i][j] != "X":
                    positions.append((j,i))

        return positions
    
    def copy_node(self, node):
        """
        Devuelve un nodo copia del dado
        """
        new_node = []
        for i in node[:-1]:
            inside_node = []
            for j in i:
                inside_node.append(j)
            new_node.append(inside_node)
        new_node.append(node[-1])
        return Node(new_node, node)
    
    def cargar(self, contador, node):
        """
        Operador cargar, carga los containers en el barco
        """

        # Obtenemos las posbiles posiciones del barco dónde se puede colocar el contenedor

        posible_positions = self.opciones_colocar(contador, node.state[:-1])

        # Lista de nodos hijo generados por este operador
        
        child_nodes = []

        for i in posible_positions:
            
            # Creamos el nuevo nodo
            new_node = self.copy_node(node)

            # Modificamos su posición a 3 (dentro del barco)
            new_node.state[contador][0] = 3

            # Cambiamos la posición del contenedor a una de las posibles
            new_node.state[contador][1] = i

            # Actualizamos el coste g del nuevo nodo: g del nodo anterior + 10 + la profundidad (más 1 al empezar en 0)
            new_node.g = node.g + 10 + (i[0] + 1)

            # Añadimos los nodos a la lista de nodos generados
            child_nodes.append(new_node)

        return child_nodes

    
    def descargar_destinadosP1_P1(self, contador, node):
        """
        Operador descargar contenedores destinados a P1 en P1,
        descarga los containers del barco que cumplen esa condición
        """
        
        # Creamos el nuevo nodo
        new_node = self.copy_node(node)

        # Obtenemos el valor de la posición en el barco del contenedor
        value = node[contador][1]

        # Modificamos su posición a 1 (puerto 1)
        new_node.state[contador][0] = 1

        # Cambiamos la posición del contenedor a None (no ubicado en el barco)
        new_node.state[contador][1] = None

        # Actualizamos el coste g del nuevo nodo: g del nodo anterior + 15 + 2 veces la profundidad de 
        new_node.g = node.g + 15 + 2*value[0]

        return new_node

    def descargar_destinadosP2_P1(self):
        """
        Operador descargar contenedores destinados a P2 en P1,
        descarga los containers del barco que cumplen esa condición
        """
        pass

    def descargar_destinadosP2_P2(self):
        """
        Operador descargar contenedores destinados a P2 en P1,
        descarga los containers del barco que cumplen esa condición
        """
        pass

    def navegar_bahia_P1(self, node):
        """
        Operador navegar desde la bahía a puerto 2
        """

        # Creamos el nuevo nodo
        new_node = self.copy_node(node)

        # Hacemos que el barco se mueva al siguiente puerto sumando 1 a la antigua posición del barco
        new_node.state[-1] = node.state[-1] + 1

        # Actualizamos el coste g del nuevo nodo: g del nodo anterior + 3500 (coste de navegar)
        new_node.g = node.g + 3500

        return new_node

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
