#!/usr/bin/python

import os
import sys

file_names = os.listdir('.')

old_names = {}

for file_name in file_names:
	file_name = file_name.split("_")
	search = "_".join(file_name[0:2])
	if not old_names.has_key(search):
		print "python " + sys.argv[1] + " " + search + "_all.csv " + search + " time"
		os.system("python " + sys.argv[1] + " " + search + "_all.csv " + search + " time")
	old_names[search] = None