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

class Muskingum(pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        self.rain = pycd3.Flow()
        self.evapo = pycd3.Flow()
        self.infiltr = pycd3.Flow()
        self.actuell_infiltr = pycd3.Flow()
        self.runoff = pycd3.Flow()
        #dir (self.inf)
        print "init node"
        self.addInPort("rain", self.rain)
        self.addInPort("evapo", self.evapo)
        self.addOutPort("infiltr", self.infiltr)
        self.addOutPort("actuell_infiltr", self.actuell_infiltr)
        self.addOutPort("runoff", self.runoff)
        
        #Catchment area + fraction info of pervious and impervious parts
        self.area_property = pycd3.Double(1)
        self.addParameter("area_property [m*m]", self.area_property)
        self.perv_area = pycd3.Double(0.4)
        self.addParameter("perv_area [-]", self.perv_area)
        self.imp_area_stormwater = pycd3.Double(0.4)
        self.addParameter("imp_area_stormwater [-]", self.imp_area_stormwater)
        self.imp_area_raintank = pycd3.Double(0.2)
        self.addParameter("imp_area_raintank [-]", self.imp_area_raintank)
        
        #number of subareas for flowconcentration
        self.amout_subareas = pycd3.Double(6)
        self.addParameter("amout_subareas [-]", self.amout_subareas)
        
        #Muskingum parameters
        self.muskingum_K = pycd3.Double(0.0359991972726627)
        self.addParameter("muskingum_K [-]", self.muskingum_K)
        self.muskingum_X = pycd3.Double(5000)
        self.addParameter("muskingum_K [s]", self.muskingum_X)
        
        #dividing are in 'amout_subareas' parts (same size)
        self.subarea_size = self.area_property*self.imp_area_raintank/self.amout_subareas
        self.time=0.0
        self.current_effective_rain_height=0.0
        
        self.save_Q_1=0.0
        self.save_Q_2=0.0
        self.save_Q_3=0.0
        self.save_Q_4=0.0
        self.save_Q_5=0.0
        self.save_Q_6=0.0
        
    def init(self, start, stop, dt):
        print start
        print stop
        print dt
        
        self.C_x=(dt/2-self.muskingum_K*self.muskingum_X)/(dt/2+self.muskingum_K*(1-self.muskingum_X))
        self.C_y=(1/(dt/2+self.muskingum_K*(1-self.muskingum_X)))
        
        return True
        
    def f(self, current, dt):
           
        self.Q_1=(self.rain[0]*self.subarea_size*self.C_x +self.save_Q_1*self.C_y)
        self.Q_2=((self.rain[0]*self.subarea_size+self.Q_1)*self.C_x+self.save_Q_2*self.C_y)
        self.Q_3=((self.rain[0]*self.subarea_size+self.Q_2)*self.C_x+self.save_Q_3*self.C_y)
        self.Q_4=((self.rain[0]*self.subarea_size+self.Q_3)*self.C_x+self.save_Q_4*self.C_y)
        self.Q_5=((self.rain[0]*self.subarea_size+self.Q_4)*self.C_x+self.save_Q_5*self.C_y)
        self.Q_6=((self.rain[0]*self.subarea_size+self.Q_5)*self.C_x+self.save_Q_6*self.C_y)
        self.save_Q_1=self.Q_1
        self.save_Q_2=self.Q_2
        self.save_Q_3=self.Q_3
        self.save_Q_4=self.Q_4
        self.save_Q_5=self.Q_5
        self.save_Q_6=self.Q_6
        self.runoff[0]=self.Q_6/1000
       
        

        return dt
    
    def getClassName(self):
        #print "getClassName"
        return "Muskingum"

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
