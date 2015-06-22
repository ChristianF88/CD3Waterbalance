# -*- coding: utf-8 -*-
"""
Created on Thu Oct 02 08:41:08 2014

@author: Acer
"""

import sys
import pycd3
import math

#class NodeFactoryCollector(pycd3.INodeFactory):
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

class Soilstorage(pycd3.Node):
    def __init__(self):
        pycd3.Node.__init__(self)
        
        self.inflow = pycd3.Flow()        
        self.porepressure = pycd3.Flow()
        self.evapofaktor = pycd3.Flow()
        self.storagecheck = pycd3.Flow()
        self.numberof_in_ports = pycd3.Integer(2)
        self.addParameter("Number_of_Inports", self.numberof_in_ports)       
        self.total_area = pycd3.Double(1000)
        self.addParameter("Total_Area_[m^2]", self.total_area)        
        self.soildepth = pycd3.Double(1000)
        self.addParameter("Depth_Of_Soil_[m]", self.soildepth)        
        self.Residualwatercontent = pycd3.Double(0.0)
        self.addParameter("Residual_Water_Content_[-]", self.Residualwatercontent) 
        self.Saturationwatercontent = pycd3.Double(0.4)
        self.addParameter("Saturation_Water_Content_[-]", self.Saturationwatercontent) 
        self.alpha = pycd3.Double(0.08)
        self.addParameter("Van_Genuchten_Parameter_Alpha_[cm^-1]",self.alpha)
        self.n = pycd3.Double(1.3)
        self.addParameter("Van_Genuchten_Parameter_n_[-]",self.n)
        self.initialwatercontent = pycd3.Double(0.3)
        self.addParameter("Initial_Water_Content_[-]",self.initialwatercontent)
        self.fieldcapacitiy = pycd3.Double(200)
        self.addParameter("Field_Capacity_[cm_Water_Column]",self.fieldcapacitiy)
        self.seepagerate = pycd3.Double(0.2)
        self.addParameter("Seepage_Rate[m/d]",self.seepagerate)

        

        
    def init(self, start, stop, dt):
#        print start
#        print stop
#        print dt
#        print "init node"
        
        for i in range(self.numberof_in_ports):
            exec 'self.Infiltration'+str(i+1)+'=pycd3.Flow()' 
            exec 'self.addInPort("Infiltration_'+str(i+1)+'", self.Infiltration'+str(i+1)+')'
            exec 'self.Watering'+str(i+1)+'=pycd3.Flow()' 
            exec 'self.addInPort("Garden_Watering'+str(i+1)+'", self.Watering'+str(i+1)+')' 
        
        self.addInPort("Underground_Inflow", self.inflow)
        self.addOutPort("Check_Pore_Pressure",self.porepressure)
        self.addOutPort("Evapofactor", self.evapofaktor)
        self.addOutPort("Storage_Check", self.storagecheck)

        self.memory = self.total_area*self.soildepth*self.initialwatercontent

        return True
        
    def f(self, current, dt):
        
        def InversVanGenuchten (Watercontent,Residualwatercontent,Saturationwatercontent,alpha,n):
             H=1/alpha*math.pow((math.pow(((Watercontent-Residualwatercontent)/(Saturationwatercontent-Residualwatercontent)),(n/(1-n)))-1),(1/n))
             return H
        
        def Evapfactor(h,hWP,hFC):
            if -1*h>=-1*hFC:                
                factor = 1
            elif -1*hWP<-1*h<-1*hFC:
                factor = (h-hWP)/(hFC-hWP)
            else:
                factor = 0
            return factor
            
        #Infiltration(from Rain and Watering) - Inflow / Evapotranspiration - Outflow
        for i in range(self.numberof_in_ports):
            exec 'self.memory += self.Infiltration'+str(i+1)+'[0] + self.Watering'+str(i+1)+'[0]' in globals(), locals()
        self.memory += self.inflow[0] 
        
        #Waterflow to lower layers
        tolowerlayer=self.seepagerate/24/3600*dt*self.total_area
        self.memory -=tolowerlayer
        
        #new water content
        newwatercontent = self.memory/(self.total_area*self.soildepth)
        #new water pressure in cm water column
        waterpressure = InversVanGenuchten (newwatercontent,self.Residualwatercontent,self.Saturationwatercontent,self.alpha,self.n)
        #evapotranspiration factor
        self.evapofaktor[0] = Evapfactor(waterpressure,math.pow(10,4.2),self.fieldcapacitiy)
        self.storagecheck[0] = self.memory
        self.porepressure[0] = waterpressure
        return dt
        
    
    def getClassName(self):
#        print "getClassName"
        return "Soilstorage"

#def register(nr):
#    for c in pycd3.Node.__subclasses__():
#        nf = NodeFactoryCollector(c)
#        nf.__disown__()
#        nr.addNodeFactory(nf)
#        


#import matplotlib
#import math
#import numpy
#import pylab
#def InversVanGenuchten (Watercontent,Residualwatercontent,Saturationwatercontent,alpha,n):
#            H=1/alpha*math.pow((math.pow(((Watercontent-Residualwatercontent)/(Saturationwatercontent-Residualwatercontent)),(n/(1-n)))-1),(1/n))
#            return H
#def Evapfactor(h,hWP,hFC):
#            if -h>=-hFC:                
#                factor = 1
#            elif -hWP<-h<-hFC:
#                factor = (h-hWP)/(hFC-hWP)
#            else:
#                factor = 0
#            return factor
#store=[]
#evap=[]
#content=[]
#for i in numpy.arange(0.044,0.37,.001):
#    store.append(InversVanGenuchten (i,0.043019,0.370687,0.087424,1.57535))
#    evap.append(Evapfactor(InversVanGenuchten (i,0.043019,0.370687,0.087424,1.57535),math.pow(10,4.2),200))
#    content.append(i)
#matplotlib.pyplot.yscale('log', nonposy='clip')
#pylab.plot(content,store)
#pylab.plot(content,evap)