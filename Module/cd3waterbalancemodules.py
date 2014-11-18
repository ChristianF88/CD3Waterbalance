# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 13:02:58 2014

@author: Acer
"""

import pycd3

import Raintank
import Household
import Stormwaterpipe
import Sewer2
import Potable_Water_Resorvior
import Pattern_Implementer
import File_Reader
import Distributor
import Collector
import Catchment_with_Routing
import Greywatertank
import Catchment

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
        return "cd3waterbalancemodules.py"



def register(nr):
    for c in pycd3.Node.__subclasses__():
        nf = NodeFactory(c)
        nf.__disown__()
        nr.addNodeFactory(nf)
        