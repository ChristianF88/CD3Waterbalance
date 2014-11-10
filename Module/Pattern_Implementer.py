# -*- coding: utf-8 -*-
"""
Created on Thu Oct 02 08:41:08 2014

@author: Acer
"""

import sys
import pycd3
from numpy import floor

class NodeFactoryPatternImplementer(pycd3.INodeFactory):
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

class Pattern_Impl(pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        self.input = pycd3.Flow()
        self.output = pycd3.Flow()
        print "init node"
        self.addInPort("Inport", self.input)
        self.addOutPort("Outport", self.output)
        
        
        
    def init(self, start, stop, dt):
        print start
        print stop
        print dt
        #pattern in [time,factor] configuration
        self.pattern=[[0.0, 0.0],[1/24., 0.0],[2/24., 0.0],[3/24., 0.0],[4/24., 0.01],[5/24., 0.02],[6/24., 0.08],[7/24., 0.21],[8/24., 0.52],
                      [9/24., 1.06],[10/24., 1.86],[11/24., 2.78],[12/24., 3.54],[13/24., 3.83],[14/24., 3.54],[15/24., 2.78],[16/24., 1.86],
                      [17/24., 1.06],[18/24., 0.52],[19/24., 0.21],[20/24., 0.08],[21/24., 0.02],[22/24., 0.01],[23/24., 0.0],[1.0, 0.0]]
        self.time=0.0
        return True
        
    def f(self, current, dt):
        
        self.time+=dt/24./3600.
        if self.time - floor(self.time) == 1.0:
            self.output[0]=self.input[0]*self.pattern[24][1]  
        else:
            count_i = 0
            while (self.time - floor(self.time) > self.pattern[count_i][0]):
                count_i+=1
            self.output[0]=self.input[0]*self.pattern[count_i][1]
       
        return dt
    
    def getClassName(self):
        #print "getClassName"
        return "Pattern_Impl"

def register(nr):
    for c in pycd3.Node.__subclasses__():
        nf = NodeFactoryPatternImplementer(c)
        nf.__disown__()
        nr.addNodeFactory(nf)
        
# def test():
#     nr = pycd3.NodeRegistry()
#     nf = NodeFactory(Household).__disown__()
#     nr.addNodeFactory(nf)
#     node = nr.createNode("Household")
    
#test()
