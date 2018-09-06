import re,sys,pdb,subprocess
from random import shuffle

raw_file=sys.argv[1]
out_file=sys.argv[2]

seq=''
fa_reads=[]
lineno=0
with open(raw_file,'r') as f:
    for line in f:
        if line.startswith('>'):
            if seq:
                fa_reads.append([title,seq])
            title=line.strip()
            seq=''
        else:
            seq+=line.strip()
    if seq:
        fa_reads.append([title,seq])

fa_pair=[]
for i in range(0,len(fa_reads),2):
    fa=fa_reads[i]
    fa.extend(fa_reads[i+1])
    #pdb.set_trace()
    fa_pair.append(fa)
#pdb.set_trace()
fo=open('shuf.fa','w')
shuffle(fa_pair)
for x in fa_pair:
    fo.write(x[0]+'\n'+x[1]+'\n'+x[2]+'\n'+x[3]+'\n')
fo.close()
                
f_out=open(out_file,'w')
count=1
lineno=0
with open('shuf.fa','r') as f:
    for line in f:
        lineno+=1
        if line.startswith('>'):
            lmap=line[1:].split('-')
            if line.strip().endswith('1'):
                f_out.write('>'+lmap[0]+'-'+str(count)+'/'+'1'+'\n')
            else:
                f_out.write('>'+lmap[0]+'-'+str(count)+'/'+'2'+'\n')
        else:
            f_out.write(line)

        if lineno%4==0:
            count+=1
f_out.close()

subprocess.call('rm shuf.fa',shell=True)
