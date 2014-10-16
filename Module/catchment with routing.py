# -*- coding: utf-8 -*-
"""
Created on Thu Oct 02 08:41:08 2014

@author: Acer
"""

import sys
import pycd3
import math

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

class Catchment_w_r(pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        self.rain = pycd3.Flow()
        self.collected_w = pycd3.Flow()
        self.runoff = pycd3.Flow()
        self.evapo = pycd3.Flow()
        self.possible_infiltr = pycd3.Flow()
        self.actual_infiltr = pycd3.Flow()
        self.outdoor_use = pycd3.Flow()
        self.inflow = pycd3.Flow()
        
        #dir (self.inf)
        print "init node"
        self.addInPort("rain", self.rain)
        self.addInPort("evapo", self.evapo)
        self.addInPort("inflow", self.inflow)
        self.addOutPort("possible_infiltr", self.possible_infiltr)
        self.addOutPort("actual_infiltr", self.actual_infiltr)
        self.addOutPort("runoff", self.runoff)
        self.addOutPort("collected_w", self.collected_w)
        self.addOutPort("outdoor_use", self.outdoor_use)
        
        #Catchment area + fraction info of pervious and impervious parts
        self.area_property = pycd3.Double(1000)
        self.addParameter("area_property [m*m]", self.area_property)
        self.perv_area = pycd3.Double(0.4)
        self.addParameter("perv_area [-]", self.perv_area)
        self.imp_area_stormwater = pycd3.Double(0.4)
        self.addParameter("imp_area_stormwater [-]", self.imp_area_stormwater)
        self.imp_area_raintank = pycd3.Double(0.2)
        self.addParameter("imp_area_raintank [-]", self.imp_area_raintank)
        
        #default values for Gras (Wikipedia)
        self.Horton_initial_cap = pycd3.Double(0.9)                             
        self.addParameter("Horton_initial_cap [m/h]", self.Horton_initial_cap)
        self.Horton_final_cap = pycd3.Double(0.29)                              
        self.addParameter("Horton_final_cap [m/h]", self.Horton_final_cap)
        self.Horton_decay_constant = pycd3.Double(2.0)                          
        self.addParameter("Horton_decay_constant [1/min]", self.Horton_decay_constant)
        
        #default values for suburbs (scrip Prof. Krebs)
        self.depression_loss = pycd3.Double(1.5)                                
        self.addParameter("depression_capacitiy [mm]", self.depression_loss)
        
        #default values for (scrip Prof. Krebs)
        self.initial_loss = pycd3.Double(0.4)                                   
        self.addParameter("initial_loss [mm]", self.initial_loss)
        
        #number of subareas for flowconcentration
        self.amount_subareas = pycd3.Double(1)
        self.addParameter("amount_subareas [-]", self.amount_subareas)
        
        #Muskingum parameters K flowtime for entire catchment
        #divided by surface Area
        self.muskingum_coll_K = pycd3.Double(400)
        self.addParameter("muskingum_coll_K [s]", self.muskingum_coll_K)
        self.muskingum_coll_X = pycd3.Double(0.05)
        self.addParameter("muskingum_coll_X [-]", self.muskingum_coll_X)
        self.muskingum_runoff_K = pycd3.Double(600)
        self.addParameter("muskingum_runoff_K [s]", self.muskingum_runoff_K)
        self.muskingum_runoff_X = pycd3.Double(0.05)
        self.addParameter("muskingum_runoff_X [-]", self.muskingum_runoff_X)
        self.muskingum_runoff_perv_K = pycd3.Double(900)
        self.addParameter("muskingum_runoff_perv_K [s]", self.muskingum_runoff_perv_K)
        self.muskingum_runoff_perv_X = pycd3.Double(0.05)
        self.addParameter("muskingum_runoff_perv_X [-]", self.muskingum_runoff_perv_X)
        
        #storage and time values
        self.current_effective_rain_height = 0.0
        self.rain_storage_imp = 0.0
        self.continuous_rain_time = 0.0
        self.continuous_rain_time_2 = 0.0                                        
        self.rain_storage_perv = 0.0
        
        #variable to check Horten model (has got to be 1 for a real simulation)
        self.k=1
        
        #storage for Muskingum inflows
        self.collected_w_raw = 0.0
        self.runoff_raw = 0.0
        self.runoff_perv_raw=0.0
        
    def init(self, start, stop, dt):
        print start
        print stop
        print dt
        
        #starting values for Horton Model
        self.possible_infiltr[0] = self.Horton_initial_cap/3600*dt
        self.temp_cap = self.Horton_initial_cap/3600*dt
        self.temp_cap_2 = self.Horton_initial_cap/3600*dt
        
        #calculating the K values for a single subreach
        self.muskingum_K_single_subreach_coll = self.muskingum_coll_K/self.amount_subareas
        self.muskingum_K_single_subreach_runoff = self.muskingum_runoff_K/self.amount_subareas
        self.muskingum_K_single_subreach_runoff_perv = self.muskingum_runoff_perv_K/self.amount_subareas
        
        #calculating the Muskingum coefficients
        self.C_coll_x=(dt/2-self.muskingum_K_single_subreach_coll*self.muskingum_coll_X)/(dt/2+self.muskingum_K_single_subreach_coll*(1-self.muskingum_coll_X))
        self.C_coll_y=(1/(dt/2+self.muskingum_K_single_subreach_coll*(1-self.muskingum_coll_X)))
        self.C_runoff_x=(dt/2-self.muskingum_K_single_subreach_runoff*self.muskingum_runoff_X)/(dt/2+self.muskingum_K_single_subreach_runoff*(1-self.muskingum_runoff_X))
        self.C_runoff_y=(1/(dt/2+self.muskingum_K_single_subreach_runoff*(1-self.muskingum_runoff_X)))
        self.C_runoff_perv_x=(dt/2-self.muskingum_K_single_subreach_runoff_perv*self.muskingum_runoff_perv_X)/(dt/2+self.muskingum_K_single_subreach_runoff_perv*(1-self.muskingum_runoff_perv_X))
        self.C_runoff_perv_y=(1/(dt/2+self.muskingum_K_single_subreach_runoff_perv*(1-self.muskingum_runoff_perv_X)))
        
        #preparing the storage coefficients for the stored Volume in each subreach
        self.Q_i_coll_storage_1 = []
        self.Q_i_coll_storage_2 = []
        self.Q_i_runoff_storage_1 = []
        self.Q_i_runoff_storage_2 = []
        self.Q_i_runoff_perv_storage_1 = []
        self.Q_i_runoff_perv_storage_2 = []
        for i in range(self.amount_subareas):
            self.Q_i_coll_storage_1.append(0)
            self.Q_i_coll_storage_2.append(0)
            self.Q_i_runoff_storage_1.append(0)
            self.Q_i_runoff_storage_2.append(0)
            self.Q_i_runoff_perv_storage_1.append(0)
            self.Q_i_runoff_perv_storage_2.append(0)
        
        return True
        
    def f(self, current, dt):
        
        #describing the current rain that doesnt evaporate in the same timestep
        #resetting the time values for the Horton model
        if self.current_effective_rain_height < 0:
            self.current_effective_rain_height= self.rain[0]-self.evapo[0]
            if self.current_effective_rain_height <= 0:
                pass
            else:
                self.continuous_rain_time=0.0
        elif self.current_effective_rain_height > 0:
            self.current_effective_rain_height= self.rain[0]-self.evapo[0]
            if self.current_effective_rain_height <= 0:
                self.continuous_rain_time_2=0.0
            else:
                pass
        else:
            self.current_effective_rain_height= self.rain[0]-self.evapo[0]
            
        #if the current effective rain height is below 0 there wont be any runoff, water collection or infiltration
        #and the outdoor water use is equal to the difference between evapotranspiration (ET) and precipitation (P)
        if self.current_effective_rain_height < 0.0:
            
            self.collected_w_raw = 0.0
            self.runoff_raw = 0.0
            self.actual_infiltr[0] =0.0
            self.outdoor_use[0] = (self.evapo[0] - self.rain[0]) / 1000 * self.area_property * self.perv_area                                 
            self.runoff_perv_raw = 0.0
            
            #resetting the storage values as a simulation of the drying process respectively the continuous infitlration
            if self.rain_storage_perv > 0:
                self.rain_storage_perv += self.current_effective_rain_height
                
            else:
                self.rain_storage_perv = 0.0
                                
            if self.rain_storage_imp > 0:
                self.rain_storage_imp += self.current_effective_rain_height
                
            else:
                self.rain_storage_imp = 0.0
            
            #as well as calculating the possilbe infiltration rate the the Horton model in a state of "drying" (+ increasing the time step for the model)
            
            self.temp_cap = self.Horton_final_cap/3600*dt + (self.temp_cap_2 - self.Horton_final_cap/3600*dt) * math.exp(-1*self.Horton_decay_constant * dt / 60 * self.continuous_rain_time/self.k)
            self.possible_infiltr[0] = self.Horton_initial_cap/3600*dt - (self.Horton_initial_cap/3600*dt - self.temp_cap) * math.exp(-1*self.Horton_decay_constant * dt / 60 * self.continuous_rain_time_2/self.k)
            self.continuous_rain_time_2 += 1.0
           
                
        #if the current effective rain height equals a value higher zero there will be infiltration, runoff and collected water
        #as soon as the initial loss has been overcome, outdoor use will be zero
        elif self.current_effective_rain_height > 0.0:
            
            #calculating the current rain storage values to keep track of when the rain loss has been overcome,
            #as well as calculating the possilbe infiltration rate the the Horton model in a state of "wetting" (+ increasing the time step for the model)
            self.rain_storage_imp += self.rain[0]-self.evapo[0]
            self.rain_storage_perv += self.rain[0]-self.evapo[0]
            
            self.temp_cap_2 = self.Horton_initial_cap/3600*dt - (self.Horton_initial_cap/3600*dt - self.temp_cap) * math.exp(-1*self.Horton_decay_constant * dt / 60 * self.continuous_rain_time_2/self.k)
            self.possible_infiltr[0] = self.Horton_final_cap/3600*dt + (self.temp_cap_2 - self.Horton_final_cap/3600*dt) * math.exp(-1*self.Horton_decay_constant * dt / 60 * self.continuous_rain_time/self.k)
            self.continuous_rain_time += 1.0
            #if the wetting loss and depression loss hasn't been overcome yet, there won't be any runoff from the impervious area
            #that contributes to stormwater
            if self.rain_storage_imp - self.initial_loss - self.depression_loss <= 0.0:
                
                #if the wetting loss hasn't beem overcome there will be no flow...
                if self.rain_storage_perv - self.initial_loss <= 0.0:
                
                    self.collected_w_raw = 0.0
                    self.runoff_raw = 0.0
                    self.actual_infiltr[0] =0.0
                    self.outdoor_use[0] = 0.0
                    self.runoff_perv_raw = 0.0
                
                #once the wetting loss has been overcome but the depression loss not yet infiltration starts, as well as water collection
                #depending on the soil runoff might be produced if the infiltration rate is very slow
                else:
                
                    if self.possible_infiltr[0] * 1000 >= self.current_effective_rain_height:
                    
                        self.collected_w_raw = (self.rain[0]-self.evapo[0]) * self.imp_area_raintank * self.area_property / 1000
                        self.actual_infiltr[0] = self.current_effective_rain_height / 1000 * self.perv_area * self.area_property
                        self.runoff_raw = 0.0
                        self.outdoor_use[0] = 0.0
                        self.runoff_perv_raw = 0.0
                
                    else:
                    
                        self.collected_w_raw = (self.rain[0]-self.evapo[0]) * self.imp_area_raintank * self.area_property / 1000
                        self.actual_infiltr[0] = self.possible_infiltr[0] * self.perv_area * self.area_property
                        self.runoff_perv_raw = (self.current_effective_rain_height - self.possible_infiltr[0] * 1000) / 1000 * self.perv_area * self.area_property
                        self.runoff_raw = 0.0
                        self.outdoor_use[0] = 0.0
                    
                    #saving the information that the initial wetting loss has been overcome
                    self.rain_storage_per = self.initial_loss + 0.000000000001
            
            #once the wetting loss and depression loss has been overcome ther will be infiltration, water collection and runoff
            else:
                
                #if more water can be infiltrated than rain is falling all rain will be infiltrated
                if self.possible_infiltr[0] * 1000 >= self.current_effective_rain_height:
                    
                    self.collected_w_raw = (self.rain[0]-self.evapo[0]) * self.imp_area_raintank * self.area_property / 1000
                    self.actual_infiltr[0] = self.current_effective_rain_height / 1000 * self.perv_area * self.area_property
                    self.runoff_raw = self.runoff[0] = (self.rain[0]-self.evapo[0]) * self.imp_area_stormwater * self.area_property / 1000
                    self.outdoor_use[0] = 0.0
                    self.runoff_perv_raw = 0.0
                    
                #if less water can be infiltrated than rain is falling , the pervious fraction will produce runoff    
                else:
                    
                    self.collected_w_raw = (self.rain[0]-self.evapo[0]) * self.imp_area_raintank * self.area_property / 1000
                    self.actual_infiltr[0] = self.possible_infiltr[0] * self.perv_area * self.area_property
                    self.runoff_perv_raw = (self.current_effective_rain_height - self.possible_infiltr[0] * 1000) / 1000 * self.perv_area * self.area_property
                    self.runoff_raw = self.runoff[0] = (self.rain[0]-self.evapo[0]) * self.imp_area_stormwater * self.area_property / 1000 
                    self.outdoor_use[0] = 0.0
                 
                #saving the information that the initial wetting loss and depression loss has been overcome 
                self.rain_storage_per = self.initial_loss + 0.000000000001
                self.rain_storage_imp = self.initial_loss + self.depression_loss + 0.00000000000001
        
        #if the effective currrent rain height equals zero there wont be any runoff thus no water collection as well as no infiltration
        #there wont be any need of watering gardens (no outdoor use)
        else:
            
            self.collected_w_raw = 0.0
            self.runoff_raw = 0.0
            self.actual_infiltr[0] =0.0
            self.outdoor_use[0] = 0.0
            self.runoff_perv_raw = 0.0
        
        #Muskingum model for folw dynamics (slower fow on gras and faster on roof)
        
        
        #dividing are in 'amout_subareas' parts (same size)
        self.subarea_size = self.area_property*self.imp_area_raintank/self.amount_subareas
        
        #preparing the flow array 
        self.Q_coll_i = []
        self.Q_runoff_i = []
        self.Q_runoff_perv_i = []
        for i in range(self.amount_subareas):
            self.Q_coll_i.append(0)
            self.Q_runoff_i.append(0)
            self.Q_runoff_perv_i.append(0)
            
            #calculating the flow in for each subreach
            if i==0:
               self.Q_coll_i[i]=(self.inflow[0]*1000+self.rain[0]*self.subarea_size)*self.C_coll_x+self.Q_i_coll_storage_2[i]*self.C_coll_y
               self.Q_i_coll_storage_2[i]=self.Q_coll_i[i]*(1-self.C_coll_x)*dt+self.Q_i_coll_storage_1[i]*(1-self.C_coll_y*dt)
               self.Q_i_coll_storage_1[i]=self.Q_i_coll_storage_2[i]
               self.Q_runoff_i[i]=(self.inflow[0]*1000+self.rain[0]*self.subarea_size)*self.C_runoff_x+self.Q_i_runoff_storage_2[i]*self.C_runoff_y
               self.Q_i_runoff_storage_2[i]=self.Q_runoff_i[i]*(1-self.C_runoff_x)*dt+self.Q_i_runoff_storage_1[i]*(1-self.C_runoff_y*dt)
               self.Q_i_runoff_storage_1[i]=self.Q_i_runoff_storage_2[i]
               self.Q_runoff_perv_i[i]=(self.inflow[0]*1000+self.rain[0]*self.subarea_size)*self.C_runoff_perv_x+self.Q_i_runoff_perv_storage_2[i]*self.C_runoff_perv_y
               self.Q_i_runoff_perv_storage_2[i]=self.Q_runoff_perv_i[i]*(1-self.C_runoff_perv_x)*dt+self.Q_i_runoff_perv_storage_1[i]*(1-self.C_runoff_perv_y*dt)
               self.Q_i_runoff_perv_storage_1[i]=self.Q_i_runoff_perv_storage_2[i]
            else:
                self.Q_coll_i[i]=(self.Q_coll_i[i-1]+self.rain[0]*self.subarea_size)*self.C_coll_x+self.Q_i_coll_storage_2[i]*self.C_coll_y
                self.Q_i_coll_storage_2[i]=self.Q_coll_i[i]*(1-self.C_coll_x)*dt+self.Q_i_coll_storage_1[i]*(1-self.C_coll_y*dt)
                self.Q_i_coll_storage_1[i]=self.Q_i_coll_storage_2[i]
                self.Q_runoff_i[i]=(self.Q_runoff_i[i-1]+self.rain[0]*self.subarea_size)*self.C_runoff_x+self.Q_i_runoff_storage_2[i]*self.C_runoff_y
                self.Q_i_runoff_storage_2[i]=self.Q_runoff_i[i]*(1-self.C_runoff_x)*dt+self.Q_i_runoff_storage_1[i]*(1-self.C_runoff_y*dt)
                self.Q_i_runoff_storage_1[i]=self.Q_i_runoff_storage_2[i]
                self.Q_runoff_perv_i[i]=(self.Q_runoff_perv_i[i-1]+self.rain[0]*self.subarea_size)*self.C_runoff_perv_x+self.Q_i_runoff_perv_storage_2[i]*self.C_runoff_perv_y
                self.Q_i_runoff_perv_storage_2[i]=self.Q_runoff_perv_i[i]*(1-self.C_runoff_perv_x)*dt+self.Q_i_runoff_perv_storage_1[i]*(1-self.C_runoff_perv_y*dt)
                self.Q_i_runoff_perv_storage_1[i]=self.Q_i_runoff_perv_storage_2[i]
        
        #outflow of catchment
        self.collected_w[0]=self.Q_coll_i[-1] /1000 
        self.runoff[0] =(self.Q_runoff_perv_i[-1]+self.Q_runoff_i[-1])/1000
           
        return dt
    
    def getClassName(self):
        #print "getClassName"
        return "Catchment_w_r"

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
