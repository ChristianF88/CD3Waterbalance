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

class Catchment_v2(pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        self.rain = pycd3.Flow()
        self.collected_w = pycd3.Flow()
        self.runoff = pycd3.Flow()
        self.evapo = pycd3.Flow()
        self.possible_infiltr = pycd3.Flow()
        self.actual_infiltr = pycd3.Flow()
        self.outdoor_use = pycd3.Flow()
        
        #dir (self.inf)
        print "init node"
        self.addInPort("rain", self.rain)
        self.addInPort("evapo", self.evapo)
        self.addOutPort("possible_infiltr", self.possible_infiltr)
        self.addOutPort("actual_infiltr", self.actual_infiltr)
        self.addOutPort("runoff", self.runoff)
        self.addOutPort("collected_w", self.collected_w)
        self.addOutPort("outdoor_use", self.outdoor_use)
        
        self.area_property = pycd3.Double(1)
        self.addParameter("area_property [m*m]", self.area_property)
        
        self.perv_area = pycd3.Double(0.4)
        self.addParameter("perv_area [-]", self.perv_area)
        
        self.imp_area_stormwater = pycd3.Double(0.4)
        self.addParameter("imp_area_stormwater [-]", self.imp_area_stormwater)
        
        self.imp_area_raintank = pycd3.Double(0.2)
        self.addParameter("imp_area_raintank [-]", self.imp_area_raintank)
        
        self.Horton_initial_cap = pycd3.Double(0.9)                             #default values for Gras (Wikipedia)
        self.addParameter("Horton_initial_cap [m/h]", self.Horton_initial_cap)
        
        self.Horton_final_cap = pycd3.Double(0.29)                              #default values for Gras (Wikipedia)
        self.addParameter("Horton_final_cap [m/h]", self.Horton_final_cap)
        
        self.Horton_decay_constant = pycd3.Double(2.0)                          #default values for Gras (Wikipedia)
        self.addParameter("Horton_decay_constant [1/min]", self.Horton_decay_constant)
        
        self.depression_loss = pycd3.Double(1.5)                                #Exponentialansatz einfügen, default values for suburbs (scrip Prof. Krebs)
        self.addParameter("depression_capacitiy [mm]", self.depression_loss)
        
        self.initial_loss = pycd3.Double(0.4)                                   #Exponentialansatz einfügen, default values for (scrip Prof. Krebs)
        self.addParameter("initial_loss [mm]", self.initial_loss)
        
        self.current_effective_rain_height = 0.0
        self.rain_storage_imp = 0.0
        self.continious_rain_time = -1.0                                        #Bodenversickerungskapazität erhöht sich viel schneller als normal
        self.rain_storage_perv = 0.0
        self.possible_infiltr[0] = self.Horton_initial_cap/10
        
    def init(self, start, stop, dt):
        print start
        print stop
        print dt
        return True
        
    def f(self, current, dt):
        
        self.current_effective_rain_height= self.rain[0]-self.evapo[0]
      
        
        if self.current_effective_rain_height < 0.0:
            
            self.collected_w[0] = 0.0
            self.runoff[0] = 0.0
            self.actual_infiltr[0] =0.0
            self.outdoor_use[0] = self.evapo[0] / 1000 * self.area_property * self.perv_area                                 #Bewässerung > Evapo
            
            if self.rain_storage_perv > 0:
                self.rain_storage_perv -= self.evapo[0]
            else:
                self.rain_storage_perv = 0.0
                self.continious_rain_time = -1.0
            
            if self.rain_storage_imp > 0:
                self.rain_storage_imp -= self.evapo[0]
            else:
                self.rain_storage_imp = 0.0
                self.possible_infiltr[0] = self.Horton_initial_cap/10
        
        elif self.current_effective_rain_height > 0.0:
            
            self.rain_storage_imp += self.rain[0]-self.evapo[0]
            self.rain_storage_perv += self.rain[0]-self.evapo[0]
            self.continious_rain_time += 1.0
            self.possible_infiltr[0] = self.Horton_final_cap/10 + (self.Horton_initial_cap/10 - self.Horton_final_cap/10) * math.exp(-1*self.Horton_decay_constant * .06 * self.continious_rain_time)
        
            if self.rain_storage_imp - self.initial_loss - self.depression_loss <= 0.0:
                
                if self.rain_storage_perv - self.initial_loss <= 0.0:
                
                    self.collected_w[0] = 0.0
                    self.runoff[0] = 0.0
                    self.actual_infiltr[0] =0.0
                    self.outdoor_use[0] = 0.0
                
                else:
                
                    if self.possible_infiltr[0] * 1000 >= self.current_effective_rain_height:
                    
                        self.collected_w[0] = (self.rain[0]-self.evapo[0]) * self.imp_area_raintank * self.area_property / 1000
                        self.actual_infiltr[0] = self.current_effective_rain_height / 1000 * self.perv_area * self.area_property
                        self.runoff[0] = 0.0
                        self.outdoor_use[0] = 0.0
                
                    else:
                    
                        self.collected_w[0] = (self.rain[0]-self.evapo[0]) * self.imp_area_raintank * self.area_property / 1000
                        self.actual_infiltr[0] = self.possible_infiltr[0] * self.perv_area * self.area_property
                        self.runoff[0] = self.runoff[0] = (self.current_effective_rain_height - self.possible_infiltr[0] * 1000) / 1000 * self.perv_area * self.area_property
                        self.outdoor_use[0] = 0.0
                        
                    self.rain_storage_per = self.initial_loss + 0.000000000001
                               
            else:
                
                if self.possible_infiltr[0] * 1000 >= self.current_effective_rain_height:
                    
                    self.collected_w[0] = (self.rain[0]-self.evapo[0]) * self.imp_area_raintank * self.area_property / 1000
                    self.actual_infiltr[0] = self.current_effective_rain_height / 1000 * self.perv_area * self.area_property
                    self.runoff[0] = self.runoff[0] = (self.rain[0]-self.evapo[0]) * self.imp_area_stormwater * self.area_property / 1000
                    self.outdoor_use[0] = 0.0
                    
                else:
                    
                    self.collected_w[0] = (self.rain[0]-self.evapo[0]) * self.imp_area_raintank * self.area_property / 1000
                    self.actual_infiltr[0] = self.possible_infiltr[0] * self.perv_area * self.area_property
                    self.runoff[0] = self.runoff[0] = (self.rain[0]-self.evapo[0]) * self.imp_area_stormwater * self.area_property / 1000 + (self.current_effective_rain_height - self.possible_infiltr[0] * 1000) / 1000 * self.perv_area * self.area_property
                    self.outdoor_use[0] = 0.0
                    
                self.rain_storage_per = self.initial_loss + 0.000000000001
                self.rain_storage_imp = self.initial_loss + self.depression_loss + 0.00000000000001
              
        else:
            
            self.collected_w[0] = 0.0
            self.runoff[0] = 0.0
            self.actual_infiltr[0] =0.0
            self.outdoor_use[0] = 0.0
           
           
        return dt
    
    def getClassName(self):
        #print "getClassName"
        return "Catchment_v2"

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
