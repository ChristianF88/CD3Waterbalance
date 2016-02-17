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
#        self.Watering = pycd3.Flow()
        self.porepressure = pycd3.Flow()
        self.storagecheck = pycd3.Flow()
        self.evapotranspiration =pycd3.Flow()
        self.outdoordemand = pycd3.Flow()
        self.outdoordemand_check = pycd3.Flow()
        self.actualevapo = pycd3.Flow()
        
        self.addInPort("Evapotranspiration", self.evapotranspiration)
        self.addOutPort("Actual_Evapotranspiration", self.actualevapo)
        self.addOutPort("Outdoordemand", self.outdoordemand)
        self.addOutPort("Outdoordemand_Check", self.outdoordemand_check)
        self.addInPort("Infiltration", self.Infiltration)
#        self.addInPort("Garden_Watering", self.Watering)
        self.addInPort("Underground_Inflow", self.inflow)
        self.addOutPort("Check_Pore_Pressure",self.porepressure)
        self.addOutPort("Soilstorage_Check", self.storagecheck)
        
        self.total_area = pycd3.Double(1000)
        self.addParameter("Total_Area_[m^2]", self.total_area)    
        self.total_perv_area = pycd3.Double(40.0)
        self.addParameter("Total_Pervious_Area_[m^2]",self.total_perv_area)
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
        self.initialwatercontent = pycd3.Double(0.18)
        self.addParameter("Initial_Water_Content_[-]",self.initialwatercontent)
        self.seepagerate = pycd3.Double(0.22)
        self.addParameter("Hydraulic_Conductivity_(Saturated_Conditions)_[m/d]",self.seepagerate)
        
        self.fieldcapacitiy = pycd3.Double(-100.0)
        self.addParameter("Field_Capacity_[cm_Water_Column]",self.fieldcapacitiy)
        #factor for calibrating outdoordemand
        self.outdoor_demand_coefficient = pycd3.Double(0.8)
        self.addParameter("Outdoor_Demand_Actual_Evapotranspiration_Ratio_(OutD/ActualEvapotr)_[-]", self.outdoor_demand_coefficient)

        
    def init(self, start, stop, dt):
#        print start
#        print stop
#        print dt
#        print "init node"
        self.fieldcapacitiy=-1*self.fieldcapacitiy
        self.memory = self.total_area*self.soildepth*self.initialwatercontent
        self.waterpressure2 = self.fieldcapacitiy*2
        
        return True
        
    def f(self, current, dt):
        
        def InversVanGenuchten (Watercontent,Residualwatercontent,Saturationwatercontent,alpha,n):
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
        
        def Evapfactor(h,hWP,hFC):
            #print [h,hWP,hFC]
            if -h>=-hFC:                
                factor = 1
            elif -hWP<-h<-hFC:
                factor = (h-hWP)/(hFC-hWP)
            else:
                factor = 0
            return factor
        #print [self.waterpressure2 , 10**4.2, self.fieldcapacitiy*1]
        
        self.actualevapo[0] = Evapfactor(self.waterpressure2, 10**4.2, self.fieldcapacitiy*1)*self.evapotranspiration[0]/1000
        
        #Infiltration(from Rain and Watering) - Inflow / Evapotranspiration - Outflow
        self.memory += self.Infiltration[0] #+ self.Watering[0]
        self.memory -= self.actualevapo[0] * self.total_perv_area
        self.memory += self.actualevapo[0] * self.total_perv_area * self.outdoor_demand_coefficient
        self.memory += self.inflow[0] 

        #Waterflow to lower layers
        tolowerlayer = VanGenuchtenConductivity (self.waterpressure2,self.alpha,self.n)*self.seepagerate/24/3600*dt*self.total_area
        self.memory -=tolowerlayer
        
        #new water content
        newwatercontent = self.memory/(self.total_area*self.soildepth)

        #new water pressure in cm water column
        waterpressure = InversVanGenuchten (newwatercontent,self.Residualwatercontent,self.Saturationwatercontent,self.alpha,self.n)
        self.waterpressure2 = waterpressure

        #evapotranspiration factor
        self.storagecheck[0] = self.memory
        self.porepressure[0] = waterpressure
        self.outdoordemand[0] = self.actualevapo[0] * self.outdoor_demand_coefficient 
        self.outdoordemand_check[0] = self.outdoordemand[0] * self.total_perv_area
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
