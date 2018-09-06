import re,sys,pdb
import numpy as np
import matplotlib.pyplot as plt

contig_file=sys.argv[1]
vcf_file=sys.argv[2]

contig_dict = {}
with open(contig_file, 'r') as f:
    for line in f:
        if line.startswith('>'):
            title=line[1:].strip().split()[0]
        else:
            seq=line.strip()
            assert not title in contig_dict, "Contig aready exist!"+'\t'+title
            contig_dict[title] = seq

num_contigs = len(contig_dict)
plt.figure(figsize=(10, 10*num_contigs))

con_profile_dict = {}
for con in contig_dict:
    con_profile = np.zeros(len(contig_dict[con]))
    con_profile_dict[con] = con_profile

with open(vcf_file, 'r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        lmap=line.strip().split('\t')
        con,pos,info = lmap[0],lmap[1],lmap[7]
        m=re.search('DP=(\d+);',info)
        depth=int(m.group(1))
        con_profile_dict[con][int(pos)-1] = depth

fig_idx = 1
for con in con_profile_dict:
    plt.subplot(num_contigs,1,fig_idx)
    plt.plot(con_profile_dict[con])
    plt.title(con)
    plt.xlabel('Contig Position')
    plt.ylabel('Depth')
    fig_idx+=1

figname='Contigs_profile.png'
plt.savefig(figname,format='png',dpi=300)
plt.close()

