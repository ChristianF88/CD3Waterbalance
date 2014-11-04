# -*- coding: utf-8 -*-
"""
Created on Thu Oct 02 08:41:08 2014

@author: Acer
"""

import sys
import pycd3
import csv
from datetime import datetime
from matplotlib.dates import date2num
from scipy.interpolate import interp1d
from numpy.core.fromnumeric import around
from numpy import floor, ceil, arange


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

class Volume_Reader (pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        self.inflow = pycd3.String("")
        self.out = pycd3.Flow()
        
        print "init node"
        self.addParameter("", self.inflow)
        self.addOutPort("out", self.out)
        
        self.growing_t = 0.0
        self.row_to_get = 0
        self.interp_counter = 0
        self.remember_line = 0
        self.decimals = 0.0
        self.rest = 0.0
        self.sum_decimals = 0.0
        
    def init(self, start, stop, dt):
        print start
        print stop
        print dt
        
        csv_file = open(str(self.inflow), "r")       
        self.data = csv.reader(csv_file, delimiter='\t')  
        self.mylist = list(self.data) 
       
        self.dt_read = abs(date2num(datetime.strptime(self.mylist[1][0]+" "+ self.mylist[1][1],"%d.%m.%Y %H:%M:%S")) - date2num(datetime.strptime(self.mylist[0][0]+" "+ self.mylist[0][1],"%d.%m.%Y %H:%M:%S")))
        self.growing_t = date2num(datetime.strptime(self.mylist[0][0]+" "+ self.mylist[0][1],"%d.%m.%Y %H:%M:%S")) + dt/24./3600.
        print 'The files time step is ' + str(int(around(self.dt_read*10*24*360))) +' seconds.'
        print self.row_to_get
        return True
        
    def f(self, current, dt):
        
        #The set time step is equal to the one of the file
        if float(repr(self.dt_read)[:11]) == float(repr(dt/24./3600.)[:11]):
            
            self.row_to_get += 1
            self.out[0] = float(self.mylist[int(0+self.row_to_get)][2])
        
        #The set time step is smaller than the files
        elif float(repr(self.dt_read)[:11]) > float(repr(dt/24./3600.)[:11]):
            
            #initial time step and interpolation
            if self.row_to_get == 0:
                
                self.row_to_get += 1
                #self.growing_t = date2num(datetime.strptime(self.mylist[0][0]+" "+ self.mylist[0][1],"%d.%m.%Y %H:%M:%S")) + dt/24./3600.
                
                #self.date_vector = [date2num(datetime.strptime(self.mylist[0][0]+" "+ self.mylist[0][1],"%d.%m.%Y %H:%M:%S")) , date2num(datetime.strptime(self.mylist[1][0]+" "+ self.mylist[1][1],"%d.%m.%Y %H:%M:%S"))]
                self.flow = float(self.mylist[1][2])
             
                
                self.flow_int = 0.0
                           
            #if the overall time is out of the last interpolation range the next to rows will be interpolated    
            elif self.growing_t > date2num(datetime.strptime(self.mylist[1+self.interp_counter][0]+" "+ self.mylist[1+self.interp_counter][1],"%d.%m.%Y %H:%M:%S")):
                
                self.interp_counter += 1
                
                #self.date_vector = [ date2num(datetime.strptime(self.mylist[int(0+self.interp_counter)][0]+" "+ self.mylist[int(0+self.interp_counter)][1],"%d.%m.%Y %H:%M:%S")) , date2num(datetime.strptime(self.mylist[int(1+self.interp_counter)][0]+" "+ self.mylist[int(1+self.interp_counter)][1],"%d.%m.%Y %H:%M:%S"))]
                self.flow = float(self.mylist[int(1+self.interp_counter)][2])
                
                self.flow_int=0.0
                
            self.flow_int= self.flow / (float(self.dt_read)/(dt/24./3600.))
            
                
            #print self.flow_int   
            self.growing_t += dt/24./3600.
            self.out[0] = float(self.flow_int) 
            
        else:
            self.sum_decimals += float(repr(((dt/24./3600.)/self.dt_read))[1:])
            self.decimals = float(repr(self.sum_decimals-floor(self.sum_decimals))[1:])

            #self.growing_t = date2num(datetime.strptime(self.mylist[0][0]+" "+ self.mylist[0][1],"%d.%m.%Y %H:%M:%S")) + dt/24./3600.
            self.myline = (self.growing_t - date2num(datetime.strptime(self.mylist[0][0]+" "+ self.mylist[0][1],"%d.%m.%Y %H:%M:%S"))) / self.dt_read
            
            if self.myline <= len(self.mylist)-1:
                    
                self.flow_int = 0.0
                self.indexes = [ int(floor(self.remember_line)), int(ceil(self.myline)) ]
                
                for i in arange(self.indexes[0]+1, self.indexes[1]):
                    self.flow_int += float(self.mylist[i][2])
                
                self.flow_int += self.decimals * float(self.mylist[int(ceil(self.myline))][2])+self.rest
                self.growing_t += dt/24./3600.
                self.out[0] = self.flow_int
                
                self.rest = (1-self.decimals)* float(self.mylist[int(ceil(self.myline))][2])
                self.remember_line = self.myline+1
                
            else:
                
                self.flow_int = 0.0
                self.indexes = [ int(floor(self.remember_line)), len(self.mylist)-1 ]
                
                for i in arange(self.indexes[0], self.indexes[1]):
                    self.flow_int += float(self.mylist[i][2])
                    
                print arange(self.indexes[0], self.indexes[1])
                
                self.flow_int += self.rest
                self.growing_t += dt/24./3600.
                self.out[0] = self.flow_int
                
                print int(floor(self.remember_line))
                
        return dt
    
    def getClassName(self):
        print "getClassName"
        return "Volume_Reader"

def register(nr):
    for c in pycd3.Node.__subclasses__():
        nf = NodeFactory(c)
        nf.__disown__()
        nr.addNodeFactory(nf)
        
