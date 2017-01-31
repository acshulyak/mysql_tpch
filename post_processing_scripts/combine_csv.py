#!/usr/bin/python

import os
import sys

files = []

print sys.argv[1],sys.argv[2],sys.argv[3]

remove_col = sys.argv[3]

file_names = os.listdir('.')

for file_name in file_names:
	if (sys.argv[2] in file_name) and (".csv" in file_name):
		files.append(open(file_name, "r"))

outfile = open(sys.argv[1], "w")

data = {"column_names": [], "column_data": []}

i = 0
f_file = True
for f in files:
	data["column_names"].append([])
	data["column_data"].append([])
	first = True
	clear = -1
	for line in f:
		line = line.strip()
		if first:
			data["column_names"][i] = line.split(',')
			if remove_col in data["column_names"][i] and f_file == False:
				print "here"
				clear = data["column_names"][i].index(remove_col)
				data["column_names"][i].pop(clear)
			else:
				clear = -1
				f_file = False
			data["column_names"][i] = [str(i)+"_"+cn for cn in data["column_names"][i]]
			#data["column_names"][i] = [data["column_names"][i][-1]]+data["column_names"][i][:-1]
			first = False
		else:
			line = line.split(',')
			if clear != -1:
				line.pop(clear)
			#line = [line[-1]]+line[:-1]
			data["column_data"][i].append(line)
	i += 1

outfile.write(",".join([",".join(cn) for cn in data["column_names"]])+"\n")

num_row = max([len(f_col) for f_col in data["column_data"]])
for i in range(num_row):
	out_line = []
	for f in range(len(data["column_data"])):
		if len(data["column_data"][f]) > i:
			out_line += data["column_data"][f][i]
		else:
			out_line += [""] * len(data["column_names"][f])
	outfile.write(",".join(out_line)+"\n")

for f in files:
	f.close()

outfile.close()