def ebob(a,b):
    d = min([a,b])
    seta=[1]
    setb=[1]
    for i in range(1,d+1):
        if a%i==0: seta.add(i)
        if b%i ==0: setb.add(i)
    setc = seta.intersection(setb)
    return max(list(setc))
ebob(15,25)

    
