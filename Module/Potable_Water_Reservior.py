# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:46:53 2015

@author: Gerhard
"""


import sys
import pycd3

#class NodeFactoryPWR(pycd3.INodeFactory):
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

class Potable_Water_Reservoir(pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        self.pot_w = pycd3.Flow()
        self.nonpot_w = pycd3.Flow()
        self.demand = pycd3.Flow()
        #dir (self.inf)
#        print "init node"
        self.addInPort("Potable_Water_Demand", self.pot_w)
        self.addInPort("Non_Potable_Water_Demand", self.nonpot_w)
        self.addOutPort("Demand", self.demand)
         
    def init(self, start, stop, dt):
#        print start
#        print stop
#        print dt
        return True
        
    def f(self, current, dt):
        
        
        self.demand[0] = self.pot_w[0]+self.nonpot_w[0]
       

        return dt
    
    def getClassName(self):
#        print "getClassName"
        return "Potable_Water_Reservoir"

#def register(nr):
#    for c in pycd3.Node.__subclasses__():
#        nf = NodeFactoryPWR(c)
#        nf.__disown__()
#        nr.addNodeFactory(nf)
        
# def test():
#     nr = pycd3.NodeRegistry()
#     nf = NodeFactory(Household).__disown__()
#     nr.addNodeFactory(nf)
#     node = nr.createNode("Household")
    
#test()
