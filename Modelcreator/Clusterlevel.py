# -*- coding: utf-8 -*-
"""
Created on Mon Dec 01 16:42:52 2014

@author: Acer
"""

from Buildinglevel import Buildinglevel
from Global_counters import Global_counters


class Clusterlevel:
    def __init__(self):
        self.allclusters = []
        self.greywater_to_sewer_coll_list = []
        self.greywater_to_reservoir_coll_list = []
        #self.blackwater_coll_list = []
        #self.potablewater_coll_list = []
        self.additionaldemand_from_gwr_coll_list = []
        self.additionaldemand_not_from_gwr_coll_list = []
        self.raintankstorage_coll_list = []
        self.runoff_coll_list = []
        self.overflow_coll_list = []
        self.street_list = []
        self.decision_not_from_gw_from_gw = []
        self.number_of_clusters = 0
        
        #self.infiltr_coll_list = []
        #self.outdoordemand = []
        
    def writeconnections(self, clusterbuildingvec):

        #circels through all elements of the clusterhouseholdsvector, calling the Householdclass, writing the Buildinglevel connections
        for i in range(len(clusterbuildingvec)):
            self.number_of_clusters += clusterbuildingvec[i][-1]            
            
            #adding collectors to runoff from catchment, overflowraintank, greywater, additional demand (from raintanks), raintank storage check
            #and one street for each cluster (as a catchment)
            for n in range(clusterbuildingvec[i][3]):
                Buildings = Buildinglevel()
                Buildings.writeconnections(clusterbuildingvec[i][:3])
                
                # adds catchment for as a street
                self.street_strings=[]
                string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                string2='\t\t\t\t<source node="Catchment_w_Routing_'+str(Global_counters.number_of_catchments)+'" port="Runoff"/> \n ' 
                string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_1"/> \n ' 
                string4='\t\t\t</connection>\n' 
                Global_counters.number_of_connections += 1
                Global_counters.number_of_catchments += 1
                #writes all string in one and puts it in list
                self.streetstrings = ''
                for o in range(5)[1:]:
                    exec 'self.streetstrings += string'+str(o)
                self.street_strings.append(self.streetstrings)

                # adds collector for runoff from catchment
                self.runoff_coll_strings=[]
                for m in range(len(Buildings.numbers_of_buildings_list)):
                    string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                    string2='\t\t\t\t<source node="Catchment_w_Routing_'+str(Buildings.numbers_of_catchments_list[m])+'" port="Runoff"/> \n ' 
                    string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(m+2)+'"/> \n ' 
                    string4='\t\t\t</connection>\n' 
                    Global_counters.number_of_connections += 1
                    #writes all string in one and puts it in list
                    self.runoffstrings = ''
                    for o in range(5)[1:]:
                        exec 'self.runoffstrings += string'+str(o)
                    self.runoff_coll_strings.append(self.runoffstrings)
                #writes collector number in list that knows number of inports for later reference
                Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, clusterbuildingvec[i][0]+1])
                #writes collector number in list that knows connection for later reference
                self.runoff_coll_list.append(Global_counters.number_of_collectors)
                Global_counters.number_of_collectors +=1
                
                # adds collector for greywater
                self.greywater_coll_strings=[]
                for m in range(len(Buildings.numbers_of_buildings_list)):
                    if type(Buildings.numbers_of_buildings_contributing_gw_list[m]) == str:
                        string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                        string2='\t\t\t\t<source node="Building_'+str(Buildings.numbers_of_buildings_list[m])+'" port="Grey_Water"/> \n ' 
                        string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(m+1)+'"/> \n ' 
                        string4='\t\t\t</connection>\n' 
                        Global_counters.number_of_connections += 1
                    else:
                        if type(Buildings.numbers_of_buildings_contributing_gw_list[m]) == int:
                            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                            string2='\t\t\t\t<source node="Building_'+str(Buildings.numbers_of_buildings_list[m])+'" port="Grey_Water"/> \n ' 
                            string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(m+1)+'"/> \n ' 
                            string4='\t\t\t</connection>\n' 
                            Global_counters.number_of_connections += 1
                        else:
                            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                            string2='\t\t\t\t<source node="Greywatertank_'+str(Buildings.numbers_of_greywatertanks_list[m][1])+'" port="Grey_Water_Overflow"/> \n ' 
                            string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(m+1)+'"/> \n ' 
                            string4='\t\t\t</connection>\n' 
                            Global_counters.number_of_connections += 1
                    #writes all string in one and puts it in list
                    self.greywaterstrings = ''
                    for o in range(5)[1:]:
                        exec 'self.greywaterstrings += string'+str(o)
                    self.greywater_coll_strings.append(self.greywaterstrings)
                #writes collector number in list that knows number of inports for later reference
                Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, clusterbuildingvec[i][0]])
                #writes collector number in list that knows connection for later reference                
                if type(Buildings.numbers_of_buildings_contributing_gw_list[0]) == str: 
                    self.greywater_to_sewer_coll_list.append(Global_counters.number_of_collectors)
                else:
                    self.greywater_to_reservoir_coll_list.append(Global_counters.number_of_collectors)
                Global_counters.number_of_collectors +=1
                
                # adds collector for overflow of Raintanks
                self.overflow_coll_strings=[]
                for m in range(len(Buildings.numbers_of_buildings_list)):
                    string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                    string2='\t\t\t\t<source node="Raintank_'+str(Buildings.numbers_of_raintanks_list[m])+'" port="Overflow"/> \n ' 
                    string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(m+1)+'"/> \n ' 
                    string4='\t\t\t</connection>\n' 
                    Global_counters.number_of_connections += 1
                    #writes all string in one and puts it in list
                    self.overflowstrings = ''
                    for o in range(5)[1:]:
                        exec 'self.overflowstrings += string'+str(o)
                    self.overflow_coll_strings.append(self.overflowstrings)
                #writes collector number in list that knows number of inports for later reference
                Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, clusterbuildingvec[i][0]])
                #writes collector number in list that knows connection for later reference
                self.overflow_coll_list.append(Global_counters.number_of_collectors)
                Global_counters.number_of_collectors +=1
                
                # adds collector for checking stored volume Raintanks on a cluster level
                self.raintankstorage_coll_strings=[]
                for m in range(len(Buildings.numbers_of_buildings_list)):
                    string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                    string2='\t\t\t\t<source node="Raintank_'+str(Buildings.numbers_of_raintanks_list[m])+'" port="Check_Storage"/> \n ' 
                    string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(m+1)+'"/> \n ' 
                    string4='\t\t\t</connection>\n' 
                    Global_counters.number_of_connections += 1
                    #writes all string in one and puts it in list
                    self.raintankstoragestrings = ''
                    for o in range(5)[1:]:
                        exec 'self.raintankstoragestrings += string'+str(o)
                    self.raintankstorage_coll_strings.append(self.raintankstoragestrings)
                #writes collector number in list that knows number of inports for later reference
                Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, clusterbuildingvec[i][0]])
                #writes collector number in list that knows connection for later reference
                self.raintankstorage_coll_list.append(Global_counters.number_of_collectors)
                Global_counters.number_of_collectors +=1
                
                # adds collector for additionaldemand of Raintanks or Greywatertanks
                self.additionaldemand_coll_strings=[]
                for m in range(len(Buildings.numbers_of_greywatertanks_list)):
                    if type(Buildings.numbers_of_greywatertanks_list[m]) == int:
                        string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                        string2='\t\t\t\t<source node="Raintank_'+str(Buildings.numbers_of_raintanks_list[m])+'" port="Additional_Demand"/> \n ' 
                        string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(m+1)+'"/> \n ' 
                        string4='\t\t\t</connection>\n' 
                    else:
                        string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                        string2='\t\t\t\t<source node="Greywatertank_'+str(Buildings.numbers_of_greywatertanks_list[m][1])+'" port="Additional_Demand"/> \n ' 
                        string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(m+1)+'"/> \n ' 
                        string4='\t\t\t</connection>\n'
                    Global_counters.number_of_connections += 1    
                    #writes all string in one and puts it in list
                    self.additionaldemandstrings = ''
                    for o in range(5)[1:]:
                        exec 'self.additionaldemandstrings += string'+str(o)
                    self.additionaldemand_coll_strings.append(self.additionaldemandstrings)
                #writes collector number in list that knows number of inports for later reference
                Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, clusterbuildingvec[i][0]])
                #writes collector number in list that knows connection for later reference
                if type(Buildings.numbers_of_buildings_using_gw_list[0]) != str:
                    self.additionaldemand_from_gwr_coll_list.append(Global_counters.number_of_collectors)
                    self.decision_not_from_gw_from_gw.append(1)
                else:
                    self.additionaldemand_not_from_gwr_coll_list.append(Global_counters.number_of_collectors)
                    self.decision_not_from_gw_from_gw.append(0)
                Global_counters.number_of_collectors +=1
                 
                #writing holdlevelstrings and added Cluster strings in one vector called allclusters
                for m in range(len(Buildings.Buildinglevel_connection_list)):    
                    self.allclusters.append(Buildings.Buildinglevel_connection_list[m])
                for m in range(len(self.street_strings)):    
                    self.allclusters.append(self.street_strings[m])    
                for m in range(len(Buildings.numbers_of_buildings_list)):    
                    self.allclusters.append(self.runoff_coll_strings[m])
                for m in range(len(Buildings.numbers_of_buildings_list)):    
                    self.allclusters.append(self.greywater_coll_strings[m])
                for m in range(len(Buildings.numbers_of_buildings_list)):    
                    self.allclusters.append(self.overflow_coll_strings[m])
                for m in range(len(Buildings.numbers_of_buildings_list)):    
                    self.allclusters.append(self.raintankstorage_coll_strings[m])
                for m in range(len(Buildings.numbers_of_buildings_list)):    
                    self.allclusters.append(self.additionaldemand_coll_strings[m])

##clusterbuildingvec = [ [Number of Buildings [Greywatertankinfo], numberofclusters ], [], [], ..., []]
clusterbuildingvec = [[6,[1,0,0,0,1,0],[1,1],1]]#,[8,[0,1,1,1,1,1,1,0],[0,1],80]]
##               
##number of inports for collectors
#Cluster = Clusterlevel()
#Cluster.writeconnections(clusterbuildingvec)
#Cluster.allclusters

#for i in range(len(Cluster.allclusters)):
#    print Cluster.allclusters[i]

#for i in range(len(Cluster.greywater_coll_strings)):
#    print Cluster.greywater_coll_strings[i]
#for i in range(len(Cluster.additionaldemand_coll_strings)):
#    print Cluster.additionaldemand_coll_strings[i]
#print len(Cluster.allclusters)
#print Global_counters.number_of_buildings
#print Global_counters.number_of_connections
#print Global_counters.number_of_greywatertanks     
#print Global_counters.number_of_raintanks
#print Global_counters.number_of_collectors
#print Global_counters.number_of_distributors
#print Global_counters.number_of_stormwaterpipes
#print Global_counters.number_of_Sewer2s
#print Global_counters.number_of_potablwaterreservoirs
#print Global_counters.number_of_catchments

