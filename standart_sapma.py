import math
def ort(liste):
    return sum(liste)/len(liste)
def stdsapma(liste):
    total = 0
    avrg = ort(liste)
    for i in range(len(liste)):
        total = total+(liste[i]-avrg)**2
    return math.sqrt(total/(len(liste)-1))
a = [i for i in range(1,11)]
print(a)
print(stdsapma(a))