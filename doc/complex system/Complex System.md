# Complex System

Included BLocks:

 - 8 x File Reader
 - 1 x Pattern Implementer
 - 8 x Distributor
 - 9 x Collector
 - 5 x Catchment
 - 5 x Household
 - 3 x Raintank
 - 1 x Grey Water Tank
 - 1 x Stormwater Drain
 - 1 x Sewer
 - 1 x Potable Water Reservoir
 - 12 x Fileout
 
<br>

## Settings of Blocks 


#### File Reader #1

| Variable  |  Value  |
| :------------ |:---------------:|
|   Inputfile   |  Evapotr. | 
|  Inputtype 	 |  H (Height) | 

# 

#### File Reader #2

| Variable  |  Value  |
| :------------ |:---------------:|
|   Inputfile   |  Rain | 
|  Inputtype 	 |  H (Height) | 


# 

#### File Reader #3

| Variable  |  Value  |
| :------------ |:---------------:|
|   Inputfile   |  Bath | 
|  Inputtype 	 |  F (Flow) | 


# 

#### File Reader #4

| Variable  |  Value  |
| :------------ |:---------------:|
|   Inputfile   |  Dishwasher | 
|  Inputtype 	 |  F (Flow)  | 

#  

#### File Reader #5

| Variable  |  Value  |
| :------------ |:---------------:|
|   Inputfile   |  Shower | 
|  Inputtype 	 |  F (Flow)  | 

# 

#### File Reader #6

| Variable  |  Value  |
| :------------ |:---------------:|
|   Inputfile   |  Toilet | 
|  Inputtype 	 |  F (Flow)  | 
# 

#### File Reader #7

| Variable  |  Value  |
| :------------ |:---------------:|
|   Inputfile   |  Tap | 
|  Inputtype 	 |  F (Flow)  | 

# 

#### File Reader #8

| Variable  |  Value  |
| :------------ |:---------------:|
|   Inputfile   |  Washing Machine | 
|  Inputtype 	 |  F (Flow)  | 


# 

#### Pattern Implementer #1

| Variable  |  Value  |
| :------------ |:---------------:|
|   Zenith [0-23 h]   |  13 | 
|  Sundown [0-23 h]	 | 20.5 | 

# 

#### Distributor #1 - #8

| Variable  |  Value  |
| :------------ |:---------------:|
|   Number of Outports   |  5 | 


# 

#### Collector #1, #2, #9

| Variable  |  Value  |
| :------------ |:---------------:|
|   Number of Inports   |  2 | 

# 

#### Collector #5, #7

| Variable  |  Value  |
| :------------ |:---------------:|
|   Number of Inports   |  5 | 

# 

#### Collector #3, #4

| Variable  |  Value  |
| :------------ |:---------------:|
|   Number of Inports   |  6 | 

#  

#### Collector #6

| Variable  |  Value  |
| :------------ |:---------------:|
|   Number of Inports   |  4 | 

#  

#### Collector #8

| Variable  |  Value  |
| :------------ |:---------------:|
|   Number of Inports   |  3 | 

#  

#### Catchment #1

| Variable  |  Value  |
| :------------ |:---------------:|
|   Length [m]   |  33 | 
|   Width [m]   |  14.7 | 
|   Decay Constant [1/min]   |  1.9 | 
|   Depression Loss [mm]  |  1.5 | 
|   Final Infiltration Capacity [m/h]   |  0.21 | 
|   Fraction of Impervious Area to Reservoir (iAR) [-]  |  0.63 | 
|   Fraction of Impervious Area to Stormwater Drain (iASD) [-]  |  0.19 | 
|   Fraction of Pervious Area (pA) [-]  |  0.18 | 
|   Initial Infiltration Capacity [m/h]  |  0.6 | 
|   Number of Subareas [-]  |  2 | 
|   Wetting Loss [mm]  |  0.39 | 
|   Runoff Velocity iAR [m/s]  |  0.04 | 
|   Weighting Coefficient iAR [-]  |  0.04 | 
|   Runoff Velocity iASD [m/s]  |  0.03 | 
|   Weighting Coefficient iASD [-]  |  0.05 | 
|   Runoff Velocity pA [m/s]  |  0.02 | 
|   Weighting Coefficient pA [-]  |  0.06 | 

#  

#### Catchment #2

| Variable  |  Value  |
| :------------ |:---------------:|
|   Length [m]   |  27 | 
|   Width [m]   |  31.7 | 
|   Decay Constant [1/min]   |  1.8 | 
|   Depression Loss [mm]  |  1.5 | 
|   Final Infiltration Capacity [m/h]   |  0.27 | 
|   Fraction of Impervious Area to Reservoir (iAR) [-]  |  0.43 | 
|   Fraction of Impervious Area to Stormwater Drain (iASD) [-]  |  0.29 | 
|   Fraction of Pervious Area (pA) [-]  |  0.28 | 
|   Initial Infiltration Capacity [m/h]  |  0.8 | 
|   Number of Subareas [-]  |  1 | 
|   Wetting Loss [mm]  |  0.4 | 
|   Runoff Velocity iAR [m/s]  |  0.07 | 
|   Weighting Coefficient iAR [-]  |  0.06 | 
|   Runoff Velocity iASD [m/s]  |  0.06 | 
|   Weighting Coefficient iASD [-]  |  0.05 | 
|   Runoff Velocity pA [m/s]  |  0.03 | 
|   Weighting Coefficient pA [-]  |  0.06 | 

#   

#### Catchment #3

| Variable  |  Value  |
| :------------ |:---------------:|
|   Length [m]   |  50 | 
|   Width [m]   |  16 | 
|   Decay Constant [1/min]   |  1.9 | 
|   Depression Loss [mm]  |  1.0 | 
|   Final Infiltration Capacity [m/h]   |  0.21 | 
|   Fraction of Impervious Area to Reservoir (iAR) [-]  |  0.30 | 
|   Fraction of Impervious Area to Stormwater Drain (iASD) [-]  |  0.60 | 
|   Fraction of Pervious Area (pA) [-]  |  0.10 | 
|   Initial Infiltration Capacity [m/h]  |  0.6 | 
|   Number of Subareas [-]  |  2 | 
|   Wetting Loss [mm]  |  0.3 | 
|   Runoff Velocity iAR [m/s]  |  0.07 | 
|   Weighting Coefficient iAR [-]  |  0.04 | 
|   Runoff Velocity iASD [m/s]  |  0.06 | 
|   Weighting Coefficient iASD [-]  |  0.05 | 
|   Runoff Velocity pA [m/s]  |  0.04 | 
|   Weighting Coefficient pA [-]  |  0.06 |

# 

#### Catchment #4

| Variable  |  Value  |
| :------------ |:---------------:|
|   Length [m]   |  20 | 
|   Width [m]   |  48 | 
|   Decay Constant [1/min]   |  1.9 | 
|   Depression Loss [mm]  |  1.5 | 
|   Final Infiltration Capacity [m/h]   |  0.21 | 
|   Fraction of Impervious Area to Reservoir (iAR) [-]  |  0.45 | 
|   Fraction of Impervious Area to Stormwater Drain (iASD) [-]  |  0.09 | 
|   Fraction of Pervious Area (pA) [-]  |  0.46 | 
|   Initial Infiltration Capacity [m/h]  |  0.6 | 
|   Number of Subareas [-]  |  1 | 
|   Wetting Loss [mm]  |  0.39 | 
|   Runoff Velocity iAR [m/s]  |  0.08 | 
|   Weighting Coefficient iAR [-]  |  0.04 | 
|   Runoff Velocity iASD [m/s]  |  0.06 | 
|   Weighting Coefficient iASD [-]  |  0.05 | 
|   Runoff Velocity pA [m/s]  |  0.04 | 
|   Weighting Coefficient pA [-]  |  0.06 |

# 

#### Catchment #5

| Variable  |  Value  |
| :------------ |:---------------:|
|   Length [m]   |  30 | 
|   Width [m]   |  40 | 
|   Decay Constant [1/min]   |  1.9 | 
|   Depression Loss [mm]  |  1.5 | 
|   Final Infiltration Capacity [m/h]   |  0.21 | 
|   Fraction of Impervious Area to Reservoir (iAR) [-]  |  0.0 | 
|   Fraction of Impervious Area to Stormwater Drain (iASD) [-]  |  1.0 | 
|   Fraction of Pervious Area (pA) [-]  |  0.0 | 
|   Initial Infiltration Capacity [m/h]  |  0.6 | 
|   Number of Subareas [-]  |  2 | 
|   Wetting Loss [mm]  |  0.39 | 
|   Runoff Velocity iAR [m/s]  |  0.03 | 
|   Weighting Coefficient iAR [-]  |  0.04 | 
|   Runoff Velocity iASD [m/s]  |  0.021 | 
|   Weighting Coefficient iASD [-]  |  0.05 | 
|   Runoff Velocity pA [m/s]  |  0.008 | 
|   Weighting Coefficient pA [-]  |  0.06 | 

# 
#### Raintank #1

| Variable  |  Value  |
| :------------ |:---------------:|
|   Storage Volume [m³]   |  5 | 

#  

#### Raintank #2

| Variable  |  Value  |
| :------------ |:---------------:|
|   Storage Volume [m³]   |  20 |

#  

#### Raintank #3

| Variable  |  Value  |
| :------------ |:---------------:|
|   Storage Volume [m³]   |  10 |

#  

#### Greywatertank #1

| Variable  |  Value  |
| :------------ |:---------------:|
|   Yield of Treatment [-]   |  0.9 |



<br>

## Layout Scheme


>![alt text](https://raw.githubusercontent.com/ChristianF88/CD3Waterbalance/master/doc/complex%20system/path4459.png?raw=true)

<br>

## Fileouts

Connected to: 

-	Raintanks
-	Greywatertank
- 	Potable Water Reservoir

<br>

## Ports

| Block  | Number of Blocks | Connected [in, out] | Possible [in, out] |
| :------------ |:---------------:|:---------------:|:---------------:|
|     File Reader|8|  1 [0, 1] |  1 [0, 1] |
|  Pattern Implementer|1|  2 [1, 1] |  2 [1, 1] |
|  Distributor|8 | 6 [1, 5] |  6 [1, 5] |
|  Catchment|5 | 6 [2, 4] |  8 [3, 5] |
|  Collector| 8| a+1 [a, 1] |  a+1 [a, 1] | a(C1, C2, C3, C4, C5, C6, C7, C8, C9) = {2, 2, 6, 6, 5, 4, 5, 3, 2}
| Household| 5| 11 [7, 4]|  11 [7, 4] | 
|  Raintank|3 | 5 [2, 3] |  5 [2, 3] |
|  Grey Water Tank|1 | 5 [2, 3] |  5 [2, 3] |
|  Stormwater Drain| 1| 2 [1, 1] |  2 [1, 1] |
|  Sewer| 1 |2 [1, 1] |  2 [1, 1] |
| Potable Water Reservoir   | 1| 3 [2, 1] |  3 [2, 1] |
| Fileout   | 12 | a+b [a, b] |  2 [1, 1] | a(Fo1 - Fo7, Fo8 - Fo12) = {[1, 0], [1, 1]}

# 

Number of Links = [ Sum( Connected (i) * Number of Blocks ) ] / 2 = 113 

<br>

## Thoughts

- Check max time step for stability of muskingum




<br>










































