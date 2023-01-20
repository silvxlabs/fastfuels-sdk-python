"""
Test Exports module
"""

# Internal imports
import sys
sys.path.append("../")
from fastfuels_sdk.exports import *


def test_write_zarr_file_to_quicfire():
    """
    Test writing a FastFuels zarr file to a QUIC-Fire .dat input file stack.
    """
    # Load the test zarr file
    test_zroot = zarr.open("test-data/test_fuelgrid.zip")

    # Get the domain size from the zarr file
    nx = test_zroot.attrs["nx"]
    ny = test_zroot.attrs["ny"]
    nz = test_zroot.attrs["nz"]

    # Add an FMC array to the canopy group. All values should be 1.5 where the
    # canopy is present and 0.0 where the canopy is absent.
    canopy_group = test_zroot["canopy"]
    canopy_group["FMC"][...] = np.where(canopy_group["bulk-density"][...] > 0.0, 1.5, 0.0)

    # Write the test zarr file to a QUIC-Fire .dat input file stack
    write_zarr_file_to_quicfire(test_zroot, "test-data")

    # Combine the surface and canopy bulk density arrays into a single array
    bd_array = canopy_group["bulk-density"][...]
    bd_array[..., 0] += test_zroot["surface"]["bulk-density"][...]

    # Load the treesrhof.dat file and check that the values are the
    # same as the bulk density array
    treesrhof_dat = FortranFile("test-data/treesrhof.dat", "r")
    treesrhof_array = treesrhof_dat.read_reals(dtype=np.float32)
    treesrhof_array = treesrhof_array.reshape((nz, ny, nx))
    treesrhof_array = np.moveaxis(treesrhof_array, 0, 2).astype(np.float32)
    assert np.allclose(treesrhof_array, bd_array)

    # Combine the surface and canopy FMC arrays into a single array
    fmc_array = canopy_group["FMC"][...]
    fmc_array[..., 0] = test_zroot["surface"]["FMC"][...]

    # Load the treesmoist.dat file and check that the values are the
    # same as the FMC array
    treesmoist_dat = FortranFile("test-data/treesmoist.dat", "r")
    treesmoist_array = treesmoist_dat.read_reals(dtype=np.float32)
    treesmoist_array = treesmoist_array.reshape((nz, ny, nx))
    treesmoist_array = np.moveaxis(treesmoist_array, 0, 2).astype(np.float32)
    assert np.allclose(treesmoist_array, fmc_array)

    # Combine the surface and canopy fuel depth arrays into a single array
    fd_array = np.zeros_like(canopy_group["bulk-density"][...])
    fd_array[..., 0] = test_zroot["surface"]["fuel-depth"][...]

    # Load the treesfueldepth.dat file and check that the values are the
    # same as the fuel-depth array
    treesfueldepth_dat = FortranFile("test-data/treesfueldepth.dat", "r")
    treesfueldepth_array = treesfueldepth_dat.read_reals(dtype=np.float32)
    treesfueldepth_array = treesfueldepth_array.reshape((nz, ny, nx))
    treesfueldepth_array = np.moveaxis(treesfueldepth_array, 0, 2).astype(np.float32)
    assert np.allclose(treesfueldepth_array, fd_array)

    # Load the topo.dat file and check that the values are the
    # same as the DEM array
    topo_dat = FortranFile("test-data/topo.dat", "r")
    topo_array = topo_dat.read_reals(dtype=np.float32)
    topo_array = topo_array.reshape((ny, nx))
    assert np.allclose(topo_array, test_zroot["surface"]["DEM"][...])
