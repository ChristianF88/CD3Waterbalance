# User Guide

This text is supposed to give a short introduction for working with City Drain 3 using especially for the DAnCE4Water designed Python Addons. A detailled description to the City Drain software can be found [here](http://www.uibk.ac.at/umwelttechnik/teaching/phd/diss_achleitner.pdf).

To be able to simulate urban water cycles in City Drain a few additonal modules were programmed.
The folder _City Drain Building Blocks_  contains all addons programmed. Depending on how many modules are being used a the complexity of the built water system reaches from simple to very compley. The following table shows the programmed modules and their function.

|Module|Function|
|:----:|:-----:|
|[Building Addon](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/CityDrain%20Building%20Blocks/Building%20Addon.md)| splits up water demand in potable and nonpotable demand and the produced water in greywater and blackwater |
|[Catchment Addon](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/CityDrain%20Building%20Blocks/Catchment%20Addon.md)| generates runoff form impervious area, infiltration on pervious area, outdoor water demand |
|[Collector Addon](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/CityDrain%20Building%20Blocks/Collector%20Addon.md)| adds up a number of streams to one stream (pipe function) |
|[Demand Model Addon](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/CityDrain%20Building%20Blocks/Demand%20Model%20Addon.md)| generates indoor water demand for buildings |
|[Distributor Addon](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/CityDrain%20Building%20Blocks/Distributor%20Addon.md)| splits up one signal into many signals |
|[File Reader Addon](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/CityDrain%20Building%20Blocks/File%20Reader%20Addon.md)| reads data out of a file (ixx, csv or txt) and passes it on |
|[Garden Watering Addon](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/CityDrain%20Building%20Blocks/Garden%20Watering%20Addon.md)| generates garden watering events |
|[Greywater Reservoir Addon](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/CityDrain%20Building%20Blocks/Greywater%20Reservoir%20Addon.md)| stores greywater for nonpotabel demand |
|[Greywater Tank Addon](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/CityDrain%20Building%20Blocks/Greywater%20Tank%20Addon.md)| stores greywater for nonpotabel demand |
|[Pattern Implementer Addon](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/CityDrain%20Building%20Blocks/Pattern%20Implementer%20Addon.md)| creates a normal distributed evapotranspiration pattern from constant data |
| [Rainwater Tank Addon](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/CityDrain%20Building%20Blocks/Rainwater%20Tank%20Addon.md)| stores rainwater for nonpotabel demand |
| [Sewer, Stromdrain, Potable Water Reservoir Addon](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/CityDrain%20Building%20Blocks/Sewer%2C%20Stormdrain%20and%20Potable%20Water%20Reservoir%20Addon.md.md)| end of the line modules that state where water ends up |
|[Stormwater Reservoir Addon](https://github.com/ChristianF88/CD3Waterbalance/blob/master/doc/CityDrain%20Building%20Blocks/Stormwaterreservoir%20Addon.md)| stores stormwater for nonpotabel demand |



