from random import randint

print
print 'PAVYZDZIAI'
print
indec=0
for i in range(30):
    indec+=1
    num=randint(1,10**randint(1,3))
    num2=num*(10**randint(-3,3))
    deg=randint(-5,5)
    if deg<>0:
        if deg<0:
            rez=1.*num2/10**(-deg)
            if rez==int(rez): rez=int(rez)
            print str(indec)+'.   ',num2,':', 10**(-deg), '=', round(rez,8)
        else:
            rez=1.*num2*10**deg
            if rez==int(rez): rez=int(rez)
            print str(indec)+'.   ',num2,'*', 10**deg, '=', rez

print
print 'UZDAVINIAI'
print

indec=0
for i in range(30):
    indec+=1
    num=randint(1,10**randint(1,3))
    num2=num*(10**randint(-3,3))
    deg=randint(-5,5)
    if deg<>0:
        if deg<0:
            print str(indec)+'.   ',num2,':', 10**(-deg)
        else: print str(indec)+'.   ',num2,'*', 10**deg
