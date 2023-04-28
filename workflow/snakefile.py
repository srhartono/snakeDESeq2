# Snakefile

import sys
import glob
import os
import re
from SRHcolorz import LCY, LGN, YW, LRD, LPR, BLU, LGY, die

MAIN_DIR = os.path.abspath("./")

myconfig = dict()
extensions = ["count", "bed8", "bed", "R", "gtf"]

for ext in extensions:
	lines = glob.glob(f"*.{ext}")
	for line in lines:
		partz = re.sub("\.[a-zA-Z0-9]+$","",line)
		if ext in myconfig:
			myconfig[ext].append(partz)
			myconfig[ext] = [v.strip('"') for v in myconfig[ext]]
		else:
			myconfig[ext] = [partz]
			myconfig[ext] = [v.strip('"') for v in myconfig[ext]]

configfilez = f"{MAIN_DIR}/configfile.txt"
#print(configfilez)

with open(configfilez, "r") as f:
	for line in f:
		partz = line.strip().split("=")
		ext = partz[0]
		value = partz[1]
		valuepartz = re.sub("\.[a-zA-Z0-9]+\"$","",value)


		#print("ext2=",ext," : ",partz,", valuepartz=",valuepartz)

		if ext in myconfig:
			myconfig[ext].append(valuepartz)
			myconfig[ext] = [v.strip('"') for v in myconfig[ext]]
		else:
			myconfig[ext] = [valuepartz]
			myconfig[ext] = [v.strip('"') for v in myconfig[ext]]
	#for ext in myconfig:
		#print(ext," : ",myconfig[ext])

#die()

#for key in myconfig:
	#value = myconfig[key]
	#print(f"keyz={LCY(key)}, value={LGN(value)}")

#fileinput = list()
#extinput = list()
A_init_dir_and_files_output = list()
for ext in myconfig:
	for file in myconfig[ext]:
		#print(file)
#		fileinput.append(f"{file}")
#		extinput.append(f"{ext}")
		A_init_dir_and_files_output.append(f"{MAIN_DIR}/workflow/{ext}/{file}.{ext}")

A_init_dir_and_files_output = [v.strip('"') for v in A_init_dir_and_files_output]


#ALWAYS FIRST ONE
rule all:
	input:
		A_init_dir_and_files_output

#make $MAIN_DIR/envs
rule A_init_dir_and_files:
	input:
		f"{MAIN_DIR}" + "/{fileName}.{ext}"
	output:
		f"{MAIN_DIR}" + "/workflow/{ext}/{fileName}.{ext}"
	shell:
		"/bin/ln -s {input} {output}"

rule B_CombineCount:
	input:
		f"{MAIN_DIR}" + "/workflow/count/{fileName}.count"
	params:
		dir=f"{MAIN_DIR}"
	output:
		f"{MAIN_DIR}" + "/workflow/counts/RNA.counts"
	shell:
		"CombineCount.pl -i ./ -o {params.dir}/workflow/counts/{fileName}.counts -b {params.dir}/workflow/counts/RNA.bed8"
