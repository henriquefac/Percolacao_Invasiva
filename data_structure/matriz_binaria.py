import numpy as np
from termcolor import colored as co
from data_structure.matriz import Matriz_base 
#junto com a matriz, implementa uma heap mínima que pode guardar os indices da matriz e organizar baseado em seus valores

class Matriz_bi(Matriz_base):
    def __init__(self, tamanho_l: int, seed=None) -> None:
        super().__init__(tamanho_l, seed)
        #armazena os indices dos valores da matriz
        self.heap = []

    # setar reset 
    def reset(self):
        super().reset()
        self.heap = []

    def get_element_matriz(self, index_heap):
        return self.matriz[self.heap[index_heap]]
    def pai(self, i):
        return (i - 1) // 2
    def left(self, i):
        return i*2 + 1
    def right(self, i):
        return i*2 + 2
    
    def inserir(self, elemento):
        if elemento in self.heap:
            return
        self.heap.append(elemento)
        self.heapify_up(len(self.heap) - 1)

    def heapify_up(self, index):
        pai_index = self.pai(index)
        
        if index > 0 and self.get_element_matriz(pai_index) > self.get_element_matriz(index):
            self.heap[pai_index], self.heap[index] = self.heap[index],self.heap[pai_index]
            self.heapify_up(pai_index)

    def extract_min(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify_down(0)

        return root
    
    def heapify_down(self, index):
        l = self.left(index)
        r = self.right(index)
        minimo = index

        if l < len(self.heap) and self.get_element_matriz(l) < self.get_element_matriz(minimo):
            minimo = l
        
        if r < len(self.heap) and self.get_element_matriz(r) < self.get_element_matriz(minimo):
            minimo = r
        
        if minimo != index:
            self.heap[minimo], self.heap[index] = self.heap[index], self.heap[minimo]
            self.heapify_down(minimo)

    def get_min(self):
        return self.heap[0] if self.heap else None
    
    def adicionar_vizinhos(self, *vizinhos):
        
        for vizinho in vizinhos:
            if self.matriz[vizinho] >= 0:
                self.inserir(vizinho)
    
    def escolher_vizinho(self):
        escolha = self.extract_min()
        self.matriz[escolha] = -1
        return escolha
    
    def conjunto_invadido(self):
        return np.where(self.matriz < 0)[0]
    
    #mostrar percolacao total
    def __str__(self):
        #conjunto dos indeces de sítios invadidos
        conjunto_invadido = self.conjunto_invadido()
        string = ""
        for i in self.cord:
            if i in conjunto_invadido:
                string += co("O ", "blue")
            elif i in self.heap:
                string += co("X ", "red")
            else:
                string += co("N ", 'black')
            if (i+1)%self.nox == self.nox -1 :
                string += "\n"
        return string