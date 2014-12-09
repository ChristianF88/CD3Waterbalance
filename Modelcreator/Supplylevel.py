# -*- coding: utf-8 -*-
"""
Created on Tue Dec 02 11:20:04 2014

@author: Acer
"""

class Supplylevel:
    def __init__(self):
        self.blackwater_coll_list = []
        self.potablewater_coll_list = []
        self.infiltr_coll_list = []
        self.outdoordemand = []
        
    def writeconnections(self, supplyvec):
        #Preparing lists with collector numbers that have certain amount of outports for later reference(values for nodes)
        for i in range(len(supplyvec)):
            exec "self.numbers_of_collectors_"+str(supplyvec[i][0])+"_inports=[]"