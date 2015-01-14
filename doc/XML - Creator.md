# XML - Creator

Basic features:

 - automated setup of an CD3 - Model
 - 5 levels of implementation

      - Building level
      -	Cluster level
      - Greywaterreservoir level
      - Stormwaterreservoir level
      - Supply level
 - basic and selective flowmeter implemetation
 # 
 - 
 
<br>

## Input


| Infrastructure Information  | Part of XML created  | Class created | 
| :------------ |:---------------:|:---------------:|  	
| Supplyvector      | Connectionlist | - |
| Catchment Attributevector | Nodelist |  Catchment  |
| Greywatertank Attributevector | Nodelist | Greywatertank   |
| Stormwaterreservoir Attributevector | Nodelist | Stormwaterreservoir   |   
| Rainwatertank Attributevector | Nodelist | Rainwatertank   |
| Building Demand Attributevector | Nodelist | Demand Model  |  


<br>

| Simulation Information  | Part of XML created  | Class created | 
| :------------ |:---------------:| 	:---------------:|
| Simulationsetup Vector  | Header, Pythonmodule, Simulation | -  |
| Needtohaveinputs Vector  | Nodelist |  - |

<br>

| Model Outputs  | Part of XML created  | Class created | 
| :------------ |:---------------:| 	:---------------:|
| Fileout Connection Name List      | Nodelist, Connectionlist | Fileout  |

<br>

## Output

An XML - File containing the model information for CD3.

## Detailed Input Description


<br>

> ### Supplyvector


The Supplyvector contains the information for all 5 model setup levels.
In its core the Clustervector accesses the Buildinglevel and creates Building Complexes.
The Clustervector contains the following information:

	[Number of Buildings, [Greywatertank existent (0 = No, 1 = Yes)], [contributing to Greywaterreservoir (0 = No, 1 = Yes), using treated Greywater from Reservoir (0 = No, 1 = Yes), using treated Stormwater (0 = No, 1 = Yes)], Number of Clusters ]
    
    For example: 
    
    	Clustervector = [6, [1,0,1,0,1,0], [0,0,0], 3]
        
        The Cluster contains 6 Buildings. The first, third and fifth Building do have a Greywatertank connected to them.
        The Cluster is not contributing to a Greywaterreservoir. It's not using Greywater from a Reservoir and it's not 
        connected to a Stormwaterreservoir. There're 3 Clusters of the configuration.
    

# 

Looking at the next higher level, the Greywaterreservoirvector needs to have the following setup:

	[[Clustervector_0, Clustervector_1, ..., Clustervector_a, Greywaterreservoir_0 existent (0 = No, 1 = Yes)], ..., 
    [Clustervector_b, Clustervector_b+1, ..., Clustervector_c, Greywaterreservoir_n existent (0 = No, 1 = Yes)]] 
    
    =
    
    [Greywaterreservoirarea _0, ..., Greywaterreservoirarea _n]
    
    
    For example: 
    
    	Greywaterreservoirvector = 
        [[[6,[1,0,1,1,1,1],[1,0,0],1], [7,[1,0,0,0,1,0,1],[1,1,0],1], [2,[0,1],[0,0,0],5], 1], 
         [[4,[1,0,1,1],[0,0,0],1], [3,[1,0,0],[0,0,0],7], [9,[0,1,0,1,1,0,1,0,1],[0,0,0],1], 0]]
         
        The vector decribes 2 areas. The first one consists out of 3 Clustervector. The 7 clusters 
        (5 clusters of the third configuration) are connected to a Greywaterreservoir. The first cluster contributes to the 
        Greywaterreservoirs inflow. The second cluster contributes to the inflow and uses the reservoirs outflow. 
        The last 5 clusters are not connected to the reservoir.
        There's no Greywaterreservoir available for the second Area. Hence none of the clusters is contributing or using
        Greywater from a reservoir.
        
# 

The next scale of implementation is the Stormwaterreservoirlevel. Its inputvector has the following structure:

	[[Greywaterreservoirvector_0, Greywaterreservoirvector_1, ..., Greywaterreservoirvector_a, Stormwaterreservoir_0 existent (0 = No, 1 = Yes)], ..., 
    [Greywaterreservoirvector_b, Greywaterreservoirvector_b+1, ..., Greywaterreservoirvector_c, Stormwaterreservoir_n existent (0 = No, 1 = Yes)]]
    
    =
    
    [Stormwaterreservoirarea _0, ..., Stormwaterreservoirarea _n]
    
    
    For example:
    	
        Stormwaterreservoirvector = 
        [[[[6,[1,0,1,0,0,0],[0,0,1],1],[4,[1,1,0,1],[1,1,1],1],[2,[0,1],[1,1,1],1],1], 
          [[3,[1,0,0],[0,0,1],1],[5,[0,0,0,0,0],[0,0,1],1],[2,[0,1],[0,0,1],1],0],1]]
          
        This example vector depicts one area only. The digit one at the vectors last position states that a Stormwaterreservoir
        is in place. It's connected to two Greywaterlevel subareas. The Clustervectors contain the "connection 
        information" (see above).
        
        Attention!!
        Is a cluster using treated Greywater from a reservoir and a Stormwaterreservoir is present too, then the cluster 
        will be connected to that one too! The Clustervector needs to look like this:
        
        [x,[...],[0,1,1],y] or [x,[...],[1,1,1],y]
        
        [[[[2,[0,1],[0,1,0],1],1],1]] is no  valid configuration!!
        

#  

Finally the Supplyvector can be explained:

	[[Stormwaterreservoirvector_0, Stormwaterreservoirvector_1, ...Stormwaterreservoirvector_a], ...,
     [Stormwaterreservoirvector_0, Stormwaterreservoirvector_1, ...Stormwaterreservoirvector_b]]
     
     =
     
     [Supplyarea_0, ..., Supplyarea_n]
     

	Thus the Supplyvector consits out of a number of different supply districts. One district my be combined out of 
    a number of Stormwatervectors.

        
<br>

> ### Catchment Attributevector

To set the Catchments features this vectors ist used.

	Catchment Attributevector = [Catchmentvector_0, Catchmentvector_1, ..., Catchmentvector_n]
    
    Each Catchmentvector contains the Catchments properties.
    
    Catchmentvector = [Number of Subareas, Decay Constant, Catchment Area, Fraktion of Impervious Area to Reservoir iAR,
    				   Fraktion of Impervious Area to Stormwater Drain iASD, Fraktion of Pervious Area pA,
                       Initial Infiltration Capacity, Final Infiltration Capacity, Depression Loss, Wetting Loss,
                       Outdoor Demand Weighing Factor, Runoff Runtime iAR, Runoff Runtime iASD, Runoff Runtime pA,
                       Weighting Coefficient iAR, Weighting Coefficient iASD, Weighting Coefficient pA]

For more detailed information regarding the input units, output, etc. please check the
[Catchment Description File](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/catchment.md)


<br>

> ### Greywatertank Attributevector

This vector is responsible for setting the Greywatertanks/Greywaterreservoirs properties.

	Greywatertank Attributevector = [Greywatertankvector_0, Greywatertankvector_1, ..., Greywatertankvector_n]
    
    Greywatertankvector =[Yield of Treatment, Storage Volume]

For more detailed information regarding the input units, output, etc. please check the
[Greywatertank Description File](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/greywatertank.md)

<br>

> ### Stormwaterreservoir Attributevector

This vector is responsible for setting the Stormwaterreservoirs properties.

	Stormwaterreservoir Attributevector = [Stormwaterreservoirvector_0, Stormwaterreservoirvector_1, ..., Stormwaterreservoirvector_n]
    
    Stormwaterreservoirvector =[Yield of Treatment, Storage Volume]

For more detailed information regarding the input units, output, etc. please check the
[Stormwaterreservoirs Description File](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/stormwaterreservoir.md)


<br>

> ### Rainwatertank Attributevector

This vector contains the properties of all raintanks.

	Rainwatertank Attributevector = [Rainwatertankvector_0, Rainwatertankvector_1, ..., Rainwatertankvector_n]
    
    Rainwatertankvector =[Storage Volume]

For more detailed information regarding the input units, output, etc. please check the
[Rainwatertank Description File](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/raintank.md)


<br>

> ### Building Demand Attributevector

A Buildings Water Demand depends on the number of units it consits out of. Furthermore their size (number of people occupying the unit) and use (residential, commercial). The vector needs to be set up as follows.

	Building Demand Attributevector = [Buildingdemandvector_0, Buildingdemandvector_1, ..., Buildingdemandvector_n]
    
    Buildingdemandvector = [[number of people in residential unit 1, number of people in residential unit 2, ..., number of people in residential unit n],
    						[number of people in commercial unit 1, number of people in commercial unit 2, ..., number of people in commercial unit n]]
	
    
    length(Buildingdemandvector[0]) = number of residential units in building
    
    length(Buildingdemandvector[1]) = number of commerical units in building
    
    Buildingdemandvector[0][i] = number of people in residential unit i
    
    Buildingdemandvector[1][i] = number of people in commercial unit i
    
    For example:
    
    	Building Demand Attributevector = [[[4,5,2],[2]], [[6],[0]]]
        
        The vector decribes 2 buildings. The first building consists out of 4 units. 3 residential and 1 commercial units.
        The first residential unit has 4 people living in it, the second one has 5 occupants and 2 people live in the 3rd 
        residential unit. 2 people are working in the commercial unit of the first building.
        The second building only has one unit, it's a residential unit with 6 occupants.
    

For more detailed information regarding the input, output, etc. please check the
[Demand Model Description File](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/demandmodel.md)


<br>

> ### Simulationsetup Vector

City Drain 3 need some basic information regarding the Simulation Setup. 

	Simulationsetup Vector = [Start Simulation, End Simulation, Time Step of Simulation, Path of Addons to implement]
    
	[Start Simulation] = "YYYY-MMM-DD hh:mm:ss"
	[End Simulation] = "YYYY-MMM-DD hh:mm:ss"
	[Time Step of Simulation] = "s"
	[Path of Addons to implement] = "path of file"
	
    For example:
    
    	Simulationsetup Vector = ["2000-Jan-01 00:00:00", "2001-Jan-01 00:00:00", "360", "C:/Users/Acer/Documents/GitHub/CD3Waterbalance/Module/cd3waterbalancemodules.py"]


<br>

> ### Needtohaveinputs Vector

This vector takes care of the input information for both [File Readers](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/file_reader.md) and the [Pattern Implementer](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/pattern_implementer.md). 

	Needtohaveinputs Vector = [Path of Rain File, Path of Evapotranspiration File, average Time of when the Sun is at its Zenith, average Time of Sundown]
    
	[Path of Rain File] = "path of file"
	[Path of Evapotranspiration File] = "path of file"
	[average Time of when the Sun is at its Zenith] = "h"
	[average Time of Sundown] = "h"
	
    For example:
    
    	Needtohaveinputs Vector = ["C:/Users/Acer/Documents/GitHub/CD3Waterbalance/simulationwithpatterns/inputfiles/rain.ixx", "C:/Users/Acer/Documents/GitHub/CD3Waterbalance/simulationwithpatterns/inputfiles/evapo.ixx", "13", "20.5"]

		
<br>

> ### Fileout Connection Name List

A City Drain Fileout is a built in block that creates a txt - file during the simulation. This file contains all quantity and quality information for every single time step simulated.
To be able to check any flow in detail, Fileouts can be inserted at any position desired. To insert Fileouts the XML - Creator must be run at first. 
Once the connection list has been generated, the numbers of the connections that are supposed to be checked, as well as the corresponding names, have to be written into the 
_Fileout Connection Name List_. After running the XML - Creator again the Model will be set up with the desired Fileouts.

	Fileout Connection Name List = [Fileoutvector_0, Fileoutvector_1, ..., Fileoutvector_n]
    
    Fileoutvector = [Number of Connection, Name of created Txt - File]

    For example:
    
    	Fileoutvector = [[407, 'Rain_Model.txt'],[435, 'Evapo_Model.txt']]
 

<br>


## The 5 Levels of Implementation in Detail


> ### Buildinglevel




> ### Clusterlevel




> ### Greywaterreservoirlevel




> ### Stormwaterreservoirlevel




> ### Supplylevel









        
