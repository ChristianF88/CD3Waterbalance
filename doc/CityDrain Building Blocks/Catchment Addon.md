# Catchment Addon

Basic features:

 - simulates the interaction between Rain and pervious, as well as impervious area
 - produces dynamic flow using the _Linear Storage Method_
 - differentiation between collected run-off and rainwater adding to the storm water drainage system can be made
 - infiltration rates estimated via _Horton Equation_
 - additional Inflows can be implemented
 - optional simplified model approach for large simulation time steps
 
<br>

## Parameters 
### Input


| Flow  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|	
| Rain      | Time Series | [mm/dt] |
| pot. Evapotranspiration      | Time Series | [mm/dt] |
| Inflow | Time Series         |    [m³/dt] |

# 

|Catchment Attributes  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|
|    Catchment Area   | Constant |  [m^2]
| Fraction of Pervious Area (pA) |   Constant  |  [-]   |
|   Fraction of Impervious Area to Reservoir (iAR)| Constant |  [-]
|    Fraction of Impervious Area to Stormwater Drain (iASD)  |    Constant     |  [-]  |
| Evaporation Factor |   Constant  |  [-]   |
| Wetting Loss |   Constant  |  [mm]   |
| Depression Loss |   Constant  |  [mm]   |
| Catchment with or without Routing |   String  |  'with' _or_ 'without'   |

# 

|Horton Method  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|
|    Initial Infiltration Capacity (Horton)   | Constant |  [m/h]
|    Final Infiltration Capacity (Horton)   |    Constant     |  [m/h]  |
| Decay Constant (Horton) |   Constant  |  [1/min]   |

# 

|Linear Storage  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|
| Linear Storage Factor Pervious Area  |   Constant  |  [s]   |
| Linear Storage Factor Impervious Area to Reservoir  |   Constant  |  [s]   |
| Linear Storage Factor Impervious Area to Stormwater Drain |   Constant  |  [s]   |

### Output 

|Flow | Type  |  Unit  |
| :------------ |:---------------:| :-----:|
| Possible Infiltration  |   Time Series  |  [m³/dt]   |
| Infiltration |   Time Series  |  [m³/dt]  |
| Runoff |   Time Series  |  [m³/dt]  |
| Collected Water|  Time Series  | [m³/dt]   |
| Gardensize |  Constant |  [m²]  |


<br>

## Description 



Runoff _R_ is being produced by rain and other inflows e.g. from another catchment. It can either be discharged into the stormwater drainage system or partly be collected in a reservoir. The quantities of water being diverted to either system can be regulated with the input parameters `Fraction of Impervious Area to Reservoir` and `Fraction of Impervious Area to Stormwater Drain`. Runoff contributing to discharged stormwater can also be produced on the pervious area, if the rain intensity is higher than the infiltration rate.

Long and short term storage _S_ has been taken under consideration. Long term storage is represented by soil infiltration and initial losses. Infiltration has been implemented using the _Horton Method_. Initial losses from floor depressions and wetting are to be set as constants (`Wetting Loss`, `Depression Loss`). For flow routing, representing short term storage, the _Linear Storage Method_ was used. 

The discharged water volumes are dependant on the catchment area. For the sake of simplicity catchments are considered squares. Their area need to be specified (`Catchment Area`). 

Depending on the chosen catchment type (with or without routing) the Routing Method will be used or not.

<br>

> ### Linear Storage Method

Runoff concentration is being simulated by the Linear Storage Method. Flow routing is peformed for all 3 types of runoff:

-	runoff of pervious areas
-	runoff of impervious area flowing to the stormwater drain
-	runoff of impervious area flowing to the reservoir

Due to the different retention properties of those areas three flow routing algorithms have been constructed, resulting in three necessary parameters instead of one.
Those parameters stand for the runoff's delay.

Used formulas:

...to come

<br>

> ### Horton Method

For estimating the soils infiltration capacity the [Horton Method](http://www.trentu.ca/iws/documents/WBA22_app-f.pdf) was used. Thereby the actual infiltration rate is limited by the possible infiltration rate. If precipitation is greater than evapotranspiration it is decreasing continuously. Whereas it is increasing when _ET_ is greater. The process of drying is simulated by the reversed Horton method.

When there's a switch of drying and wetting state the parameter ![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/possible%20infiltration%20rate%20for%20certain%20time.png?raw=true) allows for a smooth transition. The parameter takes the value of the possible infiltration calculated in the previous time step (![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/switcht%20dry%20and%20wet.png?raw=true)) and stays constant until the next switch.

Used formulas:

>![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/Horton%20equation.png?raw=true)

>![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/f_t%20start.png?raw=true) 

>![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/range%20f_t.png?raw=true) 
# 

![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/time%20index.png?raw=true)  ... time index [-]

![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/possible%20infiltration%20rate.png?raw=true) ... possible infiltrtation rate [L/T]

![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/initial%20infiltration%20rate.png?raw=true) ... initial infiltration rate [L/T]

![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/final%20infiltration%20rate.png?raw=true) ... final infiltration rate [L/T]

![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/possible%20infiltration%20rate%20for%20certain%20time.png?raw=true) ... possible infiltration rate for certain time [L/T]

![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/decay%20constant.png?raw=true) ... decay constant [1/T]



<br>

