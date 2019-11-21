#[reikia pakoreguoti] Si programa sudaro zodyna is nuskaityto failo ir priraso tame faile labas::labas
print open(r"memory\archived.tex","r").read().split('\n')
archived=dict([n for n in open(r"memory\archived.tex","r").read().split('@')])
print archived
f=open(r"memory\archived.tex","a")
f.write('\n')
f.write('labas::labas')
f.close()
#--file smp.tex| uuuuuuu