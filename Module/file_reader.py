# -*- coding: utf-8 -*-
"""
Created on Thu Oct 02 08:41:08 2014

@author: Acer
"""

import sys
import pycd3
import csv

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

class Inflow_Reader(pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        self.inflow = pycd3.String("")
        self.out = pycd3.Flow()
        
        print "init node"
        self.intern_addParameter("", self.inflow)
        self.addOutPort("out", self.out)
        
               
        
        
        
    def init(self, start, stop, dt):
        print start
        print stop
        self.list_csv=[]
        print dt
        return True
        
    def f(self, current, dt):
        
        with open(self.inflow) as csvfile:
            self.data=csv.reader(csvfile, delimiter=' ')  
            
            for row in self.data:
                self.list_csv.append(', '.join(row))
        self.out[0]=self.list_csv[0][1]
        
        
        return dt
    
    def getClassName(self):
        print "getClassName"
        return "Inflow_Reader"

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
