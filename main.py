from data_structure.matriz_list import Matriz_lis as Ml
from data_structure.matriz_binaria import Matriz_bi as MB
from data_structure.matriz_fibo import Matriz_fibo as MF
from percolacao_invasiva import Percolacao_invasiva as Pi
import time

#900246724
n = 1025
matrizL = Ml(n,900246724)
matrizB = MB(n,900246724)
matrizF = MF(n,900246724)

def set_time(time):
    list =[]
    for i in range(3):
        list.append(time//(60**(2-i)))
        time = time%(60**(2-i))
    list.append(time)
    return " : ".join(map(str, list))
def get_time(obj: Pi, matriz):
    start = time.time()
    obj.start(matriz)
    end = time.time()
    
    return set_time(end - start)

print(get_time(Pi(), matrizL))
print(get_time(Pi(), matrizB))
print(get_time(Pi(), matrizF))