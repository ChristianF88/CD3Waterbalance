# Demand Model

Basic features:

 - 
 
<br>

## Parameters 
### Input


| Input  | Type  |  Unit  |  Example  | Explanation |
| :------------ |:---------------:| :-----:|:-----:| :-----: |	
| Residential Vector     | Vector | [-] |  [4,6] |  2 residential units, 4 occupants in the first unit and 6 occupants in the second unit  |
| 	Commercial Vector | Vector  |   [-] | [0]  |  no commercial units  |


# 

| Output  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|
|    Outport Bathtub   | Time Series |  [l/h]
| Outport Shower |   Time Series  |  [l/h]   |
|   Outport Tap | Time Series |  [l/h]
|    Outport Toilet  |    Time Series     |  [l/h]  |
| Outport Dishwasher |   Time Series  |  [l/h]   |
| Outport Washing Machine |   Time Series  |  [l/h]   |
|    Outport Check Bathtub   | Time Series |  [l/h]
| Outport Check Shower |   Time Series  |  [l/h]   |
|   Outport Check Tap | Time Series |  [l/h]
|    Outport Check Toilet  |    Time Series     |  [l/h]  |
| Outport Check Dishwasher |   Time Series  |  [l/h]   |
| Outport Check Washing Machine |   Time Series  |  [l/h]   |



<br>

## Description 


The Block is solving the general water balance equation for each time step.

>![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/water%20balance%20equation.png?raw=true)

Runoff _R_ is being produced by rain and other inflows e.g. from another Catchment. It can either be discharged into the stormwater drainage system or partly be collected in a reservoir. The Quantities of Water being diverted to either system can be regulated with the input parameters `Fraction of Impervious Area to Reservoir` and `Fraction of Impervious Area to Stormwater Drain`. Runoff contributing to discharged stormwater can also be produced on the pervious Area, if the rain intensity is higher than the infiltration rate.

Long and short term storage _S_ has been taken under consideration. Long term storage is represented by soil infiltration and initial losses. Infiltration has been implemented using the _Horton Method_. Initial losses from floor depressions and wetting are to be set as constants (`Wetting Loss`, `Depression Loss`). For flow routing, representing short term storage, the _Muskingum Method_ was used. 

The outdoor water demand of a Household connected to a catchment is being considered originating mainly from garden watering. Therefore it's estimated via the relation between evapotranspiration _ET_ and rain _P_. If precipitation is higher than or equal to evapotranspiration there's no demand. For evaportranspiration being greater, the outdoor water demand is equal to their difference.

The discharged water volumes are dependant on the catchment area. For the sake of simplicity catchments are considered squares. Their dimensions need to be specified (`Catchment Width`, `Catchment Length`). 

<br>

> ### Muskingum Method

Runoff concentration is being simulated by the [Muskingum Method](http://ponce.sdsu.edu/eonvideo/enghydro091_raw.html). The approach used is simplified. A detailed description of the simplification can be found [here](http://www.uibk.ac.at/umwelttechnik/teaching/phd/diss_achleitner.pdf). Flow routing is peformed for all 3 types of runoff:

-	runoff of pervious areas
-	runoff of impervious area flowing to the stormwater drain
-	runoff of impervious area flowing to the reservoir

Due to the different retention properties of those areas three flow routing algorithms have been constructed, resulting in 6 necessary parameters instead of two.

Used formulas:

>	![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/discrete%20Muskingum%20equation%201.png?raw=true)
 
>	![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/discrete%20Muskingum%20equation%202.png?raw=true)
 
>	![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/discrete%20Muskingum%20coefficient%20equation%201.png?raw=true)
 
>	![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/discrete%20Muskingum%20coefficient%20equation%202.png?raw=true) 
 
>	![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/Muskingum%20parameter%20equation.png?raw=true) 
# 

![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/time%20index.png?raw=true) ... time index [-]

![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/space%20index.png?raw=true) ... space index [-]

![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/discharge.png?raw=true) ... discharge [L³/T]

![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/stored%20volume.png?raw=true) ... stored volume [L³]

![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/runoff%20velocity.png?raw=true) ... runoff velocity [L/T]

![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/Muskingum%20coefficient%201.png?raw=true) ... muskingum coefficient [-]

![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/Muskingum%20coefficient%202.png?raw=true) ... muskingum coefficient [1/T]

![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/Muskingum%20parameter%201.png?raw=true) ... muskingum Parameter (representing delay time) [T]

![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/Muskingum%20parameter%202.png?raw=true) ... muskingum Parameter (representing held back water) [-]

![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/length.png?raw=true) ... length the water travels [L]

![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/Formulas/Number%20of%20subareas.png?raw=true) ... number of subareas [-]

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

## Recommended Improvements

- add additional outdoor use (washing car, swimming pool,...)
- create dynamics for garden use