# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:46:53 2015

@author: Gerhard
"""

class Soilstoragesetup:
       
    def __init__(self, numberofSoilstorage, starting_value_i, **Soilstorageattributes ):
        self.numberofSoilstorage = numberofSoilstorage
        self.Soilstorageattributelist = []
        self.Soilstoragenodelist = []
        for i in range(numberofSoilstorage+starting_value_i)[starting_value_i:]:
            exec 'self.Soilstorageattributelist.append({"Soilstorage_'+str(i)+'" : dict.copy(Soilstorageattributes)})'
        
        print str(numberofSoilstorage)+' Soilstorages have been created!'
        return
    
    def Setandwrite_attributes(self,numberofSoilstorage, starting_value_i, attributevector):
        for i in range(numberofSoilstorage+starting_value_i)[starting_value_i:]:
            self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Depth_Of_Soil"] = attributevector[i-starting_value_i][0]
            self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Initial_Water_Content"] = attributevector[i-starting_value_i][1]
            self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Residual_Water_Content"] = attributevector[i-starting_value_i][2]
            self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Saturation_Water_Content"] = attributevector[i-starting_value_i][3]
            self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Hydraulic_Conductivity_Saturated_Conditions"] = attributevector[i-starting_value_i][4]
            self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Total_Area"] = attributevector[i-starting_value_i][5]
            self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Van_Genuchten_Parameter_Alpha"] = attributevector[i-starting_value_i][6]
            self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Van_Genuchten_Parameter_n"] = attributevector[i-starting_value_i][7]
            self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Field_Capacity"] = attributevector[i-starting_value_i][8]
            self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Outdoor_Demand_Actual_Evapotranspiration_Ratio"] = attributevector[i-starting_value_i][9]
                
        for i in range(numberofSoilstorage+starting_value_i)[starting_value_i:]:
            exec '''self.line1='\\t\\t\\t<node id="Soilstorage_'+str(i)+'" class="Soilstorage"> \\n' '''
            exec '''self.line2='\\t\\t\\t\\t<parameter name="Depth_Of_Soil_[m]" type="double" value="'+str(self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Depth_Of_Soil"])+'"/> \\n ' '''
            exec '''self.line3='\\t\\t\\t\\t<parameter name="Initial_Water_Content_[-]" type="double" value="'+str(self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Initial_Water_Content"])+'"/> \\n ' '''
            exec '''self.line4='\\t\\t\\t\\t<parameter name="Residual_Water_Content_[-]" type="double" value="'+str(self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Residual_Water_Content"])+'"/> \\n ' '''
            exec '''self.line5='\\t\\t\\t\\t<parameter name="Saturation_Water_Content_[-]" type="double" value="'+str(self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Saturation_Water_Content"])+'"/> \\n ' '''
            exec '''self.line6='\\t\\t\\t\\t<parameter name="Hydraulic_Conductivity_(Saturated_Conditions)_[m/d]" type="double" value="'+str(self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Hydraulic_Conductivity_Saturated_Conditions"])+'"/> \\n ' '''
            exec '''self.line7='\\t\\t\\t\\t<parameter name="Total_Area_[m^2]" type="double" value="'+str(self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Total_Area"])+'"/> \\n ' '''
            exec '''self.line8='\\t\\t\\t\\t<parameter name="Van_Genuchten_Parameter_Alpha_[cm^-1]" type="double" value="'+str(self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Van_Genuchten_Parameter_Alpha"])+'"/> \\n ' '''
            exec '''self.line9='\\t\\t\\t\\t<parameter name="Van_Genuchten_Parameter_n_[-]" type="double" value="'+str(self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Van_Genuchten_Parameter_n"])+'"/> \\n ' '''
            exec '''self.line10='\\t\\t\\t\\t<parameter name="Field_Capacity_[cm_Water_Column]" type="double" value="'+str(self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Field_Capacity"])+'"/> \\n ' '''
            exec '''self.line11='\\t\\t\\t\\t<parameter name="Outdoor_Demand_Actual_Evapotranspiration_Ratio_(OutD/ActualEvapotr)_[-]" type="double" value="'+str(self.Soilstorageattributelist[i-starting_value_i][str('Soilstorage_'+str(i))]["Outdoor_Demand_Actual_Evapotranspiration_Ratio"])+'"/> \\n ' '''            
            exec '''self.line12='\\t\\t\\t</node> \\n ' '''        
            
            alllines = ''
            for n in range(12):
                exec 'alllines += self.line'+str(n+1)
            self.Soilstoragenodelist.append(alllines)
        
        return