# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:46:53 2015

@author: Gerhard
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
        self.Infiltration = pycd3.Flow()
        self.Watering = pycd3.Flow()
        self.porepressure = pycd3.Flow()
        self.storagecheck = pycd3.Flow()
        
        self.addInPort("Infiltration/Evapotranspiration", self.Infiltration)
        self.addInPort("Garden_Watering", self.Watering)
        self.addInPort("Underground_Inflow", self.inflow)
        self.addOutPort("Check_Pore_Pressure",self.porepressure)
        self.addOutPort("Soilstorage_Check", self.storagecheck)
        
        self.total_area = pycd3.Double(1000)
        self.addParameter("Total_Area_[m^2]", self.total_area)        
        self.soildepth = pycd3.Double(1)
        self.addParameter("Depth_Of_Soil_[m]", self.soildepth)        
        self.Residualwatercontent = pycd3.Double(0.01)
        self.addParameter("Residual_Water_Content_[-]", self.Residualwatercontent) 
        self.Saturationwatercontent = pycd3.Double(0.4)
        self.addParameter("Saturation_Water_Content_[-]", self.Saturationwatercontent) 
        self.alpha = pycd3.Double(0.08)
        self.addParameter("Van_Genuchten_Parameter_Alpha_[cm^-1]",self.alpha)
        self.n = pycd3.Double(1.3)
        self.addParameter("Van_Genuchten_Parameter_n_[-]",self.n)
        self.initialwatercontent = pycd3.Double(0.3)
        self.addParameter("Initial_Water_Content_[-]",self.initialwatercontent)
        self.seepagerate = pycd3.Double(0.2)
        self.addParameter("Hydraulic_Conductivity_(Saturated_Conditions)_[m/d]",self.seepagerate)

        
    def init(self, start, stop, dt):
#        print start
#        print stop
#        print dt
#        print "init node"

        self.memory = self.total_area*self.soildepth*self.initialwatercontent
        self.waterpressure2 = 300.
        return True
        
    def f(self, current, dt):
        
        def VanGenuchten (Watercontent,Residualwatercontent,Saturationwatercontent,alpha,n):
            if Watercontent>Saturationwatercontent:
                H=-1
            else:
                H=1/alpha*math.pow((math.pow(((Watercontent-Residualwatercontent)/(Saturationwatercontent-Residualwatercontent)),(n/(1-n)))-1),(1/n))
            return H
            
        def VanGenuchtenConductivity (porepressure,alpha,n):
            if porepressure < 0:
                K=1
            else:
                K=((1-(alpha*porepressure)**(n-1)*(1+(alpha*porepressure)**n)**(1/n-1))**2)/((1+(alpha*porepressure)**n)**((1-1/n)*1/2))
                #K=(math.pow((1-math.pow((alpha*porepressure),(n-1))*math.pow((1+math.pow((alpha*porepressure),n)),(1/n-1))),2))/(math.pow((1+math.pow((alpha*porepressure),n)),((1/2)*(1-1/n))))
            return K        
        
            
        #Infiltration(from Rain and Watering) - Inflow / Evapotranspiration - Outflow
        self.memory += self.Infiltration[0] + self.Watering[0]
        print 'A '+str([self.Infiltration[0], self.Watering[0]])
        self.memory += self.inflow[0] 

        #Waterflow to lower layers
        tolowerlayer = VanGenuchtenConductivity (self.waterpressure2,self.alpha,self.n)*self.seepagerate/24/3600*dt*self.total_area
        self.memory -=tolowerlayer
        
        #new water content
        newwatercontent = self.memory/(self.total_area*self.soildepth)

        #new water pressure in cm water column
        waterpressure = VanGenuchten (newwatercontent,self.Residualwatercontent,self.Saturationwatercontent,self.alpha,self.n)
        self.waterpressure2 = waterpressure
        print 'B '+ str([self.memory, self.memory/(self.total_area*self.soildepth), tolowerlayer, waterpressure])
        #evapotranspiration factor
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
#def VanGenuchtenConductivity (Watercontent,alpha,n):
#             K=math.pow((1-math.pow((alpha*Watercontent),(n-1))*math.pow((1+math.pow((alpha*Watercontent),n)),(1/n-1))),2)/math.pow((1+math.pow((alpha*Watercontent),n)),((1/2)*(1-1/n)))
#             return K
#def Evapfactor(h,hWP,hFC):
#            if -h>=-hFC:                
#                factor = 1
#            elif -hWP<-h<-hFC:
#                factor = (h-hWP)/(hFC-hWP)
#            else:
#                factor = 0
#            return factor
#
#store=[]
#evap=[]
#content=[]
#KAY=[]
#for i in numpy.arange(0.044,0.37,.001):
#    store.append(InversVanGenuchten (i,0.043019,0.370687,0.087424,1.57535))
#    evap.append(Evapfactor(InversVanGenuchten (i,0.043019,0.370687,0.087424,1.57535),math.pow(10,4.2),200))
#    KAY.append(VanGenuchtenConductivity(InversVanGenuchten (i,0.043019,0.370687,0.087424,1.57535),0.087424,1.57535))
#    content.append(i)
#
#matplotlib.pyplot.yscale('log', nonposy='clip')
#pylab.plot(content,store)
#pylab.plot(content,evap)
#pylab.plot(content,KAY)
