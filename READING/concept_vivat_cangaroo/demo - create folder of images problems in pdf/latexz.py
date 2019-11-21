#make sure filePathStart is correct!

from subprocess import check_output
from Tkinter import*
from PIL import Image, ImageTk
from time import*
t=time()
TEX = (  # use raw strings for backslash
  unicode("\documentclass{article}"),
  unicode("\usepackage{amsmath}"),
  unicode("\usepackage{amsthm}"),
  unicode("\usepackage{amssymb}"),
  unicode("\usepackage{bm}"),
  unicode("\usepackage{graphicx}"),
  unicode("\usepackage[active,displaymath,textmath,tightpage]{preview}"),
  unicode("\pagestyle{empty}"),
  r"\begin{document}",
  r"$\includegraphics[trim={0cm 0cm 0cm 0cm},clip, bb = 0 0 20cm 20cm]{B2018.pdf}$",
  #r"$vfotonas$",
  r"\end{document}",
)

filePathStart=r"C:\Users\Vartotojas\Desktop\EnolaProject\Kodinimas\Pythoning\demo - create folder of images problems in pdf"
with open(filePathStart+r"\mintedex.tex",'w') as out_file:
  for T in TEX: out_file.write("%s\n" % T)
#print 'AFTER writing a file:', time()-t
print check_output(['latex',filePathStart+r"\mintedex.tex"])
#print 'AFTER execution of .tex:', time()-t
print check_output(['dvipng',filePathStart+r"\mintedex.dvi",'-o',filePathStart+u"\mintedex.png"])
#print 'AFTER conversion:', time()-t
#latex C:\Users\Vartotojas\Desktop\mintedex.tex
#dvipng C:\Users\Vartotojas\Desktop\mintedex.dvi -o C:\Users\Vartotojas\Desktop\mintedex.png
root = Toplevel()
image = Image.open(filePathStart+r"\mintedex.png")
photo = ImageTk.PhotoImage(image)
label = Label(root, image=photo)
label.image = photo
label.pack()
root.mainloop()