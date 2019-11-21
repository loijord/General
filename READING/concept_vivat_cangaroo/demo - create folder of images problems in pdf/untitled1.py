import numpy as np
import matplotlib.pyplot as plt
def rplot(x,y,color):
    new_x, new_y = zip(*sorted(zip(x, y)))
    plt.plot(new_x, new_y, color+'--')
    plt.plot(new_x, new_y, color+'o')
    
#1) Fizikinis stebėjimas

ilgis=np.array([0.78, 0.58, 0.3, 0.2])
laiko_f=2*np.pi*(ilgis/9.8)**0.5
laikas=np.array([1.73, 1.6, 1.25, 1.06])

rplot(ilgis, laiko_f, 'b')
plt.plot(ilgis, laikas, 'r')
plt.ylabel('laikas')
plt.xlabel('ilgis')
    
#2) Funkcijos braižymas

'''x=np.array([-3, 2, -1, 3, -4])
y=x*x+7-2*x
rplot(x,y,'b')
rplot(x,[10, 7, 10, 10, 21],'r')
plt.show()'''

