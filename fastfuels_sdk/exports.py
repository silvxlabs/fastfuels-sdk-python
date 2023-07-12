"""
FastFuels SDK Exports Module
"""
# Core imports
from __future__ import annotations
import warnings
import importlib.resources
from pathlib import Path
from string import Template
from datetime import datetime

# External imports
import numpy as np
import zarr.hierarchy
from numpy import ndarray
from scipy.io import FortranFile

try:
    # Python 3.9+
    TEMPLATES_PATH = importlib.resources.files('fastfuels_sdk'). \
    joinpath('templates')
except AttributeError:
    # Python 3.6-3.8
    from pkg_resources import resource_filename
    TEMPLATES_PATH = resource_filename('fastfuels_sdk', 'templates')


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
        "canopy": ["bulk-density", "FMC"],
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
    _write_np_array_to_dat(bulk_density_array, "treesrhof.dat", output_dir,
                           np.float32)
    del bulk_density_array

    # Write Fuel Moisture Content (FMC) data to a .dat file
    fmc_array = canopy_group["FMC"][...]
    fmc_array[..., 0] = surface_group["FMC"][...]
    _write_np_array_to_dat(fmc_array, "treesmoist.dat", output_dir, np.float32)
    del fmc_array

    # Write fuel depth data to a .dat file
    fuel_depth_array = np.zeros_like(canopy_group["bulk-density"][...])
    fuel_depth_array[..., 0] = surface_group["fuel-depth"][...]
    _write_np_array_to_dat(fuel_depth_array, "treesfueldepth.dat", output_dir,
                           np.float32)
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
    Write a FastFuels zarr file to an FDS input file stack including the .bdf
    binary arrays representing the voxelized crown bulk density, and the FDS
    input file template containing the vegetative attributes, DEM geom, and
    domain metadata.

    Required zarr groups:
    - canopy

    Required zarr arrays:
    - canopy/bulk-density
    - canopy/SAV

    Code contributed by Eric Mueller, National Institute of Standards and
    Technology on 04/05/2022. Modified by Anthony Marcozzi to work with the new
    zarr file format.
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

    # Normalize the DEM to a minimum of 0
    dem_array = surface_group["DEM"][...]
    dem_array = np.swapaxes(dem_array, 0, 1)
    dem_array -= np.min(dem_array)

    # meshgrid of x,y,z voxel centers
    xx, yy, zz = _get_voxel_centers(nx, ny, nz, dx, dy, dz)

    # For each horizontal slice of zz adjust the z value by the DEM
    zz = _adjust_z_values_by_dem(nz, zz, dem_array, dz)

    # for each fuel type identified, create binary data file
    for sav_i, sav in enumerate(sav_classes):
        _write_binary_data_file_for_fuel_type(output_dir, canopy_group, sav,
                                              sav_data, xx, yy, zz, dx, dy, dz)

    # For each canopy fuel type write a canopy SURF, INIT, and PART block
    canopy_surf_lines, canopy_init_lines, canopy_part_lines = _generate_canopy_lines(
        sav_classes)

    # For each surface fuel type write a surface SURF block
    surface_surf_lines, surface_part_lines = _generate_surface_lines(
        sav_classes)

    # Combine the canopy and surface SURF blocks
    surf_lines = canopy_surf_lines + surface_surf_lines
    init_lines = canopy_init_lines
    part_lines = canopy_part_lines + surface_part_lines

    # Generate the geom lines
    geom_lines = _generate_geom_lines(dem_array, nx, ny, dx, dy)

    # Generate the header lines
    header_lines = _generate_header_lines(nx, ny, nz, dx, dy, dz, dem_array)

    # Write the FDS template to a text file
    fds_attrs = {
        "geom_lines": "".join(geom_lines),
        "surf_lines": "".join(surf_lines),
        "part_lines": "".join(part_lines),
        "init_lines": "".join(init_lines),
        "header_lines": "".join(header_lines)
    }
    with open(Path(TEMPLATES_PATH, "fds_input.template"), "r") as fin:
        template = Template(fin.read())
    with open(Path(output_dir, "template.fds"), "w") as fout:
        fout.write(template.substitute(fds_attrs))


def _get_voxel_centers(nx: int, ny: int, nz: int, dx: float, dy: float,
                       dz: float):
    x_vec = np.linspace(dx / 2, nx - dx / 2, nx)
    y_vec = np.linspace(dy / 2, ny - dy / 2, ny)
    z_vec = np.linspace(dz / 2, nz - dz / 2, nz)
    return np.meshgrid(x_vec, y_vec, z_vec, indexing='ij')


def _adjust_z_values_by_dem(nz: int, zz: np.array, dem_array: np.array,
                            dz: float):
    for i in range(nz):
        zval = zz[:, :, i] + dem_array
        zz[:, :, i] = np.round(zval / (dz / 2)) * (dz / 2)  # Round to dz/2
    return zz


def _write_binary_data_file_for_fuel_type(output_dir: Path,
                                          canopy_group: zarr.hierarchy.Group,
                                          sav: float, sav_data: np.array,
                                          xx: np.array, yy: np.array,
                                          zz: np.array, dx: float, dy: float,
                                          dz: float):
    output_path = output_dir / f"canopy_{int(sav)}.bdf"
    with FortranFile(output_path, 'w') as f:
        zarr_array = canopy_group['bulk-density']
        bd_data = np.array(zarr_array)
        bd_data = np.swapaxes(bd_data, 0, 1)
        bd_data = bd_data[sav_data == sav]

        xv = xx[sav_data == sav]
        yv = yy[sav_data == sav]
        zv = zz[sav_data == sav]

        vxbounds = [min(xv) - dx / 2, max(xv) + dx / 2,
                    min(yv) - dy / 2, max(yv) + dy / 2,
                    min(zv) - dz / 2, max(zv) + dz / 2]
        f.write_record(np.array(vxbounds, dtype=np.float64))

        f.write_record(np.array([dx, dy, dz], dtype=np.float64))

        nvox = bd_data.shape[0]
        f.write_record(np.array(nvox, dtype=np.int32))

        for (vxc, vyc, vzc, bd) in zip(xv, yv, zv, bd_data):
            xyz = [vxc, vyc, vzc]
            f.write_record(np.array(xyz, dtype=np.float64))
            f.write_record(np.array(bd, dtype=np.float64))


def _generate_surf_lines(sav_classes: np.array, name: str):
    surf_lines = []
    part_lines = []
    for sav in sav_classes:
        id = f"{name}_{int(sav)}"
        surf_lines.append(f"&SURF ID='surf_{id}'\n")
        surf_lines.append(f"\tSURFACE_VOLUME_RATIO={sav}\n")
        surf_lines.append(f"\tCOLOR='GREEN'\n")
        surf_lines.append(f"\tLENGTH=0.5\n")
        surf_lines.append(f"\tMOISTURE_FRACTION=0.5\n")
        surf_lines.append(f"\tGEOMETRY='CYLINDRICAL' /\n\n")

        part_lines.append(f"&PART ID='part_{id}'\n")
        part_lines.append(f"\tSURF_ID='surf_{id}'\n")
        part_lines.append(f"\tDRAG_LAW='CYLINDER'\n")
        part_lines.append(f"\tSTATIC=T\n")
        part_lines.append(f"\tQUANTITIES='PARTICLE BULK DENSITY' /\n\n")

    return surf_lines, part_lines


def _generate_canopy_lines(sav_classes: np.array):
    canopy_surf_lines, canopy_part_lines = _generate_surf_lines(sav_classes,
                                                                'canopy')

    canopy_init_lines = []
    for sav in sav_classes:
        canopy_id = f"canopy_{int(sav)}"
        canopy_init_lines.append(f"&INIT ID='init_{canopy_id}'\n")
        canopy_init_lines.append(f"\tPART_ID='part_{canopy_id}'\n")
        canopy_init_lines.append(f"\tBULK_DENSITY_FILE='{canopy_id}.bdf' /\n\n")

    return canopy_surf_lines, canopy_init_lines, canopy_part_lines


def _generate_surface_lines(sav_classes: np.array):
    surface_surf_lines, surface_part_lines = _generate_surf_lines(sav_classes,
                                                                  'surface')
    return surface_surf_lines, surface_part_lines


def _generate_geom_lines(dem_array: np.ndarray, nx: int, ny: int, dx: int,
                         dy: int) -> list[str]:
    """
    Generate geom lines from the given DEM array and attributes.
    """
    # swap axes to row-major order
    dem_array = np.swapaxes(dem_array, 0, 1)

    # copy the values in the DEM array in row-major order to zvals_list
    zvals_list = [dem_array[i, j] for i in range(ny) for j in range(nx)]

    # create the geom lines
    geom_lines = ["&GEOM ID='terrain'\n",
                  "\tSURF_ID='S1'\n",
                  f"\tIJK={nx}, {ny}, XB=0.0, {int(nx / dx)}, 0.0, "
                  f"{int(ny / dy)},\n",
                  "\tZVALS=" + ", ".join(map(str, zvals_list)) + "\n",
                  "\t/\n"]

    return geom_lines


def _generate_mesh_lines(nx: int, ny: int, nz: int, dx: int, dy: int,
                         dz: int) -> list[str]:
    """
    Generate mesh lines from given attributes.
    """
    mesh_lines = [
        f"&MESH IJK={nx}, {ny}, {nz}, XB=0.0, "
        f"{float(nx * dx)}, 0.0, "
        f"{float(ny * dy)}, 0.0, "
        f"{float(nz * dz)} /\n"
    ]
    return mesh_lines


def _generate_header_lines(nx: int, ny: int, nz: int, dx: int, dy: int, dz: int,
                           dem_array: np.ndarray) -> list[str]:
    """
    Generate header lines from given attributes.
    """
    header_lines = [
        "! FDS template generated by FastFuels Python SDK \n",
        f"! {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
        f"! Fuel domain has IJK={nx}, {ny}, {nz} \n",
        f"! Fuel domain has XB="
        f"0.0, {float(nx * dx)}, "
        f"0.0, {float(ny * dy)}, "
        f"0.0, {float(nz * dz)}\n",
        f"! Topography spans from 0.0 to {dem_array.max()}\n"
    ]
    return header_lines


def _write_np_array_to_dat(array: ndarray, dat_name: str,
                           output_dir: Path, dtype: type = np.float32) -> None:
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
