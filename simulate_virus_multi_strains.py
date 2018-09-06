import re,sys,pdb,subprocess

fa_file='/mnt/home/chenjiao/research/Project-virus/Data/HXB2_NL43.fa'

## generate the coverage list
seq_count=0
total_cov=2000
title_list=[]
with open(fa_file,'r') as f:
    for line in f:
        if line.startswith('>'):
            seq_count+=1
            title_list.append(line[1:].strip())
sum_p=0
for i in range(1,seq_count+1):
    sum_p+=1.0/float(i)
C=total_cov/sum_p
print C

cov_list=[]
for i in range(1,seq_count+1):
    cov=C/float(i)
    cov_list.append(round(cov))
print sum(cov_list)

f_out=open('seq_coverages.txt','w')
for i in range(len(cov_list)):
    f_out.write(title_list[i]+'\t'+str(cov_list[i])+'\n')
f_out.close()
#pdb.set_trace()

## simulate reads
seq=''
seq_idx=0
with open(fa_file,'r') as f:
    for line in f:
        if line.startswith('>'):
            if seq:
                f_out=open('temp.fa','w')
                f_out.write(title+seq+'\n')
                f_out.close()
                out_file='temp_'+str(seq_idx)
                command='art_illumina -sam -i temp.fa -p -ef -l 100 -ss MS -f '+str(cov_list[seq_idx])+ ' -m 300 -s 30 -o '+out_file
                subprocess.call(command,shell=True)
                command2='cat temp_'+str(seq_idx)+'_errFree.sam >>virus_errFree.sam'
                subprocess.call(command2,shell=True)
                command3='cat temp_'+str(seq_idx)+'.sam >>virus.sam'
                subprocess.call(command3,shell=True)
                seq_idx+=1

            title=line
            seq=''
        else:
            seq+=line.strip()
    if seq: # process the last sequence
        f_out=open('temp.fa','w')
        f_out.write(title+seq+'\n')
        f_out.close()
        out_file='temp_'+str(seq_idx)
        command='art_illumina -sam -i temp.fa -p -ef -l 100 -ss MS -f '+str(cov_list[seq_idx])+ ' -m 300 -s 30 -o '+out_file
        subprocess.call(command,shell=True)
        command2='cat temp_'+str(seq_idx)+'_errFree.sam >>virus_errFree.sam'
        subprocess.call(command2,shell=True)
        command3='cat temp_'+str(seq_idx)+'.sam >>virus.sam'
        subprocess.call(command3,shell=True)
        seq_idx+=1

subprocess.call('python gen_errfree_sequence_pair_end.py virus_errFree.sam virus_errFree.fa',shell=True)
subprocess.call('python gen_errfree_sequence_pair_end.py virus.sam virus.fa',shell=True)
subprocess.call('rm *.aln',shell=True)
subprocess.call('rm *.sam',shell=True)
subprocess.call('rm *.fq',shell=True)
subprocess.call('python shuff_relabel_reads_pair_end.py virus_errFree.fa HXB2_NL43_errFree.fa',shell=True)
subprocess.call('python shuff_relabel_reads_pair_end.py virus.fa HXB2_NL43.fa',shell=True)
subprocess.call('rm temp.fa',shell=True)
subprocess.call('rm virus_errFree.fa',shell=True)
subprocess.call('rm virus.fa',shell=True)
