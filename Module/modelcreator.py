# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 14:59:00 2014

@author: Acer
"""
#EXAMPLE: [startdate, stopdate] = ['2000-Jan-01 00:00:00', '2001-Jan-01 00:00:00']
def header(startdate, stopdate): 
    
    string1 = """<?xml version="1.0" encoding="UTF-8"?>
<citydrain version="1.0">
    <pluginpath path="nodes"/>
    <pythonmodule module="C:/Users/Acer/Documents/GitHub/CD3Waterbalance/Module/cd3waterbalancemodules.py"/>
    <pythonmodule module="C:/Users/Acer/Documents/GitHub/CD3Waterbalance/Module/cd3waterbalancemodules.py"/>
    <simulation class="DefaultSimulation">
        <time start=""" 
    string2 = """ stop="""
    
    string3=""" dt="360">
            <flowdefinition>
                <flow name="Q"/>
                <concentration name="BOD5"/>
                <concentration name="COD"/>
                <concentration name="Cu"/>
                <concentration name="Ntot"/>
            </flowdefinition>
        </time>
    </simulation>"""
    
    string = string1 +'"'+ str(startdate) +'"'+ string2 +'"'+ str(stopdate) +'"'+ string3
    
    
    print string
    return
    
header('2000-Jan-01 00:00:00', '2001-Jan-01 00:00:00')