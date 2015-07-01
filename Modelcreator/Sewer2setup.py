# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:46:53 2015

@author: Gerhard
"""


class Sewer2setup:
    
    def __init__(self, numberofSewer2s, starting_value_i, **Sewer2attributes ):
        self.numberofSewer2s = numberofSewer2s
        self.Sewer2attributelist = []
        self.Sewer2nodelist = []
        for i in range(numberofSewer2s+starting_value_i)[starting_value_i:]:
            exec 'self.Sewer2attributelist.append({"Sewer2_'+str(i)+'" : Sewer2attributes})'
            exec '''self.line1='\\t\\t\\t<node id="Sewer2_'+str(i)+'" class="Sewer2"/> \\n' '''
         
            alllines = ''
            for n in range(1):
                exec 'alllines += self.line'+str(n+1)
                
            self.Sewer2nodelist.append(alllines)

        print str(numberofSewer2s)+' Sewers have been created!'
        return
    
    



    
    
    
    
    
    