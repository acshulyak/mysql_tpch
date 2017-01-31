#!usr/bin/python

import sys

inFile = open(sys.argv[1], "r")
outFile = open(sys.argv[1]+".csv", "w")

io_list = []
cpu_list = []

isCpu = False
isIo = 0
for line in inFile:
  line = line.strip()
  if "avg-cpu:" in line:
    isCpu = True
  elif "Device:" in line:
    isIo = 1 
    io_list.append({"tps": 0.0, "kB_read/s": 0.0, "kB_wrtn/s": 0.0, "kB_read": 0.0, "kB_wrtn": 0.0})
  elif isCpu == True:
    items = line.split(" ")
    items = filter(None, items)
    print items
    cpu_list.append({"%user": items[0], "%nice": items[1], "%system": items[2], "%iowait": items[3], "%steal": items[4], "%idle": items[5]})
    isCpu = False
  elif isIo != 0:
    items = line.split(" ")
    items = filter(None, items)
    io_list[-1]["tps"] += float(items[1])
    io_list[-1]["kB_read/s"] += float(items[2])
    io_list[-1]["kB_wrtn/s"] += float(items[3])
    io_list[-1]["kB_read"] += float(items[4])
    io_list[-1]["kB_wrtn"] += float(items[5])
    if isIo < 4:
      isIo += 1
    else:
      isIo = 0

cpu_title = cpu_list[0].keys()
io_title = io_list[0].keys()
title = cpu_title+io_title
outFile.write(",".join(title)+"\n")

for i in range(min(len(cpu_list),len(io_list))):
  values = [str(cpu_list[i][key]) for key in cpu_title] + [str(io_list[i][key]) for key in io_title]
  print values
  outFile.write(",".join(values)+"\n")

outFile.close()
inFile.close()


