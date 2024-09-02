import sys
import os
import numpy as np
import pandas as pd
import time
sys.path.append(os.path.abspath(r"C:\Users\henri\Documents\pythonProjcs\percolacao_invaisva_tif"))
from modelos.matriz import Matriz_base, Matriz_lis, Matriz_fibo, Matriz_bi
from percolacao import Percolacao_invasiva as PI

class Time_table():
    def __init__(self) -> None:
        pass

    @staticmethod
    def table(*classes_matriz: type):
        dict_names = {
            "Matriz_bi": "Heap Binária",
            "Matriz_fibo": "Heap de Fibonacci",
            "Matriz_lis": "Lista de Prioridade"
        }

        # Coletar tempos de execução e erros padrões
        resultados = {
            'Classe': [],
            'Tempo Médio (s)': [],
            'Erro Padrão (s)': []
        }

        for matriz in classes_matriz:
            nome_classe = dict_names[matriz.__name__]
            tempos = Time_table.get_cases(matriz)
            media_tempo = np.mean(tempos)
            erro_padrao = np.std(tempos) / np.sqrt(len(tempos))

            # Adicionar resultados à tabela
            resultados['Classe'].append(nome_classe)
            resultados['Tempo Médio (s)'].append(media_tempo)
            resultados['Erro Padrão (s)'].append(erro_padrao)

        # Criar DataFrame com pandas
        df_resultados = pd.DataFrame(resultados)
        return df_resultados

    @staticmethod
    def get_cases(classe_matriz: type) -> list:
        list_testes = []
        perco = PI()
        for _ in range(400):
            tempo_execucao = Time_table.get_time(classe_matriz, perco)
            list_testes.append(tempo_execucao)
        return list_testes

    @staticmethod
    def get_time(classe_matriz: type, perco: PI) -> float:
        matriz = classe_matriz()
        inicio = time.time()
        perco.start(matriz)
        fim = time.time()
        return fim - inicio

# Exemplo de uso:
df_resultados = Time_table.table(Matriz_bi, Matriz_fibo, Matriz_lis)
print(df_resultados)
