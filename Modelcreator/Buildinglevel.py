# -*- coding: utf-8 -*-
"""
Created on Mon Dec 01 15:11:56 2014

@author: Acer
"""



from Global_counters import Global_counters


#The Buildinglevel consistis out of 3 connections and 3 blocks Catchment - Household - Raintank
class Buildinglevel:
    def __init__(self):
        #preparing lists that will be used for reference in other classes
        self.Buildinglevel_connection_list=[]
        self.numbers_of_raintanks_list = []
        self.numbers_of_buildings_list = []
        self.numbers_of_greywatertanks_list = []
        self.numbers_of_catchments_list = []
        self.numbers_of_buildings_contributing_gw_list = []
        self.numbers_of_buildings_using_gw_list = []

    def writeconnections(self, number_of_buildinglevels):
        """
        number_of_buildinglevels = [number of buildings,[greywatertankvector],[contributing to ..., getting GW from GWR]]
        number_of_buildinglevels = [5,[0,1,0,1,1],[1,0]]
        number_of_buildinglevels = [5 buldings,[first b. no gwt, second yes, third no, 4th and 5th yes], [all five contibute to GWR, non gets Water from it]]        
        """
        #writing strings for each Buildinglevel 
        for i in range(number_of_buildinglevels[0]):
            string1='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
            string2='\t\t\t\t<source node="Catchment_w_Routing_'+str(Global_counters.number_of_catchments)+'" port="Collected_Water"/>\n'
            string3='\t\t\t\t<sink node="Raintank_'+str(Global_counters.number_of_raintanks)+'" port="Collected_Water"/>\n'
            string4='\t\t\t</connection>\n'
            Global_counters.number_of_connections += 1
            string5='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
            string6='\t\t\t\t<source node="Catchment_w_Routing_'+str(Global_counters.number_of_catchments)+'" port="Outdoor_Demand"/>\n'
            string7='\t\t\t\t<sink node="Building_'+str(Global_counters.number_of_buildings)+'" port="Outdoor_Demand"/>\n'
            string8='\t\t\t</connection>\n'
            Global_counters.number_of_connections += 1
            string9='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
            string10='\t\t\t\t<source node="Building_'+str(Global_counters.number_of_buildings)+'" port="Non_Potable_Water"/>\n'
            string11='\t\t\t\t<sink node="Raintank_'+str(Global_counters.number_of_raintanks)+'" port="Non_Potable_Demand"/>\n'
            string12='\t\t\t</connection>\n'
            Global_counters.number_of_connections += 1
            #adds all strings together
            self.catchment_raintank = ''
            self.catchment_building = ''
            self.building_raintank = ''
            for m in range(4):
                exec 'self.catchment_raintank += string'+str(m+1)
                exec 'self.catchment_building += string'+str(m+5)
                exec 'self.building_raintank += string'+str(m+9)
            
            #writes string in list  
            self.Buildinglevel_connection_list.append(self.catchment_raintank)
            self.Buildinglevel_connection_list.append(self.catchment_building)
            self.Buildinglevel_connection_list.append(self.building_raintank)
            #adds number of blocks to list
            self.numbers_of_raintanks_list.append(Global_counters.number_of_raintanks)
            self.numbers_of_buildings_list.append(Global_counters.number_of_buildings)
            self.numbers_of_catchments_list.append(Global_counters.number_of_catchments)
            #adds Greywatertanks
            if number_of_buildinglevels[1][i] == 1:
                string13='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
                string14='\t\t\t\t<source node="Raintank_'+str(Global_counters.number_of_raintanks)+'" port="Additional_Demand"/>\n'
                string15='\t\t\t\t<sink node="Greywatertank_'+str(Global_counters.number_of_greywatertanks)+'" port="Treated_Grey_Water_Out"/>\n'
                string16='\t\t\t</connection>\n'
                Global_counters.number_of_connections += 1
                string17='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
                string18='\t\t\t\t<source node="Building_'+str(Global_counters.number_of_buildings)+'" port="Grey_Water"/>\n'
                string19='\t\t\t\t<sink node="Greywatertank_'+str(Global_counters.number_of_greywatertanks)+'" port="Grey_Water_In"/>\n'
                string20='\t\t\t</connection>\n'
                Global_counters.number_of_connections += 1
               
                self.raintank_greywatertank = ''
                self.building_greywatertank = ''
                for n in range(4):    
                    exec 'self.raintank_greywatertank += string'+str(n+13)
                    exec 'self.building_greywatertank += string'+str(n+17)
                
                #writes string in list
                self.Buildinglevel_connection_list.append(self.building_greywatertank)
                self.Buildinglevel_connection_list.append(self.raintank_greywatertank)
                #adds number of blocks to list
                self.numbers_of_greywatertanks_list.append([Global_counters.number_of_buildings, Global_counters.number_of_greywatertanks])
                
                #prepares blocknumbers for next loop-run
                Global_counters.number_of_greywatertanks += 1
                
            else:
                #adds number of blocks to list
                self.numbers_of_greywatertanks_list.append(Global_counters.number_of_greywatertanks)
            
            #creating lists with Houses that contribute to GWR/ use for later reference 
            if number_of_buildinglevels[2][0] == 1:
                self.numbers_of_buildings_contributing_gw_list.append(self.numbers_of_greywatertanks_list[i])
            else:
                self.numbers_of_buildings_contributing_gw_list.append('not_contributing to gw')
                
            
            if number_of_buildinglevels[2][1] == 1:
                self.numbers_of_buildings_using_gw_list.append(self.numbers_of_greywatertanks_list[i])
            else:
                self.numbers_of_buildings_using_gw_list.append('not using gw')
            
            #prepares blocknumbers for next loop-run
            Global_counters.number_of_raintanks += 1
            Global_counters.number_of_buildings += 1
            Global_counters.number_of_catchments += 1
            



