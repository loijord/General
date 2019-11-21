import numpy as np
import matplotlib.pyplot as plt
def rplot(x,y,color):
    new_x, new_y = zip(*sorted(zip(x, y)))
    plt.plot(new_x, new_y, color+'--')
    plt.plot(new_x, new_y, color+'o')
    
'''#1) Fizikinis stebėjimas

ilgis=np.array([0.78, 0.58, 0.3, 0.2])
laiko_f=2*np.pi*(ilgis/9.8)**0.5
laikas=np.array([1.73, 1.6, 1.25, 1.06])

rplot(ilgis, laiko_f, 'b')
plt.plot(ilgis, laikas, 'r')
plt.ylabel('laikas')
plt.xlabel('ilgis')'''
    
#2) Funkcijos braižymas
A,B=-10, 10
plt.xlim((A,B))
plt.xticks(np.arange(A,B+1, (B-A)/20))
a,b=-1,1
plt.ylim((a,b))
plt.yticks(np.arange(a,b+1, (b-a)/10))

#x=np.array(np.arange(0,1,0.0001))

x=np.array([-3,-2,4,0,-1])
y=1/x

rplot(x,y,'b')

PRINTSIZE=6
print('x =',''.join([' '*(PRINTSIZE-len(str(n)))+str(n) for n in [round(n,2) for n in x]]))
print('y =',''.join([' '*(PRINTSIZE-len(str(n)))+str(n) for n in [round(n,2) for n in y]]))
#rplot(x,[10, 7, 10, 10, 21],'r')
plt.show()

