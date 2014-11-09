# Household

Basic features:

 - simulates household water demand by combining indoor and outdoor demand
 - differs between black water and grey water as well as potable and non potable water
 
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
|    Potable Water  | Time Series |  [m³/dt]
|    Non Potable Water |    Time Series     |  [m³/dt]  |
|    Black Water   | Time Series |  [m³/dt]
|    Grey Water    |    Time Series     |  [m³/dt]  |



<br>

## Description 

This Block uses the implemented indoor demand time series and the outdoor demand given by the catchment block to estimate the Water needed by the household as well as the waste water produced. Furthermore the block distinguishes between potable and non potable water demand as well as between produced grey water and black water.

The individual stream are calculated by simple balances:

- potable water demand consist out of Bathtub, Shower, Tap, Washing Machine, Dishwasher 
- non potable water demand is 

|Output Parameter  | Calculation  | 
| :------------ |:---------------:| 
|    Potable Water    | Bathtub + Shower + Tap + Washing Machine + Dishwasher | 
|    Non Potable Water   |    Toilet + Outdoor Demand     | 
|    Black Water   | Toilet |  
|    Grey Water    |    Bathtub + Shower + Tap + Washing Machine + Dishwasher     | 


<br>

## Recommended Improvements

- differ between kitchen tap and bathroom tap (at the moment all tap water = grey water)
- take into account additional water losses for drinking and food preperation,...