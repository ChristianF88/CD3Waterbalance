

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 14:59:00 2014

@author: Acer
"""


  
class Householdsetup:
    
    def __init__(self, numberofHouseholds, starting_value_i, **Householdattributes ):
        self.numberofHouseholds = numberofHouseholds
        self.Householdattributelist = []
        self.Householdnodelist = []
        for i in range(numberofHouseholds+starting_value_i)[starting_value_i:]:
            exec 'self.Householdattributelist.append({"Household_'+str(i)+'" : Householdattributes})'
            exec '''self.line1='\\t\\t\\t<node id="Household_'+str(i)+'" class="Household"/> \\n' '''
         
            alllines = ''
            for n in range(1):
                exec 'alllines += self.line'+str(n+1)
                
            self.Householdnodelist.append(alllines)

        print str(numberofHouseholds)+' Households have been created!'
        return
    
    



    
    
    
    
    
    