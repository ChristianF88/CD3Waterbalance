# XML - Creator

Basic features:

 - automated setup of an CD3 - Model
 - 5 levels of implementation

      - Building level
      -	Cluster level
      - Greywaterreservoir level
      - Stormwaterreservoir level
      - Supply level
 - selective fileout implementation for any flow
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
| Simulation Setupvector  | Header, Pythonmodule, Simulation | -  |
| Needtohaveinputs Vector  | Nodelist |  - |

<br>

| Model Outputs  | Part of XML created  | Class created | 
| :------------ |:---------------:| 	:---------------:|
| Connection Name List      | Nodelist, Connectionlist | Fileout  |





# 