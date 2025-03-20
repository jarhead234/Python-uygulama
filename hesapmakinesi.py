def topla(a,b):
    return a+b
def cikar(a,b):
    return a-b
def carp(a,b):
    return a*b
def bol(a,b):
    return a/b
def hesaplamak(n):
    if n==1:
        return topla
    elif n==2:
        return cikar
    elif n==3:
        return carp
    else:
        return bol
islem = int(input("işlemi girin: "))
aritmetik = hesaplamak(islem)
sayı1 = int(input("1.sayıyı giriniz: "))
sayı2 = int(input("2.sayıyı giriniz: "))
print("sonuc:" , aritmetik(sayı1,sayı2))