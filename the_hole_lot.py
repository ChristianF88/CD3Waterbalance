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


def getoutputdata(location_files1, totalarea=485.1):
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
    Outputvector=[['error']*(len(alltogether)+1) for m in range(size(alltogether,1))]
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
            
    for i in range(len(Outputvector[0])):
        if Outputvector[0][i] == 'evapo_model':
            for n in range(len(Outputvector))[1:]:
                Outputvector[n][i]=float(Outputvector[n][i])/1000*totalarea
        if Outputvector[0][i] == 'rain_model':
            for n in range(len(Outputvector))[1:]:
                Outputvector[n][i]=float(Outputvector[n][i])/1000*totalarea
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

def getinputdata(location_files2, numberhh=1., totalarea=485.1, lenindoor=9000):
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
    global Rainevapovector, Indoorvector      
    Rainevapovector=[['error']*(len(namesrainevapo)+1) for m in range(size(rainevapo[0],0)-1)]
    Indoorvector=[['error']*(len(namesindoor)+1) for m in range(size(indoor[0],0))]
    #writing time colum    
    for i in range(size(rainevapo[0],0)-1):
        Rainevapovector[i][0]=float(date2num(datetime.strptime(rainevapo[1][i+1][0]+" "+rainevapo[1][i+1][1],"%d.%m.%Y %H:%M:%S")))
    for i in range(size(indoor[0],0)):
        Indoorvector[i][0]=float(date2num(datetime.strptime(indoor[1][i][0]+" "+indoor[1][i][1],"%d.%m.%Y %H:%M:%S")))
    #writing Values of inputfiles in vector
    for i in range((len(namesrainevapo)+1))[1:]:
        for n in range(size(rainevapo[0],0)-1):
            Rainevapovector[n][i]=float(rainevapo[i-1][n+1][2])
    for i in range((len(namesindoor)+1))[1:]:
        for n in range(size(indoor[0],0)):
            Indoorvector[n][i]=float(indoor[i-1][n][2])
    
    #correcting unit and volume!
    Rainevapovector=np.asarray(Rainevapovector)
    Indoorvector=np.asarray(Indoorvector)
    for i in range(len(namesrainevapo)+1)[1:]:
        Rainevapovector[:,i]=Rainevapovector[:,i]/1000*totalarea
    for i in range(len(namesindoor)+1)[1:]:
        Indoorvector[:,i]=Indoorvector[:,i]/1000*numberhh*(float(Indoorvector[2][0])-float(Indoorvector[1][0]))*24
    #giving header for future reference
    Rainevapovector=Rainevapovector.tolist()
    Rainevapovector.insert(0,['time']*(len(namesrainevapo)+1))
    for i in range(len(namesrainevapo)+1)[1:]:
        Rainevapovector[0][i]=namesrainevapo[i-1][:(len(namesrainevapo[i-1])-4)]
    Indoorvector=Indoorvector.tolist()
    Indoorvector.insert(0,['time']*(len(namesindoor)+1))
    for i in range(len(namesindoor)+1)[1:]:
        Indoorvector[0][i]=namesindoor[i-1][:(len(namesindoor[i-1])-4)]
    Rainevapovector = np.asarray(Rainevapovector)   
    Indoorvector = np.asarray(Indoorvector) 
    print 'Indoorvector and RainEvapovector have been created'
    return 
        



#Possible Input: Outdoor_Demand, Indoor_Demand, all (plots everthing), all filenames (without endings)
def plotter(Vector1, Vector2, Vector3,limx, limy, toplot=[] ):
    #Vector1=Indoorvector
    #Vector2=Rainevapovector
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
            
        elif toplot[i] == 'all':
            for n in range(len(Vector1[0]))[1:]:
                listtoplot.append([Vector1[:,0], Vector1[:,n]])                      
            for n in range(len(Vector2[0]))[1:]:
                listtoplot.append([Vector2[:,0], Vector2[:,n]])                      
            for n in range(len(Vector3[0]))[1:]:
                listtoplot.append([Vector3[:,0], Vector3[:,n]])           
        else:
            print 'Error: Wrong input name!'
    #LEGENDE!!!save pic if wanted
    pl.figure(figsize=(20, 10), dpi=80)
    pl.xlim(float(Vector1[1][0])+float(limx[0]), float(Vector1[1][0]) + float(limx[1]))
    pl.ylim(float(limy[0]), float(limy[1]))
    lines = ["-","--","-.",":"]
    linecycler = cycle(lines)
    for i in range(len(listtoplot)):
        exec 'pl.plot(asarray(listtoplot['+str(i)+'])[0][1:],asarray(listtoplot['+str(i)+'])[1][1:], linewidth=2.5, linestyle = next(linecycler), label=listtoplot['+str(i)+'][1][0])'
    pl.legend(loc='left')
    pl.show()

    return

    #tocheck (all, Evapo, Rain, Indooruse, Outdoordemand?, System)
def Bilanz(Data, tocheck, lossfactor = 0, totalarea = 485.1):
    #tocheck=['Evapo', 'Rain', 'System']
    #Data=[Rainevapovector, Outputvector, Indoorvector]
    colorred = "\033[01;31m{0}\033[00m"
    for i in range(len(tocheck)):
        #evapotranspiration check
        if tocheck[i] == 'Evapo':
            evapomodel = 0.0
            evapoinput = 0.0
            for i in range(len(Data)):
                for n in range(len(Data[i][0])):
                    if Data[i][0][n] == 'evapo':
                        for m in range(len(Data[i][:,n]))[1:]:
                            evapoinput += float(Data[i][:,n][m])
                    elif Data[i][0][n] == 'evapo_model':
                        for m in range(len(Data[i][:,n]))[1:]:            
                            evapomodel += float(Data[i][:,n][m])
            ErrorFRPI=(1 - evapomodel/evapoinput) * 100
            print 'The difference of given and produced Evapotranspiraten calculated by the Pattern Implementer and Filereader due to rounding errors is '+ colorred.format(str(ErrorFRPI))+' %'
        #rain check    
        elif tocheck[i] == 'Rain':
            rainmodel = 0.0
            raininput = 0.0
            for i in range(len(Data)):
                for n in range(len(Data[i][0])):
                    if Data[i][0][n] == 'rain':
                        for m in range(len(Data[i][:,n]))[1:]:
                            raininput += float(Data[i][:,n][m])
                    elif Data[i][0][n] == 'rain_model':
                        for m in range(len(Data[i][:,n]))[1:]:            
                            rainmodel += float(Data[i][:,n][m])
            ErrorFR=(1 - rainmodel/raininput) * 100
            print 'The difference of given and produced Rain calculated by the Filereader due to rounding errors is '+ colorred.format(str(ErrorFR))+' %'
        #total system
        #Lists have to be in alphabetical order
        elif tocheck[i] == 'System': 
            
            totalstorage = []
            totalstoragelist = ['GreyWaterTank', 'Raintank1', 'Raintank2', 'Raintank3']
            inputER=[]
            inputERlist = ['evapo_model', 'rain_model']
            outputISSP = []
            outputISSPlist = ['Infiltration', 'PotableWaterDemand', 'Sewer', 'Stormwater']
            for i in range(len(Data)):
                for n in range(len(Data[i][0])):
                    if Data[i][0][n] in totalstoragelist:            
                        totalstorage.append(Data[i][:,n])
                    elif Data[i][0][n] in inputERlist:
                        inputER.append(Data[i][:,n])
                    elif Data[i][0][n] in outputISSPlist:
                        outputISSP.append(Data[i][:,n])
            
            totalstoragescalar = 0.0
            rainminusevapo = 0.0
            SewerStormwInfiltr = 0.0
            PWRonly = 0.0
            ETonly = 0.0
            amount = 0.0
            #Speicher
            for i in range(len(totalstorage)):
                totalstoragescalar += float(totalstorage[i][-1])
            #Potable_Water_Demand/Sewer,Infiltr.,Stormwater
            for i in range(len(outputISSP)):
                if outputISSPlist[i] == 'PotableWaterDemand':
                    for n in range(len(outputISSP[0]))[1:]:
                        PWRonly += float(outputISSP[i][n])
                else:
                    for n in range(len(outputISSP[0]))[1:]:
                        SewerStormwInfiltr -= float(outputISSP[i][n])
            #Rain and Evapo
            for i in range(len(inputER[0]))[1:]:
                if float(inputER[1][i]) > float(inputER[0][i]):
                    rainminusevapo += float(inputER[1][i])-float(inputER[0][i])
                    ETonly += float(inputER[0][i])
            #Losses
            for i in range(len(inputER[0]))[3:]: 
                if float(inputER[1][i-2]) == 0:
                    if float(inputER[1][i-1]) == 0:
                        if float(inputER[1][i]) != 0:
                            amount += 1
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            totallosses = amount * totalarea * lossfactor/1000
            #Outdoor_Demand
            
            total_error = abs(rainminusevapo - totallosses + SewerStormwInfiltr + PWRonly-totalstoragescalar)
            print (2 * total_error)/(totallosses+PWRonly+rainminusevapo+ETonly-SewerStormwInfiltr)
            print lossfactor
            print totalarea
            print 'PWR: '+str(PWRonly)
            print 'R-ET: '+str(rainminusevapo)
            print 'SewerStormwInfiltr: '+str(SewerStormwInfiltr)
            print 'Losses: '+str(totallosses)
            print 'R-ET - Losses - SewerStormwInfiltr: '+str(rainminusevapo+SewerStormwInfiltr-totallosses)
        #indooruse check
    
        #outdoor demand check
    
    
    return







def theholelot(outputfiles='C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\outputfiles', inputfiles='C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\inputfiles', numberhh=1, totalarea=485.1, Data=[Rainevapovector, Outputvector, Indoorvector], tocheck=['Evapo', 'Rain', 'System'], lossfactor = 0):
    getoutputdata(outputfiles)
    getinputdata(inputfiles, numberhh, totalarea)
    plotter(Indoorvector, Rainevapovector, Outputvector,[3,4],[0,0.1], ['evapo_model', 'rain_model', 'Infiltration', 'PotableWaterDemand', 'Sewer', 'Stormwater', 'evapo'])
    Bilanz(Data, tocheck, lossfactor, totalarea)
    print 'done'
    return








#def main():
#getoutputdata('C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\outputfiles')
#getinputdata('C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\inputfiles',5 , 4301)
#plotter(Indoorvector, Rainevapovector, Outputvector,[0,365],[0,2], ['all'])
theholelot()

#if __name__=='__main__': main()












