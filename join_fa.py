import re,sys,pdb

# join multiple lines into one line

fa_file = sys.argv[1]
f_out = open(sys.argv[2],'w')

title=''
seq=[]
with open(fa_file,'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith('>'):
            #if len(seq)>0:
            if seq:
                f_out.write(title+'\n'+''.join(seq)+'\n')
            title = line
            seq = []
        else:
            seq.append(line)
if seq:
    f_out.write(title+'\n'+''.join(seq)+'\n')

f_out.close()
