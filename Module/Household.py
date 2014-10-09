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

class Household(pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        self.black_w = pycd3.Flow()
        self.grey_w = pycd3.Flow()
        self.pot_w = pycd3.Flow()
        self.nonpot_w = pycd3.Flow()
        self.outdoor_use = pycd3.Flow()
        
        #dir (self.inf)
        print "init node"
        self.addOutPort("black_w", self.black_w)
        self.addOutPort("grey_w", self.grey_w)
        self.addOutPort("pot_w", self.pot_w)
        self.addOutPort("nonpot_w", self.nonpot_w)
        self.addInPort("outdoor_use", self.outdoor_use)
        
        self.toilet = pycd3.Double(0.0000002257)
        self.addParameter("toilet [m³/s]", self.toilet)       
        self.tab = pycd3.Double(0.000000243)
        self.addParameter("tab [m³/s]", self.tab)
        self.shower = pycd3.Double(0.0000004626)
        self.addParameter("shower [m³/s]", self.shower)
        self.washing_machine = pycd3.Double(0.0000008185)
        self.addParameter("washing_machine [m³/s]", self.washing_machine)
        self.dishwasher = pycd3.Double(0.0000000926)
        self.addParameter("dishwasher [m³/s]", self.dishwasher)
        
        
    def init(self, start, stop, dt):
        print start
        print stop
        print dt
        return True
        
    def f(self, current, dt):
        self.pot_w[0] = (self.shower+self.dishwasher+self.tab)*360
        self.nonpot_w[0] = (self.toilet+self.washing_machine)*360+self.outdoor_use[0]
        self.black_w[0] = (self.toilet)*360
        self.grey_w[0] = (self.shower+self.dishwasher+self.tab+self.washing_machine)*360
       

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
