# -*- coding: utf-8 -*-
"""
Created on Wed Dec 03 11:37:18 2014

@author: Acer
"""

from Global_counters import Global_counters
from Clusterlevel import Clusterlevel
#this class adds Greywatertanks to certain clusters
#vector is needed
#[[[6,[...],3],[7,[...],7], ...,1],[[6,[...],3],[7,[...],7], ...,1],[[6,[...],3],[7,[...],7], ...,0],...]
#[[[Numberof Buildings in Cluster, Number Clusters],...,Greywaterreservoir(1 = existing, 0 = no Greywaterreservoir)],...]
class Greywaterreservoirlevel:
    def __init__(self):
        self.Greywaterreservoirlevel_list = []
        self.additionaldemand_coll_list = []
        self.greywater_coll_list = []
        
    def writeconnections(self, greyvec):
        #Preparing lists with collector numbers that have certain amount of outports for later reference(values for nodes)
        for i in range(len(greyvec)):
                Cluster = Clusterlevel()
                Cluster.writeconnections(greyvec[i][:-1])
                
                if greyvec[i][-1] == 1:
                    # adds collector for checking stored volume Raintanks on a cluster level
                    self.additionaldemand_coll_strings=[]
                    add_dam_from_gw_listcounter = 0
                    add_dam_not_from_gw_listcounter = 0
                    for m in range(Cluster.number_of_clusters):
                        if Cluster.decision_not_from_gw_from_gw[m] == 1:
                            
                            
                            ##Problem jumping inbetween collectors!!!                            
                            
                            
                            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                            string2='\t\t\t\t<source node="Collector_'+str(Cluster.additionaldemand_from_gwr_coll_list[add_dam_from_gw_listcounter])+'" port="Outport"/> \n ' 
                            string3='\t\t\t\t<sink node="Greywatertank_'+str(Global_counters.number_of_greywatertanks)+'" port="Grey_Water_In"/> \n ' 
                            string4='\t\t\t</connection>\n' 
                            add_dam_from_gw_listcounter += 1
                            Global_counters.number_of_connections += 1
                        else:
                            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                            string2='\t\t\t\t<source node="Collector_'+str(Cluster.additionaldemand_not_from_gwr_coll_list[add_dam_not_from_gw_listcounter])+'" port="Outport"/> \n ' 
                            string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_Collectors)+'" port="Grey_Water_In"/> \n ' 
                            string4='\t\t\t</connection>\n' 
                            add_dam_not_from_gw_listcounter += 1
                            Global_counters.number_of_connections += 1
                        #writes all string in one and puts it in list
                        self.additionaldemandcollstrings = ''
                        for o in range(5)[1:]:
                            exec 'self.additionaldemandcollstrings += string'+str(o)
                            
                        self.additionaldemand_coll_strings.append(self.additionaldemandcollstrings)
                    #writes collector number in list that knows number of inports for later reference
                    Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, Cluster.number_of_clusters])
                    #writes collector number in list that knows connection for later reference
                    self.grey_coll_list.append(Global_counters.number_of_collectors)
                    Global_counters.number_of_collectors += 1
                    Global_counters.number_of_greywatertanks += 1
                else:
                    
                    
                    pass
                
                
                
                
                
                for m in range(len(Cluster.allclusters)):    
                    self.Greywaterreservoirlevel_list.append(Cluster.allclusters[m])
                for m in range(len(self.additionaldemandcollstrings)):
                    self.Greywaterreservoirlevel_list.append(self.additionaldemandcollstrings[m])

    
    #clusterbuildingvec = [ [Number of Buildings (Buildings), Clusternumber], [], [], ..., []]
    #clusterbuildingvec = [[6,1],[8,20],[25,40],[3,10]] 
               
    #number of inports for collectors
    #Cluster = Clusterlevel()
    #Cluster.writeconnections(clusterbuildingvec)
    #Cluster.allclusters



greyvec = [[[6,[1,0]*3,[1,1],3],[7,[1]*7,[0,0],7],[2,[0,1],[0,1],5],1]]#,[[4,[0,1]*2,[1,0],3],[15,[0,1,1,0,1]*3,[0,0],7],1],[[5,[0,0,0,0,1],[1,1],5],[10,[0]*10,[1,1],2],[8,[1,1,0,0,1,0,0,1],[0,1],2],[5,[1]*5,[1,0],5],[10,[0,1]*5,[1,0],2],[8,[0]*8,[1,0],2],0]]
Greytank = Greywaterreservoirlevel()
Greytank.writeconnections(greyvec)

print len(Greytank.Greywaterreservoirlevel_list)
print Global_counters.number_of_buildings
print Global_counters.number_of_connections
print Global_counters.number_of_greywatertanks     
print Global_counters.number_of_raintanks
print Global_counters.number_of_collectors
print Global_counters.number_of_distributors
print Global_counters.number_of_stormwaterpipes
print Global_counters.number_of_Sewer2s
print Global_counters.number_of_potablwaterreservoirs
print Global_counters.number_of_catchments
