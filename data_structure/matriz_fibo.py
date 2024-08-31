import numpy as np
from termcolor import colored as co
from data_structure.matriz import Matriz_base 

class FHNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.mark = False
        self.left = self
        self.right = self
    def get_value(self, matri: np.ndarray):
        return matri[self.key]

    def __str__(self) -> str:
        return f"{self.key}"


class Matriz_fibo(Matriz_base):
    def __init__(self, tamanho_l: int, seed=None) -> None:
        super().__init__(tamanho_l, seed)
        self.min_node = None
        self.num_nodes = 0
        self.conj_viz = set()
    # setar reset
    def reset(self):
        super().reset()
        self.conj_viz = set()
        self.num_nodes = 0
        self.min_node = None

    # função para saber se a heap está vazia
    def is_empty(self):
        return self.min_node is None
        # se fornecer True, está vazia
    
    # inserir nó em uma lista circular, a partir de um nó da lista
    def into_list(self, node:FHNode, no_raiz:FHNode):
        # adicionar o nó a direita da raiz
        # nó aponta para raiz a sua esquera
        node.left = no_raiz
        # no aponta para o nó a direita da raiz
        node.right = no_raiz.right
        # os nós que que o novo nó aponta, devem apontar de volta para ele
        no_raiz.right = node
        node.right.left = node
    
    # inserir nó na lista de raizes

    def into_root_list(self, node: FHNode):
        self.into_list(node, self.min_node)

    # inserir node na heap
    def insert(self, key):
        # um node é criado a partir da key fornecida
        node = FHNode(key)

        # se o nó mínimo forn none, a heap está fazia
        if self.is_empty():
            # se estiver vazio, o novo nó se torna o mínimo
            self.min_node = node
        else:
            # adicionar novo nó na lista de raizes
            self.into_root_list(node)
            # quando adicionar novo nó, verificar se ele é menor que o mínimo
            if node.get_value(self.matriz) < self.min_node.get_value(self.matriz):
                self.min_node = node
        # de qualquer forma, quando nó é adicionado, aumenta o número
        # de nós
        self.num_nodes += 1
        return node
    
    #término do método de inserir


    # método de extrair
    # métodos auxiliares para métodos de extrair
    
    # iterar por uma lista circular a partir de um nó
    def _iterate_list(self, start_node:FHNode):
        # nó inicial
        node = start_node
        while True:
            yield node
            node = node.right
            if node == start_node:
                break
    
    # itera sobre uma lista e todos os nós filhos associados a essa lista
    def _iterate_childs_list(self, start_node:FHNode):
        # nó inicial
        node = start_node
        while True:
            yield node
            
            # checar se o nó dessa iteração possui filhos
            if node.child is not None:
                for i in self._iterate_childs_list(node.child):
                    yield i
                
            
            node = node.right
            if node == start_node:
                break

    # remover no de uma lista
    def remove_from_root_list(self, node: FHNode):
        if node == self.min_node:
            self.min_node = node.right
        # nó a esquerda do removido aponta para a direta do removido
        node.left.right = node.right
        node.right.left = node.left

    # criar relaçãode filho entre dois nós
    def _link(self, pai: FHNode, filho: FHNode):
        filho.parent = None
        filho.left = filho.right = filho
        pai.left = pai.right = pai
        if pai.child is None:
            pai.child = filho
            pai.degree += 1
            return
        self.into_list(filho, pai.child)
        pai.degree += 1
        filho.mark = False


    # consolidar. Esse método é usado para unir as arvores de mesmo grau
    # dinâmicamente
    def consolidate(self):
        # lista para armazenar as arovres de determinado grau
        # grau máximo
        max_degree = int(np.ceil(np.log2(self.num_nodes)))
        
        list_degree = [None] * (max_degree + 1)
        # nós da root
        nodes = [w for w in self._iterate_list(self.min_node)]
        
        for w in range(len(nodes)):
            atual = nodes[w]
            degree = atual.degree
            # se na lista de grau, para o grau atual,
            # houver um nó, os dois serão unidos  
            atual.right = atual.left = atual
            while list_degree[degree] is not None:
                other = list_degree[degree]
                if atual.get_value(self.matriz) > other.get_value(self.matriz):
                    atual, other = other, atual
                # criar relaçao de filho
                self._link(atual, other)
                # assim que ambos forem unidos o grau 
                # do atual aumenta e o nó armazenado no indice atual 
                # se torna None
                list_degree[degree] = None
                degree += 1
            list_degree[degree] = atual
        # depois de unir as arvores da root, vamos recriar a lista 
        # elegendo um novo mínimo 
        self.min_node = None
        for node in list_degree:
            if node is None:
                # se o node atual for None, não há nada a fazer
                continue
            if self.min_node is None:
                # caso não tenha um nó mínimo 
                # o ultimo nó acessado se torna o nó mínimo 
                self.min_node = node
            else:
                # tirar ponteiros do nó
                self.remove_from_root_list(node)
                node.left = node.right = node
                # adicionar nó a root
                self.into_root_list(node)
                if node.get_value(self.matriz) < self.min_node.get_value(self.matriz):
                    self.min_node = node



    # deve remover o menor nó
    # antes de remover, todos os filhos do nó retirado devem 
    # ser adicionados a lista de raises
    def extract(self):
        # nó a ser retirado
        min_node = self.min_node

        # verificar se a lista está vazia
        if self.is_empty():
            return
        
        # verificar se o nó mínimo 
        # possui flhos
        if min_node.child is not None:
            # pegar cada fiho e inserir na root
            list_nodes_child = [i for i in self._iterate_list(min_node.child)]
            for i in list_nodes_child:
                # remover relação de parentesco do node
                i.parent = None

                # adiciona a lista de raizes
                self.into_root_list(i)
            min_node.child = None
        # depois que seusfilhos são adicionados a fila raiz
        # o nó é finalmente removido
        self.remove_from_root_list(min_node)
        if min_node.right == min_node:
            # se a direita do min_node é ele mesmo, que dizer que é o ultimo 
            # nó da heap 
            self.min_node = None
        else:
            self.min_node = min_node.right
            self.consolidate()
        self.num_nodes -= 1
    
        return min_node
    
    def adicionar_vizinhos(self, *vizinhos):

        for vizinho in vizinhos:
            if self.matriz[vizinho] >= 0 and vizinho not in self.conj_viz:
                self.conj_viz.add(int(vizinho))
                self.insert(vizinho)
        
    
    def escolher_vizinho(self):
        escolha = self.extract().key
        self.conj_viz.remove(escolha)
        self.matriz[escolha] = -1
        return escolha
    
    def conjunto_invadido(self):
        return np.where(self.matriz < 0)[0]
    
    def conjunto_vizinho(self):
        return list(map(lambda x:x.key, [a for a in self._iterate_childs_list(self.min_node)]))

    def __str__(self):
        conjunto_invadido = self.conjunto_invadido()
        conjunto_vizinho = self.conjunto_vizinho()
        string = ""
        for i in self.cord:
            if i in conjunto_invadido:
                string += co("O ", "blue")
            elif i in conjunto_vizinho:
                string += co("X ", "red")
            else:
                string += co("N ", 'black')
            if (i+1)%self.nox == self.nox -1 :
                string += "\n"
        return string