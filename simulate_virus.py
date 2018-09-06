import re,sys,pdb,subprocess

#fa_file='/mnt/home/chenjiao/research/Project-meta-virus/Data/SARS.fna'
fa_file= sys.argv[1]
out_prefix = sys.argv[2]
coverage = int(sys.argv[3])

## generate the coverage list
seq_count=0
total_cov=1000
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

#cov_list=[500]
cov_list=[coverage]
#for i in range(1,seq_count+1):
#    cov=C/float(i)
#    cov_list.append(round(cov))
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
                command='art_illumina -sam -i temp.fa -p -ef -l 250 -ss MS -f '+str(cov_list[0])+ ' -m 600 -s 150 -o '+out_file
                subprocess.call(command,shell=True)
                command2='cat temp_'+str(seq_idx)+'1.fq >>virus_1.fq'
                subprocess.call(command2,shell=True)
                command3='cat temp_'+str(seq_idx)+'2.fq >>virus_2.fq'
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
        command='art_illumina -sam -i temp.fa -p -ef -l 250 -ss MS -f '+str(cov_list[0])+ ' -m 600 -s 150 -o '+out_file
        subprocess.call(command,shell=True)
        command2='cat temp_'+str(seq_idx)+'1.fq >>virus_1.fq'
        subprocess.call(command2,shell=True)
        command3='cat temp_'+str(seq_idx)+'2.fq >>virus_2.fq'
        subprocess.call(command3,shell=True)
        seq_idx+=1

fa_whole = out_prefix+'_whole.fa'
fq_whole = out_prefix+'_whole.fq'
fa_1 = out_prefix+'_1.fa'
fa_2 = out_prefix+'_2.fa'
fq_1 = out_prefix+'_1.fq'
fq_2 = out_prefix+'_2.fq'

subprocess.call('python join_pair_end_fastq.py virus_1.fq virus_2.fq virus_whole.fq', shell=True)
subprocess.call('python shuff_pair_end_fastq.py virus_whole.fq virus_whole_shuf.fq', shell=True)
#subprocess.call('python fq2fa.py virus_whole_shuf.fq virus_whole.fa', shell=True)
subprocess.call('python fq2fa.py virus_whole_shuf.fq '+fa_whole, shell=True)
#subprocess.call('python separate_pair_end_fasta.py virus_whole.fa', shell=True)
subprocess.call('python separate_pair_end_fasta.py '+fa_whole, shell=True)
#subprocess.call('mv fa1.fa virus_1.fa', shell=True)
subprocess.call('mv fa1.fa '+fa_1, shell=True)
#subprocess.call('mv fa2.fa virus_2.fa', shell=True)
subprocess.call('mv fa2.fa '+fa_2, shell=True)

subprocess.call('rm virus_1.fq virus_2.fq',shell=True)
subprocess.call('rm virus_whole.fq',shell=True)
#subprocess.call('mv virus_whole_shuf.fq virus_whole.fq', shell=True)
subprocess.call('mv virus_whole_shuf.fq '+fq_whole, shell=True)
subprocess.call('rm temp*',shell=True)


