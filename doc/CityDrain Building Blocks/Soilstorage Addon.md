# Soilstorage Addon

Basic features:

 - simulates Soil layer
 - uses potential evapotranspiration and water content to estimate actual evapotranspiration
 - calculates hydraulic conductivity as function of water content, using the Van Genuchten approach
 - generates outdoordemand using the actual evapotranspiration and a calibration factor (Outdoor Demand - Actual Evapotranspiration Ratio (OutD/ActualEvapotr))
 
 
<br>

## Parameters 

| Input  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|	
| Evapotranspiration     | Time Series | [m³/dt] |
| Infiltration     | Time Series | [m³/dt] |
| Underground_Inflow     | Time Series | [m³/dt] |
| 	Total Area | Constant  |   [m^2] |
| Total Pervious Area     | Constant  | [m^2] |
| 	Depth Of Soil | Constant  |   [m] |
| Residual Water Content | Constant | [-] |
| Saturation Water Content | Constant | [-] |
| Van Genuchten Parameter Alpha   | Constant  | [cm^-1] |
| 	Van Genuchten Parameter n | Constant  |   [-] |
| Initial Water Content | Constant | [-] |
| Hydraulic Conductivity (Saturated Conditions) | Constant | [m/d] |
| Field Capacity | Constant | [cm Water Column] |
| Outdoor Demand - Actual Evapotranspiration Ratio (OutD/ActualEvapotr) | Constant | [-] |

# 

|Output  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|
|    Actual_Evapotranspiration  | Time Series |  [m³/dt]
|    Outdoordemand  |    Time Series     |  [m/dt]  |
|    Outdoordemand_Check  |    Time Series     |  [m³/dt]  |
|    Check_Pore_Pressure  |    Time Series     |  [m³/dt]  |
|    Soilstorage_Check  |    Time Series     |  [m³/dt]  |



<br>

## Description 

This City Drain module acts like a storage unit. It's based on relations between pressure head and soil water content. 
Infiltration and garden watering equal inflows (other inflows can be specified). Evapotranspiration and seepage to lower
layers of soil equal outflows.

A more detailed description of the models used will follow.

<br>

## 
