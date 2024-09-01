import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
sys.path.append(os.path.abspath(r"\Users\henri\Documents\pythonProjcs\Percolacao_invasiva_2"))
from data_structure.matriz import Matriz_base


class PlotMatriz():
    def __init__(self) -> None:
        pass

    @staticmethod
    def _plot(matriz: Matriz_base):
        # Ajustar valores da matriz conforme necessário
            for i in matriz.borda:
                matriz.matriz[i] = 2

            # Defina o colormap base e adicione as cores
            base_cmap = cm.get_cmap('viridis')  # Colormap base

            # Defina as cores adicionais
            colors = ['blue'] + [base_cmap(i) for i in range(base_cmap.N)] + ['red']
            new_cmap = mcolors.LinearSegmentedColormap.from_list('custom_cmap', colors)

            norm = mcolors.Normalize(vmin=-1, vmax=2)

            # Exiba a matriz
            plt.matshow(matriz.matriz.reshape(matriz.nox, matriz.nox), cmap=new_cmap, norm=norm)
            ax = plt.gca()

            #hide x-axis
            ax.get_xaxis().set_visible(False)

            #hide y-axis
            ax.get_yaxis().set_visible(False)
            plt.title(f'L: {matriz.n}x{matriz.n}')
            plt.show()