print 
import numpy as np
import matplotlib.pyplot as plt
def rplot(x,y,color, PRINTSIZE=6, dots=True, write=True):
    new_x, new_y = zip(*sorted(zip(x, y)))
    if write:
        print('x =',''.join([' '*(PRINTSIZE-len(str(n)))+str(n) for n in [round(n,2) for n in x]]))
        print('y =',''.join([' '*(PRINTSIZE-len(str(n)))+str(n) for n in [round(n,2) for n in y]]))
    plt.plot(new_x, new_y, color+'-')
    if dots: plt.plot(new_x, new_y, color+'o')
'''def miscalc(x):
    student_fails={5.0:7}
    for n in x:
        n not in student_fails.keys()
    new=np.array([x-12/x  else student_fails[n]])
    else: return new'''
#1) Fizikinis stebėjimas
'''ilgis=np.array([0.78, 0.58, 0.3, 0.2])
laiko_f=2*np.pi*(ilgis/9.8)**0.5
laikas=np.array([1.73, 1.6, 1.25, 1.06])

rplot(ilgis, laiko_f, 'b')
plt.plot(ilgis, laikas, 'r')
plt.ylabel('laikas')
plt.xlabel('ilgis')'''
    
#2) Funkcijos braižymas
A,B=-5, 6
plt.xlim((A,B))
plt.xticks(np.arange(A,B+1, 1))#(B-A)/10)
rplot([A,B],[0,0],'k', write=False, dots=False)
a,b=-5, 40
plt.ylim((a,b))
plt.yticks(np.arange(a,b+1, 2))#(b-a)/12.5
rplot([0,0],[a,b],'k', write=False, dots=False)
#CHOOSE FUNCTION AND ITS POINTS
x=np.array([1,2,3,4,8,6])
rplot(x,1/x,'g')


'''
x=np.array([-40,40])
y=np.array([0,0])
rplot(x,y,'p')

x=np.array([6,3,-8,-4,5,1,-1,0,10,0.5,-0.5,-20,-40,40,-30,0.25,-0.25])
y=-12/x
rplot(x,y,'y')
#rplot(np.array([6,3,-8,-4,5]),np.array([6,3,9.5,-4,5]),'r')
plt.show()'''



#3)Uzduotis: duota kaire puse puse, reikia prisegti desine puse, kad skaicius butu palindromas'''

'''def vaizduok(x): 
    return str(x)+''.join([str(x)[i] for i in range(int(len(str(x))/2),-1,-1)])
from time import*
t=time()

a=range(1,1000000)
b=[vaizduok(x) for x in a]

print(time()-t)'''
