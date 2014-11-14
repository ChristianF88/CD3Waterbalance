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
from itertools import cycle
from numpy import size, asarray


def getoutputdata(location_files1):
    #getting outputvector
    #location_files1='C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\outputfiles'
    file_names=os.listdir(str(location_files1)[0:])

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
    Outputvector=np.asarray(Outputvector)
    print 'Outputvector has been created'      
    return

def getinputdata(location_files2, numberhh=5., totalarea=4301., lenindoor=9000):
    #getting inputvector
    #location_files2='C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\inputfiles'
    file_names=os.listdir(str(location_files2)[0:])

    rainevapo=[]
    namesrainevapo=[]
    indoor=[]
    namesindoor=[]

    for i in range(len(file_names)): 
        if file_names[i][(len(file_names[i])-3):len(file_names[i])] == 'ixx':
            file_name=file_names[i]
            csv_file = open(str(location_files2) +"\%s" % file_name, "r")
            data = csv.reader(csv_file, delimiter='\t')
            mylist = list(data)
            if len(mylist)>lenindoor:
                rainevapo.append(mylist)
                namesrainevapo.append(file_names[i])
            else:
                indoor.append(mylist)
                namesindoor.append(file_names[i])
    #creating vector right size    
    global rainevapovector, indoorvector      
    rainevapovector=[['error']*(len(namesrainevapo)+1) for m in range(size(rainevapo[0],0)-1)]
    indoorvector=[['error']*(len(namesindoor)+1) for m in range(size(indoor[0],0))]
    #writing time colum    
    for i in range(size(rainevapo[0],0)-1):
        rainevapovector[i][0]=float(date2num(datetime.strptime(rainevapo[1][i+1][0]+" "+rainevapo[1][i+1][1],"%d.%m.%Y %H:%M:%S")))
    for i in range(size(indoor[0],0)):
        indoorvector[i][0]=float(date2num(datetime.strptime(indoor[1][i][0]+" "+indoor[1][i][1],"%d.%m.%Y %H:%M:%S")))
    #writing Values of inputfiles in vector
    for i in range((len(namesrainevapo)+1))[1:]:
        for n in range(size(rainevapo[0],0)-1):
            rainevapovector[n][i]=float(rainevapo[i-1][n+1][2])
    for i in range((len(namesindoor)+1))[1:]:
        for n in range(size(indoor[0],0)):
            indoorvector[n][i]=float(indoor[i-1][n][2])
    
    #correcting unit and volume!
    rainevapovector=np.asarray(rainevapovector)
    indoorvector=np.asarray(indoorvector)
    for i in range(len(namesrainevapo)+1)[1:]:
        rainevapovector[:,i]=rainevapovector[:,i]/1000*totalarea
    for i in range(len(namesindoor)+1)[1:]:
        indoorvector[:,i]=indoorvector[:,i]/1000*numberhh*(float(indoorvector[2][0])-float(indoorvector[1][0]))*24
    #giving header for future reference
    rainevapovector=rainevapovector.tolist()
    rainevapovector.insert(0,['time']*(len(namesrainevapo)+1))
    for i in range(len(namesrainevapo)+1)[1:]:
        rainevapovector[0][i]=namesrainevapo[i-1][:(len(namesrainevapo[i-1])-4)]
    indoorvector=indoorvector.tolist()
    indoorvector.insert(0,['time']*(len(namesindoor)+1))
    for i in range(len(namesindoor)+1)[1:]:
        indoorvector[0][i]=namesindoor[i-1][:(len(namesindoor[i-1])-4)]
    rainevapovector = np.asarray(rainevapovector)   
    indoorvector = np.asarray(indoorvector) 
    print 'Indoorvector and RainEvapovector have been created'
    return 
        



#Possible Input: Outdoor Demand, Indoor demand, all filenames (without endings)
def plotter(Vector1, Vector2, Vector3,limx, limy, toplot=[] ):
    #Vector1=indoorvector
    #Vector2=rainevapovector
    #Vector3=Outputvector
    #toplot=['bath', 'dishwasher', 'Raintank1', 'Sewer', 'rain', 'Outdoor_Demand', 'Indoor_Demand']
    #liste der zu plottenden sachen erzeugen
    global listtoplot
    listtoplot=[]
    for i in range(len(toplot)):
        #searching vector headers for inputstrings, writes in plotting list
        if toplot[i] in Vector1[0]:
            for n in range(len(Vector1[0])):
                if toplot[i]==Vector1[0][n]:
                    listtoplot.append([Vector1[:,0], Vector1[:,n]])                       
        elif toplot[i] in Vector2[0]:
            for n in range(len(Vector2[0])):
                if toplot[i]==Vector2[0][n]:
                    listtoplot.append([Vector2[:,0], Vector2[:,n]])                      
        elif toplot[i] in Vector3[0]:
            for n in range(len(Vector3[0])):
                if toplot[i]==Vector3[0][n]:
                    listtoplot.append([Vector3[:,0], Vector3[:,n]])   
        elif toplot[i] == 'Outdoor_Demand':
            allheaders=Vector1.tolist()[0]+Vector2.tolist()[0]+Vector3.tolist()[0]
            for n in range(len(allheaders)):
                if toplot[i]==repr(allheaders[n])[1:15]:
                    position=n
            if position<=len(Vector1[0]):
                a=1
            elif position<=len(Vector2[0]):
                a=2
            else:
                a=3
            exec 'variable=Vector'+str(a)
            storageOD=asarray([0.0 for m in range(len(variable))])
            for i in range(len(variable[0])):
                if repr(variable[0][i])[1:15] == 'Outdoor_Demand':
                    for n in range(len(variable))[1:]:
                        storageOD[n] += float(variable[n][i])
            storageOD=storageOD.tolist()
            storageOD[0]='Outdoor_Demand'
            listtoplot.append([variable[:,0], storageOD])
        elif toplot[i] == 'Indoor_Demand':
            allheaders=Vector1.tolist()[0]+Vector2.tolist()[0]+Vector3.tolist()[0]
            for n in range(len(allheaders)):
                if 'toilet'==(allheaders[n]):
                    position=n
            if position<=len(Vector1[0]):
                a=1
            elif position<=len(Vector2[0]):
                a=2
            else:
                a=3
            exec 'variable=Vector'+str(a)
            storageID=asarray([0.0 for m in range(len(variable))])
            for i in range(len(variable[0]))[1:]:
                for n in range(len(variable))[1:]:
                    storageID[n] += float(variable[n][i])
            storageID=storageID.tolist()
            storageID[0]='Indoor_Demand'
            listtoplot.append([variable[:,0], storageID])
        else:
            print 'Error: Wrong input name!'
    #LEGENDE!!!save pic if wanted
    pl.figure(figsize=(20, 10), dpi=80)
    pl.xlim(float(Vector1[1][0])+float(limx[0]), float(Vector1[1][0]) + float(limx[1]))
    pl.ylim(float(limy[0]), float(limy[1]))
    lines = ["-","--","-.",":"]
    linecycler = cycle(lines)
    for i in range(len(toplot)):
        exec 'pl.plot(asarray(listtoplot['+str(i)+'])[0][1:],asarray(listtoplot['+str(i)+'])[1][1:], linewidth=2.5, linestyle = next(linecycler), label=toplot['+str(i)+'])'
    pl.legend(loc='right')
    pl.show()

    return



def theholelot(outputfiles='C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\outputfiles', inputfiles='C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\inputfiles', numberhh=5, totalarea=4301):
    getoutputdata(outputfiles)
    getinputdata(inputfiles, numberhh, totalarea)
    plotter(indoorvector, rainevapovector, Outputvector,[0,365],[0,10], ['evapo', 'bath', 'dishwasher', 'Raintank1', 'rain', 'Outdoor_Demand'])
    print 'done'
    return








#def main():
#getoutputdata('C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\outputfiles')
#getinputdata('C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\inputfiles',5 , 4301)

theholelot()

#if __name__=='__main__': main()












