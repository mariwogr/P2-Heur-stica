import sys
import time

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

        if sys.argv[4] == "1":
            # h1: no_colocados
            self.heuristic = 0

        elif sys.argv[4] == "2":
            # h2: recorrido
            self.heuristic = 1

        else:
            print("La heurística introducida no es válida")
            return

        # Leemos el contenido de los dos ficheros obtenidos por las rutas combinadas respectivas
        self.map = map_file.read()
        self.cont = cont_file.read()

        self.map = self.map.split("\n")
        self.positions = []

        for i in self.map:
            self.positions.append(i.split(" "))

        # Definimos la tupla que representará el estado inicial
        self.cont = self.cont.split("\n")

        # Este self.content tendrá la información ESTÁTICA de cada contenedor para acceder a ella cuando se quiera
        self.content = []
        for i in self.cont:
            all_content = i.split(" ")
            self.content.append(tuple(all_content[1:]))

        # Se genera un estado inicial: (0, None, 0, None, ..., 0, None, 0)
        initial_state = []
        for i in range(len(self.cont)):
            container = [0, None]    
            initial_state.append(container)
        
        # Recogemos el mapa inicial de carga del barco
        self.initial_map = self.obtain_map()

        # Añadimos el estado inicial del barco
        initial_state.append(0)
    
        # Creamos el nodo inicial que no tendrá padre
        start_node = Node(initial_state)

        # Se obtiene el tiempo de inicio para obtener el tiempo dedicado para resolver el problema
        tiempo_inicio = time.time()

        # Resolvemos el problema utlizando A*
        sol = self.astar(start_node)
        
        self.write(sol, time.time()-tiempo_inicio)
        
    
    def write(self, sol, tiempo_final):
        """
        Escribe la solución con un determinado formato en un fichero aparte
        """
        output = ""
        output_stats=""

        output_stats += f"Tiempo Total: {tiempo_final} segundos\n"
        
        # @param sol contiene la siguiente tupla: (path de nodos, los nodos expandidos)

        if sol[0] == None:
            output = "No hay ninguna solucion para este problema"
            output_stats +="Coste Total: -\n"
            output_stats +="Longitud del Plan: -\n"
        
        else:
            last_index = 0
            for index, i in enumerate(sol[0]):
                if index != 0:
                    # Se obtendrán todas las acciones de cada nodo
                    output += f"{index}- {i.action}\n"
                    last_index = index
                
            output_stats += f"Coste Total: {sol[0][-1].f()}\n"
            output_stats += f"Longitud del Plan: {last_index}\n"

        nodos_exp = len(sol[1])
        output_stats += f"Nodos Expandidos: {nodos_exp}\n"


        # Se escriben en cada 
        output_file = open(sys.argv[1] + "/" + sys.argv[2] + "-" + sys.argv[3] + "-" + sys.argv[4] + ".output", "w")
        output_file.write(output)


        output_stats_file = open(sys.argv[1] + "/" + sys.argv[2] + "-" + sys.argv[3] + "-" + sys.argv[4] + ".stat", "w")
        output_stats_file.write(output_stats)

    def astar(self, start_node):
        """
        Operador cargar, carga los containers en el barco
        """   
        # Inicializamos las listas de abiertos y cerrados
        open_list = SLinkedList()
        closed_list = []

        # Añadimos el nodo inicial
        open_list.insert(start_node)

        # Bucle hasta que no queden nodos por abrir
        while not open_list.is_empty():

            # Eliminamos el nodo actual de la lista de abiertos y lo añadimos a la lista de cerrados
            current_node = open_list.pop_first()

            closed_list.append(current_node)

            # Comprobamos si hemos encontrado la meta
            if self.is_goal(current_node):
                path = []
                current = current_node
                while current is not None:
                    path.append(current)
                    current = current.parent
                return path[::-1], closed_list 
                
            # Generamos los sucesores
            children = self.get_children(current_node)

            for child in children:
                c = True

                # Si alguno de los nodos ya cerrados es igual a algún hijo => no se añade porque ya está abierto
                for i in closed_list:
                    if child ==i:
                        c = False 

                # Si no, se añade a open_list
                if c:
                    open_list.insert(child)

        return None, closed_list

    def is_goal(self, node):
        """
        Método para obtener el nodo final del problema
        """
        for cont, i in enumerate(node.state[:-1]):
            if int(i[0]) != int(self.content[cont][1]):
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
                children.extend(self.cargar(contador, node))

            # Si el barco tiene una posición distinta a 0 (no está en la bahía), la posición del contedor es 3 (bodega del barco) y no existe contenedor arriba, invoca descargar
            
            if node.state[-1] != 0 and i[0] == 3 and self.arriba(contador, node.state):
                    children.extend([self.descargar(contador, node)])

        # Si el barco no se encuentra en el puerto 2 y no hay contenedores en el puerto 0
        if node.state[-1] != 2:
            children.extend([self.navegar(node)])

        return children

    def opciones_colocar(self, contador, state):
        """
        Identifica que celdas están vacías para colocar ahí un contenedor 
        """

        # Recoge todas las posibles posiciones del mapa
        map_modified = self.obtain_map(self.content[contador][0])

        # Definimos una lista already_in a la que iremos añadiendo las posiciones ya ocupadas en el mapa
        already_in = []

        # Iteramos sobre los distintos contenedores de la tupla de estados
        for i in state:

            # Comprobamos si el contenedor está ya en el barco
            if i[1] != None and i[1] in self.initial_map:
                already_in.append(i[1])

                # Eliminamos esa opción del mapa
                if i[1] in map_modified:
                    map_modified.remove(i[1])
        
        # Asignamos posiciones factibles (no volando) iterando sobre el mapa de posibles celdas a ocupar  
        for i in map_modified:

            # pos es una variable que controlará la posición justo debajo de la posición i en las posiciones factibles

            pos = (i[0], i[1] + 1)

            # Si pos está en el mapa inicial (es una posición legal, su profundidad no es mayor que la máxima) y si no hay algún contenedor ya en la posición.
            # Si todo esto se cumple, la posición i no es legal.
            if pos in self.initial_map and pos not in already_in:
                map_modified.remove(i)

        # Devolvemos todas las posibles posiciones.
        return map_modified

    def obtain_map(self, type = None):
        """
        Devuelve las posiciones válidas de un tipo específico de container
        """

        positions = []
 
        for i in range(len(self.positions)):
             for j in range(len(self.positions[i])):
                # Se compara el tipo del contenedor pasado por argumento
                if type == "R":

                    # Si es R se filtra para solo obtener las posiciones de las casillas electrificadas.
                    if self.positions[i][j] != "X" and self.positions[i][j] != "N":
                        positions.append((j,i))
                
                # En cualquier otro caso: None o S, se obtendrán las posiciones de las casillas no X
                else:
                    if self.positions[i][j] != "X":
                        positions.append((j,i))

        return positions

    def copy_node(self, node):
        """
        Devuelve un nodo copia del dado
        """
        new_node = []
        for i in node.state[:-1]:
            inside_node = []
            for j in i:
                inside_node.append(j)
            new_node.append(inside_node)
        new_node.append(node.state[-1])
        return Node(new_node, node)

    def arriba(self, contador, state):
        """
        Comprueba si el contenedor indexado por @param contador tiene la profundidad mínima en la pila de contenedores
        """
        
        # Iteramos sobre los contenedores del estado.
        for index, i in enumerate(state[:-1]):

            # Si el contenedor está dentro del barco (es distinto de None),
            if i[1] is not None:

                # Devolverá False (no está arriba de la pila) si:
                # - si el contenedor en el índice @param contenedor tiene una profundidad mayor a la profundidad del contenedor i (state[contador][1][1] > i[1][1])
                # - si el contenedor en el índice @param contenedor está en la misma pila que i (state[contador][1][0] == i[1][0])
                # - si los contenedores que se comparan son distintos (index != contador)
                if state[contador][1][1] > i[1][1] and state[contador][1][0] == i[1][0] and index != contador:
                    return False
        
        # En otro caso, se devolverá True.
        return True
    
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

            # Calculamos su h
            new_node.h = self.h(new_node.state)

            # Guardamos su acción

            new_node.action = f"Cargar ({contador+1}, {i})"

            # Añadimos los nodos a la lista de nodos generados
            child_nodes.append(new_node)

        return child_nodes

    def descargar(self, contador, node):
        """
        Operador descargar contenedores destinados a P1 en P1,
        descarga los containers del barco que cumplen esa condición
        """
        
        # Creamos el nuevo nodo
        new_node = self.copy_node(node)

        # Obtenemos el valor de la posición en el barco del contenedor
        value = node.state[contador][1]

        # Modificamos su posición a la posición del barco (puerto donde está el barco)
        new_node.state[contador][0] = node.state[-1]

        # Cambiamos la posición del contenedor a None (no ubicado en el barco)
        new_node.state[contador][1] = None

        # Actualizamos el coste g del nuevo nodo: g del nodo anterior + 15 + 2 veces la profundidad de 
        new_node.g = node.g + 15 + 2*(value[0]+1)

        # Guardamos su acción
        new_node.action = f"Descargar ({contador + 1}, {node.state[-1]})"
        return new_node

    def navegar(self, node):
        """
        Operador navegar desde donde está el barco hacia el puerto siguiente
        """

        # Creamos el nuevo nodo
        new_node = self.copy_node(node)

        # Hacemos que el barco se mueva al siguiente puerto sumando 1 a la antigua posición del barco
        new_node.state[-1] = node.state[-1] + 1

        # Actualizamos el coste g del nuevo nodo: g del nodo anterior + 3500 (coste de navegar)
        new_node.g = node.g + 3500

        # Guardamos su acción

        new_node.action = f"Navegar ({node.state[-1]})"

        return new_node

    def h(self, state):
        """
        Operador navegar desde donde está el barco hacia el puerto siguiente
        """
        h = 0
        if self.heuristic == 0:
            # h1: no_colocados

            # Determina cuantos contenedores no están colocados en su puerto destino
            for index, i in enumerate(state[:-1]):
                if int(i[0]) != int(self.content[index][1]) and int(i[0]) == 3:
                    h += 15
                elif int(i[0]) != int(self.content[index][1]) and int(i[0]) != 3:
                    h += 25
            return  h
        
        elif self.heuristic == 1:
            # h2: recorrido

            h = 0
            for index, i in enumerate(state[:-1]):
                # Contenedor puerto actual + No está en su destino
                if int(i[0]) != state[-1] and int(i[0]) != int(self.content[index][1]):
                    # Cargar
                    h += 12.5*2
                if int(i[0]) == 3:
                    # Descargar
                    h += 15
            # Navegar
            h += (2 - state[-1]) * 3500
            return h

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, state, parent=None):
        self.parent = parent
        self.state = state

        self.g = 0
        self.h = 0
        self.action = ""

    def __eq__(self, other):
        return self.state == other.state

    def __str__(self):
        return str(self.state)

    def __repr__(self):
        return self.__str__()

    def f(self):
        return self.g + self.h

class Node_List:
    """
    Representa a un nodo de una lista simplemente enlazada (SLinkedList)
    """
    def __init__(self, dataval=None):
        self.dataval = dataval
        self.next = None

class SLinkedList:
    """
    Representa a una lista simplemente enlazada (SLinkedList)
    """
    def __init__(self):
        """
        Constructor de SLinkedList
        """
        self.head = None
        self.len = 0

    def insert(self, newdata):
        """
        Añade un elemento a la SLinkedList
        """
        new_node = Node_List(newdata)
        if self.head == None:
            self.head = new_node
            self.len +=1
            return

        temp = self.head
        value = new_node.dataval

        if self.head.dataval.f() >= value.f():
            self.head = new_node
            new_node.next = temp
            self.len += 1
            return 

        if self.len == 1:
            if temp.dataval.f() >= value.f():
                self.head = new_node
                new_node.next = temp
                self.len +=1
                return
            temp.next = new_node
            self.len +=1
            return
        
        prev = None
        while temp is not None and temp.dataval.f() <= value.f():
            prev = temp
            temp = temp.next

        prev.next = new_node
        new_node.next = temp
        self.len +=1
       
    def pop_first(self):
        """
        Elimina el primer elemento de la SLinkedList y lo devuelve
        """
        if self.len == 1:
            temp = self.head
            self.head = None
            self.len -= 1
            return temp.dataval

        if self.head != None:
            temp = self.head
            self.head = self.head.next
            self.len -= 1
            return temp.dataval 

    def is_empty(self):
        """
        Comprueba si la SLinkedList está vacía
        """
        return self.len == 0

    def element_in(self, data):
        """
        Comprueba si el data recibido está en la lista
        """
        
        if self.head == None:
            return False

        if self.head.dataval == data:
            return True
        
        temp = self.head

        while temp.next != None:
            temp = temp.next
            if temp.dataval == data:
                return True
        return False
    
if __name__=="__main__":
    a = Problema()