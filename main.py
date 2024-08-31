from data_structure.matriz_list import Matriz_lis as Ml
from percolacao_invasiva import Percolacao_invasiva as Pi
import time

#900246724
matriz = Ml(13,900246724)


def set_time(time):
    list =[]
    for i in range(3):
        list.append(time//(60**(2-i)))
        time = time%(60**(2-i))
    list.append(time)
    return " : ".join(map(str, list))
def get_time(obj: Pi):
    start = time.time()
    obj.start(matriz)
    end = time.time()
    
    return set_time(end - start)

get_time(Pi())
print(matriz)