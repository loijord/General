import pygame.midi
import matplotlib.pyplot as plt
from time import time

#restart core if u see Host Error

def plotting(inputs):
    plt.clf()
    correct_inputs=[]
    for i in range(len(inputs)):
        if i>0: correct_inputs.append((inputs[i][0], inputs[i-1][1]))
        correct_inputs.append(inputs[i])
        
    plt.plot(*zip(*correct_inputs))
    plt.pause(0.01)
    
pygame.midi.init()
devices=[pygame.midi.get_device_info(device_id) for device_id in range(pygame.midi.get_count())]
my_device_id=pygame.midi.get_default_input_id()
print(my_device_id)
inp = pygame.midi.Input(my_device_id)
inputs=[]

time_tag=0.1
t=time()
delay=time_tag
while True:
    if inp.poll():
        MIDImessage=inp.read(1000)
        pygame.time.wait(10)
        for n in MIDImessage:
            if n[0][1] != 53:
                inputs.append((n[1]/1000,n[0][2]))
        
        if ((time()-t)//delay)*delay > time_tag:
            time_tag = ((time()-t)//delay)*delay 
            plotting(inputs)
        if any([n[0][:3]==[144, 53, 127] for n in MIDImessage]): 
            plt.close()
            break


inp.close()


    
    


