# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:46:53 2015

@author: Gerhard
"""

import sys
import pycd3
import math
import numpy

#class NodeFactoryCatchmentwithRouting(pycd3.INodeFactory):
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
#        return "Addons.py"

class Catchment_w_Routing(pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        self.rain = pycd3.Flow()
        self.collected_w = pycd3.Flow()
        self.runoff = pycd3.Flow()
#        self.evapo = pycd3.Flow()
        self.possible_infiltr = pycd3.Flow()
        self.actual_infiltr = pycd3.Flow()
#        self.outdoor_use = pycd3.Flow()
        self.inflow = pycd3.Flow()
        self.gardensize = pycd3.Flow()
        
        #dir (self.inf)
#        print "init node"
        self.addInPort("Rain", self.rain)
#        self.addInPort("Evapotranspiration", self.evapo)
        self.addInPort("Inflow", self.inflow)
        self.addOutPort("Possible_Infiltration", self.possible_infiltr)
        self.addOutPort("To_Soilstorage", self.actual_infiltr)
        self.addOutPort("Runoff", self.runoff)
        self.addOutPort("Collected_Water", self.collected_w)
        self.addOutPort("Gardensize", self.gardensize)
#        self.addOutPort("Outdoor_Demand_Check", self.outdoor_use_check)
        
        #Catchment with Routing or without
        self.select_model = pycd3.String("without")
        self.addParameter("Catchment_with_or_without_Routing_(with_or_without)", self.select_model)        
        
        self.dryrate = pycd3.Double(1.4)
        self.addParameter("Average_Evaporationrate_[mm/d]", self.dryrate) 
        
        #Catchment area + fraction info of pervious and impervious parts
        self.area_property = pycd3.Double(1000)
        self.addParameter("Catchment_Area_[m^2]", self.area_property)
        self.perv_area = pycd3.Double(0.4)
        self.addParameter("Fraktion_of_Pervious_Area_pA_[-]", self.perv_area)
        self.imp_area_stormwater = pycd3.Double(0.4)
        self.addParameter("Fraktion_of_Impervious_Area_to_Stormwater_Drain_iASD_[-]", self.imp_area_stormwater)
        self.imp_area_raintank = pycd3.Double(0.2)
        self.addParameter("Fraktion_of_Impervious_Area_to_Reservoir_iAR_[-]", self.imp_area_raintank)
        
        #default values for gras (Wikipedia)
        self.Horton_initial_cap = pycd3.Double(0.9)                             
        self.addParameter("Initial_Infiltration_Capacity_[m/h]", self.Horton_initial_cap)
        self.Horton_final_cap = pycd3.Double(0.29)                              
        self.addParameter("Final_Infiltration_Capacity_[m/h]", self.Horton_final_cap)
        self.Horton_decay_constant = pycd3.Double(2.0)                          
        self.addParameter("Decay_Constant_[1/min]", self.Horton_decay_constant)
        
        #default values for suburbs (scrip Prof. Krebs)
        self.depression_loss = pycd3.Double(1.5)                                
        self.addParameter("Depression_Loss_[mm]", self.depression_loss)
        
        #default values for (scrip Prof. Krebs)
        self.initial_loss = pycd3.Double(0.4)                                   
        self.addParameter("Wetting_Loss_[mm]", self.initial_loss)
        
        #factor for calibrating outdoordemand
#        self.outdoor_demand_coefficient = pycd3.Double(0.5)
#        self.addParameter("Outdoor_Demand_Weighing_Factor_[-]", self.outdoor_demand_coefficient)
        
        #linear storage coefficients for each surface type 
        self.linearstorage_perv_K = pycd3.Double(1000)
        self.addParameter("Linear_Storage_Factor_Pervious_Area_K_[s]", self.linearstorage_perv_K)
        self.linearstorage_imperv_res_K = pycd3.Double(1000)
        self.addParameter("Linear_Storage_Factor_Impervious_Area_to_Reservoir_K_[s]", self.linearstorage_imperv_res_K)
        self.linearstorage_imperv_storm_K = pycd3.Double(1000)
        self.addParameter("Linear_Storage_Factor_Impervious_Area_to_Stormwater_Drain_K_[s]", self.linearstorage_imperv_storm_K)
        
        #storage and time values
        self.rainmemory = 0.0
        self.rain_storage_imp = 0.0
        self.continuous_rain_time = 0.0
        self.continuous_rain_time_2 = 0.0                                        
        self.rain_storage_perv = 0.0
        
        #variable to check Horten model 
        self.k=1
        
        #storage for linear storage model
        self.collected_w_raw = 0.0
        self.runoff_raw = 0.0
        self.runoff_perv_raw=0.0

    def init(self, start, stop, dt):
#        print start
#        print stop
#        print dt

        #starting values for Horton model
        self.possible_infiltr_raw = self.Horton_initial_cap/3600.*dt
        self.temp_cap = self.Horton_initial_cap/3600.*dt
        self.temp_cap_2 = self.Horton_initial_cap/3600.*dt
        
        #switches between linear storage model and a simple catchment model excluding routing
        if self.select_model == "with":

            self.Qbefore = [0,0,0]
            
        elif self.select_model == "without":
            pass
        else:
            print "Model selection not valid!"
            
        return True
        
    def f(self, current, dt):
        
        #describing the current rain that doesnt evaporate in the same timestep
        #resetting the time values for the Horton model
        #delay in possible infiltration by 1 * dt when time value reset to 0.0 now set to 1 real time
        if self.rainmemory == 0.0:
            self.rainmemory= self.rain[0]
            if self.rain[0] == 0.0:
                pass
            else:
                self.continuous_rain_time=1.0
        elif self.rainmemory > 0.0:
            self.rainmemory= self.rain[0]
            if self.rain[0] == 0.0:
                self.continuous_rain_time_2=1.0
            else:
                pass
        else:
            self.rainmemory= self.rain[0]
         
         
        self.gardensize[0] = self.area_property*self.perv_area
        
        #if the effective currrent rain height equals zero there wont be any runoff thus no water collection as well as no infiltration
        #there wont be any need of watering gardens (no outdoor use)
        if self.rain[0] == 0.0:
            
            self.collected_w_raw = 0.0
            self.runoff_raw = 0.0
            self.actual_infiltr[0] = 0.0                             
            self.runoff_perv_raw = 0.0

            #resetting the storage values as a simulation of the drying process respectively the continuous infitlration
            if self.rain_storage_perv > 0:
                self.rain_storage_perv -= self.dryrate/24/3600*dt
                if self.rain_storage_perv > 0:
                    pass
                else:
                    self.rain_storage_perv = 0.0
            else:
                self.rain_storage_perv = 0.0
                                
            if self.rain_storage_imp > 0:
                self.rain_storage_imp -= self.dryrate/24/3600*dt
                if self.rain_storage_imp > 0:
                    pass
                else:
                    self.rain_storage_imp = 0.0
            else:
                self.rain_storage_imp = 0.0
            
            #calculating the possilbe infiltration rate the the Horton model in a state of "drying" (+ increasing the time step for the model)
            self.temp_cap = self.Horton_final_cap/3600.*dt + (self.temp_cap_2 - self.Horton_final_cap/3600.*dt) * math.exp(-1*self.Horton_decay_constant * dt / (60.*6.) * self.continuous_rain_time/self.k)
            self.possible_infiltr_raw = self.Horton_initial_cap/3600.*dt - (self.Horton_initial_cap/3600.*dt - self.temp_cap) * math.exp(-1*self.Horton_decay_constant * dt / 60. * self.continuous_rain_time_2/self.k)
            self.continuous_rain_time_2 += 1.0
           
 
        #if the current effective rain height equals a value higher zero there will be infiltration, runoff and collected water
        #as soon as the initial loss has been overcome, outdoor use will be zero
        else:
            
            #calculating the current rain storage values to keep track of when the rain loss has been overcome,
            #as well as calculating the possilbe infiltration rate the the Horton model in a state of "wetting" (+ increasing the time step for the model)
            self.rain_storage_imp += self.rain[0]
            self.rain_storage_perv += self.rain[0]
            
            self.temp_cap_2 = self.Horton_initial_cap/3600.*dt - (self.Horton_initial_cap/3600*dt - self.temp_cap) * math.exp(-1*self.Horton_decay_constant * dt / 60. * self.continuous_rain_time_2/self.k)
            self.possible_infiltr_raw = self.Horton_final_cap/3600.*dt + (self.temp_cap_2 - self.Horton_final_cap/3600.*dt) * math.exp(-1*self.Horton_decay_constant * dt / 60. * self.continuous_rain_time/self.k)
            self.continuous_rain_time += 1.0
            

            #if the wetting loss and depression loss hasn't been overcome yet, there won't be any runoff from the impervious area
            #that contributes to stormwater
            if self.rain_storage_imp - self.initial_loss - self.depression_loss <= 0.0:
                
                #if the wetting loss hasn't beem overcome there will be no flow...
                if self.rain_storage_perv - self.initial_loss <= 0.0:
                
                    self.collected_w_raw = 0.0
                    self.runoff_raw = 0.0
                    self.actual_infiltr[0] =0.0

                    self.runoff_perv_raw = 0.0
                
                #once the wetting loss has been overcome but the depression loss not yet infiltration starts, as well as water collection
                #depending on the soil runoff might be produced if the infiltration rate is very slow
                else:
                
                    if self.possible_infiltr_raw * 1000. >= self.rain[0]:
                    
                        self.collected_w_raw = (self.rain[0]) * self.imp_area_raintank * self.area_property / 1000.
                        self.actual_infiltr[0] = self.rain[0] / 1000. * self.perv_area * self.area_property
                        self.runoff_raw = 0.0

                        self.runoff_perv_raw = 0.0
                
                    else:
                    
                        self.collected_w_raw = (self.rain[0]) * self.imp_area_raintank * self.area_property / 1000.
                        self.actual_infiltr[0] = self.possible_infiltr_raw * self.perv_area * self.area_property
                        self.runoff_perv_raw = (self.rain[0] - self.possible_infiltr_raw * 1000.) / 1000. * self.perv_area * self.area_property
                        self.runoff_raw = 0.0

                    
                    #saving the information that the initial wetting loss has been overcome
                    self.rain_storage_perv = self.initial_loss + 0.000000000001
            
            #once the wetting loss and depression loss has been overcome ther will be infiltration, water collection and runoff
            else:
                
               
                #if more water can be infiltrated than rain is falling all rain will be infiltrated
                if self.possible_infiltr_raw * 1000 >= self.rain[0]:
                    
                    self.collected_w_raw = (self.rain[0]) * self.imp_area_raintank * self.area_property / 1000.
                    self.actual_infiltr[0] = (self.rain[0]) / 1000. * self.perv_area * self.area_property
                    self.runoff_raw  = (self.rain[0]) * self.imp_area_stormwater * self.area_property / 1000.
 
                    self.runoff_perv_raw = 0.0
                    
                #if less water can be infiltrated than rain is falling , the pervious fraction will produce runoff    
                else:
                    
                    self.collected_w_raw = (self.rain[0]) * self.imp_area_raintank * self.area_property / 1000.
                    self.actual_infiltr[0] = self.possible_infiltr_raw * self.perv_area * self.area_property
                    self.runoff_perv_raw = (self.rain[0]  - self.possible_infiltr_raw * 1000.) / 1000. * self.perv_area * self.area_property
                    self.runoff_raw  = (self.rain[0]) * self.imp_area_stormwater * self.area_property / 1000. 

                 
                #saving the information that the initial wetting loss and depression loss has been overcome 
                self.rain_storage_perv = self.initial_loss + 0.000000000001
                self.rain_storage_imp = self.initial_loss + self.depression_loss + 0.00000000000001
        
        
        
        
        
        
        # returning the possible inflitration [m³/dt]
        self.possible_infiltr[0]=self.possible_infiltr_raw*self.area_property*self.perv_area
        
        #switches between Muskingum Model and a simple Catchment model excluding routing
        if self.select_model == "with":

            #preparing the flow array 
            def linearstorage(i,k,N_times_A): 
                Q = (self.Qbefore[i]+N_times_A*(numpy.exp(dt/k)-1))*numpy.exp(-dt/k)
                self.Qbefore[i] = Q
                return Q , self.Qbefore[i]

            self.collected_w[0] = linearstorage(0,self.linearstorage_imperv_res_K,self.collected_w_raw)[0]        
            self.runoff[0] = linearstorage(1,self.linearstorage_imperv_storm_K,self.runoff_raw)[0] + linearstorage(2,self.linearstorage_perv_K,self.runoff_perv_raw)[0]

        elif self.select_model == "without":
            
            self.collected_w[0] = self.collected_w_raw
            self.runoff[0] = self.inflow[0]+self.runoff_raw + self.runoff_perv_raw
            
        else:
            print "Model selection not valid!"
        
        return dt
    
    def getClassName(self):
        #print "getClassName"
        return "Catchment_w_Routing"

#def register(nr):
#    for c in pycd3.Node.__subclasses__():
#        nf = NodeFactoryCatchmentwithRouting(c)
#        nf.__disown__()
#        nr.addNodeFactory(nf)
        
# def test():
#     nr = pycd3.NodeRegistry()
#     nf = NodeFactory(Household).__disown__()
#     nr.addNodeFactory(nf)
#     node = nr.createNode("Household")
    
#test()
