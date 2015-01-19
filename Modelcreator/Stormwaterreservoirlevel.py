# -*- coding: utf-8 -*-
"""
Created on Wed Dec 03 11:37:18 2014

@author: Acer
"""
#this class adds Stormwatertanks to certain clusters
from Greywaterreservoirlevel import Greywaterreservoirlevel
from Global_counters import Global_counters
from Global_meaning_list import Global_meaning_list


class Stormwaterreservoirlevel:
    def __init__(self):
        self.Stormwaterreservoirlevel_list = []
        self.runoff_coll_list = []
        self.swr_inflow_coll_list = []
        self.overflow_coll_list = []
        self.swr_outflow_coll_list = []
        self.numbers_of_large_swr = []
        self.additionaldemand_from_pwr_coll_list = []
        self.runoff_overflow_to_stormwaterdrain_coll_list = []
        self.only_GWR = []
        self.greywater_to_sewer_coll_list = []   
        self.raintankstorage_coll_list = []
        self.numbers_of_large_gwr = []
        
    def writeconnections(self, stormvec):
        
        '''
        inputvector need to be in the following setup
        [6,[1,0,1,0,1,0],[0,0,0],1] = Clusterlevelvector 
        
        first number is the amount of buildings in cluster, the vector at second position contains the information whether the building has its own little
        Greywater Tank, the vector at third position consists of the Information regarding the connection to a big Greywaterreservoir/Stormwaterreservoir if present (description follows). 
        [contributing Greywater to big Greywaterres. (0 = no, 1 = yes), using treated Greywater from big Greywaterres. (0 = no, 1 = yes), using treated Stormwater from big Stormwaterres. (0 = no, 1 = yes)] 
        The last number says how many clusters of this configuration are supposed to be set up.
        
        [[[6,[1,0]*3,[0,0,0],1],[7,[1]*7,[0,0,0],1],[2,[0,1],[0,0,1],1],1]] = Greywaterreservoirlevelvector
        
        it consists out of Clusterlevelvectors and the last digit means that a Greywaterreservoir is present (1 = is present) or not (0 = not present)
        
        [[[[6,[1,0]*3,[0,0,0],1],[7,[1]*7,[0,0,0],1],[2,[0,1],[0,0,1],1],1], [[6,[1,0]*3,[0,0,1],1],[7,[1]*7,[0,0,1],1],[2,[0,1],[0,0,1],1],1],0]] = Stormwaterreservoirlevelvector
        
        it consists out of Greywaterreservoirlevelvector and the last digit means that a Stormwaterreservoir is present (1 = is present) or not (0 = not present)
        '''
        Greytanklevel = Greywaterreservoirlevel()
        for i in range(len(stormvec)):
            
            Greytanklevel.writeconnections(stormvec[i][:-1])
            
            for q in range(len(Greytanklevel.greywater_to_sewer_coll_list)):
                self.greywater_to_sewer_coll_list.append(Greytanklevel.greywater_to_sewer_coll_list[q])
            for q in range(len(Greytanklevel.raintankstorage_coll_list)):
                self.raintankstorage_coll_list.append(Greytanklevel.raintankstorage_coll_list[q])
            for q in range(len(Greytanklevel.numbers_of_large_gwr)):
                self.numbers_of_large_gwr.append(Greytanklevel.numbers_of_large_gwr[q])
            
            if stormvec[i][-1] == 1:
                
                #adds collector for stormwaterreservoir inflow
                self.swr_inflow_coll_strings=[]
                for m in range(len(Greytanklevel.runoff_overflow_coll_list)):
                    string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                    string2='\t\t\t\t<source node="Collector_'+str(Greytanklevel.runoff_overflow_coll_list[m])+'" port="Outport"/>\n' 
                    string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(m+1)+'"/>\n' 
                    string4='\t\t\t</connection>\n' 
                    Global_counters.number_of_connections += 1
                    #writes all string in one and puts it in list
                    self.swrinflowcollstrings = ''
                    for o in range(5)[1:]:
                        exec 'self.swrinflowcollstrings += string'+str(o)
                    self.swr_inflow_coll_strings.append(self.swrinflowcollstrings)
                #writes collector number in list that knows number of inports for later reference
                Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, len(Greytanklevel.runoff_overflow_coll_list)])
                #writes collector number in list that knows connection for later reference
                self.swr_inflow_coll_list.append(Global_counters.number_of_collectors)
                Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Runoff and Overflow Collectors from Clusterlevel as Stormwaterreservoir Inflow'])
                Global_counters.number_of_collectors += 1
                    
                    
                #adds collector for additional demand (Greywaterreservoirs) needed from Stormwaterreservoir
                self.swr_outflow_coll_strings=[]
                if Greytanklevel.numbers_of_large_gwr != []:
                    for n in range(len(Greytanklevel.numbers_of_large_gwr)):
                        string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                        string2='\t\t\t\t<source node="Greywatertank_'+str(Greytanklevel.numbers_of_large_gwr[n])+'" port="Additional_Demand"/>\n' 
                        string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(n+1)+'"/>\n' 
                        string4='\t\t\t</connection>\n' 
                        Global_counters.number_of_connections += 1
                        #writes all string in one and puts it in list
                        self.additionaldemandofgwtcollstrings = ''
                        for o in range(5)[1:]:
                            exec 'self.additionaldemandofgwtcollstrings += string'+str(o)
                        self.swr_outflow_coll_strings.append(self.additionaldemandofgwtcollstrings)
                else: 
                    n=-1
                            
                for m in range(len(Greytanklevel.additionaldemand_from_swr_coll_list)):
                    string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                    string2='\t\t\t\t<source node="Collector_'+str(Greytanklevel.additionaldemand_from_swr_coll_list[m])+'" port="Outport"/>\n' 
                    string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(m+n+2)+'"/>\n' 
                    string4='\t\t\t</connection>\n' 
                    Global_counters.number_of_connections += 1
                    #writes all string in one and puts it in list
                    self.swroutflowcollstrings = ''
                    for o in range(5)[1:]:
                        exec 'self.swroutflowcollstrings += string'+str(o)
                    self.swr_outflow_coll_strings.append(self.swroutflowcollstrings)  
                
                #writes collector number in list that knows number of inports for later reference
                Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, m+n+2 ])
                #writes collector number in list that knows connection for later reference
                self.swr_outflow_coll_list.append(Global_counters.number_of_collectors)
                Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Additional Demand (Greywaterreservoirs) needed from Stormwaterreservoir'])
                Global_counters.number_of_collectors += 1
                
                
                #adds Stormwaterreservoir
                self.swr_in_strings = []
                self.swr_out_strings = []
                string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                string2='\t\t\t\t<source node="Collector_'+str(self.swr_inflow_coll_list[0])+'" port="Outport"/>\n' 
                string3='\t\t\t\t<sink node="Stormwaterreservoir_'+str(Global_counters.number_of_stormwaterreservoirs)+'" port="Stormwater_In"/>\n' 
                string4='\t\t\t</connection>\n' 
                Global_counters.number_of_connections += 1
                string5='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                string6='\t\t\t\t<source node="Collector_'+str(self.swr_outflow_coll_list[0])+'" port="Outport"/>\n' 
                string7='\t\t\t\t<sink node="Stormwaterreservoir_'+str(Global_counters.number_of_stormwaterreservoirs)+'" port="Stormwater_Out"/>\n' 
                string8='\t\t\t</connection>\n' 
                Global_counters.number_of_connections += 1
                #writes all strings in one and puts it in list
                self.swrinstring = ''
                self.swroutstring = ''
                for o in range(5)[1:]:
                    exec 'self.swrinstring += string'+str(o+4)
                    exec 'self.swroutstring += string'+str(o)
                self.swr_in_strings.append(self.swrinstring)
                self.swr_out_strings.append(self.swroutstring)
                self.numbers_of_large_swr.append(Global_counters.number_of_stormwaterreservoirs)
                Global_counters.number_of_stormwaterreservoirs += 1
                
                #demand of Building not conneted to SWR
                for m in range(len(Greytanklevel.additionaldemand_from_pwr_coll_list)):
                    self.additionaldemand_from_pwr_coll_list.append(Greytanklevel.additionaldemand_from_pwr_coll_list[m])
                    
            else:
                
                for m in range(len(Greytanklevel.additionaldemand_from_swr_coll_list)):
                    self.additionaldemand_from_pwr_coll_list.append(Greytanklevel.additionaldemand_from_swr_coll_list[m])
                for m in range(len(Greytanklevel.runoff_overflow_coll_list)):
                    self.runoff_overflow_to_stormwaterdrain_coll_list.append(Greytanklevel.runoff_overflow_coll_list[m])
                for m in range(len(Greytanklevel.additionaldemand_from_pwr_coll_list)):
                    self.additionaldemand_from_pwr_coll_list.append(Greytanklevel.additionaldemand_from_pwr_coll_list[m])
                if Greytanklevel.numbers_of_large_gwr != []:
                    for m in range(len(Greytanklevel.numbers_of_large_gwr)):
                        self.only_GWR.append(Greytanklevel.numbers_of_large_gwr[m])
                else:
                    pass
                
            for m in range(len(Greytanklevel.Greywaterreservoirlevel_list)):    
                self.Stormwaterreservoirlevel_list.append(Greytanklevel.Greywaterreservoirlevel_list[m])
            if stormvec[i][-1] == 1:    
                for m in range(len(self.swr_inflow_coll_strings)):
                    self.Stormwaterreservoirlevel_list.append(self.swr_inflow_coll_strings[m])
                for m in range(len(self.swr_outflow_coll_strings)):
                    self.Stormwaterreservoirlevel_list.append(self.swr_outflow_coll_strings[m])
                self.Stormwaterreservoirlevel_list.append(self.swr_out_strings[0])
                self.Stormwaterreservoirlevel_list.append(self.swr_in_strings[0]) 
            else:
                pass
                

    
        
    
    



#
#stormvec = [[[[6,[1,0]*3,[0,0,0],1],[7,[1]*7,[0,0,0],1],[2,[0,1],[0,0,1],1],1], [[6,[1,0]*3,[0,0,1],1],[7,[1]*7,[0,0,1],1],[2,[0,1],[0,0,1],1],1],0]]
#Stormwater = Stormwaterreservoirlevel()
#Stormwater.writeconnections(stormvec)

#for i in range(len(Stormwater.swr_outflow_coll_strings)):
#    print Stormwater.swr_outflow_coll_strings[i]
##print '\n'
#
##print len(Stormwater.Stormwaterreservoirlevel_list)
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

