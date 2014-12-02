# -*- coding: utf-8 -*-
"""
Created on Mon Dec 01 15:11:56 2014

@author: Acer
"""



from Global_counters import Global_counters


#Catchment - Household - Raintank

class Householdlevel:
    def __init__(self):
        self.Householdlevel_connection_list=[]
        self.number_of_raintanks_list = []
        self.number_of_households_list = []
        self.number_of_collectors_2_inports = []
        self.number_of_catchments = []

    def writeconnections(self, number_of_householdlevels):
        for i in range(number_of_householdlevels):
            
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
            string2='\t\t\t\t<source node="Catchment_w_Routing_'+str(Global_counters.number_of_catchments)+'" port="Collected_Water"/>\n'
            string3='\t\t\t\t<sink node="Raintank_'+str(Global_counters.number_of_raintanks)+'" port="Collected_Water"/>\n'
            string4='\t\t\t</connection>\n'
            Global_counters.number_of_connections += 1
            string5='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
            string6='\t\t\t\t<source node="Catchment_w_Routing_'+str(Global_counters.number_of_catchments)+'" port="Outdoor_Demand"/>\n'
            string7='\t\t\t\t<sink node="Household_'+str(Global_counters.number_of_households)+'" port="Outdoor_Demand"/>\n'
            string8='\t\t\t</connection>\n'
            Global_counters.number_of_connections += 1
            string9='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
            string10='\t\t\t\t<source node="Catchment_w_Routing_'+str(Global_counters.number_of_catchments)+'" port="Runoff"/>\n'
            string11='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors_2_inports)+'" port="Inport_1"/>\n'
            string12='\t\t\t</connection>\n'
            Global_counters.number_of_connections += 1
            string13='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
            string14='\t\t\t\t<source node="Raintank_'+str(Global_counters.number_of_raintanks)+'" port="Overflow"/>\n'
            string15='\t\t\t\t<sink node="Collector_'+str(Global_counters.number_of_collectors_2_inports)+'" port="Inport_2"/>\n'
            string16='\t\t\t</connection>\n'
            Global_counters.number_of_connections += 1
            string17='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
            string18='\t\t\t\t<source node="Household_'+str(Global_counters.number_of_households)+'" port="Non_Potable_Water"/>\n'
            string19='\t\t\t\t<sink node="Raintank_'+str(Global_counters.number_of_raintanks)+'" port="Non_Potable_Demand"/>\n'
            string20='\t\t\t</connection>\n'
            Global_counters.number_of_connections += 1
            self.allstrings = ''
            for i in range(20):
                exec 'self.allstrings += string'+str(i+1)

            self.Householdlevel_connection_list.append(self.allstrings)
            self.number_of_raintanks_list.append(Global_counters.number_of_raintanks)
            self.number_of_households_list.append(Global_counters.number_of_households)
            self.number_of_collectors_2_inports.append(Global_counters.number_of_collectors_2_inports)
            self.number_of_catchments.append(Global_counters.number_of_catchments)
            
            
        
            Global_counters.number_of_raintanks += 1
            Global_counters.number_of_households += 1
            Global_counters.number_of_collectors_2_inports += 1
            Global_counters.number_of_catchments += 1



