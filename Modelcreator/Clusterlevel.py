# -*- coding: utf-8 -*-
"""
Created on Mon Dec 01 16:42:52 2014

@author: Acer
"""

from Householdlevel import Householdlevel
from Global_counters import Global_counters
from Collector_globals import Collector_globals





class Clusterlevel:
    def __init__(self):
        self.Householdlevel_connection_list=[]
        self.number_of_raintanks_list = []
        self.number_of_households_list = []
        self.number_of_collectors_2_inports = []
        self.number_of_catchments = []
        self.allclusters = []
        
    def writeconnections(self, clusterhouseholdvec):
        #Preparing global Collector counters
        #getting collectorvector
        collvec = []
        for i in range(len(cluhouseholdvec)):
            collvec.append(cluhouseholdvec[i][0])
        CollClust = Collector_globals(collvec)
        
        for i in range(len(clusterhouseholdvec)):
            for n in range(clusterhouseholdvec[i][1]):
                Householdlevels = Householdlevel()
                Householdlevels.writeconnections(clusterhouseholdvec[i][0])
                self.allstrings1 = ''
                for m in range(len(Householdlevels.Householdlevel_connection_list)):
                    print i
                    print m
                    exec '''string1='\\t\\t\\t<connection id="'+str(Global_counters.number_of_connections)+'">\\n' '''
                    exec '''string2='\\t\\t\\t\\t<source node="Household_'+str(Householdlevels.number_of_households_list[m])+'" port="Grey_Water"/> \\n ' '''
                    exec '''string3='\\t\\t\\t\\t<sink node="Collector_'+str(eval('CollClust.number_of_collectors_'+str(clusterhouseholdvec[i][0])+'_inports'))+'" port="Inport_'+str(m+1)+'"/> \\n ' '''
                    exec '''string4='\\t\\t\\t</connection>\\n' '''
                    Global_counters.number_of_connections += 1
                    for o in range(4):
                        exec 'self.allstrings1 += string'+str(o+1)
                #print  self.allstrings1   
                exec 'CollClust.number_of_collectors_'+str(clusterhouseholdvec[i][0])+'_inports +=1'
                for m in range(len(Householdlevels.Householdlevel_connection_list)):
                    exec '''string5='\\t\\t\\t<connection id="'+str(Global_counters.number_of_connections)+'">\\n' '''
                    exec '''string6='\\t\\t\\t\\t<source node="Household_'+str(Householdlevels.number_of_households_list[m])+'" port="Grey_Water"/> \\n ' '''
                    exec '''string7='\\t\\t\\t\\t<sink node="Collector_'+str(eval('CollClust.number_of_collectors_'+str(clusterhouseholdvec[i][0])+'_inports'))+'" port="Inport_'+str(m+1)+'"/> \\n ' '''
                    exec '''string8='\\t\\t\\t</connection>\\n' '''
                    Global_counters.number_of_connections += 1
                    self.allstrings = ''
                    for o in range(4):
                        exec 'self.allstrings += string'+str(o+1)
                    
                #exec 'CollClust.number_of_collectors_'+str(clusterhouseholdvec[i][0])+'_inports +=1'
                    
                    
                    #to DO write strings in list!
                    
                    self.allclusters.append(Householdlevels.Householdlevel_connection_list[m])
                    
                    
                    

                #Householdlevels.number_of_raintanks_list[]
                #Householdlevels.number_of_households_list[]
                #Householdlevels.number_of_collectors_2_inports[]
                #Householdlevels.number_of_catchments[]
                    
                #self.allstrings = ''
                #for i in range(20):
                #    exec 'self.allstrings += string'+str(i+1)
                    
                    

#clusterhouseholdvec = [ [Number of Households (Buildings), Clusternumber], [], [], ..., []]
cluhouseholdvec = [[6,3],[8,20],[25,40],[3,10]] 
               
     
#number of inports for collectors

Cluster = Clusterlevel()
Cluster.writeconnections(cluhouseholdvec)
print Cluster.allclusters[-1]
#print Cluster.allclusters
#print Cluster.allclusters[1]

print Global_counters.number_of_households
print Global_counters.number_of_connections
print Global_counters.number_of_greywatertanks     
print Global_counters.number_of_raintanks
print Global_counters.number_of_collectors_2_inports
print Global_counters.number_of_distributors
print Global_counters.number_of_stormwaterpipes
print Global_counters.number_of_Sewer2s
print Global_counters.number_of_potablwaterreservoirs
print Global_counters.number_of_catchments







