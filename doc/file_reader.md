# Catchment

Basic features:

- imports time series with certain time step
- adjusts time step of file to simulation time step automatically
- gives out needed times with corresponding value

 
<br>

## Parameters 



| Input  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|	
| File      | time series | [DD.MM.YYYY HH:MM:SS value(see below)] |
| 	Filecontent | String  |  "H" for Height [mm] or "F" for Flow [l/h] |


# 

|Output   | Type  |  Unit  |
| :------------ |:---------------:| :-----:|
|  Inputdata with adjusted time step  |   time series  |  [mm] or [l/h]  |


<br>

## Description 

This file reader is able to adjust the files time step automatically to any needed for the simulation. Just select a file and set the models simulation time step as desired. The files time step length ought to be constant throughout the entire time span of simulation. By reference to the file, the set time step can either be larger, smaller or the same. Different time scales result in the necessity to calculate the corresponding values for each new point in time. The algorithms needed for the calculation of time related values (flow) differ from those needed for over time summed up values (height).


<br>

### Flow

Linear interpolation was used to calculate the new values.


Used formulas:

>![alt text](?raw=true) 

>![alt text](?raw=true) 

>![alt text](?raw=true) ... time index [-] 

>![alt text](?raw=true) ... time index [-] 

>![alt text](?raw=true) ... time from file [DD.MM.YYYY HH:MM:SS]

>![alt text](?raw=true) ... time from simulation [DD.MM.YYYY HH:MM:SS]

>![alt text](?raw=true) ... value from file [l/h]

>![alt text](?raw=true) ... value for simulation [l/h] 




<br>

###Height

For the simulation time step being larger than the files, the heights between 2 time steps are being summed up. The other way around the height will be divided by a factor consisting of the time steps relation to one another.

Used formulas:

**_tf_ < _ts_**



**_tf_ > _ts_**



>![alt text](?raw=true)


<br>

##Recommended Improvements
