## Create a Dataset

The core resource in the FastFuels SDK is the 
[Dataset](reference.md#fastfuels_sdk.Dataset). 
A Dataset contains
spatial data for generating FastFuels Treelists.

The entry point for creating a 
Dataset is the 
[`create_dataset`](reference.md#fastfuels_sdk.create_dataset) function. This

### Using a GeoJSON file

```python
import json
from fastfuels_sdk import create_dataset

# Load a geojson file
with open('path/to/geojson/file') as f:
    geojson = json.load(f)

# Create a dataset
dataset = create_dataset(name="my-dataset",
                         description="My dataset description",
                         spatial_data=geojson)
```

### Using other spatial data file formats
```python
import json
import geopandas as gpd
from fastfuels_sdk import create_dataset

# Load a spatial data file
gdf = gpd.read_file('path/to/spatial/data/file')
geojson = json.loads(gdf.to_json())

# Create a dataset
dataset = create_dataset(name="my-dataset",
                         description="My dataset description",
                         spatial_data=geojson)
```

## Create a Treelist

A [Dataset](reference.md#fastfuels_sdk.Dataset) is used to generate a 
[Treelist](reference.md#fastfuels_sdk.Treelist) object with the
[`create_treelist`](reference.md#fastfuels_sdk.datasets.Dataset.create_treelist)
method.

```python
import json
from fastfuels_sdk import create_dataset

# Load a geojson file
with open('path/to/geojson/file') as f:
    geojson = json.load(f)

# Create a dataset
dataset = create_dataset(name="my-dataset",
                         description="My dataset description",
                         spatial_data=geojson)

# Create a treelist from a dataset
treelist = dataset.create_treelist(name="my-treelist",
                                   description="My treelist description")
```

### Treelist status

The 
[`create_treelist`](reference.md#fastfuels_sdk.datasets.Dataset.create_treelist)
method is asynchronous, and will return a 
[`Treelist`](reference.md#fastfuels_sdk.Treelist)
object with a status of `Queued`. Some operations, such as downloading the
Treelist data, modifying the Treelist data, or creating a Fuelgrid require the
Treelist to be in a `Finished` status. You can check the status of a Treelist
using the `status` property.

```python
# Check the status of a treelist
print(treelist.status)
```

Additionally, you can wait for a Treelist to finish generating using the
[`wait_until_finished`](reference.md#fastfuels_sdk.treelists.Treelist.wait_until_finished)
method.

```python
# Wait for a treelist to finish generating
treelist.wait_until_finished()
```

## Download Treelist data as a CSV file

Once a Treelist has finished generating, you can download the Treelist data as
a CSV file using the 
[`download_csv`](reference.md#fastfuels_sdk.treelists.Treelist.download_csv)
method.

```python
import json
from fastfuels_sdk import create_dataset

# Load a geojson file
with open('path/to/geojson/file') as f:
    geojson = json.load(f)
    
# Create a dataset
dataset = create_dataset(name="my-dataset",
                         description="My dataset description",
                         spatial_data=geojson)

# Create a treelist from a dataset
treelist = dataset.create_treelist(name="my-treelist",
                                   description="My treelist description")

# Wait for a treelist to finish generating
treelist.wait_until_finished(verbose=True)

# Get the treelist data
df = treelist.get_data()

# Download the treelist data as a CSV file
df.to_csv('path/to/treelist.csv')
```

## Simulate a silvicultural treatment on a Treelist

Some users may want to modify Treelist data to simulate different scenarios such
as forest growth, silvicultural treatments, or natural disturbance such as 
wildfire. The FastFuels SDK supports uploading custom data to the existing 
Treelist resource. The custom data must be in the form of a DataFrame with the
following columns: 

* SPCD
* DIA_cm
* HT_m
* STATUSCD
* CBH_m
* X_m
* Y_m

The following example simulates a silvicultural treatment by removing all 
trees with a diameter at breast height (DIA_cm) less than 20.32cm (8 inches). 
The Treelist data is then uploaded to the Treelist resource using the 
[`update_data`](reference.md#fastfuels_sdk.treelists.Treelist.update_data)
method for further use in the FastFuels SDK.

```python
import json
from fastfuels_sdk import create_dataset

# Load a geojson file
with open('path/to/geojson/file') as f:
    geojson = json.load(f)

# Create a dataset
dataset = create_dataset(name="my-dataset",
                         description="My dataset description",
                         spatial_data=geojson)

# Create a treelist from a dataset
treelist = dataset.create_treelist(name="my-treelist",
                                   description="My treelist description")

# Wait for a treelist to finish generating
treelist.wait_until_finished(verbose=True)

# Get the treelist data
df = treelist.get_data()

# Remove trees with diameter less than 20.32cm (8 inches)
df = df[df['DIA_cm'] >= 20.32]

# Upload the modified treelist data
treelist.update_data(df, inplace=True)
```

## Create a Fuelgrid

[Treelist](reference.md#fastfuels_sdk.Treelist) 
objects can be used to generate a 
[Fuelgrid](reference.md#fastfuels_sdk.Fuelgrid)
, or a 3D voxelized fuel
model. The Fuelgrid is generated using the 
[`create_fuelgrid`](reference.md#fastfuels_sdk.treelists.Treelist.create_fuelgrid)
method. The Fuelgrid generation process is asynchronous, and will return a
[Fuelgrid](reference.md#fastfuels_sdk.Fuelgrid) object with a status of
`Queued`. Some operations, such as downloading the Fuelgrid data, require the
Fuelgrid to be in a `Finished` status.

```python
import json
from fastfuels_sdk import create_dataset

# Load a geojson file
with open('path/to/geojson/file') as f:
    geojson = json.load(f)

# Create a dataset
dataset = create_dataset(name="my-dataset",
                         description="My dataset description",
                         spatial_data=geojson)

# Create a treelist from a dataset
treelist = dataset.create_treelist(name="my-treelist",
                                   description="My treelist description")

# Wait for a treelist to finish generating
treelist.wait_until_finished(verbose=True)

# Create a fuelgrid from a treelist
fuelgrid = treelist.create_fuelgrid(name="my-fuelgrid",
                                    description="My fuelgrid description",
                                    distribution_method="realistic",
                                    horizontal_resolution=1,
                                    vertical_resolution=1,
                                    border_pad=0)
```

## Modify Fuelgrid data

Some users may want to modify 
[Fuelgrid](reference.md#fastfuels_sdk.Fuelgrid) 
data to simulate different scenarios
such as saw line along a road or fireline, 3D fuel treatments, or blackline
operations. 

Users should note that Fuelgrid data is stored in a compressed format, and 
cannot modify the data directly. Instead, users should download the Fuelgrid
data using the 
[`download_zarr`](reference.md#fastfuels_sdk.fuelgrids.Fuelgrid.download_zarr)
method and copy the data to a new, mutable zarr store.

```python
import zarr
import json
from fastfuels_sdk import create_dataset

# Load a geojson file
with open('path/to/geojson/file') as f:
    geojson = json.load(f)

# Create a dataset
dataset = create_dataset(name="my-dataset",
                         description="My dataset description",
                         spatial_data=geojson)

# Create a treelist from a dataset
treelist = dataset.create_treelist(name="my-treelist",
                                   description="My treelist description")

# Wait for a treelist to finish generating
treelist.wait_until_finished(verbose=True)

# Create a fuelgrid from a treelist
fuelgrid = treelist.create_fuelgrid(name="my-fuelgrid",
                                    description="My fuelgrid description",
                                    distribution_method="realistic",
                                    horizontal_resolution=1,
                                    vertical_resolution=1,
                                    border_pad=0)

# Wait for a fuelgrid to finish generating
fuelgrid.wait_until_finished(verbose=True)

# Download the Fuelgrid zarr data
fuelgrid.download_zarr('path/to/fuelgrid.zip')

# Load the immutable zarr store
zarr_immutable = zarr.open('path/to/fuelgrid.zip', mode='r')

# Create a mutable zarr store
zarr_mutable = zarr.open('path/to/fuelgrid_mutable.zarr', mode='w')

# Copy the data from the immutable zarr store to the mutable zarr store
zarr.copy_all(zarr_immutable, zarr_mutable)

# Remove canopy fuels in the saw line mask
zarr_mutable['canopy']['bulk-density'][saw_line_mask] = 0
zarr_mutable['canopy']['FMC'][saw_line_mask] = 0
zarr_mutable['canopy']['SAV'][saw_line_mask] = 0

# Remove surface fuels from the blackline operation mask
zarr_mutable['surface']['bulk-density'][blackline_mask] = 0
zarr_mutable['surface']['fuel-depth'][blackline_mask] = 0
zarr_mutable['surface']['SAV'][blackline_mask] = 0
zarr_mutable['surface']['FMC'][blackline_mask] = 0
```

## Export Voxelized Fuels to Fire Model Inputs

### QUIC-fire

```python
import zarr
import json
from fastfuels_sdk import create_dataset, export_zarr_to_quicfire

# Load a geojson file
with open('path/to/geojson/file') as f:
    geojson = json.load(f)

# Create a dataset
dataset = create_dataset(name="my-dataset",
                         description="My dataset description",
                         spatial_data=geojson)

# Create a treelist from a dataset
treelist = dataset.create_treelist(name="my-treelist",
                                   description="My treelist description")

# Wait for a treelist to finish generating
treelist.wait_until_finished(verbose=True)

# Create a fuelgrid from a treelist
fuelgrid = treelist.create_fuelgrid(name="my-fuelgrid",
                                    description="My fuelgrid description",
                                    distribution_method="realistic",
                                    horizontal_resolution=1,
                                    vertical_resolution=1,
                                    border_pad=0)

# Wait for a fuelgrid to finish generating
fuelgrid.wait_until_finished(verbose=True)

# Download the Fuelgrid zarr data
fuelgrid.download_zarr('path/to/fuelgrid.zip')

# Export the Fuelgrid zarr data to QUIC-fire inputs
zroot = zarr.open('path/to/fuelgrid.zip', mode='r')
export_zarr_to_quicfire(zroot, 'path/to/quicfire/inputs')
```