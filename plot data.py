# -*- coding: utf-8 -*-
"""
Created on Thu Oct 02 08:41:08 2014

@author: Acer
"""

# import data
# collect it
# export data

import csv
import os
import numpy as np
import pylab as pl

file_names=os.listdir('C:\Users\Acer\Documents\GitHub\CD3Waterbalance\check')[0:]
list_csv=zeros((len(file_names),1)).tolist()
final_list=zeros((len(file_names),1)).tolist()

for i in range(len(file_names)): 
    file_name=file_names[i]
    
    with open("C:\Users\Acer\Documents\GitHub\CD3Waterbalance\check\%s" % file_name) as csvfile:
        data=csv.reader(csvfile, delimiter=',', quotechar='$')     
        
        global list_csv
        
        for row in data:
            list_csv[i].append(', '.join(row))
    if list_csv[i][1][0] == ' ':
        final_list[i] = list_csv[i][2:-1]
    else:
        final_list[i] = list_csv[i][2:-1]

date_2_num=[[1]*len(final_list[0]) for m in range(len(file_names))]

from datetime import datetime, date, time

for i in range(len(final_list)):
    for n in range(len(final_list[1])):
        date_2_num[i][n]=([date2num(datetime.strptime(final_list[i][n].split()[0]+" "+final_list[i][n].split()[1],"%d.%m.%Y %H:%M:%S")),float(final_list[i][n].split()[2])])
   
a=np.asarray(date_2_num[0])
b=np.asarray(date_2_num[1])
c=np.asarray(date_2_num[2])
d=np.asarray(date_2_num[3])
e=np.asarray(date_2_num[4])
f=np.asarray(date_2_num[5])
g=np.asarray(date_2_num[6])

pl.figure(figsize=(18, 10), dpi=80)
#pl.xlim(730120, 0.5+730120)
#pl.ylim(0.0, 0.0007)
pl.plot(a[:,0],a[:,1], color="blue", linewidth=2.5, linestyle="-", label=file_names[0])
pl.plot(b[:,0],b[:,1], color="green", linewidth=3.5, linestyle="--", label=file_names[1])
pl.plot(c[:,0],c[:,1], color="red", linewidth=2.5, linestyle="-", label=file_names[2])
pl.plot(d[:,0],d[:,1], color="yellow", linewidth=2.5, linestyle="--", label=file_names[3])
pl.plot(e[:,0],e[:,1], color="magenta", linewidth=2.5, linestyle="--", label=file_names[4])
pl.plot(f[:,0],f[:,1], color="black", linewidth=3.5, linestyle="-", label=file_names[5])
pl.plot(g[:,0],g[:,1], color="cyan", linewidth=2.5, linestyle="--", label=file_names[6])
pl.legend(loc='upper left')
pl.show()

##https://scipy-lectures.github.io/intro/matplotlib/matplotlib.html
## Create a figure of size 8x6 inches, 80 dots per inch
#pl.figure(figsize=(8, 6), dpi=80)
## Create a new subplot from a grid of 1x1
#pl.subplot(1, 1, 1)
#X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
#C, S = np.cos(X), np.sin(X)
## Plot cosine with a blue continuous line of width 1 (pixels)
#pl.plot(X, C, color="blue", linewidth=1.0, linestyle="-")
## Plot sine with a green continuous line of width 1 (pixels)
#pl.plot(X, S, color="green", linewidth=1.0, linestyle="-")
## Set x limits
#pl.xlim(-4.0, 4.0)
## Set x ticks
#pl.xticks(np.linspace(-4, 4, 9, endpoint=True))
## Set y limits
#pl.ylim(-1.0, 1.0)
## Set y ticks
#pl.yticks(np.linspace(-1, 1, 5, endpoint=True))
## Save figure using 72 dots per inch
# savefig("exercice_2.png", dpi=72)
## Show result on screen
#pl.show()
#plot(a[:,0],a[:,1], b[:,0],b[:,1], c[:,0],c[:,1], d[:,0],d[:,1], e[:,0],e[:,1])

