# -*- coding: utf-8 -*-
"""
Created on Mon Dec 01 12:01:46 2014

@author: Acer
"""

from Need_to_have_modelinput import Need_to_have_modelinput
from Simulation_basic_setup import Simulation_basic_setup
from Catchmentsetup import Catchmentsetup
from Buildingsetup import Buildingsetup
from Stormwaterpipesetup import Stormwaterpipesetup
from Sewer2setup import Sewer2setup
from Potablewaterreservoirsetup import Potablewaterreservoirsetup
from Raintanksetup import Raintanksetup
from Greywatertanksetup import Greywatertanksetup
from Fileoutsetup import Fileoutsetup
from Collectorsetup import Collectorsetup
from Distributorsetup import Distributorsetup


Catchattrvec=[[0]*17]*1000      
Greywaterattrvec = [[0]*2]*10 
Rainwaterattrvec = [[0]]*10
Collectorattrvec = [[0]]*10
Distributorattrvec = [[0]]*10
Fileoutattrvec = [[0]]*10
Setupheader = Simulation_basic_setup("2000-Jan-01 00:00:00", "2001-Jan-01 00:00:00", "360", "C:/Users/Acer/Documents/GitHub/CD3Waterbalance/Module/cd3waterbalancemodules.py")
Needtohaveinputs = Need_to_have_modelinput("C:/Users/Acer/Documents/GitHub/CD3Waterbalance/simulationwithpatterns/inputfiles/rain.ixx", "C:/Users/Acer/Documents/GitHub/CD3Waterbalance/simulationwithpatterns/inputfiles/evapo.ixx", "13", "20,5")
Catchments = Catchmentsetup(1000 ,0, Decay_Constant =1.9, Catchment_Area = 100, Fraktion_of_Impervious_Area_to_Reservoir_iAR= 0.4, Fraktion_of_Impervious_Area_to_Stormwater_Drain_iASD = 0.3, Fraktion_of_Pervious_Area_pA = 0.3, Number_of_Subareas = 1, Initial_Infiltration_Capacity = 0.6, Final_Infiltration_Capacity = 0.21, Depression_Loss = 1.5, Wetting_Loss = 0.4, Outdoor_Demand_Weighing_Factor = 0.5, Runoff_Runtime_iAR = 400, Runoff_Runtime_iASD = 500, Runoff_Runtime_pA = 700, Weighting_Coefficient_iAR = 0.04, Weighting_Coefficient_iASD = 0.05, Weighting_Coefficient_pA = 0.06)
Catchments.Setandwrite_attributes(1000,0,Catchattrvec)
Buildings = Buildingsetup(10,0)
Stormwaterpipe =  Stormwaterpipesetup(1,0)
Sewers =  Sewer2setup(1,0)
Potablewaterreservoir = Potablewaterreservoirsetup(1,0)
Greywatertank = Greywatertanksetup(10,0,Yield_of_Treatment = 0.9, Storage_Volume = 15.0)
Greywatertank.Setandwrite_attributes(10,0,Greywaterattrvec)
Raintank = Raintanksetup(10,0, Storage_Volume = 10.0)
Raintank.Setandwrite_attributes(10,0,Rainwaterattrvec)
Collectors=Collectorsetup(10,0,Number_of_Inports = 2)
Collectors.Setandwrite_attributes(10,0,Collectorattrvec)
Fileouts = Fileoutsetup(10,0,out_file_name = 'Test.txt')
Fileouts.Setandwrite_attributes(10,0,Fileoutattrvec)
Distributors = Distributorsetup(10,0,Number_of_Outports = 2)
Distributors.Setandwrite_attributes(10,0,Distributorattrvec)




#Writing all strings in list:
Allstrings=[]
#Basic Setup
Allstrings.append(Setupheader.Simulationsetupstring)
Allstrings.append(Needtohaveinputs.Modelinputnodesstring)
#Node List
for i in range(len(Catchments.Catchmentnodelist)):
    Allstrings.append(Catchments.Catchmentnodelist[i])
for i in range(len(Buildings.Buildingnodelist)):
    Allstrings.append(Buildings.Buildingnodelist[i])
for i in range(len(Stormwaterpipe.Stormwaterpipenodelist)):
    Allstrings.append(Stormwaterpipe.Stormwaterpipenodelist[i])
for i in range(len(Sewers.Sewer2nodelist)):
    Allstrings.append(Sewers.Sewer2nodelist[i])
for i in range(len(Potablewaterreservoir.Potablewaterreservoirnodelist)):
    Allstrings.append(Potablewaterreservoir.Potablewaterreservoirnodelist[i])
for i in range(len(Raintank.Raintanknodelist)):
    Allstrings.append(Raintank.Raintanknodelist[i])
for i in range(len(Greywatertank.Greywatertanknodelist)):
    Allstrings.append(Greywatertank.Greywatertanknodelist[i])
for i in range(len(Collectors.Collectornodelist)):
    Allstrings.append(Collectors.Collectornodelist[i])
for i in range(len(Fileouts.Fileoutnodelist)):
    Allstrings.append(Fileouts.Fileoutnodelist[i])
for i in range(len(Distributors.Distributornodelist)):
    Allstrings.append(Distributors.Distributornodelist[i])    
    
#Connectionlist
Allstrings.append('\t\t</nodelist>\n')
Allstrings.append('\t\t\t<connectionlist>\n')


#Finish file
Allstrings.append('\t\t</connectionlist>\n')
Allstrings.append('\t</model>\n')
Allstrings.append('</citydrain>\n')



outFile = open('Test.xml', 'w')
for i in range(len(Allstrings)):
    outFile.write( Allstrings[i])
outFile.close()

 