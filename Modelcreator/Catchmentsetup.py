# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:46:53 2015

@author: Gerhard
"""


class Catchmentsetup:
    
    def __init__(self, numberofCatchments, starting_value_i, **Catchmentattributes ):
        self.numberofCatchments = numberofCatchments
        self.Catchmentattributelist = []
        self.Catchmentnodelist = []
        for i in range(numberofCatchments+starting_value_i)[starting_value_i:]:
            exec 'self.Catchmentattributelist.append({"Catchment_'+str(i)+'" : dict.copy(Catchmentattributes)})'
        
        print str(numberofCatchments)+' Catchments have been created!'
        return
    
    def Setandwrite_attributes(self,numberofCatchments, starting_value_i, attributevector):
        for i in range(numberofCatchments+starting_value_i)[starting_value_i:]:
            self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Decay_Constant"] = attributevector[i-starting_value_i][0]
            self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Catchment_Area"] = attributevector[i-starting_value_i][1]
            self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Fraktion_of_Impervious_Area_to_Reservoir_iAR"] = attributevector[i-starting_value_i][2]
            self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Fraktion_of_Impervious_Area_to_Stormwater_Drain_iASD"] = attributevector[i-starting_value_i][3]
            self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Fraktion_of_Pervious_Area_pA"] = attributevector[i-starting_value_i][4]
            self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Initial_Infiltration_Capacity"] = attributevector[i-starting_value_i][5]
            self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Final_Infiltration_Capacity"] = attributevector[i-starting_value_i][6]
            self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Depression_Loss"] = attributevector[i-starting_value_i][7]
            self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Wetting_Loss"] = attributevector[i-starting_value_i][8]
            self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Drying_Factor"] = attributevector[i-starting_value_i][9]
            self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Linear_Storage_Factor_Impervious_Area_to_Stormwater_Drain_K"] = attributevector[i-starting_value_i][10]
            self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Linear_Storage_Factor_Pervious_Area_K"] = attributevector[i-starting_value_i][11]
            self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Linear_Storage_Factor_Impervious_Area_to_Reservoir_K"] = attributevector[i-starting_value_i][12]
            self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Catchment_with_or_without_Routing_with_or_without"] = attributevector[i-starting_value_i][13]
        
        for i in range(numberofCatchments+starting_value_i)[starting_value_i:]:
            exec '''self.line1='\\t\\t\\t<node id="Catchment_w_Routing_'+str(i)+'" class="Catchment_w_Routing"> \\n' '''
            exec '''self.line2='\\t\\t\\t\\t<parameter name="Fraktion_of_Impervious_Area_to_Reservoir_iAR_[-]" type="double" value="'+str(self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Fraktion_of_Impervious_Area_to_Reservoir_iAR"])+'"/> \\n ' '''
            exec '''self.line3='\\t\\t\\t\\t<parameter name="Fraktion_of_Impervious_Area_to_Stormwater_Drain_iASD_[-]" type="double" value="'+str(self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Fraktion_of_Impervious_Area_to_Stormwater_Drain_iASD"])+'"/> \\n ' '''
            exec '''self.line4='\\t\\t\\t\\t<parameter name="Depression_Loss_[mm]" type="double" value="'+str(self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Depression_Loss"])+'"/> \\n ' '''
            exec '''self.line5='\\t\\t\\t\\t<parameter name="Linear_Storage_Factor_Impervious_Area_to_Stormwater_Drain_K_[s]" type="double" value="'+str(self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Linear_Storage_Factor_Impervious_Area_to_Stormwater_Drain_K"])+'"/> \\n ' '''
            exec '''self.line6='\\t\\t\\t\\t<parameter name="Linear_Storage_Factor_Impervious_Area_to_Reservoir_K_[s]" type="double" value="'+str(self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Linear_Storage_Factor_Impervious_Area_to_Reservoir_K"])+'"/> \\n ' '''
            exec '''self.line7='\\t\\t\\t\\t<parameter name="Decay_Constant_[1/min]" type="double" value="'+str(self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Decay_Constant"])+'"/> \\n ' '''
            exec '''self.line8='\\t\\t\\t\\t<parameter name="Initial_Infiltration_Capacity_[m/h]" type="double" value="'+str(self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Initial_Infiltration_Capacity"])+'"/> \\n ' '''
            exec '''self.line9='\\t\\t\\t\\t<parameter name="Linear_Storage_Factor_Pervious_Area_K_[s]" type="double" value="'+str(self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Linear_Storage_Factor_Pervious_Area_K"])+'"/> \\n ' '''
            exec '''self.line10='\\t\\t\\t\\t<parameter name="Wetting_Loss_[mm]" type="double" value="'+str(self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Wetting_Loss"])+'"/> \\n ' '''
            exec '''self.line11='\\t\\t\\t\\t<parameter name="Final_Infiltration_Capacity_[m/h]" type="double" value="'+str(self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Final_Infiltration_Capacity"])+'"/> \\n ' '''
            exec '''self.line12='\\t\\t\\t\\t<parameter name="Fraktion_of_Pervious_Area_pA_[-]" type="double" value="'+str(self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Fraktion_of_Pervious_Area_pA"])+'"/> \\n ' '''
            exec '''self.line13='\\t\\t\\t\\t<parameter name="Catchment_Area_[m^2]" type="double" value="'+str(self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Catchment_Area"])+'"/> \\n ' '''
            exec '''self.line14='\\t\\t\\t\\t<parameter name="Drying_Factor_[-]" type="double" value="'+str(self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Drying_Factor"])+'"/> \\n ' '''
            exec '''self.line15='\\t\\t\\t\\t<parameter name="Catchment_with_or_without_Routing_(with_or_without)" type="string" value="'+str(self.Catchmentattributelist[i-starting_value_i][str('Catchment_'+str(i))]["Catchment_with_or_without_Routing_with_or_without"])+'"/> \\n ' '''            
            exec '''self.line16='\\t\\t\\t</node> \\n ' '''        
            
            alllines = ''
            for n in range(16):
                exec 'alllines += self.line'+str(n+1)
            self.Catchmentnodelist.append(alllines)

        
        return





    
    
    
    
    
    