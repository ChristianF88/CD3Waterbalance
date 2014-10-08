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

class Sewer2(pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        self.black_w = pycd3.Flow()
        self.discharged_V = pycd3.Flow()
        #dir (self.inf)
        print "init node"
        self.addInPort("black_w", self.black_w)
        self.addOutPort("discharged_V", self.discharged_V)
        self.current_V=0.0
               
        
        #self.addOutPort("gw", self.gw)
        #self.addInPort("in", self.inf)
        
    def init(self, start, stop, dt):
        print start
        print stop
        print dt
        return True
        
    def f(self, current, dt):
        
        sewer_w = self.black_w[0]
        self.current_V += sewer_w
        self.discharged_V[0] = self.current_V
       

        return dt
    
    def getClassName(self):
        print "getClassName"
        return "Sewer2"

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
