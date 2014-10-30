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

class Distributor(pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        self.inflow = pycd3.Flow()
        self.Out1 = pycd3.Flow()
        self.Out2 = pycd3.Flow()
        self.Out3 = pycd3.Flow()
        self.Out4 = pycd3.Flow()
        self.Out5 = pycd3.Flow()
        
        #self.number_outports = pycd3.Double(3)
        #self.addParameter("Number of Outports", self.number_outports)
        
        #L=zip(['self.addOutPort("Out1", self.Out1)','self.addOutPort("Out2", self.Out2)','self.addOutPort("Out3", self.Out3)','self.addOutPort("Out4", self.Out4)','self.addOutPort("Out5", self.Out5)','self.addOutPort("Out6", self.Out6)','self.addOutPort("Out7", self.Out7)','self.addOutPort("Out8", self.Out8)','self.addOutPort("Out9", self.Out9)','self.addOutPort("Out10", self.Out10)'])
        
        #for i in range(self.number_outports):
        #    exec "%s" % L[i]
        
        
        
        print "init node"
        
        self.addInPort("In", self.inflow)
        self.addOutPort("Out1", self.Out1)
        self.addOutPort("Out2", self.Out2)
        self.addOutPort("Out3", self.Out3)
        self.addOutPort("Out4", self.Out4)
        self.addOutPort("Out5", self.Out5)
     
       
       
            	
        
    def init(self, start, stop, dt):
        print start
        print stop
        print dt
        return True
        
    def f(self, current, dt):
        
        
        
        self.Out1[0] = self.inflow[0]
        self.Out2[0] = self.inflow[0]
        self.Out3[0] = self.inflow[0]
        self.Out4[0] = self.inflow[0]
        self.Out5[0] = self.inflow[0]
        
        
        
        
        
      
       

        return dt
    
    def getClassName(self):
        print "getClassName"
        return "Distributor"

def register(nr):
    for c in pycd3.Node.__subclasses__():
        nf = NodeFactory(c)
        nf.__disown__()
        nr.addNodeFactory(nf)
        
