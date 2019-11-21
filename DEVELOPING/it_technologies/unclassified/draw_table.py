import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
from matplotlib.figure import Figure
#from math import pi, sin, cos
from matplotlib import rc
from time import time
import matplotlib
import pygame.midi
import numpy as np
"""
import tkMessageBox
import wave
import sounddevice as sd"""

def draw_cells(table_vals, bbox=None, font=None, color=None, facecolor='#2b2c2c',barcolor='k'):
    visibles=[]
    #path_data = [(Path.MOVETO, (bbox[0],bbox[1])), (Path.LINETO, (bbox[0],bbox[1]+bbox[3])), (Path.LINETO, (bbox[0]+bbox[2],bbox[1]+bbox[3])), (Path.LINETO, (bbox[0]+bbox[2],bbox[1])), (Path.CLOSEPOLY, (bbox[0],bbox[1]))]
    #codes, verts = zip(*path_data)
    #path = mpath.Path(verts, codes)
    #patch = mpatches.PathPatch(path, facecolor=facecolor, alpha=0.0)
    #visibles.append(patch)
    #ax.add_patch(patch)

    table_vals=[n for n in reversed(table_vals)]
    nrow, ncol=len(table_vals), len(table_vals[0])
    col_array=np.arange(ncol+1)
    row_array=np.arange(nrow+1)
    nx,ny,nwidth,nheight=0,0,nrow,ncol
    if bbox:
        col_array=bbox[0]+bbox[2]*1.*np.arange(ncol+1)/ncol
        row_array=bbox[1]+bbox[3]*1.*np.arange(nrow+1)/nrow
        nx,ny,nwidth,nheight=bbox[0],bbox[1],bbox[2],bbox[3]

    xcoords_of_linearray_v=np.tile(col_array,(2,1))
    ycoords_of_linearray_v=np.tile([ny,ny+nheight],(ncol+1,1)).T
    xcoords_of_linearray_h=np.tile([nx,nx+nwidth],(nrow+1,1)).T
    ycoords_of_linearray_h=np.tile(row_array,(2,1))
    #for x in plt.plot(np.tile(col_array,(2,1)),np.tile([ny,ny+nheight],(ncol+1,1)).T,barcolor): visibles.append(x)
    #for x in plt.plot(np.tile([nx,nx+nwidth],(nrow+1,1)).T, np.tile(row_array,(2,1)),barcolor): visibles.append(x)

    """startpoints_v=zip(xcoords_of_linearray_v[0], ycoords_of_linearray_v[0])
    endpoints_v=zip(xcoords_of_linearray_v[1], ycoords_of_linearray_v[1])
    patches=zip(startpoints_v, endpoints_v)
    for n in patches:
        print n
        line=mpatches.ConnectionPatch(n[0], n[1], 'data','data', fc="w")
        visibles.append(line)
        ax.add_patch(line)"""

    #print zip(np.tile([ny,ny+nheight],(ncol+1,1)).T,np.tile(row_array,(2,1)))

    def cartesian(x,y):
        return np.transpose([np.tile(x, len(y)), np.repeat(y, len(x))])

    cs=cartesian(col_array, row_array)
    cells={}
    for j in range(len(row_array)-1):
        for i in range(len(col_array)-1):
            tablecell=TableCell((cs[i+len(col_array)*j], cs[1+i+len(col_array)*j],cs[1+i+len(col_array)*(j+1)],cs[i+len(col_array)*(j+1)]), table_vals[j][i])
            cells.update({(j,i):tablecell})
            tablecell.add_cell(facecolor=facecolor, alpha=0.5)
            tablecell.add_text(ha='center',va='center',color=color, fontproperties=font)
    return cells

class TableCell():

    def __init__(self, coords, text):
        self.coords=coords
        (self.a,self.b,self.c,self.d)=self.coords
        self.text=text

    def add_cell(self, **kw):
        path_data = [(Path.MOVETO, self.a), (Path.LINETO, self.b), (Path.LINETO, self.c), (Path.LINETO, self.d), (Path.CLOSEPOLY, self.a)]
        codes, verts = zip(*path_data)
        path = mpath.Path(verts, codes)
        patch = mpatches.PathPatch(path, **kw)
        ax.add_patch(patch)
        self.active_patch=patch

    def add_text(self, **kw):
        self.active_text=plt.text((self.a[0]+self.c[0])/2.,(self.a[1]+self.c[1])/2.,self.text, **kw)

    def edit_text(self, text, **kw):
        self.text=text
        self.active_text.set_visible(False)
        self.active_text=plt.text((self.a[0]+self.c[0])/2.,(self.a[1]+self.c[1])/2.,self.text, **kw)

class Knobx(Figure):
    active=True
    mappings=[]
    mappings_register={}
    def __init__(self,*args,**kw):
        #super(Knobx, self).__init__(self, args, **kw)
        Figure.__init__(self,*args,**kw)

        pygame.midi.init()
        #list of all devices
        devices=[pygame.midi.get_device_info(device_id) for device_id in range(pygame.midi.get_count())]
        #indexes of all input devices
        devices=filter(lambda x: devices[x][2]==1, range(len(devices)))
        try:
            self.inp = pygame.midi.Input(devices[0])
        except IndexError:
            print('Controller is not plugged in')
            self.active=False

    def midiloop(self):
        while self.active:
            if self.inp.poll():
                MIDImessage=self.inp.read(1000)
                #print MIDImessage
                if MIDImessage[0][0][1] in self.mappings:
                    #self.event_generate("<<CC"+str(MIDImessage[0][0][1])+"_"+str(MIDImessage[0][0][2])+">>") #e.g. CC58_127
                    print('processed:', "<<CC"+str(MIDImessage[0][0][1])+"_"+str(MIDImessage[0][0][2])+">>""")
                    #t=time()
                    self.canvas.callbacks.process("<<CC"+str(MIDImessage[0][0][1])+"_"+str(MIDImessage[0][0][2])+">>", None)
                    #print 'took time:', time()-t

    def add_event(self, index, state, action):
        if index not in self.mappings:
            self.mappings.append(index)
            #self.mappings_register.update({str(index):tag})
        self.canvas.mpl_connect("<<CC"+str(index)+"_"+str(state)+">>", lambda event, index=index, state=state: action(event, index, state))
        #self.bind("<<CC"+str(index)+"_"+str(state)+">>", lambda event, index=index, state=state: action(event, index, state))

#fig = plt.figure(1, FigureClass=Knobx)
fig, (ax, ax2) = plt.subplots(nrows=2, ncols=1, FigureClass=Knobx, sharex=True)
plt.subplot(211)
#ax=fig.add_subplot(211)
#plt.subplot(211)
#plt.plot...,ro

ax.patch.set_facecolor('#131414')
#ax2.patch.set_facecolor('#131414')
Path = mpath.Path
font=FontProperties().copy()
font.set_family('sans-serif')
font.set_size(15)
font.set_weight('semibold')

def lookup(t):
    print(time()-t)
def tick(event, index, state):
    print(index, state)
last_state=64
def onclick(event, index, state):
    global x, row3, row4, plot, section, section_below, last_state
    if index==56:
        t=time()
        plt.subplot(211)
        k=2*(state/127.-0.5) #range between -1 and
        for n in row3:
            row3[n].active_patch.set_visible(False)
            row3[n].active_text.set_visible(False)
        row3=draw_cells(data_series,[0,2,10./2**k,1],font,'w','#2b2c2c','k')

        for n in appendents[last_state]:
            appendents[-1][n].active_patch.set_visible(False)
            appendents[-1][n].active_text.set_visible(False)
        for n in appendents[state]:
            appendents[-1][n].active_patch.set_visible(False)
            appendents[-1][n].active_text.set_visible(False)
        last_state=state
        col1[0,0].edit_text(D2(k,string), ha='center',va='center',color='w', fontproperties=font)
        col1[1,0].edit_text(D1(k,string), ha='center',va='center',color='w', fontproperties=font)
        plt.subplot(212, axisbg='#131414')
        plot.set_visible(False)
        set_of_points=x
        X=set_of_points/2**k
        Y=send(set_of_points)
        #Z=np.zeros(10)
        Z=map(lambda t:0,X)
        if section: section.set_visible(False)
        if section_below: section_below.set_visible(False)
        section=plt.fill_between(X,Y,Z, where=Y >= Z, facecolor='#00ffff')
        section_below=plt.fill_between(X, Y, Z, where=Y < Z, facecolor='#ff0000')
        plot,=plt.plot(X,Y, 'o', linestyle='-', color='#00ffff')
        plt.draw()
    elif index==21:
        if state==0: fig.active=False
        else: plt.close('all')

k=1.
"""string=r'$x^2$'
domain=np.arange(0,5,0.5)
def send(x): return np.round_(x*x,1)"""

"""string=r'$1/x$'
#domain=np.concatenate([np.arange(0,0.2,0.04),np.arange(0.05,1,0.05)])#advanced plot but false position
domain=np.arange(0,1,0.1)
def send(x): return np.round_(1./x,1)"""

string=r'$\sin(x)$'
domain=np.arange(0,2*np.pi,0.5)
def send(x): return np.round_(np.sin(x),1)

"""string=r'$10\sqrt{x}$'
#domain=np.arange(0,1,0.1)
#def send(x): return np.round_(x**0.5,1) #example of not precise rounding
domain=np.arange(0,3,0.3)
def send(x): return np.round_(10*x**0.5,2)"""

"""#THIS IS A ENXAMPLE FOR STUDENT WHEN PLOT IS BAD
string=r'$\frac{1}{\sin(x)}$'
#domain=np.arange(0,2*np.pi,0.5) #PLOT IS BAD
#domain=np.arange(0,2*np.pi,0.2) #PLOT IS LITTLE BETTER
domain=np.arange(0,3.2,0.1) #TOO MUCH OF POINTS
def send(x): return np.round_(1./np.sin(x),1)"""

#THERE IS A PART NEEDED FOR AUTOMATIC GENERATION OF EXPRESSION FORMS FOR TABLE
def D1(k, string, mode='exponential'): #return suitable expression forms for afectable row
    if mode=='exponential': k=str(round(2**k,2))
    returnable=r'$x \to '+str(k)+r'x$' +'\n' +string+r'$ \to $'
    for i in range(len(string)-1,-1,-1):
        if string[i]=='x': string=string[:i]+r'('+str(k)+r'x)'+string[i+1:]
    return returnable+string
def D2(k, string, mode='exponential'): #return suitable expression forms for afectable row
    if mode=='exponential': k=str(round(2**k,2))
    start=r'$f(x)='
    for i in range(len(string)-1,-1,-1):
        if string[i]=='x': string=string[:i]+r'('+str(k)+r'x)'+string[i+1:]
    return start+string[1:]
data_names=[[r'$x$'], [r'$f(x)='+string[1:]], [D1(k,string, mode='simple')],[D2(k,string, mode='simple')]]

data_series=[domain, map(lambda x: send(x), domain)]
data_boxes=[-4,4,4,1]

#data_names.append(r'$\sqrt{x}+\sqrt{'+str(y)+r'}+\sqrt{x-'+str(y)+r'}$')

appendents=[]
for state in range(128):
    k=2*(state/127.-0.5)
    appendents.append(draw_cells(data_series,[0,2,10./2**k,1],font,'w','#2b2c2c','k'))
    #print appendents[-1]
    for n in appendents[-1]:
        appendents[-1][n].active_patch.set_visible(False)
        appendents[-1][n].active_text.set_visible(False)
print('done')

plt.ylim(1, 5)
plt.xlim([-3,10])
mng = plt.get_current_fig_manager()
mng.window.state('zoomed')
plt.show()
col1=draw_cells(data_names,[-3,1,3,4],font,'w','#2b2c2c','k')
row2=draw_cells(data_series,[0,3,10,2],font,'w','#2b2c2c','k')
#global row3
row3=draw_cells(data_series,[0,2,10./2**k,1],font,'w','#2b2c2c','k')
for n in row3:
    row3[n].active_patch.set_visible(False)
    row3[n].active_text.set_visible(False)
#row4=draw_cells(data_series,[0,0,10./2**k,1],font,'w','#2b2c2c','k')
#ROW3=[row3]
#plt.draw()

"""
#testing keyboard
def press(event):
    state=[str(n) for n in range(10)].index(event.key)*14
    print 'processed', "<<CC56_"+str(state)+">>"
    fig.canvas.callbacks.process("<<CC56_"+str(state)+">>",None)

for n in range(10):
    state=str([0, 14, 28, 42, 56, 70, 84, 98, 112, 126][n])
    fig.canvas.mpl_connect('key_press_event', press)"""

for i in range(128): fig.add_event(56,i,onclick)
for i in [0,127]: fig.add_event(21,i,onclick)
#for i in range(128): fig.add_event(56,i,tick)
#ax2=fig.add_subplot(111)

plt.subplot(212, axisbg='#131414')
x=domain #responsible for x domain in below graph
plt.xlim([min(x)-(max(x)+(x[-1]-x[-2])-min(x))*3./10.,max(x)+(x[-1]-x[-2])])
#first coord is a position of left coord of below table; then graph is being plotted after zero; (x[-1]-x[-2]) is step of arange
y=send(x)
z=map(lambda t:0, x) #some kind of consistence with x
plot,=plt.plot(x, y, 'o', linestyle='-', color='#00ffff')
plt.fill_between(x, y, z, where=y >= z, facecolor='#131f1f')
plt.fill_between(x, y, z, where=y < z, facecolor='#1f1313')
section=None
section_below=None
plt.draw()
#elements={}
fig.midiloop()