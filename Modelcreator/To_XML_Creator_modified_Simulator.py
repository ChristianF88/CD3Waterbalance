# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:46:53 2015

@author: Gerhard
"""


import subprocess
import csv
import os
import numpy as np
import pylab as pl
from datetime import datetime
from matplotlib.dates import date2num, num2date
from itertools import cycle
from numpy import size, asarray

class TheHoleLot:

    def __init__(self):
        self.Rainevapovector = []
        self.Outputvector = []
        self.area_fractions1 = []
        self.Fractioncalculatorvec = []
        self.Lossvector = []
        self.total_area = 0.0
        self.total_perv_area=0.0
        self.wettingloss = 0.0
        self.depressionloss = 0.0
        
        return
        
    #killing the cd3 process (if necessary) and deleting old ouput .txt files
    def Deleter(self,location_files1='C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\outputfiles'):
            os.system("taskkill /cd3.exe")
            todelete = [ f for f in os.listdir(location_files1) if f.endswith(".txt") ]
            for i in range(len(todelete)):
                os.remove(location_files1+"\%s" % todelete[i])
            return
    
    #executing programm
    def runcd3(self,cd3path = 'C:\Program Files (x86)\CityDrain3\\bin\cd3.exe', filename = 'C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\outputfiles\Test.xml'):
            print "Starting and running City Drain!"
            cd3 = r'"""'+cd3path+'"   '+filename+'""'         
            p = subprocess.Popen(cd3, shell=True)
            p.wait()
            return
    def Find(self,string):
            num=''
            for i in range(len(string)):
                if string[i] !='"' and string[i] !='>' and string[i] !='/' and string[i] !='':
                    num+=string[i]
                else:
                    pass
            num=float(num)
            return num
    def Decide(self,arg1,arg2):
            num=0.
            if arg1 in arg2:
                num=self.Find(arg2.split(arg1)[1])
            else:
                pass
            return num
    def Read(self,location, deli="\n"):
            txt = open(location, "r")  
            data = csv.reader(txt, delimiter=deli)  
            mylist = list(data)
            return mylist
    def DEV(self,Liste,a,b):
        value=0
        try:
            value=self.Decide('<parameter name="Catchment_Area_[m^2]" type="double" value="',Liste[a+b][0])
        except IndexError:
            pass
        return value
    #specify location xml file! reads catchment attributes 
    def Fractioncalculator(self,location):
        Liste=self.Read(location,"\n")
        numofcatchments=0.
        FIAR=0.
        FISD=0.
        FPA=0.
        TA=0.
        DF=0.
        DL=0.
        WL=0.
        SWC=0.
        SD=0.
        for i in range(len(Liste)):
            if 'class="Catchment_w_Routing">' in Liste[i][0]:
                numofcatchments+=1.
            else:
                pass
            FIAR1=self.Decide('<parameter name="Fraktion_of_Impervious_Area_to_Reservoir_iAR_[-]" type="double" value="',Liste[i][0])
            FISD1=self.Decide('<parameter name="Fraktion_of_Impervious_Area_to_Stormwater_Drain_iASD_[-]" type="double" value="',Liste[i][0])
            FPA1=self.Decide('<parameter name="Fraktion_of_Pervious_Area_pA_[-]" type="double" value="',Liste[i][0])
            TA1=self.Decide('<parameter name="Catchment_Area_[m^2]" type="double" value="',Liste[i][0])
            DF+=self.Decide('<parameter name="Drying_Factor_[-]" type="double" value="',Liste[i][0])
            DL+=self.Decide('<parameter name="Depression_Loss_[mm]" type="double" value="',Liste[i][0])
            WL+=self.Decide('<parameter name="Wetting_Loss_[mm]" type="double" value="',Liste[i][0])
            SWC+=self.Decide('<parameter name="Initial_Water_Content_[-]" type="double" value="',Liste[i][0])
            SD+=self.Decide('<parameter name="Depth_Of_Soil_[m]" type="double" value="',Liste[i][0])
            FIAR+=FIAR1*self.DEV(Liste,i,11)
            FISD+=FISD1*self.DEV(Liste,i,10)
            FPA+=FPA1*self.DEV(Liste,i,1)
            TA+=TA1
        self.soilwatercontent=SWC
        self.soildepth=SD
        self.wettingloss = WL/numofcatchments
        self.depressionloss = DL/numofcatchments 
        self.drying_rate = DF/numofcatchments
        self.total_area = TA
        self.total_perv_area = FPA
        self.area_fractions1=[FPA/TA,FIAR/TA,FISD/TA]
        return    
    
    '''
    Evapo_Model, Rain_Model need to be the file names of the filereaders and pattern implemers output
    '''    
    
    #getting model outputdata
    def getoutputdata(self,location_files1):
        file_names=os.listdir(str(location_files1)[0:])
        alltogether = []
        names = []
        for i in range(len(file_names)): 
            if file_names[i][(len(file_names[i])-3):len(file_names[i])] == 'txt':
                file_name=file_names[i]
                csv_file = open(str(location_files1) +"\%s" % file_name, "r")
                data = csv.reader(csv_file, delimiter='\t')
                mylist = list(data)
                csv_file.closed
                alltogether.append(mylist)
                names.append(file_names[i])
                csv_file.close()
 
        #creating vector right size
        self.Outputvector=[['error']*(len(alltogether)+1) for m in range(len(alltogether[0]))]
        #writing header
        self.Outputvector[0][0]='Time'
        for i in range(len(alltogether)):
            self.Outputvector[0][i+1]=names[i][:(len(names[i])-4)]
        #writing time colum
        for i in range(len(alltogether[0]))[1:]:
            self.Outputvector[i][0]=float(date2num(datetime.strptime(alltogether[1][i][0][:19],"%d.%m.%Y %H:%M:%S")))
        #writing Values of txtfiles in vector
        for i in range((len(alltogether)+1))[1:]:
            for n in range(len(alltogether[0]))[1:]:
                self.Outputvector[n][i]=float(alltogether[i-1][n][1])
        #Evapo Model and Rain Model are the filenames of the filereaders and pattern implemers output!!! (Filenames hove to be specified as fileout names in XML Creator)
        for i in range(len(self.Outputvector[0])):
            if self.Outputvector[0][i] == 'Evapo_Model':
                for n in range(len(self.Outputvector))[1:]:
                    self.Outputvector[n][i]=float(self.Outputvector[n][i])/1000*self.total_area
            if self.Outputvector[0][i] == 'Rain_Model':
                for n in range(len(self.Outputvector))[1:]:
                    self.Outputvector[n][i]=float(self.Outputvector[n][i])/1000*self.total_area
        self.Outputvector=np.asarray(self.Outputvector)
        print '\n'
        print"______________________________________________________________________________________________________"
        print 'Outputvector has been created'       
        return 
    
    def getinputdata(self,location_files2):
        #getting inputvector
        #location_files2='C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\inputfiles'
        file_names=os.listdir(str(location_files2)[0:])
        rainevapo=[]
        namesrainevapo=[]
        for i in range(len(file_names)): 
            if file_names[i][(len(file_names[i])-3):len(file_names[i])] == 'ixx':
                file_name=file_names[i]
                csv_file = open(str(location_files2) +"\%s" % file_name, "r")
                data = csv.reader(csv_file, delimiter='\t')
                mylist = list(data)
                rainevapo.append(mylist)
                namesrainevapo.append(file_names[i])
        #creating vector right size        
        self.Rainevapovector=[['error']*(len(namesrainevapo)+1) for m in range(size(rainevapo[0],0)-1)]
        #writing time colum    
        for i in range(size(rainevapo[0],0)-1):
            self.Rainevapovector[i][0]=float(date2num(datetime.strptime(rainevapo[1][i+1][0]+" "+rainevapo[1][i+1][1],"%d.%m.%Y %H:%M:%S")))
        #writing Values of inputfiles in vector
        for i in range((len(namesrainevapo)+1))[1:]:
            for n in range(size(rainevapo[0],0)-1):
                self.Rainevapovector[n][i]=float(rainevapo[i-1][n+1][2])
        #correcting unit and volume!
        self.Rainevapovector=np.asarray(self.Rainevapovector)
        for i in range(len(namesrainevapo)+1)[1:]:
            self.Rainevapovector[:,i]=self.Rainevapovector[:,i]/1000*self.total_area
        #giving header for future reference
        self.Rainevapovector=self.Rainevapovector.tolist()
        self.Rainevapovector.insert(0,['time']*(len(namesrainevapo)+1))
        for i in range(len(namesrainevapo)+1)[1:]:
            self.Rainevapovector[0][i]=namesrainevapo[i-1][:(len(namesrainevapo[i-1])-4)]
        self.Rainevapovector = np.asarray(self.Rainevapovector)   
        print 'RainEvapovector have been created'
        return 
    def GETARRAY(self,liste,string):
        date=[]
        array=[]
        a=0
        for i in range(len(liste[0])):
            if liste[0][i] == string:
                a=i
            else:
                pass
        for i in range(len(liste))[1:]:
            date.append(float(liste[i][0]))
            array.append(float(liste[i][a]))
        #if storage files are not present
        if a==0:
            date=[0]
            array=[0]
        else:
            pass
        array=np.asarray(array)
        return date,array
        #tocheck (all, Evapo, Rain, Indooruse, Outdoordemand?, System)
        #area_fractions = [perv, imperv_to_storage, imperv_to_stormw]
    def Balance(self):
        #tocheck=['Evapo', 'Rain', 'System']
        #Data=[Rainevapovector, Outputvector]
        Data = [self.Rainevapovector, self.Outputvector]
        colorred = "\033[01;31m{0}\033[00m"

        #evapotranspiration check
        #evap is the ixx files name thats the file readers input, Evapo_Model is the name specified in the XML Creator (Output Pattern Implementer)
        DETM,ETM=self.GETARRAY(self.Outputvector,'Evapo_Model')
        DETI,ETI=self.GETARRAY(self.Rainevapovector,"evap")
        evapomodel=sum(ETM)
        evapoinput=sum(ETI)
        ErrorFRPI=(1 - evapomodel/evapoinput) * 100
        print 'The difference of given and produced Evapotranspiraten calculated by the Pattern Implementer and Filereader due to rounding errors is '+ colorred.format(str(ErrorFRPI))+' %'
        
        #rain check    
        #rain is the ixx files name thats the file readers input, Rain_Model is the name specified in the XML Creator (Output Filereader)
        DRM,RM=self.GETARRAY(self.Outputvector,'Rain_Model')
        DRI,RI=self.GETARRAY(self.Rainevapovector,"rain")
        rainmodel = sum(RM)
        raininput = sum(RI)
        ErrorFR=(1 - rainmodel/raininput) * 100
        print 'The difference of given and produced Rain calculated by the Filereader due to rounding errors is '+ colorred.format(str(ErrorFR))+' %'

        
              
        DS1,S1=self.GETARRAY(self.Outputvector,"Rainwatertanklevels") 
        DS2,S2=self.GETARRAY(self.Outputvector,"Greywaterreservoirlevels")
        DS3,S3=self.GETARRAY(self.Outputvector,"Stormwaterreservoirlevels")
        DS4,S4=self.GETARRAY(self.Outputvector,"Greywatertanklevels")
        DSWD,SWD=self.GETARRAY(self.Outputvector,"Stormwaterdrain")
        DSewerV,SewerV=self.GETARRAY(self.Outputvector,"Sewer")
        DPWR,PWR=self.GETARRAY(self.Outputvector,"Potable_Water_Demand")
        DODD,ODD=self.GETARRAY(self.Outputvector,"Outdoordemand")
        DAET,AET=self.GETARRAY(self.Outputvector,"ET")
        DEX,EX=self.GETARRAY(self.Outputvector,"ex")
        DSS,SS=self.GETARRAY(self.Outputvector,"Soilstorage")
        DGW,GW=self.GETARRAY(self.Outputvector,"Gardenwateringstorage")
        DI,I=self.GETARRAY(self.Outputvector,"Infiltration")

            
        #Rain and Evapo inlcuding losses - calculates losses wit average wetting loss and depression loss
        rainminusevapolosses = 0.0
        lossstorage = 0.0
        lossmem=0.0
        onlyrain=0.0
        timestepl = round((float(self.Outputvector[2][0])-float(self.Outputvector[1][0]))*24*3600)
        print timestepl
        for i in range(len(ETM))[1:]:
            lossmem=lossstorage
            lossstorage+= RM[i]/self.total_area*1000
            if RM[i] > 0.0:
                if lossstorage> self.depressionloss + self.wettingloss:
                    difference= self.depressionloss + self.wettingloss - lossmem
                    rainminusevapolosses += RM[i]- difference*self.total_area/1000.
                    lossstorage = self.depressionloss + self.wettingloss
                else:
                    pass
            else:
                #simulation drying via evapotranspiration
                if lossstorage > 0.0:
                    lossstorage -= (ETM[i]*self.drying_rate)/self.total_area*1000
                    if lossstorage < 0.0:
                        lossstorage = 0.0
                    else:
                        pass
                else:
                    lossstorage =  0.0

            onlyrain += RM[i]
            initiallosses=onlyrain-rainminusevapolosses
            
        In=sum(PWR)+onlyrain+GW[-1]
        Out=sum(SewerV)+sum(SWD)+sum(EX)+sum(AET)+initiallosses
        deltaS=(S1[-1] -S1[0])+(S2[-1]-S2[0])+(S3[-1]-S3[0])+(S4[-1]-S4[0]) + (SS[-1]-SS[0])  
        print 'Fraction of Pervious Area: '+str(self.area_fractions1[0])
        print 'Fraction of Impervious Area to Reservoir: '+str(self.area_fractions1[1])
        print 'Fraction of Impervious Area to Stormdrain: '+str(self.area_fractions1[2])
        print 'Wetting Loss: '+str( self.wettingloss)+' mm'
        print 'Depression Loss: '+str(self.depressionloss)+' mm'
        print 'Drying Factor: '+str(self.drying_rate)
        print 'Total Rain: '+str(onlyrain) + ' m^3'
        print 'Inital Losses only: '+str(onlyrain-rainminusevapolosses)+' m^3'
        print 'Potable_Water_Demand: '+str(sum(PWR))+' m^3'
        print 'Outdoordemand: '+str(sum(ODD))+' m^3'
        print 'Rain minus all Losses: '+str(rainminusevapolosses)+' m^3'
        print 'Sewer: '+str(sum(SewerV))+' m^3'
        print 'Stormwaterdrain: '+str(sum(SWD))+' m^3'
        print 'Infiltration: '+str(sum(I))+' m^3'
        print 'Exfiltration: '+str(sum(EX)+' m^3'
        print 'Actual Evapotranspiration: '+str(sum(AET))+' m^3'
        print 'Actual Evapotranspiration: '+str(sum(AET/self.total_perv_area*1000))+' mm'
        print 'Stored in Tanks: '+str(S1[-1]+S2[-1]+S3[-1]+S4[-1])+' m^3'
        print 'GardenWateringModule: '+str(GW[-1])+' m^3'
        print 'Soilstorage: '+str((SS[-1]-SS[0]))+' m^3'
        print 'Initial Water Content '+str(self.soilwatercontent)
        print 'Delta Water Content '+str((SS[-1]-SS[0])/(self.soildepth*self.total_area))
        print 'Absolut Error of entire balance: '+str(In-Out-deltaS)+' m^3'
        print 'Realtive Error of entire balance: '+str(100*(In-Out-deltaS)*2/(In+Out+deltaS))+' %'
        print"______________________________________________________________________________________________________"
        
        return 
    
    
    
    #Possible Input: Outdoor_Demand, Indoor_Demand, all (plots everthing), all filenames (without endings)
    def Plotter(self,size=[12,10],limx=[0,365], limy=[0,1], toplot=['Rain_Model', 'Stormwaterdrain', 'Evapo_Model', 'effective_rain','Indoor_Demand','Outdoordemand'] ):
        self.listtoplot = []
        Vector1 = self.Rainevapovector
        Vector2 = self.Outputvector
        for i in range(len(toplot)):
            #searching vector headers for inputstrings, writes in plotting list
            if toplot[i] in Vector1[0]:
                for n in range(len(Vector1[0])):
                    if toplot[i]==Vector1[0][n]:
                        self.listtoplot.append([Vector1[:,0], Vector1[:,n]])                       
            elif toplot[i] in Vector2[0]:
                for n in range(len(Vector2[0])):
                    if toplot[i]==Vector2[0][n]:
                        self.listtoplot.append([Vector2[:,0], Vector2[:,n]])                        
            elif toplot[i] == 'Outdoordemand':
                allheaders=Vector1.tolist()[0]+Vector2.tolist()[0]
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
                    if repr(variable[0][i])[1:14] == 'Outdoordemand':
                        for n in range(len(variable))[1:]:
                            storageOD[n] += float(variable[n][i])
                storageOD=storageOD.tolist()
                storageOD[0]='Outdoordemand'
                self.listtoplot.append([variable[:,0], storageOD])
                
                #while time inbetween 2 days sum up and append
                outdoordemandsum=0.0
                dailyoutdoordemand=[]
                fulldaystart=ceil(float(variable[:,0][1]))
                fulldayend=floor(float(variable[:,0][-1]))
                i=1
                for n in range(int(fulldayend-fulldaystart)+1):
                    if float(variable[:,0][i]) < (int(fulldaystart)):
                        while float(variable[:,0][i]) <= (int(fulldaystart)+ n):
                            i+=1
                    else:
                        while float(variable[:,0][i]) >= (int(fulldaystart) + n-1) and float(variable[:,0][i]) < (int(fulldaystart) + n): 
                            outdoordemandsum += float(storageOD[i])
                            i += 1
                        dailyoutdoordemand.append(outdoordemandsum)
                        outdoordemandsum=0.0
                        dailyoutdoordemand_per_sm=mean(dailyoutdoordemand)/(self.area_fractions1[0]*self.total_area)
                print 'The average Outdoordemand per square meter for the simulated time frame is: '+str(dailyoutdoordemand_per_sm)+' m³/(m²d)'
                
            elif toplot[i] == 'all':
                for n in range(len(Vector1[0]))[1:]:
                    self.listtoplot.append([Vector1[:,0], Vector1[:,n]])                      
                for n in range(len(Vector2[0]))[1:]:
                    self.listtoplot.append([Vector2[:,0], Vector2[:,n]])                      
                    
            elif toplot[i] == 'effective_rain':
                if len(Vector1[0])==len(effective_rain):
                    self.listtoplot.append([Vector1[:,0], effective_rain])
                else:
                    self.listtoplot.append([Vector2[:,0], effective_rain])
    
                        
            else:
                print 'Error: Wrong input name!'
        #LEGEND!!!save pic if wanted
        pl.figure(figsize=(size[0], size[1]), dpi=80)
        pl.xlim(float(Vector1[1][0])+float(limx[0]), float(Vector1[1][0]) + float(limx[1]))
        pl.ylim(float(limy[0]), float(limy[1]))
        lines = ["-","--","-.",":"]
        linecycler = cycle(lines)
        for i in range(len(self.listtoplot)):
            exec 'pl.plot(asarray(self.listtoplot['+str(i)+'])[0][1:],asarray(self.listtoplot['+str(i)+'])[1][1:], linewidth=2.5, linestyle = next(linecycler), label=self.listtoplot['+str(i)+'][1][0])'
        pl.legend(loc='best')
        pl.title('Model In - and Output', fontsize=20)
        pl.xlabel('Time [d]')
        pl.ylabel('Volume [m^3]')
        pl.grid(True)
        pl.show()
        print 't=0: '+str(float(Vector1[1][0]))
        print 'The time range plotted: '+str([num2date(float(Vector1[1][0]) + float(limx[0])).strftime("%d.%m.%Y %H:%M:%S"), 
                                                 num2date(float(Vector1[1][0]) + float(limx[1])).strftime("%d.%m.%Y %H:%M:%S")])
        return

    





