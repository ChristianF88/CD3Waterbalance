# -*- coding: utf-8 -*-
"""
Created on Thu Oct 02 08:41:08 2014

@author: Acer
"""

import sys
import pycd3
import csv
from datetime import datetime
from scipy.interpolate import interp1d

class NodeFactory(pycd3.INodeFactory):
    def __init__(self, node):
        pycd3.INodeFactory.__init__(self)
        self.node = node
        print "NodeFactory.__init__"
        
    def getNodeName(self):
        print "NodeFactory.getName"
        return self.node.__name__
        
    def createNode(self):
        print "NodeFactory.createNode"
        n = self.node()
        n.__disown__()
        print "NodeFactory.disowned"
        return n
        
    def getSource(self):
        print "NodeFactory.getSource"
        return "Practice.py"

class Inflow_Reader(pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        self.inflow = pycd3.String("")
        self.out = pycd3.Flow()
        
        print "init node"
        self.intern_addParameter("", self.inflow)
        self.addOutPort("out", self.out)
        
        self.growing_t = 0.0
        self.row_to_get = 0.0
        self.interp_counter = 0.0
        self.line_counter = 0.0
        self.flow_vector = []
        
    def init(self, start, stop, dt):
        print start
        print stop
        print dt
        self.list_csv=[]
        with open(self.inflow) as csvfile:
            self.data = csv.reader(csvfile, delimiter=' ')  
            #list alles aus oder?!
            self.list = list(self.data) 
            
        #get dt
        self.dt_read = abs(date2num(datetime.strptime(self.list[1][0].split[0]+" "+ self.list[1][0].split[1],"%d.%m.%Y %H:%M:%S")) - date2num(datetime.strptime(self.list[0][0].split[0]+" "+ self.list[0][0].split[1],"%d.%m.%Y %H:%M:%S")))
        return True
        
    def f(self, current, dt):
        
        #The set time step is equal to the one of the file
        if float(repr(self.dt_read))[:11] == float(repr(dt/24./3600.))[:11]:
            
            #flow format- [date(dd.mm.yyyy)         time(hh:mm:ss)        bath(l/h)       shower(l/h)         toilet(l/h)      tap((l/h)      washing machine(l/h)      dishwasher(l/h)]
            #flow vector output [bath(l/h)       shower(l/h)         toilet(l/h)      tap((l/h)      washing machine(l/h)      dishwasher(l/h)]
            self.out[0] = [self.list[0+self.row_to_get][0].split[2], self.list[0+self.row_to_get][0].split[3], self.list[0+self.row_to_get][0].split[4], self.list[0+self.row_to_get][0].split[5], self.list[0+self.row_to_get][0].split[6], self.list[0+self.row_to_get][0].split[7]]
            self.row_to_get += 1
        
        #The set time step is smaller than the files
        elif float(repr(self.dt_read))[:11] > float(repr(dt/24./3600.))[:11]:
            
            #initial time step and interpolation
            if self.row_to_get == 0:
                
                self.date_vector = [ date2num(datetime.strptime(self.list[0][0].split[0]+" "+ self.list[0][0].split[1],"%d.%m.%Y %H:%M:%S")) , date2num(datetime.strptime(self.list[1][0].split[0]+" "+ self.list[1][0].split[1],"%d.%m.%Y %H:%M:%S"))]
                self.bath = [self.list[0][0].split[2], self.list[1][0].split[2] ]
                self.shower = [self.list[0][0].split[3], self.list[1][0].split[3] ]
                self.toilet = [self.list[0][0].split[4], self.list[1][0].split[4] ]
                self.tap = [self.list[0][0].split[5], self.list[1][0].split[5] ]
                self.washing_m = [self.list[0][0].split[6], self.list[1][0].split[6] ]
                self.dishwasher = [self.list[0][0].split[7], self.list[1][0].split[7] ]
    
                self.bath_int = interp1d(self.date_vector, self.bath)
                self.shower_int = interp1d(self.date_vector, self.shower)
                self.toilet_int = interp1d(self.date_vector, self.toilet)
                self.tap_int = interp1d(self.date_vector, self.tap)
                self.washing_m_int = interp1d(self.date_vector, self.washing_m)
                self.dishwasher_int = interp1d(self.date_vector, self.dishwasher)

                self.spacing=linspace(self.date_vector[0],self.date_vector[1],24*10+1)

                self.bath_int=self.bath_int(self.spacing)
                self.shower_int = self.shower_int(self.spacing)
                self.toilet_int = self.toilet_int(self.spacing)
                self.tap_int = self.tap_int(self.spacing)
                self.washing_m_int = self.washing_m_int(self.spacing)
                self.dishwasher_int =self.dishwasher_int(self.spacing)

                
                self.row_to_get += 1
                self.growing_t = date2num(datetime.strptime(self.list[0][0].split[0]+" "+ self.list[0][0].split[1],"%d.%m.%Y %H:%M:%S"))
                
            #if the overall time is out of the last interpolation range the next to rows will be interpolated    
            elif self.growing_t > date2num(datetime.strptime(self.list[1+self.interp_counter][0].split[0]+" "+ self.list[1+self.interp_counter][0].split[1],"%d.%m.%Y %H:%M:%S")):
                
                self.interp_counter += 1
                self.line_counter = 1.0
                self.date_vector = [ date2num(datetime.strptime(self.list[0+self.interp_counter][0].split[0]+" "+ self.list[0+self.interp_counter][0].split[1],"%d.%m.%Y %H:%M:%S")) , date2num(datetime.strptime(self.list[1+self.interp_counter][0].split[0]+" "+ self.list[1+self.interp_counter][0].split[1],"%d.%m.%Y %H:%M:%S"))]
                self.bath = [self.list[0+self.interp_counter][0].split[2], self.list[1+self.interp_counter][0].split[2] ]
                self.shower = [self.list[0+self.interp_counter][0].split[3], self.list[1+self.interp_counter][0].split[3] ]
                self.toilet = [self.list[0+self.interp_counter][0].split[4], self.list[1+self.interp_counter][0].split[4] ]
                self.tap = [self.list[0+self.interp_counter][0].split[5], self.list[1+self.interp_counter][0].split[5] ]
                self.washing_m = [self.list[0+self.interp_counter][0].split[6], self.list[1+self.interp_counter][0].split[6] ]
                self.dishwasher = [self.list[0+self.interp_counter][0].split[7], self.list[1+self.interp_counter][0].split[7] ]
    
                self.bath_int = interp1d(self.date_vector, self.bath)
                self.shower_int = interp1d(self.date_vector, self.shower)
                self.toilet_int = interp1d(self.date_vector, self.toilet)
                self.tap_int = interp1d(self.date_vector, self.tap)
                self.washing_m_int = interp1d(self.date_vector, self.washing_m)
                self.dishwasher_int = interp1d(self.date_vector, self.dishwasher)

                self.spacing=linspace(self.date_vector[0],self.date_vector[1],24*10+1)

                self.bath_int=self.bath_int(self.spacing)
                self.shower_int = self.shower_int(self.spacing)
                self.toilet_int = self.toilet_int(self.spacing)
                self.tap_int = self.tap_int(self.spacing)
                self.washing_m_int = self.washing_m_int(self.spacing)
                self.dishwasher_int =self.dishwasher_int(self.spacing)
                
                
            #returning flow vector 
            #flow vector output [bath(l/h)       shower(l/h)         toilet(l/h)      tap((l/h)      washing machine(l/h)      dishwasher(l/h)]
            self.growing_t += dt/24./3600.
            self.flow_vector.append([self.bath_int[self.line_counter][1], self.shower_int[self.line_counter][1], self.toilet_int[self.line_counter][1], self.tap_int[self.line_counter][1], self.washing_m_int[self.line_counter][1], self.dishwasher_int[self.line_counter][1]])
            self.out[0] = self.flow_vector[-1]
            self.line_counter += 1
            
            
            
        return dt
    
    def getClassName(self):
        print "getClassName"
        return "Inflow_Reader"

def register(nr):
    for c in pycd3.Node.__subclasses__():
        nf = NodeFactory(c)
        nf.__disown__()
        nr.addNodeFactory(nf)
        
# def test():
#     nr = pycd3.NodeRegistry()
#     nf = NodeFactory(Household).__disown__()
#     nr.addNodeFactory(nf)
#     node = nr.createNode("Household")
    
#test()
