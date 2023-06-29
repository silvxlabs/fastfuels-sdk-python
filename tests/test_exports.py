"""
Test Exports module
"""

# Internal imports
import sys

sys.path.append("../")
from fastfuels_sdk.exports import *


def test_export_zarr_to_quicfire():
    """
    Test writing a FastFuels zarr file to a QUIC-Fire .dat input file stack.
    """
    # Load the test zarr file
    test_zroot = zarr.open("test-data/test_small_fuelgrid.zip")
    canopy_group = test_zroot["canopy"]

    # Get the domain size from the zarr file
    nx = test_zroot.attrs["nx"]
    ny = test_zroot.attrs["ny"]
    nz = test_zroot.attrs["nz"]

    # Write the test zarr file to a QUIC-Fire .dat input file stack
    tmp_dir = Path("test-data/tmp")
    tmp_dir.mkdir(exist_ok=True)
    export_zarr_to_quicfire(test_zroot, tmp_dir)

    # Combine the surface and canopy bulk density arrays into a single array
    bd_array = canopy_group["bulk-density"][...]
    bd_array[..., 0] += test_zroot["surface"]["bulk-density"][...]

    # Load the treesrhof.dat file and check that the values are the
    # same as the bulk density array
    treesrhof_dat = FortranFile(tmp_dir / "treesrhof.dat", "r")
    treesrhof_array = treesrhof_dat.read_reals(dtype=np.float32)
    treesrhof_array = treesrhof_array.reshape((nz, ny, nx))
    treesrhof_array = np.moveaxis(treesrhof_array, 0, 2).astype(np.float32)
    assert np.allclose(treesrhof_array, bd_array)

    # Combine the surface and canopy FMC arrays into a single array
    fmc_array = canopy_group["FMC"][...]
    fmc_array[..., 0] = test_zroot["surface"]["FMC"][...]

    # Load the treesmoist.dat file and check that the values are the
    # same as the FMC array
    treesmoist_dat = FortranFile(tmp_dir / "treesmoist.dat", "r")
    treesmoist_array = treesmoist_dat.read_reals(dtype=np.float32)
    treesmoist_array = treesmoist_array.reshape((nz, ny, nx))
    treesmoist_array = np.moveaxis(treesmoist_array, 0, 2).astype(np.float32)
    assert np.allclose(treesmoist_array, fmc_array)

    # Combine the surface and canopy fuel depth arrays into a single array
    fd_array = np.zeros_like(canopy_group["bulk-density"][...])
    fd_array[..., 0] = test_zroot["surface"]["fuel-depth"][...]

    # Load the treesfueldepth.dat file and check that the values are the
    # same as the fuel-depth array
    treesfueldepth_dat = FortranFile(tmp_dir / "treesfueldepth.dat", "r")
    treesfueldepth_array = treesfueldepth_dat.read_reals(dtype=np.float32)
    treesfueldepth_array = treesfueldepth_array.reshape((nz, ny, nx))
    treesfueldepth_array = np.moveaxis(treesfueldepth_array, 0, 2).astype(
        np.float32)
    assert np.allclose(treesfueldepth_array, fd_array)

    # Load the topo.dat file and check that the values are the
    # same as the DEM array
    topo_dat = FortranFile(tmp_dir / "topo.dat", "r")
    topo_array = topo_dat.read_reals(dtype=np.float32)
    topo_array = topo_array.reshape((ny, nx))
    assert np.allclose(topo_array, test_zroot["surface"]["DEM"][...])


def test_export_zarr_to_duet():
    """
    Test writing a FastFuels zarr file to a Duet .dat input file stack.
    """
    # Load the test zarr file
    test_zroot = zarr.open("test-data/test_small_fuelgrid.zip")
    canopy_group = test_zroot["canopy"]

    # Get the domain size from the zarr file
    nx = test_zroot.attrs["nx"]
    ny = test_zroot.attrs["ny"]
    nz = test_zroot.attrs["nz"]
    dx = test_zroot.attrs["dx"]
    dy = test_zroot.attrs["dy"]
    dz = test_zroot.attrs["dz"]
    seed = 1234
    wind_dir = 270.0
    wind_var = 0.0
    duration = 1

    # Write the test zarr file to a Duet .dat input file stack
    tmp_dir = Path("test-data/tmp")
    tmp_dir.mkdir(exist_ok=True)
    export_zarr_to_duet(test_zroot, tmp_dir, seed=seed,
                        wind_dir=wind_dir, wind_var=wind_var,
                        duration=duration)

    # Load the treesrhof.dat file and check that the values are the
    # same as the bulk density array
    bd_array = canopy_group["bulk-density"][...]
    treesrhof_dat = FortranFile(tmp_dir / "treesrhof.dat", "r")
    treesrhof_array = treesrhof_dat.read_reals(dtype=np.float32)
    treesrhof_array = treesrhof_array.reshape((nz, ny, nx))
    treesrhof_array = np.moveaxis(treesrhof_array, 0, 2).astype(np.float32)
    assert np.allclose(treesrhof_array, bd_array)

    # Load the treesspcd.dat file and check that the values are the
    # same as the species-code array
    spcd_array = canopy_group["species-code"][...]
    treesspcd_dat = FortranFile(tmp_dir / "treesspcd.dat", "r")
    treesspcd_array = treesspcd_dat.read_ints(dtype=np.int16)
    treesspcd_array = treesspcd_array.reshape((nz, ny, nx))
    treesspcd_array = np.moveaxis(treesspcd_array, 0, 2).astype(np.int32)
    assert np.allclose(treesspcd_array, spcd_array)

    # Load the treesmoist.dat file and check that the values are the
    # same as the FMC array
    fmc_array = canopy_group["FMC"][...]
    treesmoist_dat = FortranFile(tmp_dir / "treesmoist.dat", "r")
    treesmoist_array = treesmoist_dat.read_reals(dtype=np.float32)
    treesmoist_array = treesmoist_array.reshape((nz, ny, nx))
    treesmoist_array = np.moveaxis(treesmoist_array, 0, 2).astype(np.float32)
    assert np.allclose(treesmoist_array, fmc_array)

    # Load the duet.in file and check that the values are the same as the
    # domain size and grid spacing
    duet_in = open(tmp_dir / "duet.in", "r")
    duet_in_lines = duet_in.readlines()
    assert int(duet_in_lines[0].split(" ")[0]) == nx
    assert int(duet_in_lines[1].split(" ")[0]) == ny
    assert int(duet_in_lines[2].split(" ")[0]) == nz
    assert float(duet_in_lines[3].split(" ")[0]) == dx
    assert float(duet_in_lines[4].split(" ")[0]) == dy
    assert float(duet_in_lines[5].split(" ")[0]) == dz
    assert int(duet_in_lines[6].split(" ")[0]) == seed
    assert float(duet_in_lines[7].split(" ")[0]) == wind_dir
    assert float(duet_in_lines[8].split(" ")[0]) == wind_var
    assert float(duet_in_lines[9].split(" ")[0]) == duration


def test_export_zarr_to_fds():
    # Pull in data from the test zarr file
    test_zroot = zarr.open("test-data/test_small_fuelgrid.zip")
    tmp_dir = Path("test-data/tmp")
    tmp_dir.mkdir(exist_ok=True)

    # Write the test zarr file to a FDS binary input file stack
    export_zarr_to_fds(test_zroot, tmp_dir)
