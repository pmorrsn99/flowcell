#!/usr/bin/env python
# /lab/dev/users/pmorrison/python/get_flowcell_type.py

from __future__ import print_function
import sys
import os
from datetime import datetime
now = datetime.now()
now = str(now.date())
print(now)

"""Check flowcell types for sequencer run files not yet archived.
python ~/get_flowcell_type.py
print file by 
"""

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
seq_flowcell_mode = {}  # Flowcells modes by sequencer
seqtypes = []
outfile = open("Sequencers_flowcell_types_"+now+".csv",'w')
outfile1 = open("Flowcell_type_by_sequencer_"+now+".csv",'w')

for seq in Sequencers: 
    if seq in Novaseqs:
        seqtype = "NovaSeq"
        file = '/RunParameters.xml'
    elif seq in Hiseqs:
        seqtype = "HiSeq"
        file = '/runParameters.xml'
    if seqtype not in seqtypes:
        seqtypes.append(seqtype)
    if seq not in seq_flowcell_mode:
        seq_flowcell_mode[seq] = []  # flowcell mode by sequencer
    seq_path = Sequencers[seq]
    flowcell_dirs = os.listdir(seq_path)
    for fc in flowcell_dirs:
        if "." in fc or "_" not in fc:
            continue
        run_param_file = seq_path+'/'+fc+file
        if os.path.isfile(run_param_file):
            if seqtype == "NovaSeq" and seq.split("-")[1].upper() != run_param_file.split("/")[-2].split("_")[1]:
                #print(seq.split("-")[1].upper(),"===",run_param_file.split("/")[-2].split("_")[1])
                continue
            with open(run_param_file,'r') as infile:
                if seqtype == "NovaSeq":
                    for line in infile:
                        if "<FLOWCELLMODE>" in line.upper():
                            mode = line.split(">")[1].split("<")[0]
                elif seqtype == "HiSeq":
                    for line in infile:
                        if "<FLOWCELL>" in line.upper():
                            mode = line.split(">")[1].split("<")[0]
                            mode = mode.split(" ")[-1]
            seq_flowcell_mode[seq].append((fc,mode))
            outfile.write(seqtype+","+seq_path+'/'+fc+","+mode+"\n")
            
outfile.close()
for seq in Sequencers:
    count += 1
    outfile1.write(str(count)+": "+seq+"\n")
    for a in seq_flowcell_mode[seq]:
        (name,mode) = a
        outfile1.write(mode+","+name+"\n")


outfile1.close()
print("Done!!")
