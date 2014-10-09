# -*- coding: utf-8 -*-
"""
Created on Thu Oct 02 08:41:08 2014

@author: Acer
"""

import sys
import pycd3

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

class Catchment(pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        self.rain = pycd3.Flow()
        self.collected_w = pycd3.Flow()
        self.runoff_w = pycd3.Flow()
        self.groundw_in = pycd3.Flow()
        #dir (self.inf)
        print "init node"
        self.addInPort("rain", self.rain)
        self.addOutPort("col_w", self.collected_w)
        self.addOutPort("runoff", self.runoff_w)
        self.addOutPort("groundw_in", self.groundw_in)
        
        self.perv_area = pycd3.Double(0.4)
        self.addParameter("perv_area", self.perv_area)
        
        self.imp_floor = pycd3.Double(0.4)
        self.addParameter("imp_floor", self.imp_floor)
        
        self.roof_area = pycd3.Double(0.2)
        self.addParameter("roof_area", self.roof_area)
        
        self.area_property = pycd3.Double(1)
        self.addParameter("area_property", self.area_property)
        #self.addOutPort("gw", self.gw)
        #self.addInPort("in", self.inf)
        
    def init(self, start, stop, dt):
        print start
        print stop
        print dt
        return True
        
    def f(self, current, dt):
        #Q
        #self.ww[0] = 6.
        #Ntot
        #self.gw[0] = 20.
        #d = 5
        #d = d+ 1 //6
        self.collected_w[0] = self.rain[0]*self.roof_area*self.area_property/1000
        self.runoff_w[0] = self.rain[0]*self.imp_floor*self.area_property/1000
        self.groundw_in[0] = self.rain[0]*self.perv_area*self.area_property/1000
        #print self.V

        return dt
    
    def getClassName(self):
        #print "getClassName"
        return "Catchment"

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
