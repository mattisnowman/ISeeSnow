# ISeeSnow - model intercomparison pilot-study

The ISeeSnow project aims to initiate an intercomparison project for avalanche
simulation tools. We want to start a conversation among the modelling community
with a pilot study comparing results from mainly thickness-(depth-) integrated models
based on a Voellmy friction relation. 

To keep it simple, we exclude any model verification tests that might require a
more complex model setup. We also exclude model validation tests that
potentially include model optimization.

So the focus is on standard simulations with prescribed friction parameters for
two different topographies: an idealized topography and a real-world example. 

We ask the participating groups to employ their default configuration with a
Voellmy friction relation for these simulations. The friction parameters mu,
xsi and the release thickness are set to be the same for all. As a third test
case, a simulation run with purely Coulomb friction should be performed for 
the idealized topography. If the respective model configuration is not designed
to use a friction relation with only Coulomb frition, we ask the participants to 
set the xsi value in the Voellmy friction relation to an extremely high value, 
forcing the effect of the turbulent friction term to be negligible. 

The AvaFrame-team will provide input data and parameter values for the two test
cases and compare the gathered simulation results. The analysis is performed
using the functionalities of the [ana3AIMEC](https://docs.avaframe.org/en/latest/moduleAna3AIMEC.html) and
[ana4Stats](https://docs.avaframe.org/en/latest/moduleAna4Stats.html) modules of
[AvaFrame](https://docs.avaframe.org/en/latest/index.html). 



## How to participate in ISeeSnow?

There are two different options: 

1. The minimum requirement is to perform one simulation per test case (two in total) and provide the 
  result datasets as described below. 

2. However, there is also the option to use the **runISeeSnowTest.py** script. This script offers the options to: 1) create the idealized topography and release area scenario, 2) fetch input data and provide paths to the respective files, 3) call a computational module to perform the simulations and 4) perform [ana3AIMEC](https://docs.avaframe.org/en/latest/moduleAna3AIMEC.html) analysis of the simulation results. These four steps can also be performed individually, so for example only the aimec analysis for the simulation results. The configuration of all employed modules can be found in **ISeeSnowCfgIdealizedTopo.ini**, **ISeeSnowCfgRealTopo.ini** or **ISeeSnowCfgCoulombOnly.ini**. The test case can be chosen in the very beginning of the script (line 25) and also if a call to the computational module shall be performed. It is set up to call the *comMod* specified in line 27 - exemplary for [com1DFA](https://docs.avaframe.org/en/latest/moduleCom1DFA.html)- but you are invited to include a call to your model here. Note on aimec analysis: if NO aimecDir path is provided in line 28, aimec will check for simulation results in avaName/Outputs/comMod/peakFiles - if you just want to run the aimec analysis on your simulation results - just provide the path to the results in the parameter aimecDir in line 28 of the script. The aimec analysis requires a [thalweg](https://docs.avaframe.org/en/latest/glossary.html#term-thalweg) and a splitPoint (shape files) in the inputs, these are also provided alongside the model input data. Running the **runISeeSnowTest.py** script requires an [*AvaFrame* installation](https://docs.avaframe.org/en/latest/advancedUsage.html#advanced-script-installation).

In the following, information on provided model input data and required format
of result datasets is given:

### Model input data:

The input data comprises a digital elevation model (DEM) (regularly spaced points with a spatial resolution of 5 meters) and a release area scenario per test case. The release area is provided as shape file OR alternatively as release thickness field .asc file. The .asc file has the same extent and spatial resolution as the DEM and provides the actual values of release thickness at each cell (values different from zero give the release thickness, whereas areas outside of the prescribed release polygon are represented by values of 0). Note on release thickness .asc file: The .asc files in the **Inputs/RELTH** directories are created based on the DEM and the release polygon read from the corresponding shape file. In the resulting raster, cells are set to belong to the release area as soon as there is an intersection with the release polygon. For this reason, the area of the release thickness field exceeds the area of the release polygon.

* digital elevation model as .asc file (format: https://desktop.arcgis.com/en/arcmap/10.3/manage-data/raster-and-images/esri-ascii-raster-format.htm) with a spatial resolution of 5 meters
	* testCase IdealizedTopo: **DEM_HS_Topo.asc**
	* testCase RealTopo: **realDEM.asc**
 	* testCase CoulombOnly: **DEM_HS_Topo.asc**
* release area scenario as shapefile with release area feature (polygon), homogeneous release thickness througout release area
	* testCase IdealizedTopo: **REL/release1HS.shp**
	* testCase RealTopo: **REL/realWog.shp**
 	* testCase CoulombOnly: **REL/release1HS.shp**
* release area scenario as asc file with release area feature thickness, homogeneous release thickness througout release area, covering the DEM extent and a spatial resolution of 5 meters
	* testCase IdealizedTopo: **RELTH/release1HSField5m.asc**
	* testCase RealTopo: **RELTH/realWogField5m.asc**
 	* testCase CoulombOnly: **RELTH/release1HSField5m.asc**	 
* friction parameter text file with values for mu and xsi, as well as release
  thickness value (see description of Voellmy-type friction relation for
  example here:
  https://docs.avaframe.org/en/latest/theoryCom1DFA.html#voellmy-friction-model)

#### IdealizedTopo
![test case IdealizedTopo](/images/releaseScenario_release1HS_01com1DFA_C_null_dfa.png)


#### RealTopo
![test case RealTopo](/images/releaseScenario_relWog_02com1DFA_C_null_dfa.png)


#### CoulombOnly
![test case CoulombOnly](/images/releaseScenario_release1HS_03com1DFA_C_null_dfa.png)

The corresponding files can be found in the directory **data**, where **avaIdealizedTopo** refers to the idealized test case, **avaRealTopo** represents the real-world topography and **avaCoulombOnly** provides the same topography and release area scenario as in the case of the idealizedTopo test case, but should be run with purely Coulomb friction. For all three test cases,
the DEM (*DEM_HS_Topo.asc* and *avaWog.asc*, respectively) is located in the directory **Inputs**, the release area shapefile in **Inputs/REL** and the release area thickness field in **Inputs/RELTH**. The friction parameter
values, can be found in *frictionParameterValues.csv*. Data source info for avaRealTopo can be found [here](https://docs.avaframe.org/en/latest/dataSources.html#data-sources).

### Result datasets: 

We ask all the participating groups to perform a simulation for the two test
cases, and to provide the following result datasets: 

* fields of peak flow velocity and peak flow thickness .asc file covering the
  entire computational domain (DEM extent), where peak refers to the maximum
  flow variable value over the entire duration of the simulation. The peak
  fields should have a spatial resolution of 5 meters and the same extent of
  the DEM - hence the .asc files should have the same header as the provided
  dem file. We require a specific naming of the peak field .asc files:
  *releaseAreaScenario_simulationID_simType_modelType_resltType.asc*, from now on
  referred to *A_B_C_D_E.asc*, where:
  	- A - *releaseAreaScenario*: refers to the name of the release shape file
	- B - *simType*: refers to null (no entrainment, no resistance)
	- C - *simulationID*: needs to be unique for the respective simulation and include the test case (01 for idealizedTopo, 02 for realTopo and 03 for coulombOnly) and name of your model, so e.g. 01com1DFA, 02com1DFA and 03com1DFA
	- D - *modelType*: can be any descriptive string of the employed model (here dfa for dense flow avalanche)
	- E - *result type*: is pft (peak flow thickness) and pfv (peak flow velocity)
  Basically, items A, B, C and E need to be set according to the test cases, where for D
  you can set any name.

  Note: underscores are not allowed except to separate the
  four elements of the file name and no data values should be provided as nans.
* a csv file with information on simulation duration, computational time, total
  volume at initial time step and also final time step, spatial resolution
  (example: *simulationResultTable.csv*) - one file listing the valus of all simulations
* a text file with information on model configuration, i.e. parameter values,
  numerical configuration, model version etc. Naming should be consistent with
  the peak field files: *releaseAreaScenario_simulationID_simType_modelType.txt*.
  These configuration files can optionally be also provided as [.ini files](https://docs.python.org/3/library/configparser.html#supported-ini-file-structure),
  to be interpreted by [configparser](https://docs.python.org/3/library/configparser.html#module-configparser). 

**Note:** the spatial resolution of the model input data is 5 meters (regular
grid) and the result fields are required to also have a spatial resolution of 5
meters. However, this applies to the submitted result fields, the simulations
can be performed using your default numerical setup (also if using a different
spatial resolution), but they need to be submitted as rasters with a cell size
of 5 meters.

All the listed result files should be provided as a .tar/.zip file containing
the simulationResultTable with one line per simulation, and 
one subdirectory per avalanche test case: **avaIdealizedTopo**,
**avaRealTopo** and **avaCoulombOnly** each of them providing the respective peak fields of flow
velocity and flow thickness and the model configuration file. 

All the csv files are setup so that they can directly be converted to a [pandas
DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html),
which is helpful for further postprocessing.

In addition, we ask the participating groups to already provide a paragraph
describing their simulation tool, e.g. mathematical model, numerical methods,
configuration, code availability and a reference. This should be added as a
simple .txt file in the .tar/.zip archive together with the result datasets. 

An example of all the required result files can be found in the directory 
**exampleOutputs**.


## Provide your own test case

We invite you to provide further even test cases that can be used in a potential
continuation or future intercomparison projects. We will collect these and publish
them as an open dataset (properly attributed, citeable), hopefully building a test
dataset that benefits the whole community. 
The miminum requirements for an event test case is: 

* release area scenario
* release thickness 
* documented runout line

  


