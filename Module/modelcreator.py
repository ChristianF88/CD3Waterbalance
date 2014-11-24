# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 14:59:00 2014

@author: Acer
"""
#EXAMPLE: [startdate, stopdate] = ['2000-Jan-01 00:00:00', '2001-Jan-01 00:00:00']
class Simulationsetup:
    def __init__(self, startdate, stopdate, timestep, module):
         self.startdate = startdate
         self.stopdate = stopdate
         self.timestep = timestep
         self.module= module
         
         self.string1 = """<?xml version="1.0" encoding="UTF-8"?>
    <citydrain version="1.0">
        <pluginpath path="nodes"/>
        <pythonmodule module="""
         self.string2="""/>
        <pythonmodule module="""
         self.string3="""/>
        <simulation class="DefaultSimulation">
            <time start=""" 
         self.string4 = """ stop="""
    
         self.string5=""" dt="""
         self.string6=""">
                <flowdefinition>
                    <flow name="Q"/>
                    <concentration name="BOD5"/>
                    <concentration name="COD"/>
                    <concentration name="Cu"/>
                    <concentration name="Ntot"/>
                </flowdefinition>
            </time>
        </simulation>
        <model>
            <nodelist>""" 
         self.Simulationsetupstring = self.string1 +'"'+ str(self.module) +'"'+ self.string2 +'"'+ str(self.module) +'"'+ self.string3 +'"'+ str(self.startdate) +'"'+ self.string4 +'"'+ str(self.stopdate) +'"'+ self.string5 +'"'+ str(self.timestep) +'"'+ self.string6
    
    
         print self.Simulationsetupstring

class Modelinputnodes:
    def __init__(self, rainfile, evapofile, sun_zenith, sundown):
         self.rainfile = rainfile
         self.evapofile = evapofile
         self.sun_zenith = sun_zenith
         self.sundown = sundown
         
         self.string1="""                <node id="File_Reader_0" class="File_Reader">
                    <parameter name="" type="string" value="""
         self.string2="""/>
                    <parameter name="Type_H_for_height_[mm]_or_F_for_flow_[l/h]" type="string" value="H"/>
                </node>
                <node id="File_Reader_1" class="File_Reader">
                    <parameter name="" type="string" value="""
         self.string3="""/>
                    <parameter name="Type_H_for_height_[mm]_or_F_for_flow_[l/h]" type="string" value="H"/>
                </node>
		<node id="Pattern_Impl_0" class="Pattern_Impl">
                    <parameter name="sun_zenith_[0-23h]" type="double" value="""
         self.string4="""/>
                    <parameter name="sundown_[0-23h]" type="double" value="""
         self.string5="""/>
                </node>"""
            
         self.Modelinputnodesstring = self.string1 +'"'+ str(self.rainfile) +'"'+ self.string2 +'"'+ str(self.evapofile) +'"'+ self.string3 +'"'+ str(self.sun_zenith) +'"'+ self.string4 +'"'+ str(self.sundown) +'"'+ self.string5

         print self.Modelinputnodesstring




         
Setupheader = Simulationsetup("2000-Jan-01 00:00:00", "2001-Jan-01 00:00:00", "360", "C:/Users/Acer/Documents/GitHub/CD3Waterbalance/Module/cd3waterbalancemodules.py")
Needtohaveinputs = Modelinputnodes("C:/Users/Acer/Documents/GitHub/CD3Waterbalance/simulationwithpatterns/inputfiles/rain.ixx", "C:/Users/Acer/Documents/GitHub/CD3Waterbalance/simulationwithpatterns/inputfiles/evapo.ixx", "13", "20,5")


print Setupheader.Simulationsetupstring + Needtohaveinputs.Modelinputnodesstring





outFile = open('homemade.xml', 'w')
outFile.write(Setupheader.Simulationsetupstring + Needtohaveinputs.Modelinputnodesstring)
outFile.close()