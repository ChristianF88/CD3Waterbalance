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
        <nodelist> \n """ 
         self.Simulationsetupstring = self.string1 +'"'+ str(self.module) +'"'+ self.string2 +'"'+ str(self.module) +'"'+ self.string3 +'"'+ str(self.startdate) +'"'+ self.string4 +'"'+ str(self.stopdate) +'"'+ self.string5 +'"'+ str(self.timestep) +'"'+ self.string6

class Modelinputnodes:
    
    def __init__(self, rainfile, evapofile, sun_zenith, sundown):
         self.rainfile = rainfile
         self.evapofile = evapofile
         self.sun_zenith = sun_zenith
         self.sundown = sundown
         
         self.string1="""           <node id="File_Reader_0" class="File_Reader">
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
            </node> \n """
            
         self.Modelinputnodesstring = self.string1 +'"'+ str(self.rainfile) +'"'+ self.string2 +'"'+ str(self.evapofile) +'"'+ self.string3 +'"'+ str(self.sun_zenith) +'"'+ self.string4 +'"'+ str(self.sundown) +'"'+ self.string5
    
class Catchmentsetup:
    
    def __init__(self, numberofCatchments, **Catchmentattributes ):
        self.numberofCatchments = numberofCatchments
        global Catchmentattributelist
        Catchmentattributelist = []
        for catchmentcounter in range(numberofCatchments):
            exec 'Catchmentattributelist.append({"Catchment_'+str(i)+'" : Catchmentattributes})'
        
        print str(numberofCatchments)+' Catchments have been created!'
        return
    
    def Setandwrite_attributes(self,numberofCatchments, attributevector):
        global Catchmentattributelist
        for i in range(numberofCatchments):
            print i
            Catchmentattributelist[i][str('Catchment_'+str(i))]["Number_of_Subareas"] = attributevector[i][0]
            Catchmentattributelist[i][str('Catchment_'+str(i))]["Decay_Constant"] = attributevector[i][1]
            Catchmentattributelist[i][str('Catchment_'+str(i))]["Catchment_Area"] = attributevector[i][2]
            Catchmentattributelist[i][str('Catchment_'+str(i))]["Fraktion_of_Impervious_Area_to_Reservoir_iAR"] = attributevector[i][3]
            Catchmentattributelist[i][str('Catchment_'+str(i))]["Fraktion_of_Impervious_Area_to_Stormwater_Drain_iASD"] = attributevector[i][4]
            Catchmentattributelist[i][str('Catchment_'+str(i))]["Fraktion_of_Pervious_Area_pA"] = attributevector[i][5]
            Catchmentattributelist[i][str('Catchment_'+str(i))]["Initial_Infiltration_Capacity"] = attributevector[i][6]
            Catchmentattributelist[i][str('Catchment_'+str(i))]["Final_Infiltration_Capacity"] = attributevector[i][7]
            Catchmentattributelist[i][str('Catchment_'+str(i))]["Depression_Loss"] = attributevector[i][8]
            Catchmentattributelist[i][str('Catchment_'+str(i))]["Wetting_Loss"] = attributevector[i][9]
            Catchmentattributelist[i][str('Catchment_'+str(i))]["Outdoor_Demand_Weighing_Factor"] = attributevector[i][10]
            Catchmentattributelist[i][str('Catchment_'+str(i))]["Runoff_Runtime_iAR"] = attributevector[i][11]
            Catchmentattributelist[i][str('Catchment_'+str(i))]["Runoff_Runtime_iASD"] = attributevector[i][12]
            Catchmentattributelist[i][str('Catchment_'+str(i))]["Runoff_Runtime_pA"] = attributevector[i][13]
            Catchmentattributelist[i][str('Catchment_'+str(i))]["Weighting_Coefficient_iAR"] = attributevector[i][14]
            Catchmentattributelist[i][str('Catchment_'+str(i))]["Weighting_Coefficient_iASD"] = attributevector[i][15]
            Catchmentattributelist[i][str('Catchment_'+str(i))]["Weighting_Coefficient_pA"] = attributevector[i][16]
            
        
        global Catchmentnodelist
        Catchmentnodelist = []
        for i in range(numberofCatchments):
            exec '''self.line1='\\t\\t\\t<node id="Catchment_w_Routing_'+str(i)+'" class="Catchment_w_Routing"> \\n' '''
            exec '''self.line2='\\t\\t\\t\\t<parameter name="Number_of_Subareas_[-]" type="double" value="'+str(Catchmentattributelist[i][str('Catchment_'+str(i))]["Number_of_Subareas"])+'"/> \\n ' '''
            exec '''self.line3='\\t\\t\\t\\t<parameter name="Fraktion_of_Impervious_Area_to_Reservoir_iAR_[-]" type="double" value="'+str(Catchmentattributelist[i][str('Catchment_'+str(i))]["Fraktion_of_Impervious_Area_to_Reservoir_iAR"])+'"/> \\n ' '''
            exec '''self.line4='\\t\\t\\t\\t<parameter name="Fraktion_of_Impervious_Area_to_Stormwater_Drain_iASD_[-]" type="double" value="'+str(Catchmentattributelist[i][str('Catchment_'+str(i))]["Fraktion_of_Impervious_Area_to_Stormwater_Drain_iASD"])+'"/> \\n ' '''
            exec '''self.line5='\\t\\t\\t\\t<parameter name="Depression_Loss_[mm]" type="double" value="'+str(Catchmentattributelist[i][str('Catchment_'+str(i))]["Depression_Loss"])+'"/> \\n ' '''
            exec '''self.line6='\\t\\t\\t\\t<parameter name="Runoff_Runtime_iAR_[s]" type="double" value="'+str(Catchmentattributelist[i][str('Catchment_'+str(i))]["Runoff_Runtime_iAR"])+'"/> \\n ' '''
            exec '''self.line7='\\t\\t\\t\\t<parameter name="Weighting_Coefficient_iASD_[-]" type="double" value="'+str(Catchmentattributelist[i][str('Catchment_'+str(i))]["Weighting_Coefficient_iASD"])+'"/> \\n ' '''
            exec '''self.line8='\\t\\t\\t\\t<parameter name="Decay_Constant_[1/min]" type="double" value="'+str(Catchmentattributelist[i][str('Catchment_'+str(i))]["Decay_Constant"])+'"/> \\n ' '''
            exec '''self.line9='\\t\\t\\t\\t<parameter name="Initial_Infiltration_Capacity_[m/h]" type="double" value="'+str(Catchmentattributelist[i][str('Catchment_'+str(i))]["Initial_Infiltration_Capacity"])+'"/> \\n ' '''
            exec '''self.line10='\\t\\t\\t\\t<parameter name="Weighting_Coefficient_iAR_[-]" type="double" value="'+str(Catchmentattributelist[i][str('Catchment_'+str(i))]["Weighting_Coefficient_iAR"])+'"/> \\n ' '''
            exec '''self.line11='\\t\\t\\t\\t<parameter name="Wetting_Loss_[mm]" type="double" value="'+str(Catchmentattributelist[i][str('Catchment_'+str(i))]["Wetting_Loss"])+'"/> \\n ' '''
            exec '''self.line12='\\t\\t\\t\\t<parameter name="Final_Infiltration_Capacity_[m/h]" type="double" value="'+str(Catchmentattributelist[i][str('Catchment_'+str(i))]["Final_Infiltration_Capacity"])+'"/> \\n ' '''
            exec '''self.line13='\\t\\t\\t\\t<parameter name="Fraktion_of_Pervious_Area_pA_[-]" type="double" value="'+str(Catchmentattributelist[i][str('Catchment_'+str(i))]["Fraktion_of_Pervious_Area_pA"])+'"/> \\n ' '''
            exec '''self.line14='\\t\\t\\t\\t<parameter name="Catchment_Area_[m^2]" type="double" value="'+str(Catchmentattributelist[i][str('Catchment_'+str(i))]["Catchment_Area"])+'"/> \\n ' '''
            exec '''self.line15='\\t\\t\\t\\t<parameter name="Weighting_Coefficient_pA_[-]" type="double" value="'+str(Catchmentattributelist[i][str('Catchment_'+str(i))]["Weighting_Coefficient_pA"])+'"/> \\n ' '''
            exec '''self.line16='\\t\\t\\t\\t<parameter name="Runoff_Runtime_pA_[s]" type="double" value="'+str(Catchmentattributelist[i][str('Catchment_'+str(i))]["Runoff_Runtime_pA"])+'"/> \\n ' '''
            exec '''self.line17='\\t\\t\\t\\t<parameter name="Runoff_Runtime_iASD_[s]" type="double" value="'+str(Catchmentattributelist[i][str('Catchment_'+str(i))]["Runoff_Runtime_iASD"])+'"/> \\n ' '''
            exec '''self.line18='\\t\\t\\t\\t<parameter name="Outdoor_Demand_Weighing_Factor_[-]" type="double" value="'+str(Catchmentattributelist[i][str('Catchment_'+str(i))]["Outdoor_Demand_Weighing_Factor"])+'"/> \\n ' '''
            exec '''self.line19='\\t\\t\\t</node> \\n ' '''        
            
            alllines = ''
            for n in range(19):
                exec 'alllines += self.line'+str(n+1)
                
            Catchmentnodelist.append(alllines)
        


Testattrvec=[[0]*17]*2       
Setupheader = Simulationsetup("2000-Jan-01 00:00:00", "2001-Jan-01 00:00:00", "360", "C:/Users/Acer/Documents/GitHub/CD3Waterbalance/Module/cd3waterbalancemodules.py")
Needtohaveinputs = Modelinputnodes("C:/Users/Acer/Documents/GitHub/CD3Waterbalance/simulationwithpatterns/inputfiles/rain.ixx", "C:/Users/Acer/Documents/GitHub/CD3Waterbalance/simulationwithpatterns/inputfiles/evapo.ixx", "13", "20,5")
Catchments = Catchmentsetup(2 , Decay_Constant =1.9, Catchment_Area = 100, Fraktion_of_Impervious_Area_to_Reservoir_iAR= 0.4, Fraktion_of_Impervious_Area_to_Stormwater_Drain_iASD = 0.3, Fraktion_of_Pervious_Area_pA = 0.3, Number_of_Subareas = 1, Initial_Infiltration_Capacity = 0.6, Final_Infiltration_Capacity = 0.21, Depression_Loss = 1.5, Wetting_Loss = 0.4, Outdoor_Demand_Weighing_Factor = 0.5, Runoff_Runtime_iAR = 400, Runoff_Runtime_iASD = 500, Runoff_Runtime_pA = 700, Weighting_Coefficient_iAR = 0.04, Weighting_Coefficient_iASD = 0.05, Weighting_Coefficient_pA = 0.06)
Catchments.Setandwrite_attributes(2,Testattrvec)



#Writing all strings in list:
Allstrings=[]
Allstrings.append(Setupheader.Simulationsetupstring)
Allstrings.append(Needtohaveinputs.Modelinputnodesstring)
for i in range(len(Catchmentnodelist)):
    Allstrings.append(Catchmentnodelist[i])
    
    
outFile = open('Melbourne.xml', 'w')
for i in range(len(Allstrings)):
    outFile.write( Allstrings[i])
outFile.close()

 
    
    
    
    
    
    