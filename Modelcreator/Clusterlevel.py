# -*- coding: utf-8 -*-
"""
Created on Mon Dec 01 16:42:52 2014

@author: Acer
"""

from Householdlevel import Householdlevel
from Global_counters import Global_counters

#clusterhouseholdvec = [ [Householdsize, Clusternumber], [], [], ..., []]

class Clusterlevel:
    def __init__(self, clusterhouseholdvec):
        self.allclusters = []
        for i in range(len(clusterhouseholdvec)):
            for n in range(clusterhouseholdvec[i][1]):
                Householdlevels = Householdlevel()
                Householdlevels.writeconnections(clusterhouseholdvec[i][0])
                self.allclusters.append(Householdlevels.Householdlevel_connection_list)
                
cluhouseholdvec = [[6,3],[8,21],[25,40],[3,10]]
Cluster = Clusterlevel(cluhouseholdvec)
Cluster.allclusters

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







