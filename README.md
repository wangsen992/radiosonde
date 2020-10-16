# radiosonde

General extensible radiosonde data loading, organizing and processing framework


## Description

### Rationale
Radiosonde data generally are well structured, and represents a vertical
snapshot of the atmosphere. The location of a radiosonde is based on the
vertical motion due to buoyancy and horizontal motion due to advection. Good
use of radiosonde data can provide useful information for analysis and
radiosonde data are also commonly used as input for modelling applications. 

### Key Components
* A data structure representing individual radiosonde. 
* A composite design to allow manipulation of one or multiple radiosonde in the
  same way. 
* A brdige abstraction implementing a general portal for loading radiosonde
  data from potentially different sources
* A bridge for output to required format. 
* A computation module to output desired results. 

## Note

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
