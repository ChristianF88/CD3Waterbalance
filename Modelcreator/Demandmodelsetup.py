# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 15:47:44 2014

@author: Acer
"""

class Demandmodelsetup:
       
    def __init__(self, numberofDemand_Models, starting_value_i, **Demand_Modelattributes ):
        self.numberofDemand_Models = numberofDemand_Models
        self.Demand_Modelattributelist = []
        self.Demand_Modelnodelist = []
        for i in range(numberofDemand_Models+starting_value_i)[starting_value_i:]:
            exec 'self.Demand_Modelattributelist.append({"Demand_Model_'+str(i)+'" : Demand_Modelattributes})'
        
        print str(numberofDemand_Models)+' Demand_Models have been created!'
        return
    
    def Setandwrite_attributes(self,numberofDemand_Models, starting_value_i, attributevector):
        for i in range(numberofDemand_Models+starting_value_i)[starting_value_i:]:
            self.Demand_Modelattributelist[i][str('Demand_Model_'+str(i))]["Number_of_Commercial_Units"] = attributevector[i]
            self.Demand_Modelattributelist[i][str('Demand_Model_'+str(i))]["Number_of_Residential_Units"] = attributevector[i]
    
        for i in range(numberofDemand_Models+starting_value_i)[starting_value_i:]:
            exec '''self.line1='\\t\\t\\t<node id="Demand_Model_'+str(i)+'" class="Demand_Model"> \\n' '''
            exec '''self.line2='\\t\\t\\t\\t<parameter name="Number_of_Commercial_Units" type="string" value="'+str(self.Demand_Modelattributelist[i][str('Demand_Model_'+str(i))]["Number_of_Commercial_Units"])+'"/> \\n ' '''
            exec '''self.line3='\\t\\t\\t\\t<parameter name="Number_of_Residential_Units" type="string" value="'+str(self.Demand_Modelattributelist[i][str('Demand_Model_'+str(i))]["Number_of_Residential_Units"])+'"/> \\n ' '''
            exec '''self.line4='\\t\\t\\t</node> \\n ' '''        
            
            alllines = ''
            for n in range(4):
                exec 'alllines += self.line'+str(n+1)
            self.Demand_Modelnodelist.append(alllines)
        
        return




    