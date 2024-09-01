import numpy as np
from termcolor import colored as co
from data_structure.matriz import Matriz_base 

# estrutura de dados usando lista encadeada
class Node:
    def __init__(self, key) -> None:
        self.key = key
        self.direita = None
    def value(self, matriz: np.ndarray):
        return matriz[self.key]
class Matriz_lis(Matriz_base):
    def __init__(self, tamanho_l: int, seed=None) -> None:
        super().__init__(tamanho_l, seed)
        self.root = None
        self.conj = set()
        self.qunt = 0
    
    def reset(self):
        super().reset()
        self.root = None
        self.conj = set()
        self.qunt = 0

    # adicionar elemento a lista encadeada
    def insert(self, key):
        node = Node(key)
        if self.root is None:
            self.root = node
            return
        if node.value(self.matriz) < self.root.value(self.matriz):
            node.direita = self.root
            self.root = node
            return
        self._iterate(node, self.root)

        
    def _iterate(self, node: Node, init: Node):
        node_atual = init
        while node_atual.direita is not None and node.value(self.matriz) > node_atual.direita.value(self.matriz):
            node_atual = node_atual.direita
        node.direita = node_atual.direita
        node_atual.direita = node
    
    def extract(self):
        node_min = self.root
        self.root = self.root.direita
        return node_min.key

    def escolher_vizinho(self):
        # petgar mínimo
        mim_value_key = self.extract()
        self.matriz[mim_value_key] = -1
        self.conj.remove(mim_value_key)
        return mim_value_key
    
    def adicionar_vizinhos(self, *vizinhos):
        for vizinho in vizinhos:
            if vizinho not in self.conj and self.matriz[vizinho] >=0:
                self.conj.add(vizinho)
                self.insert(vizinho)
    def conjunto_invadido(self):
        return np.where(self.matriz < 0)[0]
    def __str__(self):
        conjunto_invadido = self.conjunto_invadido()
        string = ""
        for i in self.cord:
            if i in conjunto_invadido:
                string += co("O ", "blue")
            elif i in self.conj:
                string += co("X ", "red")
            else:
                string += co("N ", 'black')
            if (i+1)%self.nox == self.nox -1 :
                string += "\n"
        return string

        
        