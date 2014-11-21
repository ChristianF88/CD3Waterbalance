# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 15:10:40 2014

@author: Acer
"""

#to open files
import csv        
csv_file = open('C:\Users\Acer\Documents\GitHub\CD3Waterbalance\evapotranspiration_two_weeks.ixx', "r") 
data = csv.reader(csv_file, delimiter='\t')             
list1 = list(data) 
print list1


#to create variables
for i in range(4):
    exec "a"+str(i)+" =i*9"  
    
#interpolation
from scipy.interpolate import interp1d
from numpy import linspace
x=[0, 800]
y=[0, 10]
f=interp1d(x,y)
delta = linspace(x[0],x[-1],6)
z=f(delta)
z_2=f(40)
print z
print''
print z_2


#find value in array with function
import numpy as np
def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

array = np.random.random(10)
print(array)
value = 0.5
print(find_nearest(array, value))


#find 2 lines that are above and below a certain value
a=arange(1,10.1,0.3)
dt_read=a[1]-a[0]
dt_given=0.4000001
index_line_below=floor(dt_given/dt_read)
index_line_above=ceil(dt_given/dt_read)
print str(a[index_line_below])+' <= '+str(a[0]+dt_given)+ ' <= ' + str(a[index_line_above])


#Schleife mit bestimmten Laufwerten
ints = [8, 23, 45, 12, 78]
for  val in enumerate(ints):
    print  val

for  val in [8, 23, 45, 12, 78]:
    print  val


#in einem vektor suchen
pattern=[[0, 0],[1/24., 0],[2/24., 0],[3/24., 0],[4/24., 0.01],[5/24., 0.02],[6/24., 0.08],[7/24., 0.21],[8/24., 0.52],
         [9/24., 1.06],[10/24., 1.86],[11/24., 2.78],[12/24., 3.54],[13/24., 3.83],[14/24., 3.54],[15/24., 2.78],[16/24., 1.86],
         [17/24., 1.06],[18/24., 0.52],[19/24., 0.21],[20/24., 0.08],[21/24., 0.02],[22/24., 0.01],[23/24., 0],[1, 0]]
time=0.7
i=0
while (time > pattern[i][0]):
    i+=1
print i
count_i = 0
while (time - floor(time) > pattern[count_i][0]):
    count_i+=1
    print "i is "+str(count_i)

#creating numberob variable and summing them all up
for i in range(4):
    exec 'Inport'+str(i)+'= '+str(i)        
memory = 0.0     
for i in range(4):
    exec 'memory += Inport'+str(i)
outflow = memory
        
#Erweiterung Patternimplementer
import numpy as np
from numpy import arange, mean, asarray
nu = 13/24.
sigma = 2.5/24.
t=arange(0,1-1/24,1/24.)
y = 1/(sigma*np.sqrt(2*pi))*np.exp(-1/2.*((t-nu)/sigma)**2)
f =y/mean(y)
pattern=asarray([t,f]).transpose().tolist()
pattern.append([1.0, pattern[0][1]])

dt=360
sundown=20.5
zenith=13
deviation = (sundown - zenith)/3./24.      
xtime=arange(0,1.0-dt/24./3600.,dt/24./3600.)
gauss_curve = 1/(deviation*np.sqrt(2*pi))*np.exp(-1/2.*((xtime-zenith/24.)/deviation)**2)
factor =gauss_curve/mean(gauss_curve)
pattern=asarray([xtime,factor]).transpose().tolist()
pattern.append([1.0, pattern[0][1]])

#bedingtes vektor anfügen
filename='simple_system_CwR_RT_indooruse.xml'

r'"""C:\Program Files (x86)\CityDrain3\bin\cd3.exe"   C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\outputfiles\%s""' % filename
r'"""C:\Program Files (x86)\CityDrain3\bin\cd3.exe"   C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\outputfiles\simple_system_CwR_RT_indooruse.xml""'
str("C:\Program Files (x86)\CityDrain3\bin\cd3.exe"   C:\Users\Acer\Documents\GitHub\CD3Waterbalance\simulationwithpatterns\outputfiles\)
str('"""')
