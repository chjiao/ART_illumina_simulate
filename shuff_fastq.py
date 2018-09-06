import re,sys,pdb,subprocess
from random import shuffle

raw_file=sys.argv[1]
out_file=sys.argv[2]

fq_reads=[]
lineno=0
with open(raw_file,'r') as f:
    for line in f:
        line=line.strip()
        lineno+=1
        if lineno%4==1:
            title = line
        elif lineno%4==2:
            seq = line
        elif lineno%4==3:
            title2 = line
        else:
            quality = line
            fq_reads.append([title,seq,title2,quality])

shuffle(fq_reads)

fo=open(out_file,'w')
for x in fq_reads:
    fo.write(x[0]+'\n'+x[1]+'\n'+x[2]+'\n'+x[3]+'\n')
fo.close()
