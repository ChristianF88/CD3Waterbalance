# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:46:53 2015

@author: Gerhard
"""


class Stormwaterdrainsetup:
    
    def __init__(self, numberofStormwaterpipes, starting_value_i, **Stormwaterpipeattributes ):
        self.numberofStormwaterpipes = numberofStormwaterpipes
        self.Stormwaterpipeattributelist = []
        self.Stormwaterpipenodelist = []
        for i in range(numberofStormwaterpipes+starting_value_i)[starting_value_i:]:
            exec 'self.Stormwaterpipeattributelist.append({"Stormwaterpipe_'+str(i)+'" : Stormwaterpipeattributes})'
            exec '''self.line1='\\t\\t\\t<node id="Stormwaterdrain_'+str(i)+'" class="Stormwaterdrain"/> \\n' '''
         
            alllines = ''
            for n in range(1):
                exec 'alllines += self.line'+str(n+1)
                
            self.Stormwaterpipenodelist.append(alllines)

        print str(numberofStormwaterpipes)+' Stormwaterdrains have been created!'
        return
    
    



    
    
    
    
    
    