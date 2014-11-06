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
        return "Addons.py"

class Household(pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        
        self.black_w = pycd3.Flow()
        self.grey_w = pycd3.Flow()
        self.pot_w = pycd3.Flow()
        self.nonpot_w = pycd3.Flow()
        self.outdoor_demand = pycd3.Flow()
        self.bath_tub = pycd3.Flow()
        self.shower = pycd3.Flow()
        self.toilet = pycd3.Flow()
        self.tap = pycd3.Flow()
        self.washing_machine = pycd3.Flow()
        self.dishwasher = pycd3.Flow() 
        
        self.addOutPort("black_w", self.black_w)
        self.addOutPort("grey_w", self.grey_w)
        self.addOutPort("pot_w", self.pot_w)
        self.addOutPort("nonpot_w", self.nonpot_w)
        self.addInPort("outdoor_demand", self.outdoor_demand)
        self.addInPort("bath_tub [l/h]", self.bath_tub)
        self.addInPort("shower [l/h]", self.shower)
        self.addInPort("toilet [l/h]", self.toilet)
        self.addInPort("tap [l/h]", self.tap)
        self.addInPort("washing_machine [l/h]", self.washing_machine)
        self.addInPort("dishwasher [l/h]", self.dishwasher)
        
        print "init node"
        
    def init(self, start, stop, dt):
        print start
        print stop
        print dt
        return True
        
    def f(self, current, dt):
        
        self.pot_w[0] = (self.bath_tub[0]+self.shower[0]+self.tap[0]+self.dishwasher[0]+self.washing_machine[0])/3600/1000*dt
        self.nonpot_w[0] = (self.toilet[0])/3600/1000*dt+self.outdoor_demand[0]
        self.black_w[0] = (self.toilet[0])/3600/1000*dt
        self.grey_w[0] = (self.bath_tub[0]+self.shower[0]+self.tap[0]+self.washing_machine[0]+self.dishwasher[0])/3600/1000*dt

        return dt
    
    def getClassName(self):
        #print "getClassName"
        return "Household"

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
