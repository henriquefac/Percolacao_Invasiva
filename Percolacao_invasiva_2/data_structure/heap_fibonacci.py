import numpy as np
from termcolor import colored as co
from matriz import Matriz_base 
#criar heap de fibonacci

class Node():
    def __init__(self, key) -> None:
        self.key = key
        self.degree = 0
        self.marked = None
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
    
    def get_val(self, matriz:np.ndarray):
        return matriz[self.key] 
    
    def __str__(self):
        return f"{self.key}"

class Matriz_fibo(Matriz_base):
    def __init__(self, tamanho_l: int, seed=None) -> None:
        super().__init__(tamanho_l, seed)
        self.min_node = None
        self.total_nodes = 0
        self.conjunto_viz = set()
    
    #adicionar elemento a heap
    #lista de roots
    def insert(self, key):
        key = int(key)
        node = Node(key)
        self.conjunto_viz.add(key)
        if self.min_node == None:
            self.min_node = node
        else:
            self._add_to_root_list(node)
            if node.get_val(self.matriz) < self.min_node.get_val(self.matriz):
                self.min_node = node
        self.total_nodes += 1
        return node


    def _add_to_root_list(self, node: Node):
        node.left = self.min_node
        node.right = self.min_node.right
        self.min_node.right.left = node
        self.min_node.right = node


    def extrair_min(self):
        menor = self.min_node
        if menor:
            if menor.child:
                self._add_child_root(menor)
            self._remove_from_root(menor)  # Remove o menor nó da lista de raízes
            if menor == menor.right:
                self.min_node = None  # A heap fica vazia
            else:
                self.min_node = menor.right
                self._consolidate()  # Consolida a lista de raízes
            self.total_nodes -= 1
        self.conjunto_viz.remove(int(menor.key))
        return menor
    
    def _consolidate(self):
        aux = [None] * self.total_nodes
        root_list = [x for x in self._iterate_root()]
        for w in root_list:
            x = w
            d = x.degree
            while aux[d]:
                y = aux[d]
                if x.get_val(self.matriz) > y.get_val(self.matriz):
                    x, y = y, x
                self._link(y, x)
                aux[d] = None
                d += 1
            aux[d] = x
        self.min_node = None
        for i in range(len(aux)):
            if aux[i]:
                if not self.min_node:
                    self.min_node = aux[i]
                else:
                    self._merge_with_root_list(self.min_node, aux[i])
                    if aux[i].get_val(self.matriz) < self.min_node.get_val(self.matriz):
                        self.min_node = aux[i]
    
    def _link(self, y: Node, x: Node):
        self._remove_from_root(y)
        y.left = y.right = y
        y.parent = x
        if not x.child: 
            x.child = y
        else:
            self._merge_with_root_list(x.child, y)
        x.degree += 1
        y.marked = False

    def _add_child_root(self, menor: Node):
        child_list = [x for x in self._iterate_child_list(menor.child)]
        for child in child_list:
            self._merge_with_root_list(self.min_node, child)
            child.parent = None
    

    def _iterate_child_list(self, child: Node):
        if child is None:
            return
        node = child
        while True:
            yield node
            node = node.right
            if node is child:
                break
        
    def _merge_with_root_list(self, min_node, node:Node):
        node.left = min_node
        node.right = min_node.right
        min_node.right.left = node
        min_node.right = node

    def _remove_from_root(self, node: Node):
        # Remove o nó da lista de raízes, ajustando os ponteiros corretamente
        node.left.right = node.right
        node.right.left = node.left

        # Se o nó removido for o único na lista, o ponteiro `min_node` deve ser ajustado.
        if self.min_node == node:
            self.min_node = node.right if node.right != node else None

    def find_min(self):
        return self.min_node
    



    #lista de root
    def _iterate_root(self):
        if self.min_node is None:
            return
        node = self.min_node
        while True:
            yield node
            node = node.right
            
            if node is self.min_node or node.right is node:
                break

        #mostrar todos os itens
    def _iterate_fibo(self, node: Node):
        if node is None:
            return
        node_atual = node
        while True:
            yield node_atual  # Retorna o nó atual
            if node_atual.child:
                # Itera recursivamente sobre os filhos e os retorna
                for child in self._iterate_fibo(node_atual.child):
                    yield child
            node_atual = node_atual.right
            if node_atual is node:
                break             
    
    def adicionar_vizinhos(self, *vizinhos):
        for vizinho in vizinhos:
            if self.matriz[vizinho] >= 0:
                self.insert(vizinho)
    def escolher_vizinho(self):
        escolha = self.extrair_min()
        print(escolha.key)
        self.matriz[escolha.key] = -1
        return escolha.key
    
    def conjunto_invadido(self):
        return np.where(self.matriz < 0)[0]
    
    def __str__(self):
        #conjunto dos indeces de sítios invadidos
        conjunto_invadido = self.conjunto_invadido()
        string = ""
        for i in self.cord:
            if i in conjunto_invadido:
                string += co("O ", "blue")
            elif i in self.conjunto_viz:
                string += co("X ", "red")
            else:
                string += co("N ", 'black')
            if (i+1)%self.nox == self.nox -1 :
                string += "\n"
        return string
matriz_fib = Matriz_fibo(9)
matriz_fib.insert(17)
matriz_fib.insert(18)
matriz_fib.insert(16)
matriz_fib.insert(13)

print("All nodes in Fibonacci heap:")
for node in matriz_fib._iterate_root():
    print(node, node.get_val(matriz_fib.matriz))

print(matriz_fib.conjunto_viz)
print("All nodes in Fibonacci heap:")
print(matriz_fib.extrair_min())
print(matriz_fib.extrair_min())
print(matriz_fib.extrair_min())
print(matriz_fib.extrair_min())

print(matriz_fib.conjunto_viz)