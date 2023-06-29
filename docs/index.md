# Welcome to the FastFuels Python SDK Documentation!

## What is FastFuels?

FastFuels is a cloud-based platform for generating forest inventory data. It
uses a combination of satellite imagery and machine learning to generate
tabular tree data and voxelized 3D fuel models. These data products can be used
to support wildfire risk assessment, fire behavior modeling, and other
applications.

## What is the FastFuels Python SDK?

The FastFuels Python SDK is a Python package that provides a convenient
interface for interacting with the FastFuels API. It can be used to create and
manage FastFuels resources. It can also be used to download and process
generated data products.

## Installation

The FastFuels Python SDK can be installed using `pip` or `conda`.

### pip

```bash
pip install fastfuels-sdk
```

### conda

```bash
conda install -c conda-forge fastfuels-sdk
```

## Authentication

The FastFuels Python SDK uses API keys to authenticate requests. FastFuels is
currently in development and is not yet available to the public. If you are
interested in using FastFuels, please contact us at anthony@silvxlabs.com


## Getting Started

Users can import the FastFuels Python SDK into their Python scripts by using 
the `fastfuels_sdk` package. During import, the SDK will attempt to load the
user's API key from the `FASTFUELS_API_KEY` environment variable. If the
environment variable is not set, the user will receive an error message.

```python
import fastfuels_sdk
```

To set the API key, the user can either set the `FASTFUELS_API_KEY` environment
variable in their shell, or directly in their Python script.

### bash
```bash
FASTFUELS_API_KEY="my-api-key"
```

### Python
```python
import os
os.environ["FASTFUELS_API_KEY"] = "my-api-key"
```

The 
[`create_dataset`](reference.md#fastfuels_sdk.create_dataset) 
function is the primary entry point for creating FastFuels
resources. It can be used to create a new dataset from a geojson file, or to
retrieve an existing dataset from the FastFuels API.

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

## Issues

If you encounter any issues with the FastFuels Python SDK, please submit an
issue on the [GitHub repository](https://github.com/silvxlabs/fastfuels-sdk-python/issues).