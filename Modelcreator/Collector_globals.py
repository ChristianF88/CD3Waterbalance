# -*- coding: utf-8 -*-
"""
Created on Tue Dec 02 11:50:05 2014

@author: Acer
"""

class Collector_globals:
    def __init__(self,vector):
        for i in range(len(vector)):
            exec "self.number_of_collectors_"+str(vector[i])+"_inports = 0"
        return