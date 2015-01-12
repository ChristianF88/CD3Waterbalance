# -*- coding: utf-8 -*-
"""
Created on Mon Jan 05 12:16:56 2015

@author: Acer
"""

from Need_to_have_modelinput import Need_to_have_modelinput
from Simulation_basic_setup import Simulation_basic_setup
from Catchmentsetup import Catchmentsetup
from Buildingsetup import Buildingsetup
from Stormwaterdrainsetup import Stormwaterdrainsetup
from Sewer2setup import Sewer2setup
from Potablewaterreservoirsetup import Potablewaterreservoirsetup
from Raintanksetup import Raintanksetup
from Greywatertanksetup import Greywatertanksetup
from Fileoutsetup import Fileoutsetup
from Collectorsetup import Collectorsetup
from Distributorsetup import Distributorsetup
from Demandmodelsetup import Demandmodelsetup
from Stormwaterreservoirsetup import Stormwaterreservoirsetup
from Supplylevel import Supplylevel
from Global_counters import Global_counters



''' Function to add additional Fileouts '''

def Additional_Fileouts(Connection_Name_List):
    Fileout_numbers_names = []
    for i in range(len(Connection_Name_List)):
        searchstring = '<connection id="'+str(Connection_Name_List[i][0])+'">'
        for u in range(len(Connectionlist)):
            if searchstring in Connectionlist[u]:
                #changing old connection
                start_cut = Connectionlist[u].index('<sink')
                stop_cut = Connectionlist[u].index('/>\n\t\t\t</connection>\n')+2
                sink_new_connection = Connectionlist[u][start_cut:stop_cut]
                Connectionlist[u] = Connectionlist[u].replace(Connectionlist[u][start_cut:stop_cut],'<sink node="FileOut_'+str(Global_counters.number_of_fileouts)+'" port="in"/>')
                
                #inserting new connection
                string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                string2='\t\t\t\t<source node="FileOut_'+str(Global_counters.number_of_fileouts)+'" port="out"/>\n' 
                string3='\t\t\t\t'+sink_new_connection+'\n' 
                string4='\t\t\t</connection>\n'
                Global_counters.number_of_connections += 1
                
                Fileout_numbers_names.append([Global_counters.number_of_fileouts, Connection_Name_List[i][1]])
                Global_counters.numbers_names_of_fileouts_list.append([Global_counters.number_of_fileouts,Connection_Name_List[i][1]])
                Connectionlist.append(string1+string2+string3+string4)
                Global_counters.number_of_fileouts += 1 
            else:
                pass
    Fileoutattrvec = []
    for i in range(len(Fileout_numbers_names)):
        Fileoutattrvec.append(Fileout_numbers_names[i][1])
    AddedFileouts = Fileoutsetup(len(Connection_Name_List), Fileout_numbers_names[0][0], out_file_name = 'Test.txt')        
    AddedFileouts.Setandwrite_attributes(len(Connection_Name_List), Fileout_numbers_names[0][0], Fileoutattrvec)
    
    for i in range(len(AddedFileouts.Fileoutnodelist)):
        Nodelist.append(AddedFileouts.Fileoutnodelist[i])


''' Creating Connections, Supplyvector necessary (explanation in the XML-Creator.md on Github in the doc folder) '''

supplyvec =[[[[[5,[1,0,1,0,0],[1,0,1],1],[3,[1,0,1],[1,1,1],2],1],[[2,[0,1],[0,0,0],1],[8,[1,0,1,0,0,1,1,0],[0,0,1],1],0],1]]]

Supplylevel = Supplylevel()
Supplylevel.writeconnections(supplyvec)


''' Attributes of Blocks!! (explanation in the XML-Creator.md on Github in the doc folder) '''

Catchattrvec=[[1,1.9,800,0.4,0.2,0.4,0.6,0.21,1.5,0.4,0.5,400,500,700,0.04,0.05,0.06],[1,1.8,10000,0.1,0.8,0.1,0.6,0.21,1.5,0.4,0.5,380,510,710,0.04,0.05,0.06],
              [1,2,900,0.3,0.3,0.4,0.6,0.21,1.5,0.4,0.5,420,520,690,0.04,0.05,0.06],[1,1.7,500,0.4,0.1,0.5,0.6,0.21,1.5,0.4,0.5,380,520,720,0.04,0.05,0.06],
[1,1.9,1400,0.0,0.6,0.4,0.6,0.21,1.5,0.4,0.5,400,500,700,0.04,0.05,0.06], [1,1.9,20000,0.0,1,0.0,0.6,0.21,1.5,0.4,0.5,400,500,700,0.04,0.05,0.06],
[1,1.9,1000,0.4,0.3,0.3,0.6,0.21,1.5,0.4,0.5,400,500,700,0.04,0.05,0.06],[1,2.1,1000,0.38,0.12,0.5,0.6,0.21,1.5,0.4,0.5,380,510,710,0.04,0.05,0.06],
[1,2,900,0.0,0.7,0.3,0.6,0.21,1.5,0.4,0.5,420,520,690,0.04,0.05,0.06],[1,1.9,20000,0.0,1,0.0,0.6,0.21,1.5,0.4,0.5,400,500,700,0.04,0.05,0.06],
[1,1.7,1200,0.4,0.1,0.5,0.6,0.21,1.5,0.4,0.5,380,520,720,0.04,0.05,0.06],[1,1.95,950,0.7,0.25,0.05,0.6,0.21,1.5,0.4,0.5,400,500,700,0.04,0.05,0.06], 
[1,1.9,2000,0.5,0.3,0.2,0.6,0.21,1.5,0.4,0.5,400,500,700,0.04,0.05,0.06],[1,1.9,20000,0.0,1,0.0,0.6,0.21,1.5,0.4,0.5,400,500,700,0.04,0.05,0.06],
[1,1.9,1800,0.2,0.2,0.6,0.6,0.21,1.5,0.4,0.5,400,500,700,0.04,0.05,0.06],[1,1.8,1000,0.0,0.9,0.1,0.6,0.21,1.5,0.4,0.5,380,510,710,0.04,0.05,0.06],
[1,1.9,20000,0.0,1,0.0,0.6,0.21,1.5,0.4,0.5,400,500,700,0.04,0.05,0.06],
[1,2,1450,0.7,0.1,0.2,0.6,0.21,1.5,0.4,0.5,420,520,690,0.04,0.05,0.06],[1,1.7,1100,0.5,0.1,0.4,0.6,0.21,1.5,0.4,0.5,380,520,720,0.04,0.05,0.06],
[1,1.9,1210,0.3,0.1,0.6,0.6,0.21,1.5,0.4,0.5,400,500,700,0.04,0.05,0.06], [1,1.9,4000,0.5,0.2,0.3,0.6,0.21,1.5,0.4,0.5,400,500,700,0.04,0.05,0.06],
[1,1.9,800,0.4,0.2,0.4,0.6,0.21,1.5,0.4,0.5,400,500,700,0.04,0.05,0.06],[1,1.8,1000,0.0,0.8,0.2,0.6,0.21,1.5,0.4,0.5,380,510,710,0.04,0.05,0.06],
[1,2,900,0.3,0.3,0.4,0.6,0.21,1.5,0.4,0.5,420,520,690,0.04,0.05,0.06],[1,1.7,1500,0.4,0.1,0.5,0.6,0.21,1.5,0.4,0.5,380,520,720,0.04,0.05,0.06],
[1,1.9,20000,0.0,1,0.0,0.6,0.21,1.5,0.4,0.5,400,500,700,0.04,0.05,0.06]]
             
              
Greywaterattrvec = [[0.9,5]]*(Global_counters.number_of_greywatertanks) 

Stormwaterresattrvec = [[0.9,40]]*(Global_counters.number_of_stormwaterreservoirs)

Rainwaterattrvec = [[5]]*(Global_counters.number_of_raintanks)

Demandmodelattrvec = [[[4,4,3],[0]], [[5,2,3,4,8,6,5],[7,2,1,3]], [[3,4],[0]], [[5],[0]], [[0],[4]],
                      [[5],[0]],[[7],[0]],[[4],[0]],[[5],[1]],[[5],[0]],[[5],[0]],[[12],[0]],[[3],[0]],
[[5,4,2],[0]],[[5,4,2],[0]],[[5,4,2],[0]],[[5,5,6],[1]],[[3,2,5],[0]],[[2,4,5],[0]],[[5,5,5],[0]],[[3,2,3],[0]]]

Simulationsetupvec = ["2000-Jan-01 00:00:00", "2001-Jan-01 00:00:00", "360", "C:/Users/Acer/Documents/GitHub/CD3Waterbalance/Module/cd3waterbalancemodules.py"]

Needtohaveinputsvec = ["C:/Users/Acer/Documents/GitHub/CD3Waterbalance/simulationwithpatterns/inputfiles/rain.ixx", "C:/Users/Acer/Documents/GitHub/CD3Waterbalance/simulationwithpatterns/inputfiles/evapo.ixx", "13", "20.5"]

Collectorattrvec = []
for i in range(len(Global_counters.number_of_collectors_ports_list)):
    Collectorattrvec.append([Global_counters.number_of_collectors_ports_list[i][1]])
    
Distributorattrvec = []
for i in range(len(Global_counters.number_of_distributors_ports_list)):
    Distributorattrvec.append([Global_counters.number_of_distributors_ports_list[i][1]])
    
Fileoutattrvec = []
for i in range(len(Global_counters.numbers_names_of_fileouts_list)):
    Fileoutattrvec.append(Global_counters.numbers_names_of_fileouts_list[i][1])
    

''' Creating Nodes  '''


#creating nodes
Setupheader = Simulation_basic_setup(Simulationsetupvec[0], Simulationsetupvec[1], Simulationsetupvec[2], Simulationsetupvec[3])
Needtohaveinputs = Need_to_have_modelinput(Needtohaveinputsvec[0], Needtohaveinputsvec[1], Needtohaveinputsvec[2], Needtohaveinputsvec[3])
Catchments = Catchmentsetup(Global_counters.number_of_catchments ,0, Decay_Constant =1.9, Catchment_Area = 100, Fraktion_of_Impervious_Area_to_Reservoir_iAR= 0.4, Fraktion_of_Impervious_Area_to_Stormwater_Drain_iASD = 0.3, Fraktion_of_Pervious_Area_pA = 0.3, Number_of_Subareas = 1, Initial_Infiltration_Capacity = 0.6, Final_Infiltration_Capacity = 0.21, Depression_Loss = 1.5, Wetting_Loss = 0.4, Outdoor_Demand_Weighing_Factor = 0.5, Runoff_Runtime_iAR = 400, Runoff_Runtime_iASD = 500, Runoff_Runtime_pA = 700, Weighting_Coefficient_iAR = 0.04, Weighting_Coefficient_iASD = 0.05, Weighting_Coefficient_pA = 0.06)
Catchments.Setandwrite_attributes(Global_counters.number_of_catchments,0,Catchattrvec)
Buildings = Buildingsetup(Global_counters.number_of_buildings,0)
Stormwaterdrain =  Stormwaterdrainsetup(Global_counters.number_of_stormwaterpipes,0)
Sewers =  Sewer2setup(Global_counters.number_of_sewers,0)
Potablewaterreservoir = Potablewaterreservoirsetup(Global_counters.number_of_potablwaterreservoirs,0)
Greywatertank = Greywatertanksetup(Global_counters.number_of_greywatertanks,0,Yield_of_Treatment = 0.9, Storage_Volume = 15.0)
Greywatertank.Setandwrite_attributes(Global_counters.number_of_greywatertanks,0,Greywaterattrvec)
Raintank = Raintanksetup(Global_counters.number_of_raintanks,0, Storage_Volume = 10.0)
Raintank.Setandwrite_attributes(Global_counters.number_of_raintanks,0,Rainwaterattrvec)
Stormwaterreservoir = Stormwaterreservoirsetup(Global_counters.number_of_stormwaterreservoirs,0, Yield_of_Treatment = 0.9, Storage_Volume = 30.0)
Stormwaterreservoir.Setandwrite_attributes(Global_counters.number_of_stormwaterreservoirs,0,Stormwaterresattrvec)
Collectors=Collectorsetup(Global_counters.number_of_collectors,0,Number_of_Inports = 2)
Collectors.Setandwrite_attributes(Global_counters.number_of_collectors,0,Collectorattrvec)
Fileoutsneedtohave = Fileoutsetup(Global_counters.number_of_fileouts,0,out_file_name = 'Test.txt')
Fileoutsneedtohave.Setandwrite_attributes(Global_counters.number_of_fileouts,0,Fileoutattrvec)
Distributors = Distributorsetup(Global_counters.number_of_distributors,0,Number_of_Outports = 2)
Distributors.Setandwrite_attributes(Global_counters.number_of_distributors,0,Distributorattrvec)
Demandmodels = Demandmodelsetup(Global_counters.number_of_demandmodels,0,Number_of_Commercial_Units = [4], Number_of_Residential_Units=[4])
Demandmodels.Setandwrite_attributes(Global_counters.number_of_demandmodels,0,Demandmodelattrvec)

#wiritng all nodes in one list
Nodelist=[]
for i in range(len(Catchments.Catchmentnodelist)):
    Nodelist.append(Catchments.Catchmentnodelist[i])
for i in range(len(Buildings.Buildingnodelist)):
    Nodelist.append(Buildings.Buildingnodelist[i])
for i in range(len(Stormwaterdrain.Stormwaterpipenodelist)):
    Nodelist.append(Stormwaterdrain.Stormwaterpipenodelist[i])
for i in range(len(Sewers.Sewer2nodelist)):
    Nodelist.append(Sewers.Sewer2nodelist[i])
for i in range(len(Potablewaterreservoir.Potablewaterreservoirnodelist)):
    Nodelist.append(Potablewaterreservoir.Potablewaterreservoirnodelist[i])
for i in range(len(Raintank.Raintanknodelist)):
    Nodelist.append(Raintank.Raintanknodelist[i])
for i in range(len(Greywatertank.Greywatertanknodelist)):
    Nodelist.append(Greywatertank.Greywatertanknodelist[i])
for i in range(len(Collectors.Collectornodelist)):
    Nodelist.append(Collectors.Collectornodelist[i])
for i in range(len(Stormwaterreservoir.Stormwaterreservoirnodelist)):
    Nodelist.append(Stormwaterreservoir.Stormwaterreservoirnodelist[i])
for i in range(len(Fileoutsneedtohave.Fileoutnodelist)):
    Nodelist.append(Fileoutsneedtohave.Fileoutnodelist[i])
for i in range(len(Distributors.Distributornodelist)):
    Nodelist.append(Distributors.Distributornodelist[i])    
for i in range(len(Demandmodels.Demand_Modelnodelist)):
    Nodelist.append(Demandmodels.Demand_Modelnodelist[i])

#writing all connections in one list
Connectionlist = []
for i in range(len(Supplylevel.Supplylevel_list)):
    Connectionlist.append(Supplylevel.Supplylevel_list[i])   

# adding additional Fileouts
Connection_Name_List = [[407, 'Rain_Model.txt'],[435, 'Evapo_Model.txt']]
Additional_Fileouts(Connection_Name_List)        
    

''' creating XML - List '''

#Writing all strings in list:Mo
Allstrings=[]

#Basic Setup
Allstrings.append(Setupheader.Simulationsetupstring)
Allstrings.append(Needtohaveinputs.Modelinputnodesstring)

#Node List
for i in range(len(Nodelist)):
    Allstrings.append(Nodelist[i])

#Connectionlist
Allstrings.append('\t\t</nodelist>\n')
Allstrings.append('\t\t<connectionlist>\n')

for i in range(len(Connectionlist)):
    Allstrings.append(Connectionlist[i])

#Finish file
Allstrings.append('\t\t</connectionlist>\n')
Allstrings.append('\t</model>\n')
Allstrings.append('</citydrain>\n')


''' Writing List in an XML File '''

outFile = open('C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\outputfiles\Test.xml', 'w')
for i in range(len(Allstrings)):
    outFile.write( Allstrings[i])
outFile.close()







 