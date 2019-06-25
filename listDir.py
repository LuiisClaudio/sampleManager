#!/usr/bin/env python
from __future__ import print_function
import os
 
path = '\'

files = os.listdir(path)
#print(files)
name_dir = []
for name in files:
    name_dir.append(path + '\\' + name)
#print(name_dir)
for i in name_dir:
    samples = os.listdir(i)
    for s in samples:
        print(s)





















































        