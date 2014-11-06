# Household

Basic features:

 - simulates houshold water demand by combining indoor and outdoor demand
 - differs between black water and grey water as well as potabel and nonpotable water
 
<br>

## Parameters 



| Input  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|	
| Outdoor Demand      | Time Series | [m/dt] |
| 	Bathtub | Time Series  |   [l/h] |
| Shower      | Time Series | [l/h] |
| 	Toilet | Time Series  |   [l/h] |
| Tap      | Time Series | [l/h] |
| 	Washing Machine | Time Series  |   [l/h] |
| 	Dishwasher  | Time Series  |   [l/h] |

# 

|Output  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|
|    Potable Water Demand   | Time Series |  [m³/dt]
|    Nonpotable Water Demand   |    Time Series     |  [m³/dt]  |
|    Black Water   | Time Series |  [m³/dt]
|    Grey Water    |    Time Series     |  [m³/dt]  |



<br>

## Description 

This Block uses the implemented indoor demand time series and the outdoor demand given by the catchment block to estimate the Water needed by the household as well as the wastewater produced. Furthermore the block distinguishes between potabel and nonpotable water demand as well as between produced grey water and black water.

The individual stream are calculated by simple balances:

- potable water demand consits out of Bathtub, Shower, Tap, Washing Machine, Dishwasher 
- nonpotable water demand is 

|Output Parameter  | Calculation  | 
| :------------ |:---------------:| 
|    Potable Water Demand   | Bathtub + Shower + Tap + Washing Machine + Dishwasher | 
|    Nonpotable Water Demand   |    Toilet + Outdoor Demand     | 
|    Black Water   | Toilet |  
|    Grey Water    |    Bathtub + Shower + Tap + Washing Machine + Dishwasher     | 


<br>

##Recommended Improvements

- differ between kitchen tap and bathroom tap (at the moment all tap water = grey water)
- take into account additional water losses for drinking and food preperation,...