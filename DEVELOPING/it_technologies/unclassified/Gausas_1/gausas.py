import numpy as np
import sympy as sp
#jeloveckas rumsiskese

def export_gauss(X, unknowns = None, C=np.array([36, -12]), mode = 'symbolic'):
    def bold(num):
        return str(r'\bm{'+str(num)+r'}')
    def blue(num):
        #print(r'\textcolor{'+r'blue}{' + str(num) + r'}')
        return r"\textcolor{blue}{%s}" % num
    def extract(X, boldable = None, blueable = None, coloring = None):
        X = X.copy().astype('object')
        COMMAND=[]
        COMMAND.append(r'\noindent$\left(\begin{array}{'+"r"*len(X)+"|"+"r"*(len(X[0])-len(X))+"}")
        for ind in range(len(X)): 
            if ind == boldable: X[ind] = [bold(n) for n in X[ind]]
            if blueable is not None: 
                if coloring=='down':
                    if ind > blueable : X[ind][blueable] = blue(X[ind][blueable])
                elif coloring == 'up':
                    if ind < blueable : X[ind][blueable] = blue(X[ind][blueable])
            COMMAND.append(' & '.join(X[ind].astype(str))+r'\\')
        COMMAND.append(r'\end{array}\right)')
        return COMMAND
    def mul(a,b): 
        #print(a,b)
        return np.array([a[i]*b[i] for i in range(len(a))])
    def cmul(a,k): 
        #print('lam',a, k)
        return np.array([a[i]*k for i in range(len(a))])
    def add(a,b): 
        #print(a,b)
        return np.array([a[i]+b[i] for i in range(len(a))])
    
    I= np.array([0, 3]) + np.array([0, 12*(len(X)-1)/2])
    """change first value of C to get spaces between arrows different"""
    
    if unknowns != None:
        for n in extract_system(X, unknowns):
            print(n)
        print
    print('\nREMIANTIS GAUSO METODU:\n')
    
    for i in range(len(X)-1): #i is row being subtracted
        GRAPHICS=[r'\setlength{\unitlength}{1pt}']
        GRAPHICS.append(r'\begin{picture} (%s, 0)' % ((len(X)-1)*C[0]-10))
        
        for n in extract(X,i,i,coloring = 'down'): print(n)
        for j in range(i+1, len(X)):
            k = sp.Rational(-X[j][i], X[i][i])
            if mode == 'simple': k = round(-X[j][i]/X[i][i],3)
            X[j] = add(X[j], cmul(X[i],k))
            coords= I + C*np.array([j-i-1,i])
            GRAPHICS.append(r'\put(%s, %s){\vector(0, -1){%s}}' % (coords[0], coords[1], abs(12*(j-i))))
            coords+=np.array([3,0])+np.array([0, -6])
            GRAPHICS.append(r'\put(%s, %s){\tiny{$\times%s$}}' % (coords[0], coords[1], [r'\left('+str(sp.latex(k))+r'\right)',sp.latex(k)][bool(k>0)]))
        GRAPHICS.append(r'\end{picture}'+'=$'+'\n')
        for n in GRAPHICS: print(n)
        
    for i in range(len(X)-1, 0, -1): #i is row being subtracted
        GRAPHICS=[r'\setlength{\unitlength}{1pt}']
        GRAPHICS.append(r'\begin{picture} (%s, 0)' % ((len(X)-1)*C[0]-10))
        for n in extract(X,i,i,coloring = 'up'): print(n)
        for j in range(i - 1, -1, -1):
            k = sp.Rational(-X[j][i]/X[i][i])
            if mode == 'simple': k = round(-X[j][i]/X[i][i],3)
            X[j] = add(X[j], cmul(X[i],k))
            coords= I + C*np.array([-j+i-1,i])
            GRAPHICS.append(r'\put(%s, %s){\vector(0, 1){%s}}' % (coords[0], coords[1], abs(12*(j-i))))
            coords+=np.array([3,0])+np.array([0, 6])
            GRAPHICS.append(r'\put(%s, %s){\tiny{$\times%s$}}' % (coords[0], coords[1], [r'\left('+str(sp.latex(k))+r'\right)',sp.latex(k)][bool(k>0)]))
        GRAPHICS.append(r'\end{picture}'+'=$'+'\n')
        for n in GRAPHICS: print(n)
    disp = extract(X)
    for i in range(len(disp)): 
        if i == len(disp) - 1: print(disp[i]+'$')
        else: print(disp[i])
    if any([X[i][i]!=1 for i in range(len(X))]):
        print('=')
        for i in range(len(X)):
            X[i]=X[i]/X[i][i]
        disp = extract(X)
        for i in range(len(disp)): 
            if i == len(disp) - 1: print(disp[i]+'$')
            else: print(disp[i])
    
    if unknowns != None:
        print
        print('\nSPRENDINIAI:\n')
        for n in extract_system(X, unknowns, True): print(n)

def extract_system(X, unknowns, show_nulls = False):
    X = X.copy().astype('object')
    COMMAND=[]
    COMMAND.append(r'$\left\{\begin{array}{'+"l"+'|'.join('r'*(len(X[0])-len(X)))+r'}')
    for ind in range(len(X)):
        row = [n for n in X[ind].astype(str)]
        for j in range(len(unknowns)): 
            if show_nulls and row[j]=='0': 
                row[j] = row[j] + unknowns[j]
                row[j] = r'\phantom{'+row[j]+'}'
            else: row[j] = row[j] + unknowns[j]
        COMMAND.append(' + '.join(row[:len(X)])+r' &='+' & '.join(row[len(X):])+r'\\')
    COMMAND.append(r'\end{array}\right.$')
    return COMMAND

    
X=np.array([[1, 1, 2, 1, 7], [3, 4, 8, 5, 29], [1, 3, 7, 8, 30], [2, 2, 5, 6, 23]])
export_gauss(X.astype(object), unknowns = ['a','b','c','d'], C=np.array([35, -12]))
extract_system(X, ['a','b','c','d'])

#X=np.array([[-5,4,-2, -11], [2,-6,2, -3.4], [-3,4,-4, -7.4]])
#export_gauss(X.astype(object), unknowns = ['P1','P2','P3'], C=np.array([36, -12]))
    
  








