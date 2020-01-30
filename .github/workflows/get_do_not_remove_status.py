#!/usr/bin/env python
# /lab/dev/users/pmorrison/python/get_do_not_remove_status.py

from __future__ import print_function
import sys
import os
from datetime import datetime
now = datetime.now()
now = str(now.date())
print(now)

"""Check sequencer flowcells for do.not.remove files and get list of sequencers and flowcells and filepaths, where found.
python ~/python/get_do_not_remove_status.py
"""

outfile = open("Flowcell_donotremove_flags"+now+".csv",'w')
outfile1 = open("Flowcell_donotremove_summed_"+now+".csv",'w')

Sequencers = {}
Novaseqs = {'novaseq-a00214r':'/lab/seq/novaseq-a00214r','novaseq-a01016':'/lab/seq/novaseq-a01016','novaseq-a00144':'/lab/seq/novaseq-a00144',
 	'novaseq-a00493':'/lab/seq/novaseq-a00493','novaseq-a00341':'/lab/seq/novaseq-a00341','novaseq-a00780':'/seq/syn-novaseq-a00780',
    'novaseq-a00879':'/seq/syn-novaseq-a00780','novaseq-a00138':'/seq/syn-novaseq-a00138','novaseq-a00339':'/seq/syn-novaseq-a00339',
    'novaseq-a00862':'/seq/syn-novaseq-a00339'}
Hiseqs = {'hiseq-557':'/lab/seq/hiseq-557','hiseq-528':'/lab/seq/hiseq-528','hiseq-03 (810, 455, 260)':'/seq/syn-hiseq-03'}

Sequencers.update(Novaseqs)
Sequencers.update(Hiseqs)

#/seq/syn-novaseq-a00339/190202_A00339_0146_AHJ35YDMXX/:
#/lab/seq/hiseq-557/190628_D00557_0813_ACDV88ANXX/:

count = 0
countseq = {}  # do.not.remove by seq type
donotrem = {}  # do.not.remove files by sequencers
donotcount = {}  # do.not.remove file counts by seq
seqtypes = []
for seq in Sequencers: #.keys():
    if seq in Novaseqs:
        seqtype = "NovaSeq"
    elif seq in Hiseqs:
        seqtype = "Hiseq"
    if seqtype not in seqtypes:
        seqtypes.append(seqtype)
    if seqtype not in donotrem:
        donotrem[seqtype] = {}  # do.not.remove files by sequencers
    seq_path = Sequencers[seq]
    flowcell_dirs = os.listdir(seq_path)
    for fc in flowcell_dirs:
        if "." in fc or "_" not in fc:
            continue
        do_not_remove_file = seq_path+'/'+fc+'/do.not.remove'
        if os.path.isfile(do_not_remove_file): #       if os.path.isdir(seq_dir+'/'+flowcell_dir):
            if seqtype == "NovaSeq" and seq.split("-")[1].upper() != do_not_remove_file.split("_")[1].upper():
                continue
            count += 1
            if seq not in donotrem[seqtype]:
                donotrem[seqtype][seq]=[do_not_remove_file]
            else:
                donotrem[seqtype][seq].append(do_not_remove_file)

for st in seqtypes:
    if st not in countseq:
        countseq[st] = 0        

    for flcell in donotrem[st]:
        countseq[st] +=  len(donotrem[st][flcell])
        outfile1.write("Found "+str(len(donotrem[st][flcell]))+" do.not.remove "+flcell+" "+st+" flowcells.\n")
        for p in donotrem[st][flcell]:
            outfile.write(flcell+","+st+","+p+"\n")

outfile.close()
outfile1.close()
for st in countseq:
    print("SUMMING",st,countseq[st])

print(count)


