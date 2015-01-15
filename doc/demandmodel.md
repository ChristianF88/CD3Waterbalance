# Demand Model

Basic features:

 - using stochastic indoor demand model
 - makes a distinction between the different indoor uses
 
<br>

## Parameters 


| Input  | Type  |  Unit  |  Example  | Explanation |
| :------------ |:---------------:| :-----:|:-----:| :-----: |	
| Residential Vector     | Vector (String) | [-] |  [4,6] |  2 residential units, 4 occupants in the first unit and 6 occupants in the second unit  |
| 	Commercial Vector | Vector (String)  |   [-] | [0]  |  no commercial units  |


# 

| Output  | Type  |  Unit  |
| :------------ |:---------------:| :-----:|
|    Outport Bathtub   | Time Series |  [l/h]
| Outport Shower |   Time Series  |  [l/h]   |
|   Outport Kitchen Tap | Time Series |  [l/h]|
|   Outport Handbasin Tap | Time Series |  [l/h]|
|    Outport Toilet  |    Time Series     |  [l/h]  |
| Outport Dishwasher |   Time Series  |  [l/h]   |
|   Outport Evapcooler | Time Series |  [l/h]|
| Outport Washing Machine |   Time Series  |  [l/h]   |
|    Outport Check Bathtub   | Time Series |  [l/h] |
| Outport Check Shower |   Time Series  |  [l/h]   |
|   Outport Check Kitchen Tap | Time Series |  [l/h] |
|   Outport Check Handbasin Tap | Time Series |  [l/h] |
|    Outport Check Toilet  |    Time Series     |  [l/h]  |
| Outport Check Dishwasher |   Time Series  |  [l/h]   |
| Outport Check Washing Machine |   Time Series  |  [l/h]   |
| Outport Check Evapcooler |   Time Series  |  [l/h]   |



<br>

## Description 

The [stochastic demand model]() used produces, every time it is being run, diurnal demand - vectors, with a hourly time step, for each Unit in a building.
The programmed City Drain 3 (CD3) addon block sums up all those vectors (for each use seperately), so that there's eight vector for a building.
(_bathtub vector, shower vector, kitchen tap vector, handbasin tap vector, evapcooler vector, toilet vector, dishwasher vector, washing machine vector_)
The by the stochastic demand model produced added up vector have the following shape:

demand model run n: 
vector n = [demand 12 pm [l/h], demand 1 am [l/h], demand 2 am [l/h], ..., demand 11 pm [l/h]]

demand model run n+1: 
vector n+1 = [demand 12 pm [l/h], demand 1 am [l/h], demand 2 am [l/h], ..., demand 11 pm [l/h]]

A demand vector used for the calculations in CD3 consists out of two vectors given out by the stochastic model:

vector - day n = [demand 1 am [l/h] (vector n), demand 2 am [l/h] (vector n), ..., demand 11 pm [l/h] (vector n), demand 12 pm [l/h] (vector n+1)]


Depending on the simulations time step the vectors time increment is being modified.
Is the time step smaller than one hour a random event during that hour is being created.

# 

| Simulations Time Step [h] | CD3 - Calculation of Demand | 
| :------------: |:---------------:| 
| < 1     | an event is being created, randomly for some time during the hour  |
| 	1  | vector doesn't need to be modified  |
| 	24  | all digits within the vector are being added up |
| 	n (n < 24)  | n digits within the vector are being added up  |


<br>

## Recommended Improvements

- fill up evapcooler use












