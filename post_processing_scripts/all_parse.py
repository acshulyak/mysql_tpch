#!usr/bin/python

import sys
import os

allFiles = os.listdir(os.getcwd())

for f_name in allFiles:
  if ".csv" not in f_name:
    os.system("python "+sys.argv[1]+" \'"+f_name+"\'")

