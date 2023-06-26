from fastfuels_sdk.api import FastFuelsAPI
from fastfuels_sdk.datasets import Dataset, create_dataset
from fastfuels_sdk.treelists import Treelist, create_treelist
from fastfuels_sdk.fuelgrids import Fuelgrid, create_fuelgrid
from fastfuels_sdk.exports import export_zarr_to_quicfire

# Create an instance of FastFuelsAPI
api = FastFuelsAPI()

# Make session and api_url available to other modules
SESSION = api.session
API_URL = api.api_url

__all__ = [
    "SESSION",
    "API_URL",
    "Dataset",
    "create_dataset",
    "Treelist",
    "create_treelist",
    "Fuelgrid",
    "create_fuelgrid",
    "export_zarr_to_quicfire",
]