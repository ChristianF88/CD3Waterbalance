# -*- coding: utf-8 -*-
"""
Created on Thu Oct 02 08:41:08 2014

@author: Acer
"""

import sys
import pycd3

#class NodeFactoryRaintank(pycd3.INodeFactory):
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

class Raintank(pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        self.collected_w = pycd3.Flow()
        self.non_pot_in = pycd3.Flow()
        self.non_pot_out = pycd3.Flow()
        self.overflow = pycd3.Flow()
        self.check_storage = pycd3.Flow()
        #dir (self.inf)
        print "init node"
        self.addInPort("Collected_Water", self.collected_w)
        self.addInPort("Non_Potable_In", self.non_pot_in)
        self.addOutPort("Overflow", self.overflow)
        self.addOutPort("Additional_Demand", self.non_pot_out)
        self.addOutPort("Check_Storage", self.check_storage)
        self.storage_v = pycd3.Double(20.0)
        self.addParameter("Storage_Volume [m^3]", self.storage_v)

        self.current_volume = 0.0

        
        #self.addOutPort("gw", self.gw)
        #self.addInPort("in", self.inf)
        
    def init(self, start, stop, dt):
        print start
        print stop
        print dt
        return True
        
    def f(self, current, dt):
        
        self.current_volume += self.collected_w[0]-self.non_pot_in[0]
        
        if self.current_volume >= self.storage_v:
            self.overflow[0] = self.collected_w[0]
            self.non_pot_out[0] = 0.0
            self.current_volume = self.storage_v
            self.check_storage[0] = self.current_volume
            
        elif self.current_volume >0:
            self.overflow[0] = 0.0
            self.non_pot_out[0] = 0.0
            self.check_storage[0] = self.current_volume
        else:
            self.overflow[0] = 0.0
            self.non_pot_out[0] = - self.non_pot_in[0]
            self.current_volume = 0.0
            self.check_storage[0] = self.current_volume
            
       
        return dt
    
    def getClassName(self):
        #print "getClassName"
        return "Raintank"

#def register(nr):
#    for c in pycd3.Node.__subclasses__():
#        nf = NodeFactoryRaintank(c)
#        nf.__disown__()
#        nr.addNodeFactory(nf)
        
# def test():
#     nr = pycd3.NodeRegistry()
#     nf = NodeFactory(Household).__disown__()
#     nr.addNodeFactory(nf)
#     node = nr.createNode("Household")
    
#test()
