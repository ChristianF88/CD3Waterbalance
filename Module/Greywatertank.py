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

class Greywatertank(pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        self.greywaterin = pycd3.Flow()
        self.greywaterout = pycd3.Flow()
        self.check_storage = pycd3.Flow()
        self.non_pot_out = pycd3.Flow()
        
        #dir (self.inf)
        print "init node"
        self.addInPort("Grey_Water_In", self.greywaterin)
        self.addInPort("Treated_Grey_Water_Out", self.greywaterout)
        self.addOutPort("Current_Volume",self.check_storage)
        self.addOutPort("Additional_Demand",self.non_pot_out)
        self.myyield = pycd3.Double(0.9)
        self.addParameter("Yield_of_Treatment [-]", self.myyield)

        
        #self.addOutPort("gw", self.gw)
        #self.addInPort("in", self.inf)
        
    def init(self, start, stop, dt):
        print start
        print stop
        print dt
        self.current_volume = 0.0
        return True
        
    def f(self, current, dt):
        
        self.current_volume += self.greywaterin[0]*self.myyield - self.greywaterout[0]
        
        if self.current_volume >= 0:
            self.non_pot_out[0] = 0.0
            self.check_storage[0] = self.current_volume
        else:
            self.non_pot_out[0] = - self.non_pot_in[0]
            self.current_volume = 0.0
            self.check_storage[0] = self.current_volume
            
       
        
      
        return dt
    
    def getClassName(self):
        #print "getClassName"
        return "Greywatertank"

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
