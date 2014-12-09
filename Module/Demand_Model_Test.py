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
        
        #Inports
        self.numberpeople = pycd3.Double(4)
        self.addParameter("Number of People living in HH", self.numberpeople)
        self.number_residential_units = pycd3.Double(4)
        self.addParameter("Number_of_Residential_Units", self.number_residential_units)
        self.number_commercial_units = pycd3.Double(4)
        self.addParameter("Number_of_Commercial_Units", self.number_commercial_units)
        
        #Outports
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
        
        #Testoutports
        self.TestBathtub=pycd3.Flow()
        self.addOutPort("TestOutport_Bathtub_[l/h]", self.TestBathtub)
        self.TestShower=pycd3.Flow()
        self.addOutPort("TestOutport_Shower_[l/h]", self.TestShower)
        self.TestToilet=pycd3.Flow()
        self.addOutPort("TestOutport_Toilet_[l/h]", self.TestToilet)
        self.TestTap=pycd3.Flow()
        self.addOutPort("TestOutport_Tap_[l/h]", self.TestTap)
        self.TestWashing_Machine=pycd3.Flow()
        self.addOutPort("TestOutport_Washing_Machine_[l/h]", self.TestWashing_Machine)
        self.TestDishwasher=pycd3.Flow()
        self.addOutPort("TestOutport_Dishwasher_[l/h]", self.TestDishwasher)
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

        self.Test=0
       
        return True
        
    
        
        
    def f(self, current, dt):
        
        if dt < 3600 :

            def randomuse(demandtimestep = 3600):
                vector =[0 for m in range(int(ceil(demandtimestep/float(dt))))]
                index = random.randint(0, int(ceil(demandtimestep/float(dt)-1)))
                vector[index]=1
                return vector
    
            #first run of demand model, when simulation starts
            if self.overall_time == self.simulation_start_time:
            
                run = WaterDemandModel([int(self.number_residential_units)],[int(self.number_commercial_units)])
                Demanddictionary = run.getDemands()
                self.shower_vector = add(Demanddictionary['C1']['shower'],Demanddictionary['R1']['shower'])
                self.toilet_vector = add(Demanddictionary['C1']['toilet'],Demanddictionary['R1']['toilet'])
                self.tap_vector = add(Demanddictionary['C1']['tap'],Demanddictionary['R1']['tap'])
                self.bath_vector = Demanddictionary['R1']['bath']
                self.washing_machine_vector = Demanddictionary['R1']['washing_machine']
                self.dishwasher_vector = add(Demanddictionary['C1']['dish_washer'],Demanddictionary['R1']['dish_washer'])
            
            
                #start value, goin through list, resetting index for next day
                self.hourly_rate = int(ceil((around(self.simulation_start_time, decimals=4)-floor(around(self.simulation_start_time, decimals=4)))*24))
                self.time_facor_index = int(floor(((around(self.simulation_start_time, decimals=4)-floor(around(self.simulation_start_time, decimals=4)))*24)%1*10)-1)
            
                self.Bathtub_demand_factor = randomuse(3600-(self.time_facor_index)*dt)
                self.Shower_demand_factor = randomuse(3600-(self.time_facor_index)*dt)
                self.Toilet_demand_factor = randomuse(3600-(self.time_facor_index)*dt)
                self.Tap_demand_factor = randomuse(3600-(self.time_facor_index)*dt)
                self.Washing_Machine_demand_factor = randomuse(3600-(self.time_facor_index)*dt)
                self.Dishwasher_demand_factor = randomuse(3600-(self.time_facor_index)*dt)
                self.string = 'DAY ONE!'            
            
            #run demand model for the next 24 hours
            elif self.overall_time >= ceil(self.overall_time) -1/24. and self.overall_time <= ceil(self.overall_time) -1/24. + (dt)/3600./24. :
                
                run = WaterDemandModel([int(self.number_residential_units)],[int(self.number_commercial_units)])
                Demanddictionary = run.getDemands()
                self.shower_vector = add(Demanddictionary['C1']['shower'],Demanddictionary['R1']['shower'])
                self.toilet_vector = add(Demanddictionary['C1']['toilet'],Demanddictionary['R1']['toilet'])
                self.tap_vector = add(Demanddictionary['C1']['tap'],Demanddictionary['R1']['tap'])
                self.bath_vector = Demanddictionary['R1']['bath']
                self.washing_machine_vector = Demanddictionary['R1']['washing_machine']
                self.dishwasher_vector = add(Demanddictionary['C1']['dish_washer'],Demanddictionary['R1']['dish_washer'])
            
                self.hourly_rate = 0
                self.time_facor_index = 0
                self.Test=0
                self.string = 'NEXT DAY!'  
            
            else:
                pass
        

            #getting a random index when new hour begins to simulate random water use at some point over the hour...  
            if self.overall_time - floor(self.overall_time) > self.hourly_rate/24. and self.overall_time - floor(self.overall_time) < self.hourly_rate/24. + (dt)/3600./24.:
            
                self.hourly_rate += 1
                self.time_facor_index = 0
            
            
                self.Bathtub_demand_factor = randomuse()
                self.Shower_demand_factor = randomuse()
                self.Toilet_demand_factor = randomuse()
                self.Tap_demand_factor = randomuse()
                self.Washing_Machine_demand_factor = randomuse()
                self.Dishwasher_demand_factor = randomuse()
                self.string2 = 'preparing random number'
            else:
                self.string2 =''
                
        
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
   
                 #print [sum(self.Bathtub_demand_factor),sum(self.Shower_demand_factor),sum(self.Toilet_demand_factor),sum(self.Tap_demand_factor),sum(self.Washing_Machine_demand_factor),sum(self.Dishwasher_demand_factor)]
                     
                else:
                    pass
        
            else: 
                pass
  
            self.Bathtub[0] = self.bath_vector[self.hourly_rate]*self.Bathtub_demand_factor[self.time_facor_index]
            self.Shower[0] = self.shower_vector[self.hourly_rate]*self.Shower_demand_factor[self.time_facor_index]
            self.Toilet[0] = self.toilet_vector[self.hourly_rate]*self.Toilet_demand_factor[self.time_facor_index]
            self.Tap[0] = self.tap_vector[self.hourly_rate]*self.Tap_demand_factor[self.time_facor_index]
            self.Washing_Machine[0] = self.washing_machine_vector[self.hourly_rate]*self.Washing_Machine_demand_factor[self.time_facor_index] 
            self.Dishwasher[0] = self.dishwasher_vector[self.hourly_rate]*self.Dishwasher_demand_factor[self.time_facor_index]

            # Test
            if self.Test == 24:
                self.Test = 0
            else:
                pass
            
            self.TestBathtub[0] = self.bath_vector[self.Test]
            self.TestShower[0] = self.shower_vector[self.Test]
            self.TestToilet[0] = self.toilet_vector[self.Test]
            self.TestTap[0] = self.tap_vector[self.Test]
            self.TestWashing_Machine[0] = self.washing_machine_vector[self.Test]
            self.TestDishwasher[0] = self.dishwasher_vector[self.Test]
            
              
            self.overall_time += dt/3600./24.
            self.time_facor_index += 1
            self.Test += 1
            print [self.string,self.string2, self.overall_time, self.hourly_rate, self.time_facor_index]  
        
        elif dt == 3600:
            
            self.hourly_rate = int(ceil((around(self.simulation_start_time, decimals=4)-floor(around(self.simulation_start_time, decimals=4)))*24))
            
            if self.overall_time == self.simulation_start_time:
                run = WaterDemandModel([int(self.number_residential_units)],[int(self.number_commercial_units)])
                Demanddictionary = run.getDemands()
                self.shower_vector = add(Demanddictionary['C1']['shower'],Demanddictionary['R1']['shower'])
                self.toilet_vector = add(Demanddictionary['C1']['toilet'],Demanddictionary['R1']['toilet'])
                self.tap_vector = add(Demanddictionary['C1']['tap'],Demanddictionary['R1']['tap'])
                self.bath_vector = Demanddictionary['R1']['bath']
                self.washing_machine_vector = Demanddictionary['R1']['washing_machine']
                self.dishwasher_vector = add(Demanddictionary['C1']['dish_washer'],Demanddictionary['R1']['dish_washer'])
            elif self.hourly_rate > 23:
                run = WaterDemandModel([int(self.number_residential_units)],[int(self.number_commercial_units)])
                Demanddictionary = run.getDemands()
                self.shower_vector = add(Demanddictionary['C1']['shower'],Demanddictionary['R1']['shower'])
                self.toilet_vector = add(Demanddictionary['C1']['toilet'],Demanddictionary['R1']['toilet'])
                self.tap_vector = add(Demanddictionary['C1']['tap'],Demanddictionary['R1']['tap'])
                self.bath_vector = Demanddictionary['R1']['bath']
                self.washing_machine_vector = Demanddictionary['R1']['washing_machine']
                self.dishwasher_vector = add(Demanddictionary['C1']['dish_washer'],Demanddictionary['R1']['dish_washer'])
                
                self.hourly_rate = 0
                print 'it was greater than 23'
            else:
                pass
        
            self.Bathtub[0] = self.bath_vector[self.hourly_rate]
            self.Shower[0] = self.shower_vector[self.hourly_rate]
            self.Toilet[0] = self.toilet_vector[self.hourly_rate]
            self.Tap[0] = self.tap_vector[self.hourly_rate]
            self.Washing_Machine[0] = self.washing_machine_vector[self.hourly_rate]
            self.Dishwasher[0] = self.dishwasher_vector[self.hourly_rate]
        
            print self.hourly_rate
            self.hourly_rate += 1
        
        else:
            pass
        return dt
    
    def getClassName(self):
        print "getClassName"
        return "Demand_Model"

def register(nr):
    for c in pycd3.Node.__subclasses__():
        nf = NodeFactory(c)
        nf.__disown__()
        nr.addNodeFactory(nf)
        




