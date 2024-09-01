import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(r"\Users\henri\Documents\pythonProjcs\Percolacao_invasiva_2"))
from data_structure.matriz import Matriz_base
from percolacao_invasiva import Percolacao_invasiva as PI

class Graph:
    def __init__(self) -> None:
        pass

    # Gráfico de pontos com barras de erro (Erro Padrão)
    @staticmethod
    def plot_point(matriz_classe: type, l_inicial: int, l_fim: int, passo: int):
        if not issubclass(matriz_classe, Matriz_base):
            raise TypeError(f"A classe fornecida {matriz_classe.__name__} não herda de Matriz_base.")
        
        dict_v, erros_padrao = Graph.get_graph(matriz_classe, l_inicial, l_fim, passo)
        
        tamanhos = list(dict_v.keys())
        tempos = [np.mean(tempos) for tempos in dict_v.values()]


        plt.figure(figsize=(10, 6))
        plt.errorbar(tamanhos, tempos, yerr=erros_padrao, fmt='-', ecolor='red', capsize=5, label='Erro Padrão')
        plt.xlabel('Tamanho da Rede (L)')
        plt.ylabel('Tempo Médio de Execução (s)')
        plt.title('Tempo Médio de Execução por Tamanho da Rede com Erro Padrão')
        plt.grid(True)
        plt.legend()
        plt.show()



    # Gera o gráfico e calcula o erro padrão
    @staticmethod
    def get_graph(matriz_classe: type, l_inicial: int, l_fim: int, passo: int):
        # Garantir que l_inicial e l_fim sejam ímpares
        if l_inicial % 2 == 0:
            l_inicial += 1
        if l_fim % 2 == 0:
            l_fim -= 1
        passo = abs(passo) if abs(passo) % 2 == 1 else abs(passo) + 1
        
        map_n = lambda x: int(100 + ((x - l_inicial) * 300) / (l_fim - l_inicial))

        dict_time = {}
        erros_padrao = []

        # Calcular tempos e erros padrão para cada tamanho de rede
        for i in range(l_inicial, l_fim + 1, 2*passo):
            tempos_execucao = Graph.mean(matriz_classe(i), map_n(i))
            dict_time[i] = tempos_execucao
            erros_padrao.append(np.std(tempos_execucao) / np.sqrt(len(tempos_execucao)))
        
        return dict_time, erros_padrao

    # Calcula o tempo médio de execução
    @staticmethod
    def mean(matriz: Matriz_base, n: int):
        lista_exe = []
        for _ in range(n):
            lista_exe.append(Graph.get_time(matriz))
            matriz.reset()
        return lista_exe
    
    # Calcula o tempo de uma única execução
    @staticmethod
    def get_time(matriz: Matriz_base) -> float:
        pi = PI()
        init_time = time.time()
        pi.start(matriz)
        end_time = time.time()
        return (end_time - init_time)
    
    @staticmethod
    def plot_mult_graphs(l_inicial: int, l_fim: int, passo: int, *classes):
        plt.figure(figsize=(20, 12))  # Mova a criação da figura para fora do loop
        dict_names = {
            "Matriz_bi":"Heap Binária",
            "Matriz_fibo":"Heap de Fibonacci",
            "Matriz_lis":"Lista de prioridade"
        }
        for matriz in classes:
            if not issubclass(matriz, Matriz_base):
                raise TypeError(f"A classe fornecida {matriz.__name__} não herda de Matriz_base.")
        
            dict_v, erros_padrao = Graph.get_graph(matriz, l_inicial, l_fim, passo)
        
            tamanhos = list(dict_v.keys())
            tempos = [np.mean(tempos) for tempos in dict_v.values()]

            plt.errorbar(tamanhos, tempos, yerr=erros_padrao, fmt='-', ecolor='red', capsize=5, label=dict_names[matriz.__name__])
        
        plt.xlabel('Tamanho da Rede (L)')
        plt.ylabel('Tempo Médio de Execução (s)')
        plt.title('Tempo Médio de Execução por Tamanho da Rede com Erro Padrão')
        plt.grid(True)
        plt.legend()
        plt.show()