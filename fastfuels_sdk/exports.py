"""
FastFuels SDK Exports Module
"""

# Core imports
from pathlib import Path

# External imports
import numpy as np
import zarr.hierarchy
from numpy import ndarray
from scipy.io import FortranFile


def write_zarr_to_quicfire(zroot: zarr.hierarchy.Group,
                                output_dir: Path | str) -> None:
    """
    Write a FastFuels zarr file to a QUIC-Fire .dat input file stack.

    Parameters
    ----------
    zroot
    output_dir

    Returns
    -------

    """
    if isinstance(output_dir, str):
        output_dir = Path(output_dir)
    # if not output_dir.is_dir():
    #     raise ValueError("Output directory must be a directory.")

    try:
        canopy_group = zroot["canopy"]
        surface_group = zroot["surface"]
    except KeyError:
        raise ValueError("The zarr file does not contain the required "
                         "'surface' and 'canopy' groups.")

    # Write bulk-density data to a .dat file
    bulk_density_array = canopy_group["bulk-density"][...]
    bulk_density_array[..., 0] += surface_group["bulk-density"][...]
    write_np_array_to_dat(bulk_density_array, "treesrhof.dat", output_dir)
    del bulk_density_array

    # Write Fuel Moisture Content (FMC) data to a .dat file
    fmc_array = canopy_group["FMC"][...]
    fmc_array[..., 0] = surface_group["FMC"][...]
    write_np_array_to_dat(fmc_array, "treesmoist.dat", output_dir)
    del fmc_array

    # Write fuel depth data to a .dat file
    fuel_depth_array = np.zeros_like(canopy_group["bulk-density"][...])
    fuel_depth_array[..., 0] = surface_group["fuel-depth"][...]
    write_np_array_to_dat(fuel_depth_array, "treesfueldepth.dat",
                          output_dir)
    del fuel_depth_array

    # Write DEM data to a .dat file
    dem_array = surface_group["DEM"][...]
    write_np_array_to_dat(dem_array, "topo.dat", output_dir)


def write_np_array_to_dat(array: ndarray, dat_name: str,
                          output_dir: Path) -> None:
    """
    Write a numpy array to a 32-bit float fortran binary file.

    Parameters
    ----------
    array
    dat_name
    output_dir

    Returns
    -------

    """
    # Cast the data to 32-bit Float for Fortran
    if len(array.shape) == 2:
        data = np.array(array, dtype=np.float32)
    else:
        # Reshape array from (y, x, z) to (z, y, x) (also for fortran)
        data = np.moveaxis(array, 2, 0).astype(np.float32)

    # Write the zarr array to a dat file with scipy FortranFile package
    f = FortranFile(Path(output_dir, dat_name), "w", "uint32")
    f.write_record(data)
