from data_structure.matriz import Matriz_base
import numpy as np
from memory_profiler import profile

class Percolacao_invasiva():
    def __init__(self) -> None:
        pass

    def start(self, matriz: Matriz_base):
        self.invadir(matriz)

    #lista visinhos
    def get_vizinhos(self, i, nox):
        return np.array([i + 1, i - 1, i + nox, i - nox])
    
    def continuar(self, ultimos_vizinhos, borda):
        return len(np.intersect1d(ultimos_vizinhos, borda)) == 0

    
    def invadir(self, matrix: Matriz_base):
        atual = matrix.indice_meio
        vizinhos = self.get_vizinhos(atual, matrix.nox)
        
        while self.continuar(vizinhos, matrix.borda):
            #adicionar vizinhos para heap
            matrix.adicionar_vizinhos(*vizinhos)
            
            #escolher elemento para ser vizitado
            atual = matrix.escolher_vizinho()
            vizinhos = self.get_vizinhos(atual, matrix.nox)