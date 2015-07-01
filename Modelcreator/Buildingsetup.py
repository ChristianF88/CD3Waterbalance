# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:46:53 2015

@author: Gerhard
"""


  
class Buildingsetup:
    
    def __init__(self, numberofBuildings, starting_value_i, **Buildingattributes ):
        self.numberofBuildings = numberofBuildings
        self.Buildingattributelist = []
        self.Buildingnodelist = []
        for i in range(numberofBuildings+starting_value_i)[starting_value_i:]:
            exec 'self.Buildingattributelist.append({"Building_'+str(i)+'" : Buildingattributes})'
            exec '''self.line1='\\t\\t\\t<node id="Building_'+str(i)+'" class="Building"/> \\n' '''
         
            alllines = ''
            for n in range(1):
                exec 'alllines += self.line'+str(n+1)
                
            self.Buildingnodelist.append(alllines)

        print str(numberofBuildings)+' Buildings have been created!'
        return
    
    



    
    
    
    
    
    