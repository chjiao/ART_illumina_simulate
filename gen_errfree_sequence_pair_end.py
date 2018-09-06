import re,sys,pdb

sam_file=sys.argv[1]
fa_file=sys.argv[2]

lineno=0
f_out=open(fa_file,'w')
with open(sam_file,'r') as f:
    for line in f:
        if line.startswith('@'):
            continue
        lineno+=1
        line_map=line.strip().split()
        if lineno%2==1:
            title1=line_map[0]
            flag1=line_map[1]
            seq1=line_map[9]
        elif lineno%2==0:
            title2=line_map[0]
            flag2=line_map[1]
            seq2=line_map[9]
            if title1==title2:
                if flag1=='99' and flag2=='147':
                    title1='>'+title1+'/1'
                    title2='>'+title2+'/2'
                    f_out.write(title1+'\n'+seq1+'\n'+title2+'\n'+seq2+'\n')
                elif flag1=='83' and flag2=='163':
                    title1='>'+title1+'/2'
                    title2='>'+title2+'/1'
                    f_out.write(title2+'\n'+seq2+'\n'+title1+'\n'+seq1+'\n')


f_out.close()
