from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
from time import time
import matplotlib.pyplot as plt

def plotter(array):
    plt.plot(array)
    plt.show()
    
t=time()
def convert(filename,needed,spacing=30,second_increase=150,safezone=range(550,1100)):
    pages = convert_from_path(filename)
    INDEX=0
    print(time()-t)
    for page in pages:
        if INDEX in [n-1 for n in needed]:
            print('WORKING on', 'out'+str(INDEX+1)+'.jpg','-'*50)
            page.save('out'+str(INDEX+1)+'.jpg', 'JPEG')
            im = Image.open('out'+str(INDEX+1)+'.jpg')
            width, height = im.size
            print(width, height)
            rgb_im = im.convert('RGB')
            #finding startline and endline of a number
            potential_numbers=[]
            pos=False
            vcut=[[rgb_im.getpixel((i, j))==(255,255,255) for j in range(height)].count(False) for i in range(400)]
            
            #print('vcuts at columns 1..370:','\n', vcut,end=' ') #try another decreasal values (than 50) if u get endline refrenced before an assignment
            plotter(vcut[270:])
            jumps_of_vcut=[0]+[vcut[i+1]-vcut[i] for i in range(len(vcut)-1)]
            for it in range(len(vcut)):
                if vcut[it]>50:
                    if pos==False: 
                        pos=True
                        startline=it
                    else:
                        if jumps_of_vcut[it]>second_increase:
                            endline=it-8
                            break
            print('startline=',startline,'endline=',endline)
            '''use in case u want to check vcut only:'''
            #INDEX+=1
            #continue
            #finding indexes of row that are non-empty between startline and endline
            for j in range(height):
                potential_cut=(False in [rgb_im.getpixel((i, j))==(255,255,255) for i in range(startline, endline)])
                #omitting rows that are empty on the rightside
                potential_cut=potential_cut and (False in [rgb_im.getpixel((i, j))==(255,255,255) for i in safezone])
                potential_numbers.append(potential_cut)
            #list of rows that intersects numbering of problems:
            number_lines=[i for i in range(len(potential_numbers)) if potential_numbers[i]]
            #[440, 441, ..., 460, 461, 462, 463, 840, 841, ... , 867, 868, 869, 870, 871, 1032, 1033, ..., 2013, 2014, 2015]
            #given list of rows, lets take only those that are boundary
        
            '''print('list of rows that intersects numbering of problems:', number_lines)'''
            bounds=[number_lines[0]]
            bound=number_lines[0]
            for n in number_lines[1:]:
                #listing of data that has a jump
                if n - bound > 10: #use 10 because pagelines are dangerous
                    bounds.append(bound)
                    bounds.append(n)
                bound=n
            bounds.append(number_lines[-1])
            boundaries=[(bounds[i],bounds[i+1]) for i in range(0,len(bounds)-1,2) if (bounds[i+1]-bounds[i]>15)]
            '''print('sides of numeration:', startline, endline)
            print('downs and tops of numeration:', boundaries)'''
            
            #show blue rectangles (if you want here)
            
            problemBounds=[]
            for item in range(len(boundaries)):
                #if n-th problem has spacing that is assigned manually, use jump = this assignment
                if sum(info)+len(problemBounds)+1 in manual_spacings.keys(): 
                    jump = manual_spacings[sum(info)+len(problemBounds)+1]
                else: jump=spacing
                 #if n-th problem omits checking picturezone, use k=part of zone not in picture
                if sum(info)+len(problemBounds)+1 in manual_picturecuts.keys(): 
                    k = manual_picturecuts[sum(info)+len(problemBounds)+1]
                else: k=1
                h=boundaries[item][0]
                #if problem previous to n-th problem has spacing that is assigned manually, use jump_above analogically
                if sum(info)+len(problemBounds) in manual_spacings.keys(): 
                    jump_above = manual_spacings[sum(info)+len(problemBounds)]
                else: jump_above=spacing
                #if problem previous to n-th problem omits checking picturezone, use k_above analogically
                if sum(info)+len(problemBounds) in manual_picturecuts.keys(): 
                    k_above = manual_picturecuts[sum(info)+len(problemBounds)]
                else: k_above=1
                #searching for the first white space above the problem
                while(False in [rgb_im.getpixel((i, h))==(255,255,255) for i in range(int(k_above*width))]):
                    h-=1
                    if boundaries[item][0]-h>jump_above: break #stopping if area above the problem is too big
                upperBound=h #assigning to what we have found
                h=boundaries[item][1]
                lowerBound=h
                while True:
                    #using k of width because emptyspace in leftside is more trusted than in rigtside because of images
                    while(False in [rgb_im.getpixel((i, h))==(255,255,255) for i in range(int(k*width))]):
                        h+=1
                    if all([not(False in [rgb_im.getpixel((i, space))==(255,255,255) for i in range(int(k*width))]) for space in range(h,h+jump)]):
                        lowerBound=h
                        #break
                        #don't identify a problem separator if number space is white and problemzone has some not white points in a zone below 
                        #if not(all([not(False in [rgb_im.getpixel((i, space))==(255,255,255) for i in range(startline,endline)]) for space in range(h+30,h+60)]) and
                        #       not(all([not(False in [rgb_im.getpixel((i, space))==(255,255,255) for i in range(startline,int(width))]) for space in range(h+30,h+60)]))):
                        break
                    else: h+=jump
                problemBounds.append([upperBound, lowerBound])
            '''print('downs and tops of problems:', problemBounds)'''
            '''
            for i in range(1,len(problemBounds)):
                #in case lowerBound of a problem A is lost 
                #(due to image of B not leaving empty space between problems or etc.)
                #it goes together with lowerBound of a problem B;
                #make it equal to upperBound of problem B:
                if problemBounds[i-1]==problemBounds[i]:
                    print('WARNING:',i,'and',i+1,'got merged')
                elif problemBounds[i-1][1]>problemBounds[i][0]:
                    problemBounds[i-1][1]=problemBounds[i][0]-1
            print('CORRECTED d&t of problems:', problemBounds)'''
            #TESTING
            #type 'im' in console to check the results of identifying enumeration
            draw=ImageDraw.Draw(im)
            i=width-1
            while not(False in [rgb_im.getpixel((i, j))==(255,255,255) for j in range(height)]): i-=1
            rightSide=i
            
            for x in boundaries:
                #draw.rectangle([startline,x[0],endline,x[1]],outline='blue')
                font = ImageFont.truetype("arial.ttf", 16)
                draw.text((startline,x[1]),filename.split('.')[0],fill='blue',font=font)
            for i in range(len(problemBounds)):
                x=problemBounds[i]
                area = im.crop([startline,x[0],rightSide+5,x[1]])
                area.save(filename.split('.')[0]+'_'+str(sum(info)+i+1)+'.jpg')
                #draw.rectangle([startline,x[0],rightSide+5,x[1]],outline='red')
            im.save('out'+str(INDEX+1)+'.jpg')
            info.append(len(problemBounds))#recording number of problemBounds found in a current loop
        INDEX+=1

info=[8]
manual_spacings={9:5, 11:25, 13:5, 14:17, 16:5, 17:5, 25:5, 27:10}#0:5, 5:14, 8:14, 12:15, 14:10,23:5}
manual_picturecuts={0:0.65, 11:0.65}#6:0.65, 7:0.65, 11:0.65, 12:0.65, 13:0.65, 24:0.65}
convert(filename='B2012.pdf', needed=[12,13,14], spacing=20, safezone=list(range(660,1000)))#,19,20,21])
'''
needed = pythonic numbers of pages
spacing = number of pixels that identifies problem splitting
safezone = columns that identify liar numberings
'''

'''How to work:
1) check if all pages are right
2) change some manual spacings and picturecuts to avoid duplicated problems
3) if you see some liar problems that are headlines:
    -try to fix safezones
    -some of the safezones differs at each page; in this case: 
        try conversion in a separate steps by defining different values of needed'''
        
'''What it does:
    converts pdf into images and for each image:
        assigns startline and endline to first big increase and first big decrease of columns on the right (1..220) of picture
        assigns boundaries to a list of rows that intersects numbering of problems (area between startline and endline)
        identifies upperBounds and lowerBounds
        '''
#OPTIONS that are changeable: 

#<>if you see some headlines: check range of whiteZone at 34 
#<>in case of some problems not assigned:
#1) values of startline and endline are wrong:
#   get the the index of rapid decrease (=decreasal) at problemNumberingPoints
#   of nonwhite cells by checking behaviour of vcut at 30
#2) spacing is wrong
#<>local variable 'endline' referenced before assignment:
#check why vcut doesnt reach decreasal

    
        

    
