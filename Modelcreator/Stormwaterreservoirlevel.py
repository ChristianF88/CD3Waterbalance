# -*- coding: utf-8 -*-
"""
Created on Wed Dec 03 11:37:18 2014

@author: Acer
"""
#this class adds Stormwatertanks to certain clusters
#vector is needed
#[[[[6,3],[7,7], ...,1],[[6,3],[7,7], ...,1],[[6,3],[7,7], ...,0], ...,1],...]
#[[[[Numberof Buildings in Cluster, Number Clusters],...,Greywaterreservoir(1 = existing, 0 = no Greywaterreservoir)],...,Stormwaterreservoir(1 = existing, 0 = no Stormwaterreservoir)],....]
class Stormwaterreservoirlevel:
    def __init__(self):
        self.Stormwaterreservoirlevel_list = []
        self.runoff_coll_list = []
        self.overflow_coll_list = []
        self.street_list = []
    def writeconnections(self, stormvec):
        #Preparing lists with collector numbers that have certain amount of outports for later reference(values for nodes)

        
    
    #clusterhouseholdvec = [ [Number of Buildings , Clusternumber], [], [], ..., []]
    #cluhouseholdvec = [[6,1],[8,20],[25,40],[3,10]] 
               
    #number of inports for collectors
    #Cluster = Clusterlevel()
    #Cluster.writeconnections(cluhouseholdvec)
    #Cluster.allclusters



stormvec = [[[[6,3],[7,7],[2,5],1],[[4,3],[15,7],1],[[5,5],[10,2],[8,2],0],1],[[[2,3],[12,4],[4,3],0],[[9,5],[12,3],0],[[24,1],[7,5],[17,3],0],0]]
#print reservoirvec[0] ... Stormwaterreservoirlevel
#print reservoirvec[0][0] ... Greywaterreservoirlevel
