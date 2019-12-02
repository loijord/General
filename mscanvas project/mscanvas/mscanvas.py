#PLEASE SET Python Engine OPTION TO Remote!
'''Once we've defined what MsCanvas is, we need to identify in mathematical way,
where will startpoint and endpoint of segment between two mscanvases be located.
Let's write a function named find_connect_bb to find these locations'''
#hexcode:
#print '#'+''.join([['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'][k] for k in [18/16, 18%16, 33/16, 33%16, 8/16, 8%16]])
from Tkinter import*
from subprocess import call
from random import randint
from PIL import Image, ImageTk, ImageColor
from types import*
from time import*
from re import finditer
import tkMessageBox
import tkFileDialog
root = Tk()
SAMPLES=[]
# this file demonstrates the movement of a single canvas item under mouse control

class SCanvas(Canvas, object):
    '''
    Implementation of de button equivalent via Canvas
    It can create text, image and rectangle and use options of any of them.
    Options: the same as create_text, create_rectangle except {fill} + {command(buggy) + bg, fg, image}
    Author: Night Simon
    Date: 07.16.2017
    '''
    numOfButtons = 0
    rectangle_fill, text_fill = '', 'black'
    image=''

    def __init__(self, root, *args, **kwargs):
        Canvas.__init__(self, root, *args, **kwargs)

    def click(self,event,Id,config):
        '''only ids but not tags!old version of itemconfig'''
        super(SCanvas,self).itemconfig(Id, config)

    def find_withbuttontag(self,tag):
        #X in button family or X='buttonX' |-> 3 numbers that represents button family
        #print 'find_withbuttontag of tag =',tag,'which has',type(tag)
        if type(tag) is str and 'button' in tag:
            return self.find_withtag(tag) #case1: input is buttonX
        else:
            button_tags=self.gettags(tag) #case2: input is a number
            if 'button' in button_tags: return self.find_withtag(button_tags[0])#case2_1: input is a number of buttonFamily
            else: raise TclError('tag = '+str(tag)+' is not a button') #case2_2: input is not a number of buttonFamily

    def type(self,tag):
        #if X is in buttonFamily or X=='buttonX', return 'button'
        #print 'type of tag =', tag, 'which has',type(tag)
        if type(tag) is str: #case1: input is buttonX or edgeX
            if 'button' in tag: return 'button'
            elif 'edge' in tag: return 'edge'
        else: #case2: input is a number
            tags=self.gettags(tag)
            if 'button' in tags: return 'button' #case2_1: input is a number of buttonFamily or edge
            elif 'edge' in tags: return 'edge'
            else: return super(SCanvas,self).type(tag)
            #raise TypeError('scanvas.type of tag =',tag,' is unidentified') #case2_2: input is not a number of buttonFamily

    def mixcolor(self, string_obj):
        """Internal function that converts '.tex-color' to hex-color"""
        #print 'args of self.mixcolor:', string_obj
        color_array=string_obj.split('!')
        if len(color_array) == 1:
            c=ImageColor.getrgb(color_array[0])
            #print 'result of self.mix_color(',string_obj,'):', '#%02x%02x%02x' % tuple([int(c[i]) for i in [0,1,2]])
            return '#%02x%02x%02x' % tuple([int(c[i]) for i in [0,1,2]])
        elif len(color_array) == 2: color_array.append('white')
        c1=ImageColor.getrgb(color_array[0])
        c2=ImageColor.getrgb(color_array[2])

        m1=int(color_array[1])/100.
        m2=1-m1
        #print 'result of self.mix_color(',string_obj,'):','#%02x%02x%02x' % tuple([int(m1*c1[i]+m2*c2[i]) for i in [0,1,2]])
        return '#%02x%02x%02x' % tuple([int(m1*c1[i]+m2*c2[i]) for i in [0,1,2]])

    def replace_color(self, img, color):
        """Internal function that converts black&white PIL.Image to PIL.Image with white pixels replaced with given color;
        color type is stringType (.tex-color, hex-color or named-color)"""
        image=img.copy()
        pixels=image.load()
        #pixals=pixels[for x in range(img.size[0])
        c=self.getrgb(color)
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                px = (pixels[x,y][0]+pixels[x,y][1]+pixels[x,y][2])/3
                pixels[x,y] = (int(px*c[0]/255.), int(px*c[1]/255.), int(px*c[2]/255.))
        img.save('watchout.png')
        return image

    def getrgb(self, string_obj):
        """Internal function that converts hex-color to rgb-tuple"""
        #print 'args of self.getrgb:', string_obj
        It=[['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'].index(n) for n in string_obj[1:]]
        #print 'result of self.getrgb(',string_obj,'):',(It[0]*16+It[1], It[2]*16+It[3], It[4]*16+It[5])
        return (It[0]*16+It[1], It[2]*16+It[3], It[4]*16+It[5])

    def itemconfig(self, tag, **kwargs):
        #overriding itemconfig to accept tags such as 'buttonX', X in button family or 'edgeX'
        #text ['justify', 'text', 'font', 'underline', 'anchor']
        #rectangle ['disabledoutlinestipple', 'dash', 'disabledwidth', 'activeoutlinestipple', 'dashoffset', 'activewidth', 'disabledoutline', 'disableddash', 'outlinestipple', 'activedash', 'activeoutline', 'outlineoffset', 'outline']
        #image ['image', 'disabledimage', 'anchor', 'activeimage']
        if self.type(tag)=='button':
            tags_of_button=self.find_withbuttontag(tag)
            if kwargs:
                for n in kwargs.keys():
                    #----------------------------------------------------------------------------------------------------------------------
                    if n=='fill': raise TclError('fill can be whether text or rectangle fill; use bg for background and fg for textcolor')
                    elif n=='bg': #allowed in mscanvas class only; used in mscanvas.create_button only
                        if super(SCanvas,self).type(tags_of_button[1])=='image':
                            buttonX=self.gettags(tags_of_button[1])[0]
                            super(SCanvas,self).itemconfig(tags_of_button[0], fill=self.register[buttonX].color)
                            for it in tags_of_button:
                                self.tag_bind(it,"<Enter>", lambda event, tag=tags_of_button[1], config={'image':self.register[buttonX].photo_active}: self.click(event,tag,config))
                                self.tag_bind(it,"<Leave>", lambda event, tag=tags_of_button[1], config={'image':self.register[buttonX].photo}: self.click(event,tag,config))
                            #super(SCanvas,self).itemconfig(tags_of_button[0], fill=self.mixcolor(kwargs['bg']+'!60'))
                            #self.tag_bind(it,"<Enter>", lambda event, tag=tags_of_button[0], config={'fill':self.mixcolor(kwargs['bg'])}: self.click(event,tag,config))
                        else:
                            print 'other case'
                    elif n=='fg':
                        super(SCanvas,self).itemconfig(tags_of_button[1], fill=self.mixcolor(kwargs['fg']))
                    #----------------------------------------------------------------------------------------------------------------------
                    elif n=='width': raise TclError('width can be whether text or rectangle fill; use textwidth or borderwidth')
                    elif n=='textwidth': super(SCanvas,self).itemconfig(tags_of_button[1], width=kwargs['textwidth'])
                    elif n=='borderwidth': super(SCanvas,self).itemconfig(tags_of_button[0], width=kwargs['borderwidth'])
                    #----------------------------------------------------------------------------------------------------------------------
                    elif n=='image':
                        if super(SCanvas,self).type(tags_of_button[1]) <> 'image':
                            print 'fixing the subtype:', super(SCanvas,self).type(tags_of_button[1])
                            print 'getting coords:', self.coords(tags_of_button[1])
                            coords_of_image=self.coords(tags_of_button[1])
                            self.delete(tags_of_button[1])
                            print 'deleting subtype'
                            tags_of_button[0] = self.create_image(*coords_of_image, image=kwargs['image'])
                            print 'placed a new image at', coords_of_image
                            self.coords(tags_of_button[0], self.bbox(tags_of_button[0]))
                            print 'creating a bounding box at', self.bbox(tags_of_button[0])
                        else:
                            super(SCanvas,self).itemconfig(tags_of_button[1],{'image':kwargs['image']})
                            self.coords(tags_of_button[0], self.bbox(tags_of_button[1]))
                            #print 'rebox', self.bbox(tags_of_button[1])
                    elif n in super(SCanvas,self).itemconfig(tags_of_button[0]).keys(): super(SCanvas,self).itemconfig(tags_of_button[0],{n:kwargs[n]})
                    elif n in super(SCanvas,self).itemconfig(tags_of_button[1]).keys(): super(SCanvas,self).itemconfig(tags_of_button[1],{n:kwargs[n]})
                    #elif n in super(SCanvas,self).itemconfig(tags_of_button[2]).keys(): super(SCanvas,self).itemconfig(tags_of_button[2],{n:kwargs[n]})
                    elif n in ['disabledstipple', 'stipple', 'active_stiple', 'activefill', 'disabledfill', 'offset', 'width', 'tags', 'state']:
                        raise TclError(n+' is ill-defined argument')
                    else: raise TclError('unrecognised argument', n, 'in itemconfig')
            else:
                cnf=super(SCanvas,self).itemconfig(tags_of_button[0])
                cnf.update(super(SCanvas,self).itemconfig(tags_of_button[1]))
                cnf.update(super(SCanvas,self).itemconfig(tags_of_button[2]))
                return cnf

        else: return super(SCanvas,self).itemconfig(tag, **kwargs)

    '''def bbox(self, tag):
        """Internal"""
        bb=super(SCanvas,self).bbox(tag)
        print bb
        return (bb[0]-2, bb[1]-2, bb[2]+2, bb[3]+2)'''

    def create_button(self,*args,**kwargs):
        self.numOfButtons+=1
        sticker="button"+str(self.numOfButtons)
        #['disabledstipple', 'stipple', 'active_stiple', 'activefill', 'disabledfill', 'offset'] are both ill-defined arguments of create_text and create_rectangle
        #'tags', 'state' is an argument for all of them
        subtype=''
        for n in kwargs.keys():
            if n in ['justify', 'text', 'font', 'underline', 'anchor']:
                if subtype=='':
                    tag1=self.create_text(args)
                    subtype='text'
                super(SCanvas,self).itemconfig(tag1,{n:kwargs[n]})
                kwargs.pop(n)
            if n in ['image', 'disabledimage', 'anchor', 'activeimage']:
                if subtype=='text': raise TclError('can''t identify subtype: there are arguments of both subtypes')
                else:
                    if subtype=='':
                        tag1=self.create_image(args)
                        subtype='image'
                    super(SCanvas,self).itemconfig(tag1,{n:kwargs[n]})
                    kwargs.pop(n)
        if subtype=='': raise TclError('no subtype identified')
        tag2=self.create_rectangle(self.bbox(tag1))
        #print tag2, 'is created at', self.bbox(tag1), 'of type', subtype
        self.tag_lower(tag2, tag1)
        #adding tag 'buttonX' to all of the 3 items
        for it in [tag1, tag2]:
            super(SCanvas, self).itemconfig(it, {'tags':sticker})
            self.addtag_withtag("button", sticker)
        if kwargs<>{}: self.itemconfig('button'+str(self.numOfButtons), **kwargs)
        #if 'bg' not in kwargs: kwargs.update({'bg':self.rectangle_fill})
        return sticker

class script():
    def __init__(self):
        self.formulas={}
        self.commands=[]
        self.coordinates={}

class MsCanvas(SCanvas, object):
    '''
    Taken from google search of "canvas-moving-w-mouse.py"
    Extension of de scanvas with ability to move
    It can create text, image and rectangle and use options of any of them.
    Options of scanvas: the same as create_text, create_rectangle except {fill} + {command(buggy), bg, fg, image}
    Additional options: motion
    Author: Night Simon
    Date: 07.19.2017
    '''
    register={} #a dictionary of all clickables whose values are corresponding objects of button or edge class
    clickables={}
    templink=False
    numOfEdges=0
    numOfPolygons=0
    button_color='orange'
    edge_color='lightblue'
    select_color='blue'
    SCRIPT=script()

    def save(self):
        code=''
        for i in range(len(self.SCRIPT.commands)):
            n = self.SCRIPT.commands[i]
            if n[0:6]=='button':
                if self.SCRIPT.commands[i:].count(n)<=1:
                    #not including if there goes at least one more buttonX after buttonX; this means self.SCRIPT.formulas[buttonX] will be edited later
                    code+=self.SCRIPT.formulas[n]+'\n'
                    buttontags=self.find_withtag(n)
                    for i in range(len(buttontags)):
                        code+='self.coords('+"self.find_withtag('"+n+"')["+str(i)+'], '+str(tuple(self.coords(buttontags[i])))+');\n'
            else: code+=n+';\n'
            code+='\n'
        return code

    def print_clickables(self, event, tag): print 'CLICKABLES:', mscanvas.clickables
    def print_register(self, event, tag): print 'REGISTER:', mscanvas.register

    def button_menu_delete(self, buttonX=''):
        #edgeX should be not number, Ill correct later
        if not(buttonX): buttonX=self.gettags(self.find_withtag('popup')[0])[0]
        self.erase_button(True, buttonX)
        #self.SCRIPT.commands.append("self.button_menu_mathinput('"+' '+"')")
        self.SCRIPT.commands.append("self.button_menu_delete('"+buttonX+"')")
        self.dtag('popup')

    def edge_menu_delete(self, edgeX=''):
        #edgeX should be not number, Ill correct later
        if not(edgeX): edgeX=self.gettags(self.find_withtag('popup')[0])[0]
        self.erase_edge(True, edgeX)
        self.SCRIPT.commands.append("self.edge_menu_delete('"+edgeX+"')")
        self.dtag('popup')

    def polygon_menu_delete(self, polygonX=''):
        #polygonX shoud be not number, Ill correct later
        if not(polygonX): polygonX=self.gettags(self.find_withtag('popup')[0])[0]
        self.delete(True, polygonX)
        self.SCRIPT.commands.append("self.polygon_menu_delete('"+polygonX+"')")
        self.dtag('popup')

    def button_menu_color(self, buttonX=None):
        if not(buttonX): buttonX=self.gettags(self.find_withtag('popup')[0])[0]
        self.register[buttonX].color=self.button_color
        self.register[buttonX].photo_active = ImageTk.PhotoImage(self.replace_color(self.register[buttonX].image_snap, self.mixcolor(self.button_color)))
        self.register[buttonX].photo = ImageTk.PhotoImage(self.replace_color(self.register[buttonX].image_snap, self.mixcolor(self.button_color+'!60')))
        self.itemconfig(buttonX, bg='its important to stay awake', outline=self.button_color, image=self.register[buttonX].photo)
        self.dtag('popup')
        self.SCRIPT.commands.append("self.button_menu_color('"+buttonX+"')")

    def edge_menu_color(self, edgeX=None):
        if not(edgeX): edgeX=self.gettags(self.find_withtag('popup')[0])[0]
        self.register[edgeX].color=self.edge_color
        self.itemconfig(edgeX, fill=self.edge_color)
        self.dtag('popup')
        self.SCRIPT.commands.append("self.edge_menu_color('"+edgeX+"')")

    def button_menu_open(self):
        if self.find_withtag('popup'):
            buttonX=self.gettags(self.find_withtag('popup')[0])[0]
            link = 'C:\Users\Vartotojas\Desktop\mscanvas\\'+self.register[buttonX].link
        else:
            link = tkFileDialog.askopenfilename()
        #if 'link' in self.register[buttonX].__dict__.keys(): print 'assume I opened', self.register[buttonX].link
        if '.tex' in link:
            if self.SCRIPT.commands==[]: response = False
            else: response = tkMessageBox.askyesnocancel("Save?", "Do you want to save your progress?")
            if response==None: pass
            else:
                if response:
                    f=tkFileDialog.asksaveasfile(mode='w', defaultextension=".tex")
                    f.write(self.save())
                    f.close()
                SAMPLES.append(self.save())
                print 'running a routine from',link,':'
                self = MsCanvas(root, width="14i", height="6i", bg='#122108')
                self.place(x = 0, y = 0, width=1400, height=850)
                script=open(link, "r").read()
                exec(script)
        else:
            print 'opening a file from',link,':'
            not(call([link], shell=True))
        self.dtag('popup')

    def button_menu_mathinput(self, formula=''):
        dont_tex, save_tex= False, False
        if not(formula): formula=self.mathinput.get("1.0",'end-1c').encode('utf-8')
        else: #we are sure script is being run; everytime we run script, we must check if this formula has image and include if not
            #print 'WOUP', formula, 'in', self.archived.keys(),':',formula in self.archived.keys()
            if formula not in self.archived.keys():
                save_tex=True
            else: dont_tex=True
        print '-'*100
        link=''
        self.templink=False
        self.temporary_formula=formula
        #capturing commands used and formula

        parameters_count = {'default': [0], 'huge': [0], 'file': [1], 'image': [2]}
        options={}
        if '|' in formula:
            splitted=[m.start() for m in finditer('--', formula[:formula.index('|')])]+[formula.index('|')]
            parameters = []
            for i in range(len(splitted)-1):
                n = splitted[i] #index of a current '--'
                m = splitted[i+1] #index of next '--'
                #constructing an array which consists of a command and its arguments
                assignment = filter(lambda x: x<>'', formula[n+2:m].split(' '))
                if len(assignment)==0: raise IndexError('-- appeared with no keyword')
                if assignment[0] in parameters_count.keys():
                    if len(assignment)-1 not in parameters_count[assignment[0]]:
                        raise IndexError('Expected '+' or '.join([str(x) for x in parameters_count[assignment[0]]])+' parameters of '+assignment[0]+', got '+str(len(assignment)-1))
                else:
                    raise KeyError('No option named '+assignment[0])
                options.update({assignment[0]:assignment[1:]})
            formula=formula[splitted[-1]+1:]
            print 'initial formula =', formula
            #put options that should be applied when '|' apears
            if 'file' in options.keys():
                link=options['file'][0]
                self.templink=True

        #put options that are applied always except the cases they appear
        if 'default' not in options.keys(): #if not default, we allow use of enters
            formula=formula.split('\n')
            if len(formula)<2: formula=r"$\text{"+formula[0]+"}$"
            else: formula=r"$\begin{array}{l}"+r"\\".join([r"\text{"+n+"}" for n in formula])+r"\end{array}$"
        if 'image' in options.keys():
            imagefile = options['image'][0]
            w,h = Image.open(imagefile).size
            newcommand = options['image'][1]
            definition = unicode(r"\newcommand{"+'\\'+newcommand+r"}[1]{\includegraphics[width=#1\textwidth,natwidth="+\
            str(w)+r",natheight="+str(h)+r"]{c:/Users/Vartotojas/Desktop/mscanvas/"+imagefile+r"}}")
            formula=definition+'\n'+formula
        if 'huge' in options.keys(): formula = r"\Huge "+formula

        print 'final formula:', formula
        print 'external commands:', options

        #creating a file named temptex.tex and assigning 'is compiling successful' to 'successful'
        successful=True
        if not(dont_tex):
            TEX = (
              unicode("\documentclass{article}"),
              unicode("\usepackage[utf8]{inputenc}"),
              unicode("\usepackage[L7x]{fontenc}"),
              unicode("\usepackage[lithuanian]{babel}"),
              unicode("\usepackage{lmodern}"),
              unicode("\usepackage{amsmath}"),
              unicode("\usepackage{amsthm}"),
              unicode("\usepackage{amssymb}"),
              unicode("\usepackage{bm}"),
              unicode("\usepackage{xcolor}"),
              unicode("\usepackage{graphicx}"),
              unicode("\usepackage{tikz}"),
              #unicode("\usepackage{main}"),
              unicode("\usepackage[active,displaymath,textmath,tightpage]{preview}"),
              unicode("\pagestyle{empty}"),
              unicode(r"\newcommand{\cc}[2]{\begin{cases}#1 \\ #2\end{cases}}"),
              unicode(r"\newcommand{\ccc}[3]{\begin{cases}#1 \\ #2 \\ #3\end{cases}}"),
              unicode(r"\newcommand{\cccc}[4]{\begin{cases}#1 \\ #2 \\ #3 \\ #4\end{cases}}"),
              unicode(r"\newcommand{\ccccc}[5]{\begin{cases}#1 \\ #2 \\ #3 \\ #4 \\ #5\end{cases}}"),
              unicode(r"\newcommand{\cccccc}[6]{\begin{cases}#1 \\ #2 \\ #3 \\ #4 \\ #5 \\ #6\end{cases}}"),
              unicode(r"\newcommand{\CC}[2]{\begin{cases}\text{#1} \\ \text{#2}\end{cases}}"),
              unicode(r"\newcommand{\CCC}[3]{\begin{cases}\text{#1} \\ \text{#2} \\ \text{#3}\end{cases}}"),
              unicode(r"\newcommand{\CCCC}[4]{\begin{cases}\text{#1} \\ \text{#2} \\ \text{#3} \\ \text{#4}\end{cases}}"),
              unicode(r"\newcommand{\CCCCC}[5]{\begin{cases}\text{#1} \\ \text{#2} \\ \text{#3} \\ \text{#4} \\ \text{#5}\end{cases}}"),
              unicode(r"\newcommand{\CCCCCC}[6]{\begin{cases}\text{#1} \\ \text{#2} \\ \text{#3} \\ \text{#4} \\ \text{#5} \\ \text{#6} \end{cases}}"),
              unicode(r"\newcommand{\R}{\mathbb{R}}"),
              unicode(r"\newcommand{\N}{\mathbb{N}}"),
              unicode(r"\newcommand{\Z}{\mathbb{Z}}"),
              r"\begin{document}",
              formula,
              r"\end{document}")
            with open(r"C:\Users\Vartotojas\Desktop\EnolaProject\Matematikos idejos\Visual Tools\mscanvas\mscanvas project\temptex.tex",'w') as out_snap:
                for T in TEX: out_snap.write("%s\n" % T)
            #print 'AFTER writing a file:', time()-t
            print 'temp file compiled succesfully:',
            successful=not(call(['latex','--interaction', 'nonstopmode', r"C:\Users\Vartotojas\Desktop\EnolaProject\Matematikos idejos\Visual Tools\mscanvas\mscanvas project\temptex.tex"]))
            print successful

        if successful:
            if not(dont_tex):
                print '.dvi converted to .png succesfully:', not(call(['dvipng','--interaction', 'nonstopmode', 'temptex.dvi','-o',r"C:\Users\Vartotojas\Desktop\EnolaProject\Matematikos idejos\Visual Tools\mscanvas\mscanvas project\temptex.png"]))
                self.temporary_image = Image.open(r"C:\Users\Vartotojas\Desktop\EnolaProject\Matematikos idejos\Visual Tools\mscanvas\mscanvas project\temptex.png")
            else:
                print 'took this from archive:', self.temporary_formula
                self.temporary_image = Image.open('memory'+r"/"+self.archived[self.temporary_formula])
            if save_tex:
                f=open(r"memory\archived.tex","a")
                f.write('@\n')
                currentfile='f'+str(int(self.lastfile[1:self.lastfile.index('.')])+1)+'.png'
                f.write(self.temporary_formula+'::'+currentfile)
                f.close()
                print 'saving formula to', currentfile
                self.temporary_image.save('memory'+r"/"+currentfile)
                self.lastfile=currentfile
            #latex --interaction nonstopmode C:\Users\Vartotojas\Desktop\mintedex.tex
            #dvipng --interaction nonstopmode mintedex.dvi -o C:\Users\Vartotojas\Desktop\mintedex.png
            self.temporary_photo=ImageTk.PhotoImage(self.temporary_image)
            popupids=self.find_withtag('popup')
            if popupids:
                buttonX=self.gettags(popupids[0])[0]

                self.register[buttonX].formula=formula
                self.update_formula(buttonX)
                self.itemconfig(buttonX, bg='its important to stay awake')
                self.dtag('popup')
            else:
                x,y=randint(400, 700-1), randint(100, 400-1)
                print 'line 438:','x=',x,'y=',y, 'image_photo=', self.temporary_photo,'image=', self.temporary_image
                buttonX=self.create_button(x,y, borderwidth=5, image = self.temporary_photo)

            if link: self.register[buttonX].link=link #adding linked content
            elif 'link' in self.register[buttonX].__dict__.keys(): del self.register[buttonX].link
            self.templink=False
            self.itemconfig(buttonX, outline=self.button_color, image = self.register[buttonX].photo)
            print 'temp file removed succesfully:', not(call(['del','--interaction', 'nonstopmode', r"C:\Users\Vartotojas\Desktop\EnolaProject\Matematikos idejos\Visual Tools\mscanvas\mscanvas project\temptex.png"], shell=True))
            self.temporary_formula="+'\\n'+".join(['r"'+n+'"' for n in self.temporary_formula.split('\n')])
            self.SCRIPT.formulas.update({buttonX:'self.button_menu_mathinput(formula='+self.temporary_formula+')'})
            self.SCRIPT.commands.append(buttonX)
        else: raise TclError("formula processing didn't succeed")
        print '-'*100

    def button_menu_scriptinput(self):
        script=self.scriptinput.get("1.0",'end-1c').encode('utf-8')
        exec(script)

    def main_menu_paint(self, event):
        a=3
        if not(self.find_withtag(CURRENT)):
            self.create_oval(event.x-a, event.y-a, event.x+a, event.y+a, fill="blue", tags='trace')
    def main_menu_painton(self):
        self.bind("<Button-1>", lambda event: self.main_menu_paint(event))
        self.main_menu.add_command(label='end paint', command = self.main_menu_paintoff)
        while True:
            try: self.main_menu.delete('begin paint')
            except TclError: break
    def main_menu_paintoff(self, points=[]):
        if not(points):
            points=[self.coords(n) for n in self.find_withtag('trace')]
            points=[((n[0]+n[2])/2, (n[1]+n[3])/2) for n in points]
        self.numOfPolygons+=1
        sticker="polygon"+str(self.numOfPolygons)
        shape=self.create_polygon(points, fill=self.button_color, tags=sticker)
        self.addtag_withtag("polygon", sticker)
        self.tag_bind(shape,"<Button-3>",lambda event, i=shape: self.popup(event,i))
        self.tag_lower(shape)
        for n in self.find_withtag('trace'): self.delete(n)
        try: self.main_menu.delete('end paint')
        except TclError: pass
        self.unbind("<Button-1>")
        self.main_menu.add_command(label='begin paint', command = self.main_menu_painton)
        self.SCRIPT.commands.append("self.main_menu_paintoff("+str(points)+")")
    def polygon_menu_color(self, polygonX=''):
        if not(polygonX): polygonX=self.gettags(self.find_withtag('popup')[0])[0]
        self.itemconfig(polygonX, fill=self.button_color)
        self.dtag('popup')
        self.SCRIPT.commands.append("self.polygon_menu_color('"+polygonX+"')")

    def delete_window_callback(self):
        response=tkMessageBox.askyesnocancel("Quit", "Do you want to save your progress?")
        if response:
            f=tkFileDialog.asksaveasfile(mode='w', defaultextension=".tex")
            f.write(self.save())
            f.close()
            root.destroy()
        elif response==False:
            root.destroy()
        else: pass

    def display_code(self):
        self.codeoutput.delete('1.0', END)
        self.codeoutput.insert(INSERT, self.save())

    def __init__(self, root, **kwargs):
        SCanvas.__init__(self, root, kwargs)
        self.archived=[n.split('::') for n in open('memory/archived.tex','r').read().split('@\n')]
        print self.archived
        self.lastfile=self.archived[-1][-1]
        self.archived=dict(self.archived)
        print 'PREPARING ARCHIVE...'
        print self.archived.keys()
        root.geometry('{}x{}'.format(1300, 850))

        root.protocol("WM_DELETE_WINDOW", self.delete_window_callback)
        #self.bind("<Button-1>", lambda event: self.info(event))
        #self.bind("<Double-Button-1>", lambda event: self.info_detailed(event))
        #self.bind("<B1-ButtonRelease>", lambda event: self.record(event)) #self.mouseDown is inside!
        self.bind("<Button-3>", lambda event: self.popup_main(event))
        self.paint_active=False

        #rightclicks of main
        self.main_menu=Menu(self, tearoff=0)
        self.main_menu.add_command(label='begin paint', command = self.main_menu_painton)

        #rightclicks of buttons
        self.button_menu=Menu(self, tearoff=0)
        self.button_menu.add_command(label='delete button', command = self.button_menu_delete)
        self.button_menu.add_command(label='change color', command = self.button_menu_color)
        self.button_menu.add_command(label='edit formula', command = self.button_menu_mathinput)

        #rightclicks of edges
        self.edge_menu=Menu(self, tearoff=0)
        self.edge_menu.add_command(label='delete edge', command = self.edge_menu_delete)
        self.edge_menu.add_command(label='change color', command = self.edge_menu_color)

        #rightclicks if polygons
        self.polygon_menu=Menu(self, tearoff=0)
        self.polygon_menu.add_command(label='change color', command = self.polygon_menu_color)
        self.polygon_menu.add_command(label='delete', command = self.polygon_menu_delete)
        '''
        recttag=self.create_rectangle(0, 0, 40, 40, fill='yellow')
        self.tag_bind(recttag,"<Button-1>", lambda event, i=recttag: CLICK2(event, i))

        clickables=self.create_text(70, 20, text='clickables')
        box=self.create_rectangle(self.bbox(clickables), fill="orange", tags='info')
        self.tag_lower(box, clickables)
        self.tag_bind(clickables,"<Button-1>", lambda event, i = clickables: self.print_clickables(event, i))

        register=self.create_text(132, 20, text='register')
        box=self.create_rectangle(self.bbox(register), fill="orange", tags='info')
        self.tag_lower(box, register)
        self.tag_bind(register,"<Button-1>", lambda event, i=register: self.print_register(event, i))'''

        #creating the palette for button color; each item has tags: colorname, 'buttoncolorselect' and 'activebuttoncolor' (for a color assigned to self.button_color)
        buttoncolor = self.create_text(100, 15, text = r"Button/polygon", font = "Helvetica 14 bold")
        bounding_box=self.bbox(buttoncolor)
        self.coords(buttoncolor, 5+(bounding_box[2]-bounding_box[0])/2., 15)
        box=self.create_rectangle(self.bbox(buttoncolor), fill="yellow", tags='info')
        self.tag_lower(box, buttoncolor)
        fill=['sienna','firebrick','maroon','purple','magenta','pink','red','orange','yellow','green','darkgreen','darkblue','blue','lightblue', 'grey']+['pink']*18
        for i in range(len(fill)):
            color=self.create_rectangle(160+20*i, 5, 160+20*(i+1), 25, fill=fill[i])
            colorcode=self.itemconfig(color)['fill'][-1]
            self.addtag_withtag(colorcode, color)
            self.addtag_withtag('buttoncolorselect', color)
            self.tag_bind(color, "<Button-1>", lambda event, i=color: self.set_buttoncolor(event, i))
            self.itemconfig(color, outline='white')

        #creating the palette for edge color; each item has tags: colorname, 'edgecolorselect' and 'activeedgecolor' (for a color assigned to self.edge_color)
        edgecolor = self.create_text(100, 35, text = r"Edge", font = "Helvetica 14 bold")
        bounding_box=self.bbox(edgecolor)
        self.coords(edgecolor, 5+(bounding_box[2]-bounding_box[0])/2., 35)
        box=self.create_rectangle(self.bbox(edgecolor), fill="yellow", tags='info')
        self.tag_lower(box, edgecolor)
        fill=['sienna','firebrick','maroon','purple','magenta','pink','red','orange','yellow','green','darkgreen','darkblue','blue','lightblue', 'grey']+['pink']*18
        for i in range(len(fill)):
            color=self.create_rectangle(160+20*i, 25, 160+20*(i+1), 45, fill=fill[i])
            colorcode=self.itemconfig(color)['fill'][-1]
            self.addtag_withtag(colorcode, color)
            self.addtag_withtag('edgecolorselect', color)
            self.tag_bind(color, "<Button-1>", lambda event, i=color: self.set_edgecolor(event, i))
            self.itemconfig(color, outline='white')

        #configuring initial color selections
        activebuttoncolorid=tuple(set(self.find_withtag('buttoncolorselect'))&set(self.find_withtag(self.button_color)))[0]
        activeedgecolorid=tuple(set(self.find_withtag('edgecolorselect'))&set(self.find_withtag(self.edge_color)))[0]
        self.addtag_withtag('activebuttoncolor', activebuttoncolorid)
        self.addtag_withtag('activeedgecolor', activeedgecolorid)
        self.itemconfig(activebuttoncolorid, outline=self.select_color, width=3)
        self.itemconfig(activeedgecolorid, outline=self.select_color, width=3)
        self.tag_raise('activeedgecolor')
        self.tag_raise('activebuttoncolor')

        #creating mathinput entry
        Button(root, text='formula', bg='#00ff00', command=lambda: self.button_menu_mathinput()).place(x=460, y=630, width=80, height=20)
        self.mathinput=Text(root)
        self.mathinput.place(x=0, y=650, width=1000, height=200)

        #creating scriptinput entry
        Button(root, text='external run', bg='#00ff00', command=lambda: self.button_menu_scriptinput()).place(x=1060, y=630, width=80, height=20)
        self.scriptinput=Text(root)
        self.scriptinput.place(x=1000, y=650, width=200, height=200)

        #creating showcode entry
        Button(root, text='Display code', bg='#00ff00', command=lambda: self.display_code()).place(x=1030, y=50, width=80, height=30)
        self.codeoutput=Text(root, font="Helvetica 6 bold")
        self.codeoutput.place(x=920, y=70, width=360, height=550)
        #BACK
        Button(root, text='BACK', bg='#00ffff', command=lambda: self.back()).place(x=840, y=10, width=80, height=30)
        #NEW
        Button(root, text='NEW', bg='#ffff00', command=lambda: self.new()).place(x=920, y=10, width=80, height=30)
        #OPEN
        Button(root, text='OPEN', bg='#ff00ff', command=lambda: self.button_menu_open()).place(x=1000, y=10, width=80, height=30)

    def set_buttoncolor(self, event, tag):
        """pick a color in a palette provided its id or first tag (colorname)"""
        if type(tag) is StringType: #if it is not id (but tag consistent of colorname), change to id
            tag=tuple(set(self.find_withtag('buttoncolorselect'))&set(self.find_withtag(tag)))[0]
        for n in self.find_withtag('activebuttoncolor'):
            self.itemconfig(n, outline='white', width=1)
        self.dtag('activebuttoncolor')
        self.addtag_withtag('activebuttoncolor', tag)
        self.itemconfig(tag, outline=self.select_color, width=3)
        self.tag_raise('activeedgecolor')
        self.tag_raise('activebuttoncolor')
        #tag consistent of colorname is needed here
        tag=self.gettags(tag)[0]
        self.SCRIPT.commands.append("self.set_buttoncolor(True, '"+tag+"')")
        self.button_color=tag

    def set_edgecolor(self, event, tag):
        """pick a color in a palette provided its id or first tag (colorname)"""
        if type(tag) is StringType: #if it is not id (but tag consistent of colorname), change to id
            tag=tuple(set(self.find_withtag('edgecolorselect'))&set(self.find_withtag(tag)))[0]
        for n in self.find_withtag('activeedgecolor'):
            self.itemconfig(n, outline='white', width=1)
        self.dtag('activeedgecolor')
        self.addtag_withtag('activeedgecolor', tag)
        self.itemconfig(tag, outline=self.select_color, width=3)
        self.tag_raise('activeedgecolor')
        self.tag_raise('activebuttoncolor')
        #tag consistent of colorname is needed here
        tag=self.gettags(tag)[0]
        self.SCRIPT.commands.append("self.set_edgecolor(True, '"+tag+"')")
        self.edge_color = tag

    def update_formula(self, buttonX):
        """opening image of formula in a given location and adding image and its both photos to self.register[buttonX] parameters"""
        try:
            if self.templink:
                im1=self.temporary_image
                im2=Image.open(r"docu.png")
                x=int(im2.size[0]*im1.size[1]/(1.*im2.size[1]))
                pic = Image.new("RGBA", (im1.size[0]+x, im1.size[1]))
                pic.paste(im1, (0, 0))
                pic.paste(im2.resize((x,im1.size[1])), (im1.size[0], 0))
                self.register[buttonX].image_snap = pic
            else: self.register[buttonX].image_snap = self.temporary_image
            #its is opened in button_menu_mathinput but we need reassign because we dont have buttonX name yet
            self.register[buttonX].formula = self.temporary_formula
            self.register[buttonX].photo_active = ImageTk.PhotoImage(self.replace_color(self.register[buttonX].image_snap, self.mixcolor(self.register[buttonX].color)))
            self.register[buttonX].photo = ImageTk.PhotoImage(self.replace_color(self.register[buttonX].image_snap, self.mixcolor(self.register[buttonX].color+'!60')))
        except TypeError:
            print 'FORMAT IS WRONG! For example, two math modes'

    def back(self):
        try:
            script=SAMPLES[-1]
            del SAMPLES[-1]
            print 'runing a previous routine'
            self = MsCanvas(root, width="14i", height="6i", bg='#122108')
            self.place(x = 0, y = 0, width=1400, height=850)
            exec(script)
        except IndexError: pass

    def new(self):
        if self.SCRIPT.commands==[]: response = False
        else: response = tkMessageBox.askyesnocancel("Save?", "Do you want to save your progress?")
        if response==None: pass
        else:
            if response:
                f=tkFileDialog.asksaveasfile(mode='w', defaultextension=".tex")
                f.write(self.save())
                f.close()
            SAMPLES.append(self.save())
        self = MsCanvas(root, width="14i", height="6i", bg='#122108')
        self.place(x = 0, y = 0, width=1400, height=850)

    def popup(self, event, tag):
        self.addtag_withtag('popup', tag)
        if self.type(tag)=='button':
            buttonX=self.gettags(tag)[0]
            if 'link' in self.register[buttonX].__dict__.keys():
                try: self.button_menu.delete('open...')
                except TclError: pass
                self.button_menu.add_command(label='open...', command = self.button_menu_open)
            else:
                try: self.button_menu.delete('open...')
                except TclError: pass
            self.button_menu.tk_popup(event.x_root, event.y_root, 0)
        elif self.type(tag)=='edge':
            #edgeX=self.gettags(tag)[0]
            self.edge_menu.tk_popup(event.x_root, event.y_root, 0)
        elif self.type(tag)=='polygon':
            self.polygon_menu.tk_popup(event.x_root, event.y_root, 0)

    def popup_main(self, event):
        if not(self.find_withtag(CURRENT)):
            self.main_menu.tk_popup(event.x_root, event.y_root, 0)

    '''def record(self, event):
        if self.find_withtag(CURRENT)==(): #make sure the rightclick
            print 'dont know how to save you'
            for n in self.find_withtag('displayed'): self.delete(n)

    def _boxify(self, tag, text):
        """Internal function that shows text over the tag"""
        C=self.coords(tag)
        temp=self.create_text((C[0]+C[2])/2, (C[1]+C[3])/2, text=text, tags='displayed')
        tempbox=self.create_rectangle(self.bbox(temp), fill="yellow", tags='displayed')
        self.tag_lower(tempbox, temp)

    def info(self, event):
        if self.find_withtag(CURRENT)==(): #make sure no edgebutton is rightclicked
            for n in self.register.keys():
                txt=n
                if self.type(n)=='button': self._boxify(self.find_withbuttontag(n)[1],txt)
                elif self.type(n)=='edge': self._boxify(self.find_withtag(n),txt)

    def info_detailed(self, event):
        if self.find_withtag(CURRENT)==():
            for n in self.register.keys():
                txt=n
                if n in self.clickables.keys(): txt+=';\n'+'self.clickables['+n+'] = '+str(self.clickables[n])
                else: txt+=';\nnot found in self.clickables'
                if type(self.register[n]) is StringType:
                    txt+='\n'+'self.register['+n+'] = '+str(self.register[n])
                    print 'IT SHOULDNT BE'

                else:
                    txt+='\n'+'self.register['+n+'] = {'
                    for it in self.register[n].__dict__.keys():
                        txt+='\n'+str(it)+': '+str(self.register[n].__dict__[it])
                    txt+='}'
                if self.type(n)=='button': self._boxify(self.find_withbuttontag(n)[1],txt)
                elif self.type(n)=='edge': self._boxify(self.find_withtag(n),txt)'''
    def _redraw(self, edgeX):
        """Internal function of self.redraw that uses recursion"""
        for m in self.clickables[edgeX]:
            coords=self.connect_bp(self.register[m].begin, edgeX)
            self.coords(self.register[m].id, coords)
            self._redraw(m)

    def redraw(self, buttonX):
        """Internal function that redraws edge that relates buttonX"""
        for n in self.clickables[buttonX]:
            if self.register[n].begin==buttonX:
                if self.type(self.register[n].end)=='button': #edit edge between two buttons (forward direction)
                    coords=self.connect_bb(self.register[n].begin, self.register[n].end)
                elif self.type(self.register[n].end)=='edge':
                    coords=self.connect_bp(self.register[n].begin, self.register[n].end) #edit edge that ends up with another edge
                self.coords(self.register[n].id, coords)
            if self.register[n].end==buttonX: #edit edge between two buttons (backward direction)
                self.coords(self.register[n].id, self.connect_bb(self.register[n].begin, self.register[n].end))
            self._redraw(n)

    def mouseDown(self, event, tag):
        # remember where the mouse went down
        self.lastx = event.x
        self.lasty = event.y

    def mouseMove(self, event, tag):
        # if the mouse is over scanvas button tagged as CURRENT we move some objects:
        if self.find_withtag('selected_button'):
            self.join(event, tag) #eliminate ability to join at first!
        #1) motion of buttonFamily
        movetag=self.find_withbuttontag(tag)
        for n in movetag:
            self.move(n, event.x - self.lastx, event.y - self.lasty)
        #2) motion of corresponding edges
        buttonX=self.gettags(tag)[0]
        if self.type(buttonX)=='button': self.redraw(buttonX)
        self.mouseDown(event, tag)

    def mouseSelectButton(self, event, buttonX):
        #OLD VERSION of mouseSelectButton(self, event, buttonX)
        if 'dangerous' not in self.gettags(self.find_withtag(CURRENT)):
            #if self.find_withtag('selected_button'):
                self.itemconfig(buttonX, outline=self.select_color)
                selected=self.gettags(self.find_withtag('selected_button')[0])[0]
                selection_edge=self.create_line(*self.connect_bb(selected, buttonX), arrow=LAST)
                self.itemconfig(selection_edge, fill=self.select_color, tags='selected_edge')
        #NEW VERSION of mouseSelectButton(self, event)
        '''print 'mscurrent:',self.find_withtag(CURRENT),
        buttonX=self.gettags(self.find_withtag(CURRENT))[0]
        print 'ms',buttonX
        if buttonX<>self.selection_button: #current selection differs from stored selection
            self.itemconfig(buttonX, outline='green')
            self.selection_edge=self.connect_bb(self.selection_button,buttonX)
            self.itemconfig(self.selection_edge, fill='green')
            print self.selection_edge'''

    def mouseUnselectButton(self, event, buttonX):
        #OLD VERSION of mouseUnselectButton(self, event, buttonX)
        self.addtag_withtag('dangerous', CURRENT)
        self.itemconfig(buttonX, outline=self.register[buttonX].color)
        self.delete('selected_edge')
        #NEW VERSION of mouseUnselectButton(self, event)
        '''print 'mucurrent:',self.find_withtag(CURRENT),
        buttonX=self.gettags(self.find_withtag(CURRENT))[0]
        print 'mu',buttonX
        if buttonX<>self.selection_button:
            self.itemconfig(buttonX, outline='darkgreen')
            self.delete(self.selection_edge)
            self.update_idletasks()'''

    def mouseSelectEdge(self, event, edgeX):
        #edgeX is id of edge object
        if 'dangerous' not in self.gettags(self.find_withtag(CURRENT)):
            self.itemconfig(edgeX, fill=self.select_color)
            selected=self.gettags(self.find_withtag('selected_button')[0])[0]
            selection_edge=self.create_line(*self.connect_bp(selected, edgeX), arrow=LAST)
            self.itemconfig(selection_edge, fill=self.select_color, tags='selected_edge')

    def mouseUnselectEdge(self, event, Id):
        #tag is id of edge object
        edgeX=self.gettags(Id)[0]
        self.addtag_withtag('dangerous', CURRENT)
        self.itemconfig(edgeX, fill=self.register[edgeX].color)
        self.delete('selected_edge')

    def join(self, event, tag):
        #constructs a new edge and configures shapes back
        if self.find_withtag('selected_button'):
            #adding an edge
            buttonX=self.gettags(self.find_withtag('selected_button')[0])[0]
            edgebuttonY=self.gettags(tag)[0] #EdgeY or ButtonY
            if buttonX<>edgebuttonY:
                self.create_edge(buttonX, edgebuttonY)
                #reconfiguring connected objects back to previous settings
                if self.type(edgebuttonY)=='button': self.itemconfig(edgebuttonY, outline=self.register[edgebuttonY].color) #if buttonX=EdgebuttonY it works twice, ha ha...
                elif self.type(edgebuttonY)=='edge': self.itemconfig(edgebuttonY, fill=self.register[edgebuttonY].color)
            self.itemconfig(buttonX, outline=self.register[buttonX].color) #configuring outline back to previous color
            self.delete('selected_edge')
            self.dtag('selected_button')
            self.dtag('selected_edge')
            #cleaning tag binds for button and edge selects/unselects
            for n in self.find_withtag('button'):
                #associated_tags=self.find_withbuttontag(n)
                buttonZ=self.gettags(n)[0]
                '''for m in associated_tags:
                    print m, 'in', associated_tags, 'of'
                    print self.register[buttonZ].photo_active
                    print self.register[buttonZ].photo
                    print self.mixcolor(self.register[buttonZ].color)
                    self.tag_bind(m,"<Enter>", lambda event, i=associated_tags[1], config={'image':self.register[buttonZ].photo_active}: self.click(event,i,config))
                    self.tag_bind(m,"<Leave>", lambda event, i=associated_tags[1], config={'image':self.register[buttonZ].photo}: self.click(event,i,config))
                    self.tag_bind(m,"<Enter>", lambda event, i=associated_tags[0], config={'fill':self.mixcolor(self.register[buttonZ].color)}: self.click(event,i,config))
                    self.tag_bind(m,"<Leave>", lambda event, i=associated_tags[0], config={'fill':self.mixcolor(self.register[buttonZ].color+'!60')}: self.click(event,i,config))'''
                self.itemconfig(buttonZ, bg='its important to stay awake')
            for n in self.find_withtag('edge'):
                self.tag_unbind(n, "<Enter>")
                self.tag_unbind(n, "<Leave>")
            #replace mathinput text after simple click (no double click selection done before)
        #tag is any number that is catched
        #puts border on the button if double clicked and bind Select-Unselect construction to every button
        else:
            buttonZ=self.gettags(tag)[0]
            self.addtag_withtag('selected_button', buttonZ)
            for n in self.find_withtag('button'):
                buttonX=self.gettags(n)[0]
                if buttonX<>self.gettags(tag)[0]:
                    self.tag_bind(n,"<Enter>", lambda event, i=buttonX: self.mouseSelectButton(event, i))
                    self.tag_bind(n,"<Leave>", lambda event, i=buttonX: self.mouseUnselectButton(event, i))
            for n in self.find_withtag('edge'):
                self.tag_bind(n,"<Enter>", lambda event,i=n: self.mouseSelectEdge(event, i))
                self.tag_bind(n,"<Leave>", lambda event,i=n: self.mouseUnselectEdge(event, i))
            self.itemconfig(buttonZ, bg='its important to stay awake')
            self.itemconfig(tag, outline=self.select_color)
        self.mouseDown(event, tag)
        if self.type(tag)=='button':
            buttonX=self.gettags(tag)[0]
            self.mathinput.delete('1.0', END)
            self.mathinput.insert(INSERT, self.register[buttonX].formula)
        #NEW VERSION
        '''if self.selection_button==None:
            self.selection_button=self.gettags(tag)[0]#of the form buttonX
            self.tag_bind('button',"<Any-Enter>", lambda event: self.mouseSelectButton(event))
            self.tag_bind('button',"<Any-Leave>", lambda event: self.mouseUnselectButton(event))
            self.itemconfig(tag, bg='red')
            self.itemconfig(tag, outline='green')'''

    def _erase(self, erasable):
        """Internal function that removes edgeX and its connectives from CLICKABLES"""
        removed=self.clickables.pop(erasable) #removing edgeX from CLICKABLES
        for n in removed: self._erase(n)
        BEGIN=self.register[erasable].begin
        if self.type(BEGIN)=='button': self.clickables[BEGIN].remove(erasable) #removing edgeX from beginners of edgebuttonX
        END=self.register[erasable].end
        if self.type(END)=='button':
            self.clickables[END].remove(erasable) #removing edgeX from enders of edgebuttonX
        self.delete(self.register[erasable].id)
        self.register.pop(erasable) #removing edgeX from REGISTER

    def erase_edge(self, event, tag):
        self.SCRIPT.commands.append('self.erase_edge(True, '+str(tag)+')')
        #obj is any object of edge class #WHAT IF POINTS?
        erasable=self.gettags(tag)[0] #edgeX
        self._erase(erasable)
        #print 'after erase edge', self.clickables

    def erase_button(self, event, tag):
        #tag is any number that is catched
        #self.SCRIPT.commands.append("self.erase_button(True, '"+str(tag)+"')")
        erasable=self.gettags(tag)[0]
        relatives=[n for n in self.clickables[erasable]]
        for n in relatives: self._erase(n)
        for n in self.find_withbuttontag(erasable): self.delete(n)
        #connected_to=self.clickables.pop(erasable)
        #print 'after erase button', self.clickables

    def create_edge(self, buttonX, edgebuttonY):
        #create edge between buttonX and (buttonY or tag of line) and return a new object of a class "edge"
        self.SCRIPT.commands.append('self.create_edge('+"'"+buttonX+"'"','+"'"+edgebuttonY+"')")
        self.numOfEdges+=1
        sticker="edge"+str(self.numOfEdges)
        if self.type(edgebuttonY)=='button':
            new_edge = edge(self.create_line(*self.connect_bb(buttonX, edgebuttonY), arrow=LAST), buttonX, edgebuttonY)
        elif self.type(edgebuttonY)=='edge':
            new_edge = edge(self.create_line(*self.connect_bp(buttonX, edgebuttonY), arrow=LAST), buttonX, edgebuttonY)
        new_edge.color=self.edge_color
        self.itemconfig(new_edge.id, tags=sticker, fill=self.edge_color, width=5)
        self.addtag_withtag("edge", sticker)
        self.tag_lower(new_edge.id)
        self.tag_bind(new_edge.id,"<Button-3>",lambda event, i=new_edge.id: self.popup(event,i))
        self.tag_bind(new_edge.id,"<Button-1>",lambda event, i=new_edge.id: self.join(event,i))
        #storing info: including a new edge to the keys (of clickables)
        self.register.update({sticker: new_edge})
        self.clickables.update({sticker: []})
        self.clickables[new_edge.begin].append(sticker)
        self.clickables[new_edge.end].append(sticker)
        return sticker

    def create_button(self,*args,**kwargs):
        buttonX=super(MsCanvas,self).create_button(*args,**kwargs)
        self.register.update({buttonX: button(buttonX)})
        self.register[buttonX].color=self.button_color
        if 'image' in kwargs:
            self.update_formula(buttonX)
        self.clickables.update({buttonX:[]})
        self.itemconfig(buttonX, bg='its important to stay awake')
        button_tags=self.find_withbuttontag(buttonX)
        for n in button_tags:
            self.tag_bind(n,"<Button-1>",lambda event, i=n: self.join(event,i)) #self.mouseDown is inside!
            self.tag_bind(n,"<B1-Motion>",lambda event, i=n: self.mouseMove(event, i))
            self.tag_bind(n,"<Button-3>",lambda event, i=n: self.popup(event,i))
        #print 'after create button', self.clickables
        return buttonX

    def connect_bb(self, button1, button2):
        #we use a math to get intersection points of edge between two buttons
        #B1,B2 are quadruples of cordinates of these buttons provided as (x1, y1, x2, y2)
        #segment that joins centers (a,b) and (c,d) is given as y-b=(x-a)*(d-b)/(c-a) with limitation {x in [a,c]}
        #SEGMENTS ARE:
        #segments 1,2,5,6 are involved in a first button; if these are hit, we assign a hitpoint to finalSTART
        #segments 3,4,7,8 are involved in a second button; if these are hit, we assign a hitpoint to finalEND
        #print 'connect_bbing', button1, 'and', button2
        rectangle1, rectangle2 = self.find_withbuttontag(button1)[0], self.find_withbuttontag(button2)[0]
        if rectangle1 not in self.find_overlapping(*self.coords(rectangle2)):
            B1,B2=self.coords(rectangle1), self.coords(rectangle2)
            C1 = ((B1[0]+B1[2])/2, (B1[1]+B1[3])/2) #center of button1
            C2 = ((B2[0]+B2[2])/2, (B2[1]+B2[3])/2) #center of button2

            if C2[1]==C1[1]:
                if C1[0]<C2[0]: return (B1[2], C1[1], B2[0], C2[1])#edge from right center of 1 to left center of 2
                else: return (B2[2], C1[1], B1[0],C2[1])#reverse

            if C2[0]==C1[0]:
                if C1[1]<C2[1]: return (C1[0], B1[3], C2[0], B2[1])#edge from bottom center of 1 to top center of 2
                else: return (C1[0], B2[3], C2[0], B1[1])#reverse

            START,END=min(C1[0],C2[0]),max(C1[0],C2[0]) #these are x coordinates of both buttons such that START<END

            def get_y(x):
                #given x coordinate in an edge that joins centers of button1 and button2, return y coordinate
                return C1[1]+(x-C1[0])*(C2[1]-C1[1])/(C2[0]-C1[0])
            def get_x(y):
                #given y coordinate in an edge that joins centers of button1 and button2, return x coordinate
                return C1[0]+(y-C1[1])*(C2[0]-C1[0])/(C2[1]-C1[1])

            x,y=B1[0], get_y(B1[0])
            if B1[1]-0.001<y<B1[3]+0.001 and START<x<END: finalSTART=(x,y)
            ##print 'edge1: x =',x,'y =',y,'\n cond1: y is between',B1[1],'and',B1[3],'is',B1[1]<y<B1[3], '\n cond2: x is between',START,'and',END,'is',START<x<END
            x,y=B1[2], get_y(B1[2])
            if B1[1]-0.001<y<B1[3]+0.001 and START<x<END: finalSTART=(x,y)
            ##print 'edge2: x =',x,'y =',y,'\n cond1: y is between',B1[1],'and',B1[3],'is',B1[1]<y<B1[3], '\n cond2: x is between',START,'and',END,'is',START<x<END
            x,y=B2[0], get_y(B2[0])
            if B2[1]-0.001<y<B2[3]+0.001 and START<x<END: finalEND=(x,y)
            ##print 'edge3: x =',x,'y =',y,'\n cond1: y is between',B2[1],'and',B2[3],'is',B2[1]<y<B2[3], '\n cond2: x is between',START,'and',END,'is',START<x<END
            x,y=B2[2], get_y(B2[2])
            if B2[1]-0.001<y<B2[3]+0.001 and START<x<END: finalEND=(x,y)
            ##print 'edge4: x =',x,'y =',y,'\n cond1: y is between',B2[1],'and',B2[3],'is',B2[1]<y<B2[3], '\n cond2: x is between',START,'and',END,'is',START<x<END
            x,y=get_x(B1[1]), B1[1]
            if B1[0]-0.001<x<B1[2]+0.001 and START<x<END: finalSTART=(x,y)
            ##print 'edge5: x =',x,'y =',y,'\n cond1: x is between',B1[0],'and',B1[2],'is',B1[0]<x<B1[2], '\n cond2: x is between',START,'and',END,'is',START<x<END
            x,y=get_x(B1[3]), B1[3]
            if B1[0]-0.001<x<B1[2]+0.001 and START<x<END: finalSTART=(x,y)
            ##print 'edge6: x =',x,'y =',y,'\n cond1: x is between',B1[0],'and',B1[2],'is',B1[0]<x<B1[2], '\n cond2: x is between',START,'and',END,'is',START<x<END
            x,y=get_x(B2[1]), B2[1]
            if B2[0]-0.001<x<B2[2]+0.001 and START<=x<=END: finalEND=(x,y)
            ##print 'edge7: x =',x,'y =',y,'\n cond1: y is between',B2[0],'and',B2[2],'is',B2[0]<x<B2[2], '\n cond2: x is between',START,'and',END,'is',START<x<END
            x,y=get_x(B2[3]), B2[3]
            if B2[0]-0.001<x<B2[2]+0.001 and START<=x<END: finalEND=(x,y)
            ##print 'edge8: x =',x,'y =',y,'\n cond1: y is between',B2[0],'and',B2[2],'is',B2[0]<x<B2[2], '\n cond2: x is between',START,'and',END,'is',START<x<END
            return finalSTART+finalEND

    def connect_bp(self, button, edge):
        #copied from connect_bb assuming B=B1 and C=C1 and P=(B2[0],B2[1])=(C2[0],C2[1]) where B2[0]=B2[2] and B2[1]=B2[3]
            rectangle = self.find_withbuttontag(button)[0]
        #if rectangle1 not in self.find_overlapping(*self.coords(rectangle2)):
            pos=self.coords(edge)
            midpoint_of_edge=((pos[0]+pos[2])/2, (pos[1]+pos[3])/2)
            B, P = self.coords(rectangle), midpoint_of_edge
            C = ((B[0]+B[2])/2, (B[1]+B[3])/2) #center of button

            if P[1]==C[1]:
                if C[0]<P[0]: return (B[2], C[1], P[0], P[1])#edge from right center of 1 to left center of 2
                else: return (P[0], C[1], B[0], P[1])#reverse

            if P[0]==C[0]:
                if C[1]<P[1]: return (C[0], B[3], P[0], P[1])#edge from bottom center of 1 to top center of 2
                else: return (C[0], P[1], P[0], B[1])#reverse

            START,END=min(C[0],P[0]),max(C[0],P[0]) #these are x coordinates of both buttons such that START<END

            def get_y(x): return C[1]+(x-C[0])*(P[1]-C[1])/(P[0]-C[0])
            def get_x(y): return C[0]+(y-C[1])*(P[0]-C[0])/(P[1]-C[1])

            x,y=B[0], get_y(B[0])
            if B[1]-0.001<y<B[3]+0.001 and START<x<END: finalSTART=(x,y)
            ##print 'edge1: x =',x,'y =',y,'\n cond1: y is between',B1[1],'and',B1[3],'is',B1[1]<y<B1[3], '\n cond2: x is between',START,'and',END,'is',START<x<END
            x,y=B[2], get_y(B[2])
            if B[1]-0.001<y<B[3]+0.001 and START<x<END: finalSTART=(x,y)
            ##print 'edge2: x =',x,'y =',y,'\n cond1: y is between',B1[1],'and',B1[3],'is',B1[1]<y<B1[3], '\n cond2: x is between',START,'and',END,'is',START<x<END
            x,y=get_x(B[1]), B[1]
            if B[0]-0.001<x<B[2]+0.001 and START<x<END: finalSTART=(x,y)
            ##print 'edge5: x =',x,'y =',y,'\n cond1: x is between',B1[0],'and',B1[2],'is',B1[0]<x<B1[2], '\n cond2: x is between',START,'and',END,'is',START<x<END
            x,y=get_x(B[3]), B[3]
            if B[0]-0.001<x<B[2]+0.001 and START<x<END: finalSTART=(x,y)
            ##print 'edge6: x =',x,'y =',y,'\n cond1: x is between',B1[0],'and',B1[2],'is',B1[0]<x<B1[2], '\n cond2: x is between',START,'and',END,'is',START<x<END
            return finalSTART+P


class edge():
    def __init__(self, id, begin, end):
        self.id = id
        self.begin = begin
        self.end = end

class button():
    def __init__(self, tag):
        self.tag = tag

def click(event, tag):
    print 'tag is:', tag

mscanvas = MsCanvas(root, width="14i", height="6i", bg='#122108')
mscanvas.place(x = 0, y = 0, width=1400, height=850)
root.mainloop()