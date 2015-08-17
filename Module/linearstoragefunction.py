# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:46:53 2015

@author: Gerhard
"""

import numpy
import pylab as pl
import time
t1=time.time()

area = 1.
dt = 1.
K = 1.
#helpvec1 = numpy.random.rand(1,10000)[0]
#helpvec2 = numpy.random.randint(2, size=10000)
#rainvec = list(helpvec1*helpvec2)
rainvec = [0,0,0,0,1,1,1,1,1,1,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
flowlist=[]
Qtlist=[]
dtlist=[]
cut=0
num=0
flow=0
def linearstorage(i,dt,K,area,dtlist,rainvec):
    global num
    Qtlist=map(lambda x,y : (x*area/dt)*(numpy.exp((2*dt-y)/K)-numpy.exp(-y+dt/K)), rainvec[0:i+1], dtlist[0:i+1])
    global flow
    flow = sum(numpy.array(Qtlist))
    return num,flow


for i in range(len(rainvec)):
    dtlist.insert(0,i)
    linearstorage(i,dt,K,area,dtlist,rainvec)
    flowlist.append(flow)



t2=time.time()

Qbefore = [0,0,0]
def newway(i,dt,k,N,A):
    global Qbefore

    Q = (Qbefore[i]+A/dt*N*(numpy.exp(dt/k)-1))*numpy.exp(-dt/k)
    Qbefore[i] = Q
    return Q , Qbefore[i]
    
flowvector = []
for i in range(len(rainvec)):
    flowvector.append(newway(0,dt,K,rainvec[i],area)[0])
t3=time.time()


'''plot'''
pl.figure(figsize=(14, 5), dpi=80)
#pl.xlim(0,10)
#pl.ylim(0,1.1)
pl.plot(flowlist)
pl.plot(flowvector)
pl.legend(loc='best')
pl.title('Model In - and Output', fontsize=20)
pl.xlabel('Time [dt]')
pl.ylabel('Volume [m^3]')
pl.grid(True)
pl.show()

print 'Simulationtime1: '+str(t2-t1)
print 'Simulationtime2: '+str(t3-t2)