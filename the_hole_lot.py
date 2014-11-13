# -*- coding: utf-8 -*-
"""
Created on Thu Oct 02 08:41:08 2014

@author: Acer
"""


import csv
import os
import numpy as np
import pylab as pl
from datetime import datetime
from matplotlib.dates import date2num

def getoutputdata(location_files1):
    #getting outputvector
    #location_files1='C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\outputfiles'
    file_names=os.listdir(str(location_files1='C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\outputfiles')[0:])

    alltogether = []
    names = []

    for i in range(len(file_names)): 
        if file_names[i][(len(file_names[i])-3):len(file_names[i])] == 'txt':
            file_name=file_names[i]
            csv_file = open(str(location_files1) +"\%s" % file_name, "r")
            data = csv.reader(csv_file, delimiter='\t')
            mylist = list(data)
            alltogether.append(mylist)
            names.append(file_names[i])
    #creating vector right size
    global Outputvector
    Outputvector=[['error']*len(file_names) for m in range(size(alltogether,1))]
    #writing header
    Outputvector[0][0]='Time'
    for i in range(size(alltogether,0)):
        Outputvector[0][i+1]=names[i][:(len(names[i])-4)]
    #writing time colum
    for i in range(size(alltogether,1))[1:]:
        Outputvector[i][0]=float(date2num(datetime.strptime(alltogether[1][i][0][:19],"%d.%m.%Y %H:%M:%S")))
    #writing Values of inputfiles in vector
    for i in range((len(alltogether)+1))[1:]:
        for n in range(size(alltogether,1))[1:]:
            Outputvector[n][i]=float(alltogether[i-1][n][1])
    #checks whether all values have been inserted
    for i in range(size(Outputvector,0)):
        if 'error' in Outputvector[i]:
            print 'A problem has occured, please check getoutputdata() function'
            print 'The problem has occured in line '+str(i)+' of the Outputvector'
        else:
            pass
    global Outputvector_without_header
    Outputvector_without_header=np.asarray(Outputvector[1:])
    print 'Outputvector and Outputvector without header has been created'      
    return

def getinputdata(location_files2):
    #getting inputvector
    #location_files2='C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\inputfiles'
    file_names=os.listdir(str(location_files2='C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\inputfiles')[0:])

    alltogether=[]
    names=[]

    for i in range(len(file_names)): 
        if file_names[i][(len(file_names[i])-3):len(file_names[i])] == 'ixx':
            file_name=file_names[i]
            csv_file = open(str(location_files2) +"\%s" % file_name, "r")
            data = csv.reader(csv_file, delimiter='\t')
            mylist = list(data)
            alltogether.append(mylist)
            names.append(file_names[i])
    #creating vector right size    
    global Inputvector        
    Inputvector=[['error']*(len(file_names)+1) for m in range(size(alltogether[0],0)+1)]
    #writing header
    Inputvector[0][0]='Time'
    for i in range(len(file_names)+1)[1:]:
        Inputvector[0][i]=names[i-1][:(len(names[i-1])-4)]
    #writing time colum    
    for i in range(size(alltogether[0],0)+1)[1:]:
        Inputvector[i][0]=float(date2num(datetime.strptime(alltogether[1][i-1][0]+" "+alltogether[1][i-1][1],"%d.%m.%Y %H:%M:%S")))
    #writing Values of inputfiles in vector
    for i in range((len(file_names)+1))[1:]:
        for n in range(size(alltogether[0],0)+1)[1:]:
            Inputvector[n][i]=float(alltogether[i-1][n-1][2])
    #checks whether all values have been inserted
    for i in range(size(Inputvector,0))[1:]:
        if 'error' in Inputvector[i]:
            print 'A problem has occured, please check getinputdata() function'
            print 'The problem has occured in line '+str(i)+'of the Inputvector'
        else:
            pass
    global Inputvector_no_header
    Inputvector_no_header=np.asarray(Inputvector[1:])
    print 'Inputvector and Inputvector without header has been created'
    return 
        

#converting units to m or m^3 
#vector=Inputvector_no_header
#unitlist=['time', 'l/h', 'l/h','mm', 'mm', 'l/h', 'l/h', 'l/h', 'l/h']
def unitconverter(vector=Inputvector_no_header, unitlist=['time', 'l/h', 'l/h','mm', 'mm', 'l/h', 'l/h', 'l/h', 'l/h']):
    flowlist=[]
    heightlist=[]
    for i in range(len(unitlist)):
        if unitlist[i] == 'l/h':
            flowlist.append(i)
        elif unitlist[i] == 'mm':
            heightlist.append(i)
        else:
            pass
    if (flowlist) == []:
        if heightlist == []:
            print 'The inputdata does have the wrong unit format for this function.' 
            print "The unitconverter() can only handle 'mm' and 'l/h'"
    for i in heightlist:
        vector[:,i] = vector[:,i]/1000
    for i in flowlist:
        vector[:,i] = vector[:,i]/1000*(vector[1][0]-vector[0][0])*24
    global Inputvector_no_header_correct_units 
    Inputvector_no_header_correct_units = vector
    print 'Inputvector_no_header_correct_unit has been created'
    #plausible?
    #summe=0.0
    #for n in range(24):
    #    for i in flowlist:
    #        summe+=vector[n][i]
    #print summe
    return
#possible input number of HH(of same inputfiles), total Area
def rightvolume(vector=Inputvector_no_header_correct_units, numberhh=5, totalarea=4301, order= ['time', 'l/h', 'l/h','mm', 'mm', 'l/h', 'l/h', 'l/h', 'l/h']):
    toHHlist=[]
    toArealist=[]
    for i in range(len(unitlist)):
        if unitlist[i] == 'l/h':
            toHHlist.append(i)
        elif unitlist[i] == 'mm':
            toArealist.append(i)
        else:
            pass
    for i in toArealist:
        vector[:,i] = vector[:,i]*totalarea
    for i in toHHlist:
        vector[:,i] = vector[:,i]*numberhh
    global Volume_into_system 
    Volume_into_system = vector
    print 'Volume_into_system has been created'
    return

#Possible Input: HH, Outdoor Demand, Indoor demand, all filenames (without endings)
def plotter(toplot=[]):
    #liste der zu plottenden sachen erzeugen
    listtoplot=
    for i in range(len(toplot)):
        if toplot[i] in vector...:
            
            plot        
                        
        elif name in vector...:
        
            plot
    
    return



def theholelot(outputfiles='C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\outputfiles', inputfiles='C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\inputfiles', units=['time', 'l/h', 'l/h','mm', 'mm', 'l/h', 'l/h', 'l/h', 'l/h']):
    getoutputdata(outputfiles)
    getinputdata(inputfiles)
    unitconverter(Inputvector_no_header, units)
    rightvolume(Inputvector_no_header_correct_units, 5, 4301, ['time', 'l/h', 'l/h','mm', 'mm', 'l/h', 'l/h', 'l/h', 'l/h'])
    print 'done'
    return


plotter()











a=np.asarray(date_2_num[0])
b=np.asarray(date_2_num[1])
c=np.asarray(date_2_num[2])/1000
d=np.asarray(date_2_num[3])
e=np.asarray(date_2_num[4])
f=np.asarray(date_2_num[5])/1000
g=np.asarray(date_2_num[6])

pl.figure(figsize=(18, 10), dpi=80)
pl.xlim(730120, 0.17+730120)
#pl.ylim(0.0, 30)
pl.plot(a[:,0],a[:,1], color="blue", linewidth=2.5, linestyle="-", label=file_names[0])
pl.plot(b[:,0],b[:,1], color="green", linewidth=3.5, linestyle="--", label=file_names[1])
pl.plot(c[:,0],c[:,1], color="red", linewidth=2.5, linestyle="-", label=file_names[2])
pl.plot(d[:,0],d[:,1], color="yellow", linewidth=2.5, linestyle="--", label=file_names[3])
pl.plot(e[:,0],e[:,1], color="magenta", linewidth=2.5, linestyle="--", label=file_names[4])
pl.plot(f[:,0],f[:,1], color="black", linewidth=3.5, linestyle="-", label=file_names[5])
pl.plot(g[:,0],g[:,1], color="cyan", linewidth=2.5, linestyle="--", label=file_names[6])
pl.legend(loc='upper right')
pl.show()

#def main():
getoutputdata()
getinputdata()
unitconverter()
rightvolume()
theholelot()

#if __name__=='__main__': main()