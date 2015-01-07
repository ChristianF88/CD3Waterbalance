# -*- coding: utf-8 -*-
"""
Created on Tue Dec 02 11:20:04 2014

@author: Acer
"""
from Stormwaterreservoirlevel import Stormwaterreservoirlevel
from Global_counters import Global_counters
from Global_meaning_list import Global_meaning_list


class Supplylevel:
    def __init__(self):
        self.Supplylevel_list = []
        self.Supplylevel_loop_list = []
        self.blackwater_coll_list = []
        self.potablewater_coll_list = []
        self.infiltr_coll_list = []
        self.outdoordemand = []
        self.indoor_demand_coll_list = []
        self.need_to_have_filout_list = []
        self.fileout_numbers_names_list = []
        
    def writeconnections(self, supplyvec):
        
        '''
        supplyvec need to be in the following setup
        [6,[1,0,1,0,1,0],[0,0,0],1] = Clusterlevelvector 
        
        first number is the amount of buildings in cluster, the vector at second position contains the information whether the building has its own little
        Greywater Tank, the vector at third position consists of the Information regarding the connection to a big Greywaterreservoir/Stormwaterreservoir if present (description follows). 
        [contributing Greywater to big Greywaterres. (0 = no, 1 = yes), using treated Greywater from big Greywaterres. (0 = no, 1 = yes), using treated Stormwater from big Stormwaterres. (0 = no, 1 = yes)] 
        The last number says how many clusters of this configuration are supposed to be set up.
        
        [[[6,[1,0]*3,[0,0,0],1],[7,[1]*7,[0,0,0],1],[2,[0,1],[0,0,1],1],1]] = Greywaterreservoirlevelvector
        
        it consists out of Clusterlevelvectors and the last digit means that a Greywaterreservoir is present (1 = is present) or not (0 = not present)
        
        [[[[6,[1,0]*3,[0,0,0],1],[7,[1]*7,[0,0,0],1],[2,[0,1],[0,0,1],1],1], [[6,[1,0]*3,[0,0,1],1],[7,[1]*7,[0,0,1],1],[2,[0,1],[0,0,1],1],1],0]] = Stormwaterreservoirlevelvector
        
        it consists out of Greywaterreservoirlevelvector and the last digit means that a Stormwaterreservoir is present (1 = is present) or not (0 = not present)
        
        the supplyvec consists can consist out of more than one Stormwaterreservoirlevelvector and more than one supplyarea
        [[Stormwaterreservoirlevelvector1,Stormwaterreservoirlevelvector2],[Stormwaterreservoirlevelvector3,Stormwaterreservoirlevelvector4,Stormwaterreservoirlevelvector5]]
        = [supplyarea1,supplyarea2] = supplyvec
        '''
        
        
        for i in range(len(supplyvec)):
            Stormwater = Stormwaterreservoirlevel()
            Stormwater.writeconnections(supplyvec[i])
            
            '''
            adding Potable Water Reservoir
            '''            
            
            #adds collector for potable water reservoir of nonpot(Additional Demand)
            self.nonpot_coll_strings=[]
            if Stormwater.numbers_of_large_swr != []:
                for n in range(len(Stormwater.numbers_of_large_swr)):
                    string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                    string2='\t\t\t\t<source node="Stormwaterreservoir_'+str(Stormwater.numbers_of_large_swr[n])+'" port="Additional_Demand"/>\n' 
                    string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(n+1)+'"/>\n' 
                    string4='\t\t\t</connection>\n' 
                    Global_counters.number_of_connections += 1
                    #writes all string in one and puts it in list
                    self.nonpotcollstrings = ''
                    for o in range(5)[1:]:
                        exec 'self.nonpotcollstrings += string'+str(o)
                    self.nonpot_coll_strings.append(self.nonpotcollstrings)
            else:
                n = -1
                
            if Stormwater.only_GWR != []:
                for p in range(len(Stormwater.numbers_of_large_swr)):
                    string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                    string2='\t\t\t\t<source node="Greywatertank_'+str(Stormwater.only_GWR[p])+'" port="Additional_Demand"/>\n' 
                    string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(p+n+2)+'"/>\n' 
                    string4='\t\t\t</connection>\n' 
                    Global_counters.number_of_connections += 1
                    #writes all string in one and puts it in list
                    self.nonpotcollstrings = ''
                    for o in range(5)[1:]:
                        exec 'self.nonpotcollstrings += string'+str(o)
                    self.nonpot_coll_strings.append(self.nonpotcollstrings)
            else:
                p = -1
            #adds collector for potable water reservoir of nonpot (from buildings, not connected to GWR/SWR)
            if Stormwater.additionaldemand_from_pwr_coll_list != []:
                for m in range(len(Stormwater.additionaldemand_from_pwr_coll_list)):
                    string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                    string2='\t\t\t\t<source node="Collector_'+str(Stormwater.additionaldemand_from_pwr_coll_list[m])+'" port="Outport"/>\n' 
                    string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(m+n+p+3)+'"/>\n' 
                    string4='\t\t\t</connection>\n' 
                    Global_counters.number_of_connections += 1
                    #writes all string in one and puts it in list
                    self.nonpotcollstrings = ''
                    for o in range(5)[1:]:
                        exec 'self.nonpotcollstrings += string'+str(o)
                    self.nonpot_coll_strings.append(self.nonpotcollstrings)
            else:
                m = -1

            #adds potable water reservoir connecting nonpot
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Outport"/>\n' 
            string3='\t\t\t\t<sink node="Potable_Water_Resorvoir_'+str(Global_counters.number_of_potablwaterreservoirs)+'" port="Non_Potable_Water_Demand"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.nonpotcollstrings = ''
            for o in range(5)[1:]:
                exec 'self.nonpotcollstrings += string'+str(o)
            self.nonpot_coll_strings.append(self.nonpotcollstrings)
            #writes collector number in list that knows number of inports for later reference
            Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, m+n+p+3])
            #writes collector number in list that knows connection for later reference
            Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Additonal Demands from small Tanks (Buildings) and GW-/SW-Reservoirs for nonpot Demand from PWR'])
            Global_counters.number_of_collectors += 1
            
            #adds collector for potable water reservoir of pot
            self.pot_coll_strings=[]
            for m in range(Global_counters.number_of_buildings):
                string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                string2='\t\t\t\t<source node="Building_'+str(m)+'" port="Potable_Water"/>\n' 
                string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(m+1)+'"/>\n' 
                string4='\t\t\t</connection>\n' 
                Global_counters.number_of_connections += 1
                #writes all string in one and puts it in list
                self.potcollstrings = ''
                for o in range(5)[1:]:
                    exec 'self.potcollstrings += string'+str(o)
                self.pot_coll_strings.append(self.potcollstrings)
            
            #adds potable water reservoir connecting pot
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Outport"/>\n' 
            string3='\t\t\t\t<sink node="Potable_Water_Resorvoir_'+str(Global_counters.number_of_potablwaterreservoirs)+'" port="Potable_Water_Demand"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.potcollstrings = ''
            for o in range(5)[1:]:
                exec 'self.potcollstrings += string'+str(o)
            self.pot_coll_strings.append(self.potcollstrings)  
            #writes collector number in list that knows number of inports for later reference
            Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, Global_counters.number_of_buildings])
            #writes collector number in list that knows connection for later reference
            Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects potable Demand from Buildings for pot Demand from PWR'])
            Global_counters.number_of_collectors += 1
            Global_counters.number_of_potablwaterreservoirs += 1
            
            '''
            adding Stormwaterdrain
            '''  

            #adds collector for runoff and overflow collectors and stormwateroverflow
            self.stormdrain_strings=[]
            if len(Stormwater.numbers_of_large_swr) != []:
                for n in range(len(Stormwater.numbers_of_large_swr)):
                    string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                    string2='\t\t\t\t<source node="Stormwaterreservoir_'+str(Stormwater.numbers_of_large_swr[n])+'" port="Overflow"/>\n' 
                    string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(n+1)+'"/>\n' 
                    string4='\t\t\t</connection>\n' 
                    Global_counters.number_of_connections += 1
                    #writes all string in one and puts it in list
                    self.stormdrainstrings = ''
                    for o in range(5)[1:]:
                        exec 'self.stormdrainstrings += string'+str(o)
                    self.stormdrain_strings.append(self.stormdrainstrings)
                number_of_inports_1 = len(Stormwater.numbers_of_large_swr)
                    
            else:
                n=-1
                number_of_inports_1 = 0
                
            if len(Stormwater.runoff_overflow_to_stormwaterdrain_coll_list) != []:
                for m in range(len(Stormwater.runoff_overflow_to_stormwaterdrain_coll_list)):
                    string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                    string2='\t\t\t\t<source node="Collector_'+str(Stormwater.runoff_overflow_to_stormwaterdrain_coll_list[m])+'" port="Outport"/>\n' 
                    string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(m+2+n)+'"/>\n' 
                    string4='\t\t\t</connection>\n' 
                    Global_counters.number_of_connections += 1
                    #writes all string in one and puts it in list
                    self.stormdrainstrings = ''
                    for o in range(5)[1:]:
                        exec 'self.stormdrainstrings += string'+str(o)
                    self.stormdrain_strings.append(self.stormdrainstrings)
                number_of_inports_2 = len(Stormwater.runoff_overflow_to_stormwaterdrain_coll_list)
            else:
                number_of_inports_2 = 0
                
            #adds stormwaterdrain
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Outport"/>\n' 
            string3='\t\t\t\t<sink node="Stormwaterpipe_'+str(Global_counters.number_of_stormwaterpipes)+'" port="Runoff"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.stormdrainstrings = ''
            for o in range(5)[1:]:
                exec 'self.stormdrainstrings += string'+str(o)
            self.stormdrain_strings.append(self.stormdrainstrings)  
            #writes collector number in list that knows number of inports for later reference
            Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, number_of_inports_1 + number_of_inports_2])
            #writes collector number in list that knows connection for later reference
            Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Additional Demand and Runoff leading to Stormwaterpipe'])
            Global_counters.number_of_collectors += 1
            Global_counters.number_of_stormwaterpipes += 1
            
            '''
            adds sewer
            '''
            #collects waste water from Stormwaterreservoirs if present
            self.sewer_strings=[]
            if len(Stormwater.numbers_of_large_swr) != []:
                for n in range(len(Stormwater.numbers_of_large_swr)):
                    string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                    string2='\t\t\t\t<source node="Stormwaterreservoir_'+str(Stormwater.numbers_of_large_swr[n])+'" port="Waste_Water"/>\n' 
                    string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(n+1)+'"/>\n' 
                    string4='\t\t\t</connection>\n' 
                    Global_counters.number_of_connections += 1
                    #writes all string in one and puts it in list
                    self.sewerstrings = ''
                    for o in range(5)[1:]:
                        exec 'self.sewerstrings += string'+str(o)
                    self.sewer_strings.append(self.sewerstrings)
                
                number_of_inports_1 = len(Stormwater.numbers_of_large_swr)
            else:
                number_of_inports_1 = 0
                n = -1
               
            #collects waste water from big Greywaterreservoirs if present    
            if Global_counters.number_of_greywatertanks != 0:
                for m in range(Global_counters.number_of_greywatertanks):
                    string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                    string2='\t\t\t\t<source node="Greywatertank_'+str(m)+'" port="Waste_Water"/>\n' 
                    string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(m+n+2)+'"/>\n' 
                    string4='\t\t\t</connection>\n' 
                    Global_counters.number_of_connections += 1
                    #writes all string in one and puts it in list
                    self.sewerstrings = ''
                    for o in range(5)[1:]:
                        exec 'self.sewerstrings += string'+str(o)
                    self.sewer_strings.append(self.sewerstrings)
               
                number_of_inports_2 = Global_counters.number_of_greywatertanks
            else:
               
                number_of_inports_2 = 0
                m = -1
                
            #collects Greywater form buildings/small greywatertanks that are not connected to bis reservoir    
            if Stormwater.greywater_to_sewer_coll_list != []:
                for p in range(len(Stormwater.greywater_to_sewer_coll_list)):
                    string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                    string2='\t\t\t\t<source node="Collector_'+str(Stormwater.greywater_to_sewer_coll_list[p])+'" port="Outport"/>\n' 
                    string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(p+m+n+3)+'"/>\n' 
                    string4='\t\t\t</connection>\n' 
                    Global_counters.number_of_connections += 1
                    #writes all string in one and puts it in list
                    self.sewerstrings = ''
                    for o in range(5)[1:]:
                        exec 'self.sewerstrings += string'+str(o)
                    self.sewer_strings.append(self.sewerstrings)
               
                number_of_inports_3 = len(Stormwater.greywater_to_sewer_coll_list)
            else:
               
                number_of_inports_3 = 0
                p = -1
            #collects all black water from buildings
            for q in range(Global_counters.number_of_buildings):
                    string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
                    string2='\t\t\t\t<source node="Building_'+str(q)+'" port="Black_Water"/>\n' 
                    string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(q+p+m+n+4)+'"/>\n' 
                    string4='\t\t\t</connection>\n' 
                    Global_counters.number_of_connections += 1
                    #writes all string in one and puts it in list
                    self.sewerstrings = ''
                    for o in range(5)[1:]:
                        exec 'self.sewerstrings += string'+str(o)
                    self.sewer_strings.append(self.sewerstrings)
                    
            #adds sewer       
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Outport"/>\n' 
            string3='\t\t\t\t<sink node="Sewer2_'+str(Global_counters.number_of_sewers)+'" port="Black_Water"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.sewerstrings = ''
            for o in range(5)[1:]:
                exec 'self.sewerstrings += string'+str(o)
            self.sewer_strings.append(self.sewerstrings)
            
            #writes collector number in list that knows number of inports for later reference
            Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, number_of_inports_1 + number_of_inports_2 + number_of_inports_3+Global_counters.number_of_buildings])
            Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Black Water from Buildings, Greywater not connected to Reservoir, Waste Water from Greywaterreservoirs and Stormwaterreservoirs leading to Sewer'])            
            Global_counters.number_of_collectors += 1
            Global_counters.number_of_sewers += 1
         
            
            for m in range(len(Stormwater.Stormwaterreservoirlevel_list)):    
                self.Supplylevel_loop_list.append(Stormwater.Stormwaterreservoirlevel_list[m])
            for m in range(len(self.pot_coll_strings)):    
                self.Supplylevel_loop_list.append(self.pot_coll_strings[m])    
            for m in range(len(self.nonpot_coll_strings)):    
                self.Supplylevel_loop_list.append(self.nonpot_coll_strings[m])
            for m in range(len(self.stormdrain_strings)):    
                self.Supplylevel_loop_list.append(self.stormdrain_strings[m])
            for m in range(len(self.sewer_strings)):    
                self.Supplylevel_loop_list.append(self.sewer_strings[m])
            
   
        '''    
        connecting filereader (rain) and pattern implementer (evapo) to all Catchments (including catchment streets)
        '''
        self.modelinput_strings = []
        #filereader - distributor connection
        string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
        string2='\t\t\t\t<source node="File_Reader_'+str(Global_counters.number_of_filereaders)+'" port="Outport"/>\n' 
        string3='\t\t\t\t<sink node="Distributor_'+str(Global_counters.number_of_distributors)+'" port="Inport"/>\n' 
        string4='\t\t\t</connection>\n' 
        Global_counters.number_of_connections += 1
        #writes all string in one and puts it in list
        self.modelinputstrings = ''
        for o in range(5)[1:]:
            exec 'self.modelinputstrings += string'+str(o)
        self.modelinput_strings.append(self.modelinputstrings)
        
        #distributor - catchment connection (rain)
        for q in range(Global_counters.number_of_catchments):
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Distributor_'+str(Global_counters.number_of_distributors)+'" port="Outport_'+str(q+1)+'"/>\n' 
            string3='\t\t\t\t<sink node="Catchment_w_Routing_'+str(q)+'" port="Rain"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.modelinputstrings = ''
            for o in range(5)[1:]:
                exec 'self.modelinputstrings += string'+str(o)
            self.modelinput_strings.append(self.modelinputstrings)
        
        #writes collector number in list that knows number of inports for later reference
        Global_counters.number_of_distributors_ports_list.append([Global_counters.number_of_distributors, Global_counters.number_of_catchments])
        Global_counters.number_of_filereaders += 1
        Global_counters.number_of_distributors += 1
        
        #filereader - pattern_implementer connection
        string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
        string2='\t\t\t\t<source node="File_Reader_'+str(Global_counters.number_of_filereaders)+'" port="Outport"/>\n' 
        string3='\t\t\t\t<sink node="Pattern_Impl_'+str(Global_counters.number_of_patternimplementers)+'" port="Inport"/>\n' 
        string4='\t\t\t</connection>\n' 
        Global_counters.number_of_connections += 1
        #writes all string in one and puts it in list
        self.modelinputstrings = ''
        for o in range(5)[1:]:
            exec 'self.modelinputstrings += string'+str(o)
        self.modelinput_strings.append(self.modelinputstrings)
        
        Global_counters.number_of_filereaders += 1
        
        #pattern_implementer - distributor connection
        string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
        string2='\t\t\t\t<source node="Pattern_Impl_'+str(Global_counters.number_of_patternimplementers)+'" port="Outport"/>\n' 
        string3='\t\t\t\t<sink node="Distributor_'+str(Global_counters.number_of_distributors)+'" port="Inport"/>\n' 
        string4='\t\t\t</connection>\n' 
        Global_counters.number_of_connections += 1
        #writes all string in one and puts it in list
        self.modelinputstrings = ''
        for o in range(5)[1:]:
            exec 'self.modelinputstrings += string'+str(o)
        self.modelinput_strings.append(self.modelinputstrings)
        
        #distributor - catchment connection (evapo)
        for q in range(Global_counters.number_of_catchments):
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Distributor_'+str(Global_counters.number_of_distributors)+'" port="Outport_'+str(q+1)+'"/>\n' 
            string3='\t\t\t\t<sink node="Catchment_w_Routing_'+str(q)+'" port="Evapotranspiration"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.modelinputstrings = ''
            for o in range(5)[1:]:
                exec 'self.modelinputstrings += string'+str(o)
            self.modelinput_strings.append(self.modelinputstrings)
             
        #writes collector number in list that knows number of inports for later reference
        Global_counters.number_of_distributors_ports_list.append([Global_counters.number_of_distributors, Global_counters.number_of_catchments])
        Global_counters.number_of_patternimplementers += 1
        Global_counters.number_of_distributors += 1
        
        '''
        adds collector for storagelevel of greywatertanks
        '''
        self.check_greytanks_strings = []
        for q in range(Global_counters.number_of_greywatertanks):
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Greywatertank_'+str(q)+'" port="Current_Volume"/>\n' 
            string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(q+1)+'"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.checkgreytanksstrings = ''
            for o in range(5)[1:]:
                exec 'self.checkgreytanksstrings += string'+str(o)
            self.check_greytanks_strings.append(self.checkgreytanksstrings)
             
        #writes collector number in list that knows number of inports for later reference
        Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, Global_counters.number_of_greywatertanks])
        Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Current_Volume of Greywatertanks/reservoirs (for checking levels)'])
        self.need_to_have_filout_list.append([Global_counters.number_of_collectors, 'Greywatertanklevels'])
        Global_counters.number_of_collectors += 1

        '''
        adds collector for storagelevel of stormwatertanks
        '''
        self.check_stormtanks_strings = []
        for q in range(Global_counters.number_of_stormwaterreservoirs):
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Stormwaterreservoir_'+str(q)+'" port="Current_Volume"/>\n' 
            string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(q+1)+'"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.checkstormtanksstrings = ''
            for o in range(5)[1:]:
                exec 'self.checkstormtanksstrings += string'+str(o)
            self.check_stormtanks_strings.append(self.checkstormtanksstrings)
             
        #writes collector number in list that knows number of inports for later reference
        Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, Global_counters.number_of_stormwaterreservoirs])
        Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Current_Volume of Stormwaterreservoirs (for checking levels)'])
        self.need_to_have_filout_list.append( [Global_counters.number_of_collectors, 'Stormwaterreservoirlevels'])
        Global_counters.number_of_collectors += 1
        
        '''
        adds collector for storagelevel of rainwatertanks
        '''
        self.check_raintanks_strings = []
        for q in range(len(Stormwater.raintankstorage_coll_list)):
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Collector_'+str(Stormwater.raintankstorage_coll_list[q])+'" port="Outport"/>\n' 
            string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(q+1)+'"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.checkraintanksstrings = ''
            for o in range(5)[1:]:
                exec 'self.checkraintanksstrings += string'+str(o)
            self.check_raintanks_strings.append(self.checkraintanksstrings)
             
        #writes collector number in list that knows number of inports for later reference
        Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, len(Stormwater.raintankstorage_coll_list)])
        Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Current_Volume Collectors from Clusterlevel of Raintanks (for checking levels)'])
        self.need_to_have_filout_list.append([Global_counters.number_of_collectors, 'Rainwatertanklevels'])
        Global_counters.number_of_collectors += 1
        
        '''
        adds collector for infiltration of catchments
        '''
        self.check_infiltration_strings = []
        for q in range(Global_counters.number_of_catchments):
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Catchment_w_Routing_'+str(q)+'" port="Actual_Infiltration"/>\n' 
            string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(q+1)+'"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.checkinfiltrationstrings = ''
            for o in range(5)[1:]:
                exec 'self.checkinfiltrationstrings += string'+str(o)
            self.check_infiltration_strings.append(self.checkinfiltrationstrings)
             
        #writes collector number in list that knows number of inports for later reference
        Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, Global_counters.number_of_catchments])
        Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Actual Infiltration of all Catchments'])
        self.need_to_have_filout_list.append([Global_counters.number_of_collectors, 'Actual_Infiltration'])
        Global_counters.number_of_collectors += 1

        '''
        adds collector for checking outdoordemand
        '''
        self.check_outdoordemand_strings = []
        for q in range(Global_counters.number_of_catchments):
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Catchment_w_Routing_'+str(q)+'" port="Outdoor_Demand_Check"/>\n' 
            string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(q+1)+'"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.checkoutdoordemandstrings = ''
            for o in range(5)[1:]:
                exec 'self.checkoutdoordemandstrings += string'+str(o)
            self.check_outdoordemand_strings.append(self.checkoutdoordemandstrings)
             
        #writes collector number in list that knows number of inports for later reference
        Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, Global_counters.number_of_catchments])
        Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Outdoor Demand of all Catchments'])
        self.need_to_have_filout_list.append([Global_counters.number_of_collectors, 'Outdoor_Demand'])
        Global_counters.number_of_collectors += 1
        
        '''
        adds collector for checking demandmodel
        '''
        self.check_demandmodel_bath_strings = []
        for q in range(Global_counters.number_of_demandmodels):
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Demand_Model_'+str(q)+'" port="Outport_Check_Bathtub_[l/h]"/>\n' 
            string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(q+1)+'"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.checkdemandmodelbathstrings = ''
            for o in range(5)[1:]:
                exec 'self.checkdemandmodelbathstrings += string'+str(o)
            self.check_demandmodel_bath_strings.append(self.checkdemandmodelbathstrings)   
        #writes collector number in list that knows number of inports for later reference
        Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, Global_counters.number_of_demandmodels])
        Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Bathtub Demand from all Demandmodels'])
        self.indoor_demand_coll_list.append(Global_counters.number_of_collectors)
        Global_counters.number_of_collectors += 1
        
        self.check_demandmodel_shower_strings = []
        for q in range(Global_counters.number_of_demandmodels):
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Demand_Model_'+str(q)+'" port="Outport_Check_Shower_[l/h]"/>\n' 
            string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(q+1)+'"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.checkdemandmodelbathstrings = ''
            for o in range(5)[1:]:
                exec 'self.checkdemandmodelbathstrings += string'+str(o)
            self.check_demandmodel_shower_strings.append(self.checkdemandmodelbathstrings)   
        #writes collector number in list that knows number of inports for later reference
        Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, Global_counters.number_of_demandmodels])
        Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Shower Demand from all Demandmodels'])
        self.indoor_demand_coll_list.append(Global_counters.number_of_collectors)
        Global_counters.number_of_collectors += 1
        
        self.check_demandmodel_tap_strings = []
        for q in range(Global_counters.number_of_demandmodels):
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Demand_Model_'+str(q)+'" port="Outport_Check_Tap_[l/h]"/>\n' 
            string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(q+1)+'"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.checkdemandmodelbathstrings = ''
            for o in range(5)[1:]:
                exec 'self.checkdemandmodelbathstrings += string'+str(o)
            self.check_demandmodel_tap_strings.append(self.checkdemandmodelbathstrings)   
        #writes collector number in list that knows number of inports for later reference
        Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, Global_counters.number_of_demandmodels])
        Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Tap Demand from all Demandmodels'])
        self.indoor_demand_coll_list.append(Global_counters.number_of_collectors)
        Global_counters.number_of_collectors += 1
        
        self.check_demandmodel_toilet_strings = []
        for q in range(Global_counters.number_of_demandmodels):
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Demand_Model_'+str(q)+'" port="Outport_Check_Toilet_[l/h]"/>\n' 
            string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(q+1)+'"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.checkdemandmodelbathstrings = ''
            for o in range(5)[1:]:
                exec 'self.checkdemandmodelbathstrings += string'+str(o)
            self.check_demandmodel_toilet_strings.append(self.checkdemandmodelbathstrings)   
        #writes collector number in list that knows number of inports for later reference
        Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, Global_counters.number_of_demandmodels])
        Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Toilet Demand from all Demandmodels'])
        self.indoor_demand_coll_list.append(Global_counters.number_of_collectors)
        Global_counters.number_of_collectors += 1
        
        self.check_demandmodel_washingmachine_strings = []
        for q in range(Global_counters.number_of_demandmodels):
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Demand_Model_'+str(q)+'" port="Outport_Check_Washing_Machine_[l/h]"/>\n' 
            string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(q+1)+'"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.checkdemandmodelbathstrings = ''
            for o in range(5)[1:]:
                exec 'self.checkdemandmodelbathstrings += string'+str(o)
            self.check_demandmodel_washingmachine_strings.append(self.checkdemandmodelbathstrings)   
        #writes collector number in list that knows number of inports for later reference
        Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, Global_counters.number_of_demandmodels])
        Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Washing Machine Demand from all Demandmodels'])
        self.indoor_demand_coll_list.append(Global_counters.number_of_collectors)
        Global_counters.number_of_collectors += 1
        
        self.check_demandmodel_dishwasher_strings = []
        for q in range(Global_counters.number_of_demandmodels):
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Demand_Model_'+str(q)+'" port="Outport_Check_Dishwasher_[l/h]"/>\n' 
            string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(q+1)+'"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.checkdemandmodelbathstrings = ''
            for o in range(5)[1:]:
                exec 'self.checkdemandmodelbathstrings += string'+str(o)
            self.check_demandmodel_dishwasher_strings.append(self.checkdemandmodelbathstrings)   
        #writes collector number in list that knows number of inports for later reference
        Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, Global_counters.number_of_demandmodels])
        Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects Dishwasher Demand from all Demandmodels'])
        self.indoor_demand_coll_list.append(Global_counters.number_of_collectors)
        Global_counters.number_of_collectors += 1
        
        #all indoordemands togehter
        self.check_indoordemand_strings = []
        for q in range(len(self.indoor_demand_coll_list)):
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Collector_'+str(self.indoor_demand_coll_list[q])+'" port="Outport"/>\n' 
            string3='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors)+'" port="Inport_'+str(q+1)+'"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            #writes all string in one and puts it in list
            self.checkindoordemandstrings = ''
            for o in range(5)[1:]:
                exec 'self.checkindoordemandstrings += string'+str(o)
            self.check_indoordemand_strings.append(self.checkindoordemandstrings)   
        #writes collector number in list that knows number of inports for later reference
        Global_counters.number_of_collectors_ports_list.append([Global_counters.number_of_collectors, len(self.indoor_demand_coll_list)])
        Global_meaning_list.collectors.append(['Collector_'+str(Global_counters.number_of_collectors), 'collects entire Indoor Demand from all 6 individuell Collectors'])
        self.need_to_have_filout_list.append([Global_counters.number_of_collectors, 'Indoor_Demand'])
        Global_counters.number_of_collectors += 1
        
        '''
        ads need to have fileouts
        '''
        #adds fileouts to collectors
        self.fileout_strings =[]
        for q in range(len(self.need_to_have_filout_list)):
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
            string2='\t\t\t\t<source node="Collector_'+str(self.need_to_have_filout_list[q][0])+'" port="Outport"/>\n' 
            string3='\t\t\t\t<sink node="FileOut_'+str(Global_counters.number_of_fileouts)+'" port="in"/>\n' 
            string4='\t\t\t</connection>\n' 
            Global_counters.number_of_connections += 1
            
            #writes all string in one and puts it in list
            self.fileoutstrings = ''
            for o in range(5)[1:]:
                exec 'self.fileoutstrings += string'+str(o)
            self.fileout_strings.append(self.fileoutstrings) 
            Global_counters.numbers_names_of_fileouts_list.append([Global_counters.number_of_fileouts, str(self.need_to_have_filout_list[q][1])+'_'+str(i)+'.txt'])
            Global_counters.number_of_fileouts += 1
        
        
        #adds fileout for Sewer
        string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
        string2='\t\t\t\t<source node="Sewer2_'+str(Global_counters.number_of_sewers-1)+'" port="Discharged_Volume"/>\n' 
        string3='\t\t\t\t<sink node="FileOut_'+str(Global_counters.number_of_fileouts)+'" port="in"/>\n' 
        string4='\t\t\t</connection>\n' 
        Global_counters.number_of_connections += 1
        #writes all string in one and puts it in list
        self.fileoutstrings = ''
        for o in range(5)[1:]:
            exec 'self.fileoutstrings += string'+str(o)
        self.fileout_strings.append(self.fileoutstrings)
        Global_counters.numbers_names_of_fileouts_list.append([Global_counters.number_of_fileouts, 'Sewer_'+str(i)+'.txt'])
        Global_counters.number_of_fileouts += 1
        
        #adds fileout for Stormwaterdrain
        string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
        string2='\t\t\t\t<source node="Stormwaterpipe_'+str(Global_counters.number_of_stormwaterpipes-1)+'" port="Discharged_Volume"/>\n' 
        string3='\t\t\t\t<sink node="FileOut_'+str(Global_counters.number_of_fileouts)+'" port="in"/>\n' 
        string4='\t\t\t</connection>\n' 
        Global_counters.number_of_connections += 1
        #writes all string in one and puts it in list
        self.fileoutstrings = ''
        for o in range(5)[1:]:
            exec 'self.fileoutstrings += string'+str(o)
        self.fileout_strings.append(self.fileoutstrings)
        Global_counters.numbers_names_of_fileouts_list.append([Global_counters.number_of_fileouts, 'Stormwaterdrain_'+str(i)+'.txt'])
        Global_counters.number_of_fileouts += 1
        
        #adds fileout for Potable_Water_Resorvoir
        string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n' 
        string2='\t\t\t\t<source node="Potable_Water_Resorvoir_'+str(Global_counters.number_of_potablwaterreservoirs-1)+'" port="Demand"/>\n' 
        string3='\t\t\t\t<sink node="FileOut_'+str(Global_counters.number_of_fileouts)+'" port="in"/> \n ' 
        string4='\t\t\t</connection>\n' 
        Global_counters.number_of_connections += 1
        #writes all string in one and puts it in list
        self.fileoutstrings = ''
        for o in range(5)[1:]:
            exec 'self.fileoutstrings += string'+str(o)
        self.fileout_strings.append(self.fileoutstrings)
        Global_counters.numbers_names_of_fileouts_list.append([Global_counters.number_of_fileouts, 'Potable_Water_Demand_'+str(i)+'.txt'])
        Global_counters.number_of_fileouts += 1
        
        
        for m in range(len(self.Supplylevel_loop_list)):
            self.Supplylevel_list.append(self.Supplylevel_loop_list[m])
        for m in range(len(self.modelinput_strings)):
            self.Supplylevel_list.append(self.modelinput_strings[m])  
        for m in range(len(self.check_greytanks_strings)):
            self.Supplylevel_list.append(self.check_greytanks_strings[m])
        for m in range(len(self.check_stormtanks_strings)):
            self.Supplylevel_list.append(self.check_stormtanks_strings[m])
        for m in range(len(self.check_raintanks_strings)):
            self.Supplylevel_list.append(self.check_raintanks_strings[m])
        for m in range(len(self.check_infiltration_strings)):
            self.Supplylevel_list.append(self.check_infiltration_strings[m])
        for m in range(len(self.check_outdoordemand_strings)):
            self.Supplylevel_list.append(self.check_outdoordemand_strings[m])
        for m in range(len(self.check_demandmodel_bath_strings)):
            self.Supplylevel_list.append(self.check_demandmodel_bath_strings[m])
        for m in range(len(self.check_demandmodel_shower_strings)):
            self.Supplylevel_list.append(self.check_demandmodel_shower_strings[m])
        for m in range(len(self.check_demandmodel_tap_strings)):
            self.Supplylevel_list.append(self.check_demandmodel_tap_strings[m])
        for m in range(len(self.check_demandmodel_toilet_strings)):
            self.Supplylevel_list.append(self.check_demandmodel_toilet_strings[m])
        for m in range(len(self.check_demandmodel_washingmachine_strings)):
            self.Supplylevel_list.append(self.check_demandmodel_washingmachine_strings[m])
        for m in range(len(self.check_demandmodel_dishwasher_strings)):
            self.Supplylevel_list.append(self.check_demandmodel_dishwasher_strings[m])
        for m in range(len(self.check_indoordemand_strings)):
            self.Supplylevel_list.append(self.check_indoordemand_strings[m])
        for m in range(len(self.fileout_strings)):
            self.Supplylevel_list.append(self.fileout_strings[m])
            




#supplyvec =[[[[[6,[1,0]*3,[0,0,0],800],[7,[1]*7,[0,0,0],1],[2,[0,1],[0,0,1],1],0], 
#              [[6,[1,0]*3,[0,0,1],1],[7,[1]*7,[0,0,1],1],[2,[0,1],[0,0,1],1],0],1],
#[[[6,[1,0]*3,[0,0,0],1],[7,[1]*7,[0,0,0],1],[2,[0,1],[0,0,1],1],0], 
# [[6,[1,0]*3,[0,0,1],1],[7,[1]*7,[0,0,1],1],[2,[0,1],[0,0,1],1],1],0]]]
#
#Supplylevel = Supplylevel()
#Supplylevel.writeconnections(supplyvec)            
#
#Supplylevel.stormdrain_strings
#
#
##for i in range(len(Supplylevel.Supplylevel_list)):
##    print Supplylevel.Supplylevel_list[i]
#
#for i in range(len(Supplylevel.check_outdoordemand_strings)):
#    print Supplylevel.check_outdoordemand_strings[i]
   
#print len(Stormwater.Stormwaterreservoirlevel_list)
#print Global_counters.number_of_demandmodels
#print Global_counters.number_of_buildings
#print Global_counters.number_of_connections
#print Global_counters.number_of_greywatertanks     
#print Global_counters.number_of_raintanks
#print Global_counters.number_of_collectors
#print len(Global_counters.number_of_collectors_ports_list)
#print '\n'
#print Global_counters.number_of_distributors
#print Global_counters.number_of_stormwaterpipes
#print Global_counters.number_of_sewers
#print Global_counters.number_of_potablwaterreservoirs
#print Global_counters.number_of_catchments    
    
 
    
    
    
    
    