

# Greywatertank

Basic features:

 - simulates simple storage unit for Rainwater
 - storage size can be specified
 
<br>

## Parameters 



| Input  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|	
| Collected Water      | Time Series | _any_ |
| 	Non_Potable_Demand | Time Series  |   _any_ |
| 	Storage Volume | Constant  |   [m^3] |


# 

|Output  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|
|    Current Volume  | Time Series |  _same as input_ |
|    Additional Demand |    Time Series     |  _same as input_  |




<br>

## Description 

This module collects and stores Rainwater. If the tanks specified volume is exceeded inflowing water is given to the Overflow, thereby being added to the Stormwaterdrain or Stormwaterreservoir (if present).


<br>



