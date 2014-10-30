# Catchment

Basic features:

 - simulates the interaction between rain, evapotranspiration and pervious, as well as impervious area
 - produces dynamic flow using the _Muskingum Method_
 - differentiation between collected run-off and rainwater adding to the storm water drainage system can be made
 - infiltration rates estimated via _Horton Equation_
 - catchment can be divided in subareas
 - estimates outdoor use of connected Households
 - additional inflows can be implemented
 
<br>

## Parameters 
### Input


| Flow  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|	
| Rain      | Time Series | [mm/dt] |
| 	Evapotranspiration | Time Series  |   [mm/dt] |
| Inflow | Time Series         |    [m³/dt] |

# 

|Catchment Attributes  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|
|    Catchment Width   | Scalar |  [m]
|    Catchment Length   |    Scalar     |  [m]  |
| Fraction of Pervious Area (pA) |   Scalar  |  [-]   |
|   Fraction of Impervious Area to Reservoir (iAR)| Scalar |  [-]
|    Fraction of Impervious Area to Stormwater Drain (iASD)  |    Scalar     |  [-]  |
| Number of Subareas |   Scalar  |  [-]   |
| Wetting Loss |   Scalar  |  [mm]   |
| Depression Loss |   Scalar  |  [mm]   |

# 

|Horton Method  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|
|    Initial Infiltration Capacity (Horton)   | Scalar |  [m/h]
|    Final Infiltration Capacity (Horton)   |    Scalar     |  [m/h]  |
| Decay Constant (Horton) |   Scalar  |  [1/min]   |

# 

|Muskingum Method  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|
| Runoff Velocity (pA)  |   Scalar  |  [m/s]   |
| Weighting Coefficient (pA) |   Scalar  |  [-]   |
| Runoff Velocity  (iAR) |   Scalar  |  [m/s]   |
| Weighting Coefficient (iAR)|   Scalar  |  [-]   |
| Runoff Velocity  (iASD) |   Scalar  |  [m/s]   |
| Weighting Coefficient (iASD)|   Scalar  |  [-]   |

### Output 

|Flow  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|
| Possible Infiltration  |   time series  |  [m³/dt]   |
| Actual Infiltration |   time series  |  [m³/dt]  |
| Runoff |   time series  |  [m³/dt]  |
| Collected Water|   time series  | [m³/dt]   |
| Outdoor Demand |   time series  |  [m³/dt]  |

<br>

## Description 


The Block is solving the general water balance equation for each time step.

>![equation](http://www.sciweavers.org/tex2img.php?eq=P%3DR%20%2B%20ET%20%2B%20%20%5Ctriangle%20S&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)

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

>	![equation](http://www.sciweavers.org/tex2img.php?eq=Q_%7Bi%7D%5E%7B%20j%2B1%7D%20%3D%20C_X%20%2A%20Q_%7Bi%7D%5E%7Bj%7D%20%2B%20C_Y%20%2A%20V_%7B%20i-1%7D%5E%7Bj%7D&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)
 
>	![equation](http://www.sciweavers.org/tex2img.php?eq=V_%7Bi%7D%5E%7B%20j%7D%20%3D%28%201%20-%20C_X%20%29%20%2A%20Q_%7Bi%7D%5E%7Bj%7D%20%2A%20%20%5Ctriangle%20t%20%2B%28%201%20-%20%20C_Y%20%2A%20%20%5Ctriangle%20t%29%20%2A%20V_%7B%20i-1%7D%5E%7Bj%7D&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)
 
>	![equation](http://www.sciweavers.org/tex2img.php?eq=C_X%20%3D%20%20%5Cfrac%7B%20%5Cfrac%7B%20%5Ctriangle%20t%7D%7B2%7D%20-%20%20%5Cfrac%7BX%2AK%7D%7BN%7D%20%7D%7B%20%5Cfrac%7B%20%5Ctriangle%20t%7D%7B2%7D%20%2B%20%20%5Cfrac%7B%281-X%29%2AK%7D%7BN%7D%7D&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)
 
>	![equation](http://www.sciweavers.org/tex2img.php?eq=C_Y%20%3D%20%20%5Cfrac%7B%201%7D%7B%20%5Cfrac%7B%20%5Ctriangle%20t%7D%7B2%7D%20%2B%20%20%5Cfrac%7B%281-X%29%2AK%7D%7BN%7D%7D&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)
 
>	![equation](http://www.sciweavers.org/tex2img.php?eq=K%3D%20%5Cfrac%7BL%7D%7Bv_R%7D&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) 
# 

![equation](http://www.sciweavers.org/tex2img.php?eq=i&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) ... time index [-]

![equation](http://www.sciweavers.org/tex2img.php?eq=j&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) ... space index [-]

![equation](http://www.sciweavers.org/tex2img.php?eq=Q%5E%7Bj%7D_%7Bi%7D&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) ... discharge [L³/T]

![equation](http://www.sciweavers.org/tex2img.php?eq=V%5E%7Bj%7D_%7Bi%7D&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) ... stored volume [L³]

![equation](http://www.sciweavers.org/tex2img.php?eq=v_R&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) ... runoff velocity [L/T]

![equation](http://www.sciweavers.org/tex2img.php?eq=C_X&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) ... muskingum coefficient [-]

![equation](http://www.sciweavers.org/tex2img.php?eq=C_Y&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) ... muskingum coefficient [1/T]

![equation](http://www.sciweavers.org/tex2img.php?eq=K&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) ... muskingum Parameter (representing delay time) [T]

![equation](http://www.sciweavers.org/tex2img.php?eq=X&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) ... muskingum Parameter (representing held back water) [-]

![equation](http://www.sciweavers.org/tex2img.php?eq=L&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) ... length the water travels [L]

![equation](http://www.sciweavers.org/tex2img.php?eq=N&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) ... number of subareas [-]

<br>

> ### Horton Method

For estimating the soils infiltration capacity the [Horton Method](http://www.trentu.ca/iws/documents/WBA22_app-f.pdf) was used. Thereby the actual infiltration rate is limited by the possible infiltration rate. If precipitation is greater than evapotranspiration it is decreasing continuously. Whereas it is increasing when _ET_ is greater. The process of drying is simulated by the reversed Horton method.

When there's a switch of drying and wetting state the parameter <img src="http://www.sciweavers.org/tex2img.php?eq=f_t%20&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0" align="center" border="0" alt="f_t " width="17" height="19" /> allows for a smooth transition. The parameter takes the value of the possible infiltration calculated in the previous time step (<img src="http://www.sciweavers.org/tex2img.php?eq=%20f_t%20%3Df_%7Bi-1%7D&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0" align="center" border="0" alt=" f_t =f_{i-1}" width="65" height="19" />) and stays constant until the next switch.

Used formulas:

>![equation](http://www.sciweavers.org/tex2img.php?eq=%20f_i%20%3D%5Cbegin%7Bcases%7Df_%20%20%5Cinfty%20%20%2B%20%28%20f_t%20%2B%20f_%20%5Cinfty%20%29%20%2A%20%20e%5E%7B-k%20%2A%20i%7D%20%26%20P%20%3E%20ET%5C%5Cf_t%20%26%20P%20%3D%20ET%20%5C%5Cf_%200%20-%20%28f_0%20-%20f_t%29%20%2A%20e%5E%7B-k%2Ai%7D%20%26%20P%20%3C%20ET%5Cend%7Bcases%7D%20&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)

>![equation](http://www.sciweavers.org/tex2img.php?eq=f_t%20%28i%3D0%29%20%3Df_0&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) 

>![equation](http://www.sciweavers.org/tex2img.php?eq=f_t%20%20%20%5Cepsilon%20%20%5D%20f_%20%5Cinfty%20%2C%20f_0%20%5D&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) 
# 

![equation](http://www.sciweavers.org/tex2img.php?eq=i&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)  ... time index [-]

![equation](http://www.sciweavers.org/tex2img.php?eq=f_i&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) ... possible infiltrtation rate [L/T]

![equation](http://www.sciweavers.org/tex2img.php?eq=f_0&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) ... initial infiltration rate [L/T]

![equation](http://www.sciweavers.org/tex2img.php?eq=f_%5Cinfty&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) ... final infiltration rate [L/T]

![equation](http://www.sciweavers.org/tex2img.php?eq=f_t&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) ... possible infiltration rate for certain time [L/T]

![equation](http://www.sciweavers.org/tex2img.php?eq=k&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0) ... decay constant [1/T]

<br>

##Recommended Improvements
