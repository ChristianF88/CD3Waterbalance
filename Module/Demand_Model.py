# -*- coding: utf-8 -*-
"""
Created on Thu Oct 02 08:41:08 2014

@author: Acer
"""

import sys
import pycd3
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

class Demand_Model (pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)

        self.numberpeople = pycd3.Double(4)
        self.addParameter("Number of People living in HH", self.numberpeople)
        self.numberunits = pycd3.Double(4)
        self.addParameter("Number of Householdes", self.numberunits)
        self.unittype = pycd3.String("Residential")
        self.addParameter("Unit Type: Residential or Commercial", self.unittype)

        print "init node"
        
        
    def init(self, start, stop, dt):
        print start
        print stop
        print dt
        
        #simulation start time and stop time for Demand Model
        self.simulation_start_time = date2num(datetime.strptime(str(start.to_datetime()),"%Y-%m-%d %H:%M:%S"))
        self.simulation_stop_time = date2num(datetime.strptime(str(stop.to_datetime()),"%Y-%m-%d %H:%M:%S"))
        
        #start value counting - time - variable for interpolation 
        self.overall_time = date2num(datetime.strptime(str(start.to_datetime()),"%Y-%m-%d %H:%M:%S"))

        #Creating Outports for Demandmodel
        for m in range(self.numberunits):
            exec 'self.Bathtub'+str(m+1)+'=pycd3.Flow()'
            exec 'self.addOutPort("Outport_Bathtub_'+str(m+1)+'_[l/h]", self.Bathtub'+str(m+1)+')'
            
            exec 'self.Shower'+str(m+1)+'=pycd3.Flow()'
            exec 'self.addOutPort("Outport_Shower_'+str(m+1)+'_[l/h]", self.Shower'+str(m+1)+')'
            
            exec 'self.Toilet'+str(m+1)+'=pycd3.Flow()'
            exec 'self.addOutPort("Outport_Toilet_'+str(m+1)+'_[l/h]", self.Toilet'+str(m+1)+')' 
            
            exec 'self.Tap'+str(m+1)+'=pycd3.Flow()'
            exec 'self.addOutPort("Outport_Tap_'+str(m+1)+'_[l/h]", self.Tap'+str(m+1)+')' 
            
            exec 'self.Washing_Machine'+str(m+1)+'=pycd3.Flow()'
            exec 'self.addOutPort("Outport_Washing_Machine_'+str(m+1)+'_[l/h]", self.Washing_Machine'+str(m+1)+')'
            
            exec 'self.Dishwasher'+str(m+1)+'=pycd3.Flow()'
            exec 'self.addOutPort("Outport_Dishwasher_'+str(m+1)+'_[l/h]", self.Dishwasher'+str(m+1)+')'   
         
         
        #preparing empty inp vectors 
        self.Bathtub_demand_factor = []
        self.Shower_demand_factor = []
        self.Toilet_demand_factor = []
        self.Tap_demand_factor = []
        self.Washing_Machine_demand_factor = []
        self.Dishwasher_demand_factor = []
        
        return True
        
        
    def f(self, current, dt):
        
        #first run of demand model, when simulation starts
        if self.overall_time == self.simulation_start_time:
            
            #start value, goin through list, resetting index for next day
            self.hourly_rate = 1
            self.time_facor_index = 0
            
            #getting a random index when new hour begins to simulate random water use at some point over the hour...   
            for n in range( self.numberhouseholds):
                self.Bathtub_demand_factor.append([0 for m in range(3600/dt)])
                self.Bathtub_demand_factor[n][random.randint(0, 3600/dt)] = 1 
                self.Shower_demand_factor.append([0 for m in range(3600/dt)])
                self.Shower_demand_factor[n][random.randint(0, 3600/dt)] = 1
                self.Toilet_demand_factor.append([0 for m in range(3600/dt)])
                self.Toilet_demand_factor[n][random.randint(0, 3600/dt)] = 1
                self.Tap_demand_factor.append([0 for m in range(3600/dt)])
                self.Tap_demand_factor[n][random.randint(0, 3600/dt)] = 1
                self.Washing_Machine_demand_factor.append([0 for m in range(3600/dt)])
                self.Washing_Machine_demand_factor[n][random.randint(0, 3600/dt)] = 1
                self.Dishwasher_demand_factor.append([0 for m in range(3600/dt)])
                self.Dishwasher_demand_factor[n][random.randint(0, 3600/dt)] = 1
                
        
            
        #run demand model for the next day
        elif self.overall_time + dt > ceil(self.overall_time)  :
            
        
        else:
            pass
        
        #lists created form demand model, containing demand vectors at different times time in list would be good
        #example = [[1.1, 2.1, ..., 2.3],[0.1, 1.5, ..., 4.4],....,[0.8, 5.5, ..., 6.4],[1.2, 0.5, ..., 2.4]]
        self.Bathtub_demand =        
        self.Shower_demand =
        self.Toilet_demand =
        self.Tap_demand =
        self.Washing_Machine_ldemand =
        self.Dishwasher_demand =
        
        #interpolation to correct time step
        #interp between example[i-1][0 .... numberhouseholds-1] and example[i][0 .... numberhouseholds-1]
           
        if (self.overall_time + dt) - floor(self.overall_time) > self.hourly_rate/24. and self.hourly_rate/24. <= 1 :
            self.hourly_rate += 1
            
        else:
            self.hourly_rate = 1
            self.time_facor_index = 0
            
            #getting a random index when new hour begins to simulate random water use at some point over the hour...   
            for n in range( self.numberhouseholds):
                self.Bathtub_demand_factor.append([0 for m in range(3600/dt)])
                self.Bathtub_demand_factor[n][random.randint(0, 3600/dt)] = 1 
                self.Shower_demand_factor.append([0 for m in range(3600/dt)])
                self.Shower_demand_factor[n][random.randint(0, 3600/dt)] = 1
                self.Toilet_demand_factor.append([0 for m in range(3600/dt)])
                self.Toilet_demand_factor[n][random.randint(0, 3600/dt)] = 1
                self.Tap_demand_factor.append([0 for m in range(3600/dt)])
                self.Tap_demand_factor[n][random.randint(0, 3600/dt)] = 1
                self.Washing_Machine_demand_factor.append([0 for m in range(3600/dt)])
                self.Washing_Machine_demand_factor[n][random.randint(0, 3600/dt)] = 1
                self.Dishwasher_demand_factor.append([0 for m in range(3600/dt)])
                self.Dishwasher_demand_factor[n][random.randint(0, 3600/dt)] = 1
                
######CHECK ALL IF, DEPENDING OF FORM OF VECTOR!!!        

        
        #result of interp. Vectors with with a length equal to number of households values for dt timestep
        self.Bathtub_vector =        
        self.Shower_vector =
        self.Toilet_vector =
        self.Tap_vector =
        self.Washing_Machine_vector =
        self.Dishwasher_vector =
        
        #creating outports with corresponding value in vector
        #combine with first loop
        for m in range(self.numberhouseholds):
            exec 'self.Bathtub'+str(m+1)+'[0] = self.Bathtub_demand['+str(m)+'][1]['+str(self.hourly_rate)+']*self.Bathtub_demand_factor['+str(m)+']['+str(self.time_facor_index)+']'
            
            exec 'self.Shower'+str(m+1)+'[0] = self.Shower_demand['+str(m)+'][2]['+str(self.hourly_rate)+']*self.Shower_demand_factor['+str(m)+']['+str(self.time_facor_index)+']'
            
            exec 'self.Toilet'+str(m+1)+'[0] = self.Toilet_demand['+str(m)+'][3]['+str(self.hourly_rate)+']*self.Toilet_demand_factor['+str(m)+']['+str(self.time_facor_index)+']'
            
            exec 'self.Tap'+str(m+1)+'[0] = self.Tap_demand['+str(m)+'][4]['+str(self.hourly_rate)+']*self.Tap_demand_factor['+str(m)+']['+str(self.time_facor_index)+']'
            
            exec 'self.Washing_Machine'+str(m+1)+'[0] = self.Washing_Machine_demand['+str(m)+'][5]['+str(self.hourly_rate)+']*self.Washing_Machine_demand_factor['+str(m)+']['+str(self.time_facor_index)+']'
            
            exec 'self.Dishwasher'+str(m+1)+'[0] = self.Dishwasher_demand['+str(m)+'][6]['+str(self.hourly_rate)+']*self.Dishwasher_demand_factor['+str(m)+']['+str(self.time_facor_index)+']'
         
        self.overall_time += dt
        self.time_facor_index += 1

        return dt
    
    def getClassName(self):
        print "getClassName"
        return "Demand_Model"

def register(nr):
    for c in pycd3.Node.__subclasses__():
        nf = NodeFactory(c)
        nf.__disown__()
        nr.addNodeFactory(nf)
        
