## FastFuels Resources
FastFuels is a Python SDK for generating synthetic forest fuels data. The SDK
connects to a FastFuels API and communicates with it using a REST protocol.
The API defines a set of endpoints for creating and managing FastFuels data
in the form of three resources: Dataset, Treelist, and Fuelgrid. In brief,
a Dataset is a collection of spatial data, a Treelist is a collection of
trees, and a Fuelgrid is a collection of fuel cells. The SDK provides
convenience methods for creating and managing these resources.

### Dataset
A Dataset is a collection of spatial data. The spatial data is used to query
data products for generating Treelists and Fuelgrids.

Dataset resources also maintain connections to Treelist and Fuelgrid resources
that are generated from the Dataset's spatial data. This allows for easy
access to Treelist and Fuelgrid resources that are generated from the same
spatial data.


### Treelist
A Treelist is a collection of trees. Trees are populated in a Treelist by
querying the 
[TreeMap](https://www.firelab.org/project/treemap-tree-level-model-forests-united-states) 
and 
[FIA Database](https://www.fia.fs.usda.gov/library/database-documentation)
products using the spatial data from a Dataset resource. A Treelist maintains
a reference to a tabular data structure that contains information about the
trees in the Treelist. 

#### DataFrame

Trees are stored in a 
[pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html),
which is a two-dimensional, size-mutable, potentially heterogeneous tabular
data structure with labeled axes (rows and columns).
Each row in the DataFrame represents a unique tree on the landscape.
Columns of the DataFrame are as follows:

- `SPCD`: FIA Species code. This is an identifier for the species of the tree according to the Forest Inventory and Analysis (FIA) program of the U.S. Forest Service.

- `DIA_cm`: Tree Diameter at Breast Height (DBH). This is a standard forestry measurement representing the diameter of the tree's trunk at a standard height of 1.3 meters (or 4.5 feet) above ground level. In this dataset, the DBH is measured in centimeters.

- `HT_m`: Tree height. The total height of the tree, measured in meters.

- `STATUSCD`: FIA Status code. This code indicates the status of the tree (e.g., whether it's alive, dead, or has been cut down) as per the FIA's coding system.

- `CBH_m`: Tree Crown Base Height. This represents the height above ground level at which the tree's crown (branches and leaves) starts. In this dataset, the crown base height is measured in meters.

- `X_m` and `Y_m`: These are the tree's projected coordinates in meters. Projections are in the EPSG:5070 coordinate reference system, which is a standard projection for the conterminous United States.



### Fuelgrid

A Fuelgrid is a collection of 3D fuel cells. Fuelgrids are voxelized 
representations of the landscape that contain canopy and surface fuel
information for use in fire behavior models. Fuelgrids are generated using
the individual trees in a Treelist and the spatial data of a Dataset resource.
Fuelgrid canopy data comes from voxelizing the trees in a Treelist, and
surface fuel data comes from querying the 
[LANDFIRE 40 Scott and Burgan Fire Behavior Fuel Models](https://landfire.gov/fbfm40.php)
product using the spatial data from a Dataset resource.

Additionally, surface fuel data can be modified using 
[DUET](https://www.sciencedirect.com/science/article/abs/pii/S0304380023001564?via%3Dihub)
to account for the distribution of leaf litter based on tree canopy structure.
The SDK provides functionality for exporting Fuelgrid data to DUET input files.

#### Zarr

A Fuelgrid maintains a reference to a 
[zarr](https://zarr.readthedocs.io/en/stable/)
array group that contains the 3D canopy and 2D surface fuel data. The zarr array
group is organized as follows:

```
/
 ├── canopy
 │   ├── FMC; float32; Fuel moisture content, in percent
 │   ├── SAV; float32; Surface area to volume ratio, in 1/m
 │   ├── bulk-density; float32; Canopy bulk density, in kg/m^3
 │   └── species-code; uint16; FIA species code for the dominant voxel species
 └── surface
     ├── DEM; float32; Digital Elevation Model, in meters
     ├── FMC; float32; Fuel moisture content, in percent
     ├── SAV; float32; Surface area to volume ratio, in 1/m
     ├── bulk-density; float32; Surface fuel bulk density, in kg/m^3
     └── fuel-depth; float32; Surface fuel depth (or height), in meters
```

An in-depth tutorial for interacting with Fuelgrid data in the zarr format can
be found [here](https://github.com/silvxlabs/demos/blob/main/notebooks/zarr-demo.ipynb).

In addition to the above data hierarchy, zarr Fuelgrids also contain metadata
in an `attrs` dictionary. The `attrs` dictionary contains the following:

- `dx`: The x-axis resolution of the Fuelgrid, in meters
- `dy`: The y-axis resolution of the Fuelgrid, in meters
- `dz`: The z-axis resolution of the Fuelgrid, in meters
- `nx`: The number of cells in the x-axis of the Fuelgrid
- `ny`: The number of cells in the y-axis of the Fuelgrid
- `nz`: The number of cells in the z-axis of the Fuelgrid
- `pad`: The number of cells to pad the Fuelgrid with in each direction
- `xmax`: The maximum x-coordinate of the Fuelgrid, in meters
- `xmin`: The minimum x-coordinate of the Fuelgrid, in meters
- `ymax`: The maximum y-coordinate of the Fuelgrid, in meters
- `ymin`: The minimum y-coordinate of the Fuelgrid, in meters
- `zmax`: The maximum z-coordinate of the Fuelgrid, in meters
- `zmin`: The minimum z-coordinate of the Fuelgrid, in meters


The 2D affine transformation matrix is not currently stored in the 
attributes dictionary, but can be created as follows:

```python
import numpy as np

dx, dy = fuelgrid.attrs['dx'], fuelgrid.attrs['dy']
xmin, ymin = fuelgrid.attrs['xmin'], fuelgrid.attrs['ymin']

affine = np.array([[dx, 0, xmin - dx/2], 
                   [0, dy, ymin - dy/2], 
                   [0, 0, 1]])
```

Note that all spatial coordinates use the EPSG:5070 coordinate reference system.
