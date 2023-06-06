"""
FastFuels SDK Exports Module
"""
# Core imports
import warnings
import pkg_resources
from pathlib import Path
from string import Template

# External imports
import numpy as np
import zarr.hierarchy
from numpy import ndarray
from scipy.io import FortranFile

TEMPLATES_PATH = pkg_resources.resource_filename('fastfuels_sdk', 'templates/')


def export_zarr_to_quicfire(zroot: zarr.hierarchy.Group,
                            output_dir: Path | str) -> None:
    """
    Write a FastFuels zarr file to a QUIC-Fire .dat input file stack. The
    QUIC-Fire .dat files are written to the output directory, and consists of
    the following files:
    - treesrhof.dat
    - treesmoist.dat
    - treesfueldepth.dat
    - topo.dat

    Canopy and surface data are combined into a single .dat file for each
    variable. The surface data is written to the first layer of the .dat file,
    and the canopy data is written to the remaining layers. Overlap in the first
    layer is handled differently for each attribute:
    - Bulk Density: Overlap in the first layer in the treesrhof.dat is resolved
        by summing the surface and canopy bulk density values at the first
        layer.
    - Fuel Moisture Content (FMC): Overlap in the first layer in the
        treesmoist.dat is resolved by using the surface FMC value at the first
        layer.
    - Fuel Depth: Overlap in the first layer in the treesfueldepth.dat is
        resolved by using the cell height in the layer where overlap occurs.
        This signals that the entire height of the cell is occupied with fuel.

    The .dat files require certain groups and arrays to be present in the zarr
    file. The required groups and arrays are:

    Required Groups:
    - canopy
    - surface

    Required Arrays:
    - canopy/bulk-density
    - canopy/FMC
    - surface/bulk-density
    - surface/FMC
    - surface/fuel-depth
    - surface/DEM


    Parameters
    ----------
    zroot: zarr.hierarchy.Group
        The root group of the zarr file to be exported.
    output_dir: Path | str
        The directory to write the .dat files to.

    Returns
    -------
    None
        Files are written to the output directory.
    """
    # Validate the zarr file
    required_groups = ["canopy", "surface"]
    required_arrays = {
        "canopy": ["bulk-density", "FMC", "fuel-depth"],
        "surface": ["bulk-density", "FMC", "fuel-depth", "DEM"]
    }
    _validate_zarr_file(zroot, required_groups, required_arrays)

    # Convert output_dir to a Path object if it is a string
    if isinstance(output_dir, str):
        output_dir = Path(output_dir)

    # Get the canopy and surface groups
    canopy_group = zroot["canopy"]
    surface_group = zroot["surface"]

    # Write bulk-density data to a .dat file
    bulk_density_array = canopy_group["bulk-density"][...]
    bulk_density_array[..., 0] += surface_group["bulk-density"][...]
    _write_np_array_to_dat(bulk_density_array, "treesrhof.dat", output_dir, np.float32)
    del bulk_density_array

    # Write Fuel Moisture Content (FMC) data to a .dat file
    fmc_array = canopy_group["FMC"][...]
    fmc_array[..., 0] = surface_group["FMC"][...]
    _write_np_array_to_dat(fmc_array, "treesmoist.dat", output_dir, np.float32)
    del fmc_array

    # Write fuel depth data to a .dat file
    fuel_depth_array = np.zeros_like(canopy_group["bulk-density"][...])
    fuel_depth_array[..., 0] = surface_group["fuel-depth"][...]
    _write_np_array_to_dat(fuel_depth_array, "treesfueldepth.dat", output_dir, np.float32)
    del fuel_depth_array

    # Write DEM data to a .dat file
    dem_array = surface_group["DEM"][...]
    _write_np_array_to_dat(dem_array, "topo.dat", output_dir, np.float32)


def export_zarr_to_duet(zroot: zarr.hierarchy.Group,
                        output_dir: Path | str, seed: int,
                        wind_dir: float, wind_var: float,
                        duration: int) -> None:
    """
    Write a FastFuels zarr file to a DUET .dat input file stack and DUET input
    file. The DUET input files are written to the output directory, and consists
    of the following files:
    - treesrhof.dat
    - treesmoist.dat
    - treesspcd.dat
    - duet.in

    For writing the .dat files, certain groups and arrays are required in the
    zarr file. The required groups and arrays are listed below.

    Required zarr groups:
    - canopy

    Required zarr arrays:
    - canopy/bulk-density
    - canopy/FMC
    - canopy/species-code

    Parameters
    ----------
    zroot : zarr.hierarchy.Group
        The root group of the zarr file.
    output_dir : Path | str
        The output directory to write the DUET input files to.
    seed : int
        The seed to use for the DUET simulation.
    wind_dir : float
        The wind direction to use for the DUET simulation. The wind direction
        is in degrees clockwise from north.
    wind_var : float
        The wind variability to use for the DUET simulation. The wind
        variability is in degrees clockwise from north.
    duration : int
        The duration to use for the DUET simulation. The duration is in
        years.

    Returns
    -------
    None
        DUET input files are written to the output directory.
    """
    # Validate the zarr file
    required_groups = ["canopy"]
    required_arrays = {"canopy": ["bulk-density", "FMC", "species-code"]}
    _validate_zarr_file(zroot, required_groups, required_arrays)

    # Raise a warning if a user passed duration as a float and cast to int
    if isinstance(duration, float):
        warnings.warn("The duration parameter was passed as a float. The "
                      "value was cast to an integer.")
        duration = int(duration)

    # Convert the output directory to a Path object if it is a string
    if isinstance(output_dir, str):
        output_dir = Path(output_dir)

    # Pull the canopy group from the zarr file
    canopy_group = zroot["canopy"]

    # Write the canopy bulk density to a .dat file
    canopy_bulk_density_array = canopy_group["bulk-density"][...]
    _write_np_array_to_dat(canopy_bulk_density_array, "treesrhof.dat",
                           output_dir, np.float32)
    del canopy_bulk_density_array

    # Write the spcd to a .dat file
    spcd_array = canopy_group["species-code"][...]
    _write_np_array_to_dat(spcd_array, "treesspcd.dat", output_dir, np.int16)
    del spcd_array

    # Write Fuel Moisture Content (FMC) data to a .dat file
    fmc_array = canopy_group["FMC"][...]
    _write_np_array_to_dat(fmc_array, "treesmoist.dat", output_dir, np.float32)
    del fmc_array

    # Write a duet input file
    duet_attrs = {
        "nx": zroot.attrs["nx"],
        "ny": zroot.attrs["ny"],
        "nz": zroot.attrs["nz"],
        "dx": zroot.attrs["dx"],
        "dy": zroot.attrs["dy"],
        "dz": zroot.attrs["dz"],
        "seed": seed,
        "wind_dir": wind_dir,
        "wind_var": wind_var,
        "duration": duration,
    }
    with open(Path(TEMPLATES_PATH, "duet_input.template"), "r") as fin:
        template = Template(fin.read())
    with open(Path(output_dir, "duet.in"), "w") as fout:
        fout.write(template.substitute(duet_attrs))


def export_zarr_to_fds(zroot: zarr.hierarchy.Group,
                       output_dir: Path | str) -> None:
    """
    Write a FastFuels zarr file to an FDS input file stack.

    Required zarr groups:
    - canopy

    Required zarr arrays:
    - canopy/bulk-density
    - canopy/SAV

    Code contributed by Eric Mueller, NIST on 04/05/2022. Modified by Anthony
    Marcozzi to work with the new zarr file format.
    """
    # Validate the zarr file
    required_groups = ["canopy"]
    required_arrays = {"canopy": ["bulk-density", "SAV"]}
    _validate_zarr_file(zroot, required_groups, required_arrays)

    # Convert the output directory to a Path object if it is a string
    if isinstance(output_dir, str):
        output_dir = Path(output_dir)

    # Pull the canopy and surface groups from the zarr file
    canopy_group = zroot["canopy"]
    surface_group = zroot["surface"]

    # Get the attributes from the zarr file
    dx = zroot.attrs["dx"]
    dy = zroot.attrs["dy"]
    dz = zroot.attrs["dz"]
    nx = zroot.attrs["nx"]
    ny = zroot.attrs["ny"]
    nz = zroot.attrs["nz"]

    # grab a np array from the zarr group
    zarr_array = canopy_group['SAV']
    sav_data = np.round(np.array(zarr_array))
    sav_data = np.swapaxes(sav_data, 0, 1)

    # identify unique fuel types from SAV values
    sav_classes = (np.unique(sav_data))
    sav_classes = sav_classes[sav_classes > 0]

    # meshgrid of x,y,z voxel centers
    xv = np.linspace(dx / 2, nx - dx / 2, nx)
    yv = np.linspace(dy / 2, ny - dy / 2, ny)
    zv = np.linspace(dz / 2, nz - dz / 2, nz)
    xx, yy, zz = np.meshgrid(xv, yv, zv, indexing='ij')

    # for each fuel type identified, create binary data file
    for sav_i, sav in enumerate(sav_classes):
        # Create a new file for each fuel type
        output_path = output_dir / f"foliage_part_{sav_i}.bdf"
        f = FortranFile(output_path, 'w')

        # get bulk density data from the zarr group
        zarr_array = canopy_group['bulk-density']
        bd_data = np.array(zarr_array)
        bd_data = np.swapaxes(bd_data, 0, 1)
        bd_data = bd_data[sav_data == sav]

        # voxel centers for relevant fuel class
        xv = xx[sav_data == sav]
        yv = yy[sav_data == sav]
        zv = zz[sav_data == sav]

        # write out global bounding voxel faces
        vxbounds = [min(xv) - dx / 2, max(xv) + dx / 2,
                    min(yv) - dy / 2, max(yv) + dy / 2,
                    min(zv) - dz / 2, max(zv) - dz / 2]
        f.write_record(np.array(vxbounds, dtype=np.float64))

        # write out voxel resolution
        f.write_record(np.array([dx, dy, dz],
                                dtype=np.float64))

        # number of voxels for relevant fuel class
        nvox = bd_data.shape[0]
        f.write_record(np.array(nvox, dtype=np.int32))

        # write out center and bulk density for each voxel
        for (vxc, vyc, vzc, bd) in zip(xv, yv, zv, bd_data):
            xyz = [vxc, vyc, vzc]
            f.write_record(np.array(xyz, dtype=np.float64))
            f.write_record(np.array(bd, dtype=np.float64))

        f.close()


def _write_np_array_to_dat(array: ndarray, dat_name: str,
                           output_dir: Path, dtype: type =np.float32) -> None:
    """
    Write a numpy array to a fortran binary file. Array must be cast to the
    appropriate data type before calling this function. If the array is 3D,
    the array will be reshaped from (y, x, z) to (z, y, x) for fortran.
    """
    # Reshape array from (y, x, z) to (z, y, x) (also for fortran)
    if len(array.shape) == 3:
        array = np.moveaxis(array, 2, 0).astype(dtype)
    else:
        array = array.astype(dtype)

    # Write the zarr array to a dat file with scipy FortranFile package
    f = FortranFile(Path(output_dir, dat_name), "w")
    f.write_record(array)


def _validate_zarr_file(zgroup: zarr.hierarchy.Group,
                        required_groups: list[str],
                        required_arrays: dict[str, list[str]]) -> None:
    """
    Validate the zarr file for various export functions.

    Parameters
    ----------
    zgroup
        The zarr group to validate.
    required_groups : list[str]
        A list of required groups.
    required_arrays : dict[str, list[str]]
        A dictionary of required arrays. The keys are the group names and the
        values are a list of required arrays in that group.

    Raises
    ------
    ValueError
        If the zarr file does not contain the required groups or arrays.
    """
    # Check for required groups
    for group in required_groups:
        if group not in zgroup:
            raise ValueError(f"The zarr file does not contain the required "
                             f"'{group}' group.")

    # Check for required arrays
    for group, arrays in required_arrays.items():
        for array in arrays:
            if array not in zgroup[group]:
                raise ValueError(f"The zarr file does not contain the required "
                                 f"'{array}' array in the '{group}' group.")
