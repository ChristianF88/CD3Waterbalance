# -*- coding: utf-8 -*-
"""
Created on Wed Dec 03 11:37:18 2014

@author: Acer
"""

from Global_counters import Global_counters
from Clusterlevel import Clusterlevel
from Global_meaning_list import Global_meaning_list
#Global_counters = Global_counters.Instance()

class Greywaterreservoirlevel:
    def __init__(self):
        
        self.Greywaterreservoirlevel_list = []
        self.additionaldemand_from_gw_coll_list = []
        self.gw_inflow_coll_list = []
        self.additionaldemand_from_swr_coll_list = []
        self.additionaldemand_from_pwr_coll_list = []
        self.greywater_to_sewer_coll_list = []
        self.numbers_of_large_gwr = []
        self.runoff_overflow_coll_list_to_swr = []
        self.runoff_overflow_coll_list_to_swd = []
        self.raintankstorage_coll_list = []
        self.numbers_builidng_catchments = []
        
    def writeconnections(self, greyvec):
        #runs clusterclass
          
        clusterlen= 0
        for i in range(len(greyvec)):
                       
            Cluster = Clusterlevel() 
            if i == 0:
                pass
            else:
                clusterlen += len(greyvec[i-1][:-1])
                
            Cluster.writeconnections(greyvec[i][:-1])

            #transfers collector lists of runoff and overflow to greywatertanklevel
            for m in range(len(Cluster.runoff_coll_list_to_swd)):
                self.runoff_overflow_coll_list_to_swd.append(Cluster.runoff_coll_list_to_swd[m])
            for m in range(len(Cluster.runoff_coll_list_to_swr)):
                self.runoff_overflow_coll_list_to_swr.append(Cluster.runoff_coll_list_to_swr[m])
            for m in range(len(Cluster.overflow_coll_list_to_swr)):
                self.runoff_overflow_coll_list_to_swr.append(Cluster.overflow_coll_list_to_swr[m])
            for m in range(len(Cluster.overflow_coll_list_to_swd)):
                self.runoff_overflow_coll_list_to_swd.append(Cluster.overflow_coll_list_to_swd[m])
            for m in range(len(Cluster.raintankstorage_coll_list)):
                self.raintankstorage_coll_list.append(Cluster.raintankstorage_coll_list[m])    
            for m in range(len(Cluster.additionaldemand_from_swr_coll_list)):
                self.additionaldemand_from_swr_coll_list.append(Cluster.additionaldemand_from_swr_coll_list[m])
            for m in range(len(Cluster.additionaldemand_from_pwr_coll_list)):
                self.additionaldemand_from_pwr_coll_list.append(Cluster.additionaldemand_from_pwr_coll_list[m])

                
            #transfers numbers of building - catchments to this level
            for num in range(len(Cluster.numbers_builidng_catchments)):
                self.numbers_builidng_catchments.append(Cluster.numbers_builidng_catchments[num])
            for m in range(len(Cluster.greywater_to_sewer_coll_list)):
                self.greywater_to_sewer_coll_list.append(Cluster.greywater_to_sewer_coll_list[m])
                    
                    
            if greyvec[i][-1] == 1:
                
                # adds collector for additional demand from gwr
                self.additionaldemand_coll_strings=[]
                for m in range(len(Cluster.additionaldemand_from_gwr_coll_list)):
                    #if cluster is connected to greywaterreservoir
                    string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                    string2='\t\t\t\t<source node="Collector_'+str(Cluster.additionaldemand_from_gwr_coll_list[m])+'" port="Outport"/>\n' 
                    string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(m+1)+'"/>\n' 
                    string4='\t\t\t</connection>\n' 
                    #writes all string in one and puts it in list
                    self.additionaldemandcollstrings = ''
                    for o in range(5)[1:]:
                        exec 'self.additionaldemandcollstrings += string'+str(o)
                    self.additionaldemand_coll_strings.append(self.additionaldemandcollstrings)
                #writes collector number in list that knows number of inports for later reference
                Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, m+1])
                #writes collector number in list that knows connection for later reference
                self.additionaldemand_from_gw_coll_list.append(Global_counters.number_of_collectors)
                Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Additional from Clusterlevels and gives it to Greywaterreservoirs'])
                Global_counters.number_of_collectors += 1
                    
                    
                # adds collector for gwr inflow
                self.gwr_inflow_strings = []
                for m in range(len(Cluster.greywater_to_reservoir_coll_list)):
                    string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                    string2='\t\t\t\t<source node="Collector_'+str(Cluster.greywater_to_reservoir_coll_list[m])+'" port="Outport"/>\n' 
                    string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(m+1)+'"/>\n' 
                    string4='\t\t\t</connection>\n' 
                    Global_counters.number_of_connections += 1
                    #writes all string in one and puts it in list
                    self.gwrinflowstring = ''
                    for o in range(5)[1:]:
                        exec 'self.gwrinflowstring += string'+str(o)
                    self.gwr_inflow_strings.append(self.gwrinflowstring)
                if Cluster.greywater_to_reservoir_coll_list == []:
                    pass
                else:
                    #writes collector number in list that knows number of inports for later reference
                    Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, m+1])
                    #writes collector number in list that knows connection for later reference
                    self.gw_inflow_coll_list.append(Global_counters.number_of_collectors)
                    Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Greywater Collectors from Clusterlevel for Greywaterreservoirs'])
                    Global_counters.number_of_collectors += 1
                    
                    
                #adds Greywaterreservoir
                self.gwr_in_strings = []
                self.gwr_out_strings = []
                string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                string2='\t\t\t\t<source node="Collector_'+str(self.additionaldemand_from_gw_coll_list[0])+'" port="Outport"/>\n' 
                string3='\t\t\t\t<sink node="Greywaterreservoir_'+str(Global_counters.number_of_greywaterreservoirs)+'" port="Greywater_Out"/>\n' 
                string4='\t\t\t</connection>\n' 
                Global_counters.number_of_connections += 1
                string5='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                string6='\t\t\t\t<source node="Collector_'+str(self.gw_inflow_coll_list[0])+'" port="Outport"/>\n' 
                string7='\t\t\t\t<sink node="Greywaterreservoir_'+str(Global_counters.number_of_greywaterreservoirs)+'" port="Greywater_In"/>\n' 
                string8='\t\t\t</connection>\n' 
                Global_counters.number_of_connections += 1
                #writes all string in one and puts it in list
                self.gwrinstring = ''
                self.gwroutstring = ''
                for o in range(5)[1:]:
                    exec 'self.gwrinstring += string'+str(o+4)
                    exec 'self.gwroutstring += string'+str(o)
                self.gwr_in_strings.append(self.gwrinstring)
                self.gwr_out_strings.append(self.gwroutstring)
                
                self.numbers_of_large_gwr.append(Global_counters.number_of_greywaterreservoirs)
                Global_counters.number_of_greywaterreservoirs += 1
                
            #transfers lists from clusterlevel to greywaterreservoirlevel if there's no gwr 
            else:
                pass

                

                        
                    
                

                
            for m in range(len(Cluster.allclusters)):    
                self.Greywaterreservoirlevel_list.append(Cluster.allclusters[m])
            if greyvec[i][-1] == 1:    
                for m in range(len(self.additionaldemand_coll_strings)):
                    self.Greywaterreservoirlevel_list.append(self.additionaldemand_coll_strings[m])
                for m in range(len(self.gwr_inflow_strings)):
                    self.Greywaterreservoirlevel_list.append(self.gwr_inflow_strings[m])
                self.Greywaterreservoirlevel_list.append(self.gwr_out_strings[0])
                self.Greywaterreservoirlevel_list.append(self.gwr_in_strings[0])
            else:
                pass
                

    

               

#greyvec = [[[6,[1,0]*3,[1,0,0],1],[7,[1]*7,[1,0,0],1],[2,[0,1],[0,1,0],1],1]]#,[[4,[0,1]*2,[1,0,1],3],[15,[0,1,1,0,1]*3,[1,1,0],7],1],[[5,[0,0,0,0,1],[0,0,1],5],[10,[0]*10,[0,0,0],2],[8,[1,1,0,0,1,0,0,1],[0,0,0],2],[5,[1]*5,[0,0,1],5],[10,[0,1]*5,[0,0,0],2],[8,[0]*8,[0,0,1],2],0]]
#Greytank = Greywaterreservoirlevel()
#Greytank.writeconnections(greyvec)

#for i in range(len(Greytank.Greywaterreservoirlevel_list)):
#    print Greytank.Greywaterreservoirlevel_list[i]
#print '\n'

#print len(Greytank.Greywaterreservoirlevel_list)
#print Global_counters.number_of_demandmodels
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
