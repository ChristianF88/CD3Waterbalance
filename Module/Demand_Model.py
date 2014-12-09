# -*- coding: utf-8 -*-
"""
Created on Thu Oct 02 08:41:08 2014

@author: Acer
"""

import sys
import pycd3
from datetime import datetime
from matplotlib.dates import date2num
import random
from math import floor, ceil
from numpy import add, around
sys.path.append('C:\Users\Acer\Documents\GitHub\CD3Waterbalance\WaterDemandModel')
from C_WaterDemandModel import WaterDemandModel
import config


#class NodeFactory(pycd3.INodeFactory):
#    def __init__(self, node):
#        pycd3.INodeFactory.__init__(self)
#        self.node = node
#        print "NodeFactory.__init__"
#        
#    def getNodeName(self):
#        print "NodeFactory.getName"
#        return self.node.__name__
#        
#    def createNode(self):
#        print "NodeFactory.createNode"
#        n = self.node()
#        n.__disown__()
#        print "NodeFactory.disowned"
#        return n
#        
#    def getSource(self):
#        print "NodeFactory.getSource"
#        return "Practice.py"

class Demand_Model (pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        
        #Inports
        #self.numberpeople = pycd3.Double(4)
        #self.addParameter("Number of People living in Building", self.numberpeople)
        self.number_residential_units = pycd3.Double(4)
        self.addParameter("Number_of_Residential_Units", self.number_residential_units)
        self.number_commercial_units = pycd3.Double(4)
        self.addParameter("Number_of_Commercial_Units", self.number_commercial_units)
        
        #Outports to connect to Household
        self.Bathtub=pycd3.Flow()
        self.addOutPort("Outport_Bathtub_[l/h]", self.Bathtub)
        self.Shower=pycd3.Flow()
        self.addOutPort("Outport_Shower_[l/h]", self.Shower)
        self.Toilet=pycd3.Flow()
        self.addOutPort("Outport_Toilet_[l/h]", self.Toilet)
        self.Tap=pycd3.Flow()
        self.addOutPort("Outport_Tap_[l/h]", self.Tap)
        self.Washing_Machine=pycd3.Flow()
        self.addOutPort("Outport_Washing_Machine_[l/h]", self.Washing_Machine)
        self.Dishwasher=pycd3.Flow()
        self.addOutPort("Outport_Dishwasher_[l/h]", self.Dishwasher)
        
        #Outports to check Demand
        self.CheckBathtub=pycd3.Flow()
        self.addOutPort("Outport_Check_Bathtub_[l/h]", self.CheckBathtub)
        self.CheckShower=pycd3.Flow()
        self.addOutPort("Outport_Check_Shower_[l/h]", self.CheckShower)
        self.CheckToilet=pycd3.Flow()
        self.addOutPort("Outport_Check_Toilet_[l/h]", self.CheckToilet)
        self.CheckTap=pycd3.Flow()
        self.addOutPort("Outport_Check_Tap_[l/h]", self.CheckTap)
        self.CheckWashing_Machine=pycd3.Flow()
        self.addOutPort("Outport_Check_Washing_Machine_[l/h]", self.CheckWashing_Machine)
        self.CheckDishwasher=pycd3.Flow()
        self.addOutPort("Outport_Check_Dishwasher_[l/h]", self.CheckDishwasher)
        print "init node"
        
    def init(self, start, stop, dt):
        print start
        print stop
        print dt
        
        #simulation start time and stop time for Demand Model
        self.simulation_start_time = date2num(datetime.strptime(str(start.to_datetime()),"%Y-%m-%d %H:%M:%S"))
        self.simulation_stop_time = date2num(datetime.strptime(str(stop.to_datetime()),"%Y-%m-%d %H:%M:%S"))
        
        #start value counting - time - variable for interpolation 
        self.overall_time = self.simulation_start_time
      
        return True
        
    def f(self, current, dt):
        #if dt <... größer kleiner als h und größer als tag
    
        #creates vector with zeors and a single 1 at a random spot within the vector
        def randomuse(demandtimestep = 3600):
            vector =[0 for m in range(int(ceil(demandtimestep/float(dt))))]
            index = random.randint(0, int(ceil(demandtimestep/float(dt)-1)))
            vector[index]=1
            return vector

        #first run of demand model, when simulation starts
        if self.overall_time == self.simulation_start_time:
            
            #runs Demandmodel and adds residential and commercial use
            run = WaterDemandModel([int(self.number_residential_units)],[int(self.number_commercial_units)])
            Demanddictionary = run.getDemands()
            self.shower_vector = add(Demanddictionary['C1']['shower'],Demanddictionary['R1']['shower'])
            self.toilet_vector = add(Demanddictionary['C1']['toilet'],Demanddictionary['R1']['toilet'])
            self.tap_vector = add(Demanddictionary['C1']['tap'],Demanddictionary['R1']['tap'])
            self.bath_vector = Demanddictionary['R1']['bath']
            self.washing_machine_vector = Demanddictionary['R1']['washing_machine']
            self.dishwasher_vector = add(Demanddictionary['C1']['dish_washer'],Demanddictionary['R1']['dish_washer'])
             
            #start value, goin through lists, resetting index for next day
            self.hourly_rate = int(ceil((around(self.simulation_start_time, decimals=4)-floor(around(self.simulation_start_time, decimals=4)))*24))
            self.time_facor_index = int(floor(((around(self.simulation_start_time, decimals=4)-floor(around(self.simulation_start_time, decimals=4)))*24)%1*10)-1)
            
            #creating random demand vector eg.:[0,0,..,1,0]
            self.Bathtub_demand_factor = randomuse(3600-(self.time_facor_index)*dt)
            self.Shower_demand_factor = randomuse(3600-(self.time_facor_index)*dt)
            self.Toilet_demand_factor = randomuse(3600-(self.time_facor_index)*dt)
            self.Tap_demand_factor = randomuse(3600-(self.time_facor_index)*dt)
            self.Washing_Machine_demand_factor = randomuse(3600-(self.time_facor_index)*dt)
            self.Dishwasher_demand_factor = randomuse(3600-(self.time_facor_index)*dt)
        
        #run demand model for the next 24 hours
        elif self.overall_time >= ceil(self.overall_time) -1/24. and self.overall_time <= ceil(self.overall_time) -1/24. + (dt)/3600./24. :
            
            #runs Demandmodel and adds residential and commercial use
            run = WaterDemandModel([int(self.number_residential_units)],[int(self.number_commercial_units)])
            Demanddictionary = run.getDemands()
            self.shower_vector = add(Demanddictionary['C1']['shower'],Demanddictionary['R1']['shower'])
            self.toilet_vector = add(Demanddictionary['C1']['toilet'],Demanddictionary['R1']['toilet'])
            self.tap_vector = add(Demanddictionary['C1']['tap'],Demanddictionary['R1']['tap'])
            self.bath_vector = Demanddictionary['R1']['bath']
            self.washing_machine_vector = Demanddictionary['R1']['washing_machine']
            self.dishwasher_vector = add(Demanddictionary['C1']['dish_washer'],Demanddictionary['R1']['dish_washer'])
            
            #resetting counter that index Demandvector and Demandfactorvector
            self.hourly_rate = 0
            self.time_facor_index = 0
            
        else:
            pass
        
        #getting a random index when new hour begins to simulate random water use at some point over the hour...  
        if self.overall_time - floor(self.overall_time) > self.hourly_rate/24. and self.overall_time - floor(self.overall_time) < self.hourly_rate/24. + (dt)/3600./24.:
            
            #counter that index Demandvector and Demandfactorvector
            self.hourly_rate += 1
            self.time_facor_index = 0
            
            #creating random demand vector eg.:[0,0,..,1,0]
            self.Bathtub_demand_factor = randomuse()
            self.Shower_demand_factor = randomuse()
            self.Toilet_demand_factor = randomuse()
            self.Tap_demand_factor = randomuse()
            self.Washing_Machine_demand_factor = randomuse()
            self.Dishwasher_demand_factor = randomuse()
        else:
            pass
        
        '''
        for arkward timesteps like 557 seconds the randomvector is to long and so the single value of one (the factor that creates demand during the hour) could be at the last 
        position of the vector and so not create any demand during that hour. The following if statement solves that problem by checkin the ones postion and if necessary correcting it.
        '''
        if self.overall_time - floor(self.overall_time) +dt/3600./24. > self.hourly_rate/24. and self.overall_time - floor(self.overall_time) < self.hourly_rate/24.:
             self.Bathtub_demand_factor_check = sum(self.Bathtub_demand_factor[:self.time_facor_index+1])
             self.Shower_demand_factor_check = sum(self.Shower_demand_factor[:self.time_facor_index+1])
             self.Toilet_demand_factor_check = sum(self.Toilet_demand_factor[:self.time_facor_index+1])
             self.Tap_demand_factor_check = sum(self.Tap_demand_factor[:self.time_facor_index+1])
             self.Washing_Machine_demand_factor_check = sum(self.Washing_Machine_demand_factor[:self.time_facor_index+1])
             self.Dishwasher_demand_factor_check = sum(self.Dishwasher_demand_factor[:self.time_facor_index+1])
             
             if  self.Bathtub_demand_factor_check != 1 or self.Shower_demand_factor_check != 1 or self.Toilet_demand_factor_check != 1 or self.Tap_demand_factor_check != 1 or self.Washing_Machine_demand_factor_check != 1 or self.Dishwasher_demand_factor_check != 1:
                 
                 if self.Bathtub_demand_factor_check != 1:
                     self.Bathtub_demand_factor[self.time_facor_index] = 1
                     self.Bathtub_demand_factor[self.time_facor_index + 1] = 0
                 else:
                     pass      
                 if self.Shower_demand_factor_check != 1:
                     self.Shower_demand_factor[self.time_facor_index] = 1
                     self.Shower_demand_factor[self.time_facor_index + 1] = 0
                 else:
                     pass
                 if self.Toilet_demand_factor_check != 1:
                     self.Toilet_demand_factor[self.time_facor_index] = 1
                     self.Toilet_demand_factor[self.time_facor_index + 1] = 0
                 else:
                     pass
                 if self.Tap_demand_factor_check != 1:
                     self.Tap_demand_factor[self.time_facor_index] = 1
                     self.Tap_demand_factor[self.time_facor_index + 1] = 0
                 else:
                     pass
                 if self.Washing_Machine_demand_factor_check != 1:
                     self.Washing_Machine_demand_factor[self.time_facor_index] = 1
                     self.Washing_Machine_demand_factor[self.time_facor_index + 1] = 0
                 else:
                     pass
                 if self.Dishwasher_demand_factor_check != 1:
                     self.Dishwasher_demand_factor[self.time_facor_index] = 1
                     self.Dishwasher_demand_factor[self.time_facor_index + 1] = 0
                 else:
                     pass   
             else:
                 pass
        else: 
            pass
          
        #Outports for connecting to Builing
        self.Bathtub[0] = self.bath_vector[self.hourly_rate]*self.Bathtub_demand_factor[self.time_facor_index]
        self.Shower[0] = self.shower_vector[self.hourly_rate]*self.Shower_demand_factor[self.time_facor_index]
        self.Toilet[0] = self.toilet_vector[self.hourly_rate]*self.Toilet_demand_factor[self.time_facor_index]
        self.Tap[0] = self.tap_vector[self.hourly_rate]*self.Tap_demand_factor[self.time_facor_index]
        self.Washing_Machine[0] = self.washing_machine_vector[self.hourly_rate]*self.Washing_Machine_demand_factor[self.time_facor_index] 
        self.Dishwasher[0] = self.dishwasher_vector[self.hourly_rate]*self.Dishwasher_demand_factor[self.time_facor_index]

        '''
        what time steps ought to be necessarry?!?!?!!?!?!
        '''
        #Outports for Checking Demand
        self.CheckBathtub[0] = self.Bathtub[0]
        self.CheckShower[0] = self.Shower[0]
        self.CheckToilet[0] = self.Toilet[0]
        self.CheckTap[0] = self.Tap[0]
        self.CheckWashing_Machine[0] = self.Washing_Machine[0]
        self.CheckDishwasher[0] = self.Dishwasher[0]
        
        #counter that index Demandvector and Demandfactorvector
        self.overall_time += dt/3600./24.
        self.time_facor_index += 1
#        print [self.string,self.string2, self.overall_time, self.hourly_rate, self.time_facor_index]  
        
        return dt
    
    def getClassName(self):
        print "getClassName"
        return "Demand_Model"

#def register(nr):
#    for c in pycd3.Node.__subclasses__():
#        nf = NodeFactory(c)
#        nf.__disown__()
#        nr.addNodeFactory(nf)





