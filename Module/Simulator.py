# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 14:12:52 2014

@author: Acer
"""

import subprocess

#call(["C:\Program Files (x86)\CityDrain3\bin\cd3.exe"], ["C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\complex_system.xml"])

cd3 = r'"""C:\Program Files (x86)\CityDrain3\bin\cd3.exe"   C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\complex_system.xml""'
print cd3
p = subprocess.Popen(cd3, shell=True)
print p
print "hallo"