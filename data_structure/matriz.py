import numpy as np
from termcolor import colored as co
#criar matriz para percolacao


#possui estrutura basica para matriz
class Matriz_base():
    def __init__(self, tamanho_l: int, seed = None) -> None:

        self.n = tamanho_l
        self.nox = tamanho_l+2

        # coordenada do meio da matriz
        self.indice_meio = (self.nox**2)//2
        if seed is None:
            seed = np.random.randint(0, 2**31)

        self.seed = seed
        np.random.seed(self.seed)

        self.matriz = self.gerar_matriz()
        # cordenadas iteráveis da matriz
        self.cord = self.cord_Matriz()
        # cordenadas da borda
        self.borda = self.borda_matriz()
        # atribuir valor negativo para meio
        self.matriz[self.indice_meio] = -1

    def gerar_matriz(self):
        return np.random.rand(self.nox**2)

    # recriar matriz para sofre percolacao, mantendo: 
    # tamanho 
    # seed
    def reset(self, seed:bool = False):
        # caso o parâmetro seed seja 
        # True, seed original será mantida 
        if not seed:
            self.seed = np.random.randint(0, 2**31)
            np.random.seed(self.seed)
        # reria a matriz
        self.matriz = self.gerar_matriz()
        # recalcular valor do meio (invadido)
        self.matriz[self.indice_meio] = -1

    def cord_Matriz(self) -> np.ndarray:
        n = self.n
        nox = self.n + 2
        lista = np.zeros((n, n), dtype=int)

        for i in range(n):
            for j in range(n):
                lista[i, j] = nox * (i + 1) + (j + 1)
        return lista.flatten()
    
    def borda_matriz(self) -> np.ndarray:
        return np.setdiff1d(np.array(range((self.nox)**2)), self.cord, assume_unique=True)
    
    #implementar na classe filha
    def adicionar_vizinhos(self, *vizinhos):
        pass

    #implemmentar na classe filha
    def escolher_vizinho(self):
        pass
    
    def __str__(self):
        string = ""
        n = self.n
        nox = self.nox


        for i in range(n):
            for j in range(n):
                string += "{:.2f} ".format(self.matriz[nox * (i + 1) + (j + 1)])
            string += "\n"
        return string
    


"""

#junto com a matriz, implementa uma heap mínima que pode guardar os indices da matriz e organizar baseado em seus valores
class Matriz_heap(Matriz_base):
    def __init__(self, tamanho_l: int, seed=None) -> None:
        super().__init__(tamanho_l, seed)
        #armazena os indices dos valores da matriz
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
        self.matriz[escolha] -= 10
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
        


"""