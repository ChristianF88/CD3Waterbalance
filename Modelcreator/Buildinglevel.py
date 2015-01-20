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
        self.numbers_of_buildings_connected_to_stormw = []

    def writeconnections(self, number_of_buildinglevels):
        """
        number_of_buildinglevels = [number of buildings,[greywatertankvector],[contributing to ..., getting GW from GWR, connected to stormwaterreservoir]]
        number_of_buildinglevels = [5,[0,1,0,1,1],[1,0,1]]
        number_of_buildinglevels = [5 buldings,[first b. no gwt, second yes, third no, 4th and 5th yes], [all five contibute to GWR, non gets Water from it, connected to stormwaterreservoir]]        
        """
        #writing strings for each Buildinglevel 
        for i in range(len(number_of_buildinglevels[0])):
            string13='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
            string14='\t\t\t\t<source node="Demand_Model_'+str(Global_counters.number_of_demandmodels)+'" port="Outport_Bathtub_[l/h]"/>\n'
            string15='\t\t\t\t<sink node="Building_'+str(Global_counters.number_of_buildings)+'" port="Bathtub_[l/h]"/>\n'
            string16='\t\t\t</connection>\n'
            Global_counters.number_of_connections += 1
            string17='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
            string18='\t\t\t\t<source node="Demand_Model_'+str(Global_counters.number_of_demandmodels)+'" port="Outport_Shower_[l/h]"/>\n'
            string19='\t\t\t\t<sink node="Building_'+str(Global_counters.number_of_buildings)+'" port="Shower_[l/h]"/>\n'
            string20='\t\t\t</connection>\n'
            Global_counters.number_of_connections += 1
            string21='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
            string22='\t\t\t\t<source node="Demand_Model_'+str(Global_counters.number_of_demandmodels)+'" port="Outport_Toilet_[l/h]"/>\n'
            string23='\t\t\t\t<sink node="Building_'+str(Global_counters.number_of_buildings)+'" port="Toilet_[l/h]"/>\n'
            string24='\t\t\t</connection>\n'
            Global_counters.number_of_connections += 1
            string25='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
            string26='\t\t\t\t<source node="Demand_Model_'+str(Global_counters.number_of_demandmodels)+'" port="Outport_Kitchen_Tap_[l/h]"/>\n'
            string27='\t\t\t\t<sink node="Building_'+str(Global_counters.number_of_buildings)+'" port="Kitchen_Tap_[l/h]"/>\n'
            string28='\t\t\t</connection>\n'
            Global_counters.number_of_connections += 1
            string29='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
            string30='\t\t\t\t<source node="Demand_Model_'+str(Global_counters.number_of_demandmodels)+'" port="Outport_Washing_Machine_[l/h]"/>\n'
            string31='\t\t\t\t<sink node="Building_'+str(Global_counters.number_of_buildings)+'" port="Washing_Machine_[l/h]"/>\n'
            string32='\t\t\t</connection>\n'
            Global_counters.number_of_connections += 1
            string33='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
            string34='\t\t\t\t<source node="Demand_Model_'+str(Global_counters.number_of_demandmodels)+'" port="Outport_Dishwasher_[l/h]"/>\n'
            string35='\t\t\t\t<sink node="Building_'+str(Global_counters.number_of_buildings)+'" port="Dishwasher_[l/h]"/>\n'
            string36='\t\t\t</connection>\n'
            Global_counters.number_of_connections += 1
            string37='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
            string38='\t\t\t\t<source node="Demand_Model_'+str(Global_counters.number_of_demandmodels)+'" port="Outport_Handbasin_Tap_[l/h]"/>\n'
            string39='\t\t\t\t<sink node="Building_'+str(Global_counters.number_of_buildings)+'" port="Handbasin_Tap_[l/h]"/>\n'
            string40='\t\t\t</connection>\n'
            Global_counters.number_of_connections += 1
            string41='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
            string42='\t\t\t\t<source node="Demand_Model_'+str(Global_counters.number_of_demandmodels)+'" port="Outport_Evapcooler_[l/h]"/>\n'
            string43='\t\t\t\t<sink node="Building_'+str(Global_counters.number_of_buildings)+'" port="Evapcooler_[l/h]"/>\n'
            string44='\t\t\t</connection>\n'
            Global_counters.number_of_connections += 1
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
            string10='\t\t\t\t<source node="Building_'+str(Global_counters.number_of_buildings)+'" port="Non_Potable_Demand"/>\n'
            string11='\t\t\t\t<sink node="Raintank_'+str(Global_counters.number_of_raintanks)+'" port="Non_Potable_Demand"/>\n'
            string12='\t\t\t</connection>\n'
            Global_counters.number_of_connections += 1
            
            #adds all strings together
            self.catchment_raintank = ''
            self.catchment_building = ''
            self.building_raintank = ''
            self.demandmodel_building_bathtub = ''
            self.demandmodel_building_kitchen_tap = ''
            self.demandmodel_building_toilet = ''
            self.demandmodel_building_shower = ''
            self.demandmodel_building_washing_machine = ''
            self.demandmodel_building_dishwasher = ''
            self.demandmodel_building_handbasin_tap = ''
            self.demandmodel_building_evapcooler = ''
            for m in range(4):
                exec 'self.catchment_raintank += string'+str(m+1)
                exec 'self.catchment_building += string'+str(m+5)
                exec 'self.building_raintank += string'+str(m+9)
                exec 'self.demandmodel_building_bathtub += string'+str(m+13)
                exec 'self.demandmodel_building_kitchen_tap += string'+str(m+17)
                exec 'self.demandmodel_building_handbasin_tap += string'+str(m+37)
                exec 'self.demandmodel_building_toilet += string'+str(m+21)
                exec 'self.demandmodel_building_shower += string'+str(m+25)
                exec 'self.demandmodel_building_washing_machine += string'+str(m+29)
                exec 'self.demandmodel_building_dishwasher += string'+str(m+33)
                exec 'self.demandmodel_building_evapcooler += string'+str(m+41)
            #writes string in list  
            self.Buildinglevel_connection_list.append(self.demandmodel_building_bathtub)
            self.Buildinglevel_connection_list.append(self.demandmodel_building_kitchen_tap)
            self.Buildinglevel_connection_list.append(self.demandmodel_building_handbasin_tap)
            self.Buildinglevel_connection_list.append(self.demandmodel_building_toilet)
            self.Buildinglevel_connection_list.append(self.demandmodel_building_shower)
            self.Buildinglevel_connection_list.append(self.demandmodel_building_washing_machine)
            self.Buildinglevel_connection_list.append(self.demandmodel_building_dishwasher)
            self.Buildinglevel_connection_list.append(self.demandmodel_building_evapcooler)
            self.Buildinglevel_connection_list.append(self.catchment_raintank)
            self.Buildinglevel_connection_list.append(self.catchment_building)
            self.Buildinglevel_connection_list.append(self.building_raintank)
            
            #adds number of blocks to list
            self.numbers_of_raintanks_list.append(Global_counters.number_of_raintanks)
            self.numbers_of_buildings_list.append(Global_counters.number_of_buildings)
            self.numbers_of_catchments_list.append(Global_counters.number_of_catchments)
            #adds Greywatertanks
            if number_of_buildinglevels[0][i] == 1:
                string37='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
                string38='\t\t\t\t<source node="Raintank_'+str(Global_counters.number_of_raintanks)+'" port="Additional_Demand"/>\n'
                string39='\t\t\t\t<sink node="Greywatertank_'+str(Global_counters.number_of_greywatertanks)+'" port="Greywater_Out"/>\n'
                string40='\t\t\t</connection>\n'
                Global_counters.number_of_connections += 1
                string41='\t\t\t<connection id="'+str(Global_counters.number_of_connections)+'">\n'
                string42='\t\t\t\t<source node="Building_'+str(Global_counters.number_of_buildings)+'" port="Greywater"/>\n'
                string43='\t\t\t\t<sink node="Greywatertank_'+str(Global_counters.number_of_greywatertanks)+'" port="Greywater_In"/>\n'
                string44='\t\t\t</connection>\n'
                Global_counters.number_of_connections += 1
               
                self.raintank_greywatertank = ''
                self.building_greywatertank = ''
                for n in range(4):    
                    exec 'self.raintank_greywatertank += string'+str(n+37)
                    exec 'self.building_greywatertank += string'+str(n+41)
                
                #writes string in list
                self.Buildinglevel_connection_list.append(self.raintank_greywatertank)
                self.Buildinglevel_connection_list.append(self.building_greywatertank)
                
                #adds number of blocks to list
                self.numbers_of_greywatertanks_list.append([Global_counters.number_of_buildings, Global_counters.number_of_greywatertanks])
                
                #prepares blocknumbers for next loop-run
                Global_counters.number_of_greywatertanks += 1
                
            else:
                #adds number of blocks to list
                self.numbers_of_greywatertanks_list.append(Global_counters.number_of_raintanks)
            
            #creating lists with Houses that contribute to GWR/ use for later reference 
            if number_of_buildinglevels[1][0] == 1:
                self.numbers_of_buildings_contributing_gw_list.append(self.numbers_of_greywatertanks_list[i])
            else:
                self.numbers_of_buildings_contributing_gw_list.append('not_contributing to gw '+str(type(self.numbers_of_greywatertanks_list[i])))
                
            if number_of_buildinglevels[1][1] == 1:
                self.numbers_of_buildings_using_gw_list.append(self.numbers_of_greywatertanks_list[i])
            else:
                self.numbers_of_buildings_using_gw_list.append('not using gw')
            
            if number_of_buildinglevels[1][2] == 1:
                self.numbers_of_buildings_connected_to_stormw.append(self.numbers_of_greywatertanks_list[i])
            else:
                self.numbers_of_buildings_connected_to_stormw.append('not connected to SWR')

            
            #prepares blocknumbers for next loop-run
            Global_counters.number_of_raintanks += 1
            Global_counters.number_of_buildings += 1
            Global_counters.number_of_catchments += 1
            Global_counters.number_of_demandmodels += 1
            
            
            
