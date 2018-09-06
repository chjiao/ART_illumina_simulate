import re,sys,pdb
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna

def rev_com(seq):
    dna_seq = Seq(seq, generic_dna)
    rev_seq = dna_seq.reverse_complement()
    return str(rev_seq) 

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
        title=line_map[0]
        flag=line_map[1]
        seq=line_map[9]
        if flag=='0':
            f_out.write('>'+title+'\n'+seq+'\n')
        elif flag=='16':
            f_out.write('>'+title+'\n'+rev_com(seq)+'\n')

f_out.close()
