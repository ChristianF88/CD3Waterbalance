# Building

Basic features:

 - simulates household water demand by combining indoor and outdoor demand
 - differs between black water and grey water as well as potable and non potable water
 
<br>

## Parameters 



| Input  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|	
| Outdoor Demand      | Time Series | [m³/dt] |
| 	Bathtub | Time Series  |   [m³/dt] |
| Shower      | Time Series | [m³/dt] |
| 	Toilet | Time Series  |   [m³/dt] |
| Kitchen Tap      | Time Series | [m³/dt] |
| Handbasin Tap      | Time Series | [m³/dt] |
| 	Washing Machine | Time Series  |   [m³/dt] |
| 	Dishwasher  | Time Series  |   [m³/dt] |
| 	Evapcooler  | Time Series  |   [m³/dt] |

# 

|Output  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|
|    Potable Water  | Time Series |  [m³/dt]
|    Non Potable Water |    Time Series     |  [m³/dt]  |
|    Black Water   | Time Series |  [m³/dt]
|    Grey Water    |    Time Series     |  [m³/dt]  |



<br>

## Description 

This Block uses the implemented indoor demand time series and the outdoor demand given by the catchment block to estimate the Water needed by the household as well as the waste water produced. Furthermore the block distinguishes between potable and non potable water demand as well as between produced grey water and black water.

The individual stream are calculated by simple balances:

|Output Parameter  | Calculation  | 
| :------------ |:---------------:| 
|    Potable Water    | Bathtub + Shower + Kitchen Tap + Handbasin Tap + Washing Machine + Dishwasher + Evapcooler | 
|    Non Potable Water   |    Toilet + Outdoor Demand     | 
|    Black Water   | Toilet + Kitchen Tap |  
|    Grey Water    |    Bathtub + Handbasin Tap + Shower + Tap + Washing Machine + Dishwasher + Evapcooler    | 


<br>

## Recommended Improvements

- enable water use selection for evap cooler as well as a factor that rules the input-output-ratio
- take into account additional water losses for drinking, sweating, food preperation,...