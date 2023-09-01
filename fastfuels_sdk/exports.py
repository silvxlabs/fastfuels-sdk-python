"""
FastFuels SDK Exports Module

"""
# Core imports
from __future__ import annotations
from pydoc import doc
from turtle import setundobuffer
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
import geojson
import landfire
from landfire.geospatial import get_bbox_from_polygon
import zipfile
import rasterio as rio
import rasterio.mask
from rasterio.enums import Resampling
import pandas as pd
import re


try:  # Python 3.9+
    TEMPLATES_PATH = importlib.resources.files('fastfuels_sdk').joinpath('templates')
except AttributeError:  # Python 3.6-3.8
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

def calibrate_duet(zroot: zarr.hierarchy.Group,
                   output_dir: Path | str,
                   param_dir: Path | str = None,
                   keep_duet: str = None,
                   **kwargs: float) -> None:
    """
    Calibrate the values of the surface bulk density output from DUET by changing
    the range or center and spread. Calibration can be based off of SB40-derived 
    fuel loading values from Landfire, or from user inputs of summary statistics
    of bulk density.

    Possible summary statistics:
    - Mean and standard deviation OR
    - Maximum and minimum

    These inputs may be supplied for the following fuel types:
    - Grass AND/OR
    - Litter (currently combined deciduous and coniferous) 
    OR
    - Total

    Inputs are provided in the keyword arguments. For any inputs that are not provided,
    calibration is based off of min and max values of SB40-derived fuel loads. No user
    inputs are necessary.

    The fuelgrid zarr is required to parameterize Landfire queries, with the following
    groups and arrays:

    Required zarr groups:
    - surface

    Required zarr arrays:
    - surface/bulk-density

    Parameters
    ----------
    zroot : zarr.hierarchy.Group
        The root group of the zarr file.
    output_dir : Path | str
        The output directory where DUET files are stored, 
        and where the calibrated file will be written to.
    param_dir : Path | str = None
        The directory containing the Sb40 parameters table, if
        different from output_dir. Defaults to None
    keep_duet : str
        Which fuel type should not be modified by the calibration, 
        if any. One of "grass" or "litter"
    **kwargs : float
        Keyword arguments are reserved for summary statistics
        of target values for fuel loading. Calibration is based 
        on either a mean and standard deviation OR a maximum 
        and minimum. Valid fuel types are "grass", "litter", 
        or "total". Arguements should be given in the format 
        fueltype_statistic = float (eg: litter_mean = 0.8).

    Returns
    -------
    None
        Calibrated array of DUET surface bulk density is saved to the output directory.
    
    TODO: make keep_duet boolean 
    """
    # Validate the zarr file
    required_groups = ["surface"]
    required_arrays = {
        "surface": ["bulk-density"]
    }
    _validate_zarr_file(zroot, required_groups, required_arrays)
    
    # Convert the output and SB40 parameters directories to a Path objects if they are strings
    if isinstance(output_dir, str):
        output_dir = Path(output_dir)
    if isinstance(param_dir, str):
        param_dir = Path(param_dir)

    # Get fuel type(s) from kwargs
    valid_ftypes = [["grass"],["litter"],["total"],["grass","litter"],["litter","grass"],["none"]]
    fuel_types = []
    if any([key for key in kwargs.keys() if key.startswith("total")]):
        fuel_types.append("total")
    if any([key for key in kwargs.keys() if key.startswith("grass")]):
        fuel_types.append("grass")
    if any([key for key in kwargs.keys() if key.startswith("litter")]):
        fuel_types.append("litter")
    if len(kwargs.keys()) == 0:
        fuel_types.append("none")

    # Validate the fuel types
    if fuel_types not in valid_ftypes:
        raise ValueError("calibrate_duet: Invalid fuel type in keyword arguements. Must be one of %r." % valid_ftypes)

    # Validate kwargs
    # Make sure kwargs match fuel_types
    grass_kwargs = {"grass_mean","grass_sd","grass_max","grass_min"}
    litter_kwargs = {"litter_mean","litter_sd","litter_max","litter_min"}
    total_kwargs = {"total_mean","total_sd","total_max","total_min"}
    for key in kwargs.keys():
        if fuel_types == ["grass"]:
            if key not in grass_kwargs:
                raise ValueError("calibrate_duet: Invalid keyword argument '{}'. Must be two of {}".format(key,grass_kwargs))
        elif fuel_types == ["litter"]:
            if key not in litter_kwargs:
                raise ValueError("calibrate_duet: Invalid keyword argument '{}'. Must be two of {}".format(key,litter_kwargs))
        elif fuel_types == ["total"]:
            if key not in total_kwargs:
                raise ValueError("calibrate_duet: Invalid keyword argument '{}'. Must be two of {}".format(key,total_kwargs))
    # Make sure kwarg statistics match each other (eg providing mean necessitates providing sd)
    kwarg_pairs = {"mean":"sd",
                   "sd":"mean",
                   "min":"max",
                   "max":"min"}
    for k, v in kwarg_pairs.items(): #note: this will not allow user to input different statistics for grass and litter (eg grass max/min and litter mean/sd)
        if ([key for key in kwargs.keys() if key.endswith(k)]):
            if ([key for key in kwargs.keys() if key.endswith(v)]):
                pass
            else:
                raise ValueError("calibrate_duet: Invalid keyword argument pair. *_mean and *_sd must be paired and/or *_max and *_min must be paired.")
    # Make sure kwarg statistics are given as a pair (eg mean AND sd, mean alone is not allowed)
    if len(kwargs.keys()) > 0 and len(kwargs.keys())%2 != 0:
        raise ValueError("calibrate_duet: Insufficient keyword arguments. *_mean and *_sd must be paired and/or *_max and *_min must be paired.")
    
    # Validate keep_duet argument
    valid_keep_args = ["grass","litter"]
    if keep_duet is not None:
        if keep_duet not in valid_keep_args:
            raise ValueError("calibrate_duet: Invalid fuel type in keep_duet. Must be one of %r" % valid_keep_args)
        if keep_duet in fuel_types:
            raise ValueError("calibrate_duet: Same fuel type in keyword arguments and keep_duet.")
        if fuel_types == "total":
            raise Warning("All fuel types will be calibrated when keyword argument fuel type is 'total'. Consider removing keep_duet argument. Proceeding with calibration.")
        
    # Print function specifications

    if fuel_types == ["none"]:
        grass_print = "Landfire SB40"
        litter_print = "Landfire SB40"
    elif fuel_types in [["total"],["grass","litter"],["litter","grass"]]:
        grass_print = "User inputs"
        litter_print = "User inputs"
    elif fuel_types == ["grass"]:
        grass_print = "User inputs"
        litter_print = "Landfire SB40"
    elif fuel_types == ["litter"]:
        grass_print = "Landfire SB40"
        litter_print = "User inputs"
    
    if keep_duet == "grass":
        grass_print = "Keep DUET values"
    elif keep_duet == "litter":
        litter_print = "Keep DUET values"
    
    if grass_print == "Landfire SB40":
        grass_method = "max/min"
    elif ([key for key in kwargs.keys() if key.endswith("mean") or key.endswith("sd")]):
        grass_method = "mean/sd"
    elif ([key for key in kwargs.keys() if key.endswith("max") or key.endswith("min")]):
        grass_method = "max/min"
    if litter_print == "Landfire SB40":
        litter_method = "max/min"
    elif ([key for key in kwargs.keys() if key.endswith("mean") or key.endswith("sd")]):
        litter_method = "mean/sd"
    elif ([key for key in kwargs.keys() if key.endswith("max") or key.endswith("min")]):
        litter_method = "max/min"
    
    
    print("\nCalibration Specifications:")
    print("GRASS: {} ({})".format(grass_print,grass_method))
    print("LITTER: {} ({})\n".format(litter_print,litter_method))


    # If user inputs are not present for all fuel types, use values from Landfire:
    if fuel_types == ["litter"] and keep_duet=="grass":
        pass
    elif fuel_types == ["grass"] and keep_duet=="litter":
        pass
    elif fuel_types == ["litter"] or fuel_types == ["grass"] or fuel_types == ["none"]:
        print("Querying LandFire...\n")
        # Query Landfire and return array of SB40 keys
        sb40_arr = _query_landfire(zroot, output_dir)
        # Import SB40 FBFM parameters table
        if param_dir == None:
            param_dir = output_dir
        sb40_params = pd.read_csv(Path(param_dir,"sb40_parameters.csv"))

        # Generate dict of fastfuels bulk density values and apply to Landfire query
        sb40_dict = _get_sb40_fuel_params(sb40_params)
        ftype_arr, rhof_arr = _get_sb40_arrays(sb40_arr, sb40_dict)
    
    # Read in bulk density output from DUET
    nx = zroot.attrs["nx"]
    ny = zroot.attrs["ny"]
    nz = 2 # number of duet layers, right now grass and litter. Will be number of tree species + 1
    dim = (nz,ny,nx)
    duet_rhof = _read_dat_file(output_dir, "surface_rhof.dat", dim, order="F")
    # Calibrate based on fuel_types and kwargs
    if fuel_types == ["total"]:
        duet_rhof = np.add(duet_rhof[0,:,:], duet_rhof[1,:,:])
    else:
        duet_grass = duet_rhof[0,:,:]
        duet_litter = duet_rhof[1,:,:]
    if fuel_types == ["total"]:
        if ([key for key in kwargs.keys() if key.endswith("mean") or key.endswith("sd")]):
            mean = [kwargs.get(key) for key in kwargs.keys() if key.endswith("mean")][0]
            sd = [kwargs.get(key) for key in kwargs.keys() if key.endswith("sd")][0]
            duet_calibrated = _calibrate_meansd(duet_rhof,mean,sd)
        elif ([key for key in kwargs.keys() if key.endswith("max") or key.endswith("min")]):
            max = [kwargs.get(key) for key in kwargs.keys() if key.endswith("max")][0]
            min = [kwargs.get(key) for key in kwargs.keys() if key.endswith("min")][0]
            duet_calibrated = _calibrate_maxmin(duet_rhof,max,min)
    elif fuel_types == ["litter"]:
        if ([key for key in kwargs.keys() if key.endswith("mean") or key.endswith("sd")]):
            mean = [kwargs.get(key) for key in kwargs.keys() if key.endswith("mean")][0]
            sd = [kwargs.get(key) for key in kwargs.keys() if key.endswith("sd")][0]
            litter_calibrated = _calibrate_meansd(duet_litter,mean,sd)
        elif ([key for key in kwargs.keys() if key.endswith("max") or key.endswith("min")]):
            max = [kwargs.get(key) for key in kwargs.keys() if key.endswith("max")][0]
            min = [kwargs.get(key) for key in kwargs.keys() if key.endswith("min")][0]
            litter_calibrated = _calibrate_maxmin(duet_litter,max,min)
        if keep_duet is None:
            # Use max/min from SB40 to calibrate grass values
            max = np.max(rhof_arr[ftype_arr==1])
            grass_arr = rhof_arr[ftype_arr==1]
            min = np.min(grass_arr[grass_arr>0])
            grass_calibrated = _calibrate_maxmin(duet_grass,max,min)
            # Combine calibrated grass and litter arrays
            duet_calibrated = np.add(grass_calibrated,litter_calibrated)
        else:
            # Combine calibrated litter and duet grass arrays
            duet_calibrated = np.add(duet_grass,litter_calibrated)
    elif fuel_types == ["grass"]:
        if ([key for key in kwargs.keys() if key.endswith("mean") or key.endswith("sd")]):
            mean = [kwargs.get(key) for key in kwargs.keys() if key.endswith("mean")][0]
            sd = [kwargs.get(key) for key in kwargs.keys() if key.endswith("sd")][0]
            grass_calibrated = _calibrate_meansd(duet_grass,mean,sd)
        elif ([key for key in kwargs.keys() if key.endswith("max") or key.endswith("min")]):
            max = [kwargs.get(key) for key in kwargs.keys() if key.endswith("max")][0]
            min = [kwargs.get(key) for key in kwargs.keys() if key.endswith("min")][0]
            grass_calibrated = _calibrate_maxmin(duet_grass,max,min)
        if keep_duet is None:
            # Use max/min from SB40 to calibrate grass values
            max = np.max(rhof_arr[ftype_arr==-1])
            litter_arr = rhof_arr[ftype_arr==-1]
            min = np.min(litter_arr[litter_arr>0])
            litter_calibrated = _calibrate_maxmin(duet_litter,max,min)
            # Combine calibrated grass and litter arrays
            duet_calibrated = np.add(grass_calibrated,litter_calibrated)
        else:
            # Combine duet litter and calibrated grass arrays
            duet_calibrated = np.add(grass_calibrated,duet_litter)
    elif fuel_types == ["litter","grass"] or fuel_types == ["grass","litter"]:
        if ([key for key in kwargs.keys() if key.endswith("mean") or key.endswith("sd")]):
            grass_mean = [kwargs.get(key) for key in kwargs.keys() if key == "grass_mean"][0]
            grass_sd = [kwargs.get(key) for key in kwargs.keys() if key == "grass_sd"][0]
            litter_mean = [kwargs.get(key) for key in kwargs.keys() if key == "litter_mean"][0]
            litter_sd = [kwargs.get(key) for key in kwargs.keys() if key == "litter_sd"][0]
            grass_calibrated = _calibrate_meansd(duet_grass,grass_mean,grass_sd)
            litter_calibrated = _calibrate_meansd(duet_litter,litter_mean,litter_sd)
        elif ([key for key in kwargs.keys() if key.endswith("max") or key.endswith("min")]):
            grass_max = [kwargs.get(key) for key in kwargs.keys() if key == "grass_max"][0]
            grass_min = [kwargs.get(key) for key in kwargs.keys() if key == "grass_min"][0]
            litter_max = [kwargs.get(key) for key in kwargs.keys() if key == "litter_max"][0]
            litter_min = [kwargs.get(key) for key in kwargs.keys() if key == "litter_min"][0]
            grass_calibrated = _calibrate_maxmin(duet_grass,grass_max,grass_min)
            litter_calibrated = _calibrate_maxmin(duet_litter,litter_max,litter_min)
        # Combine grass and litter arrays
        duet_calibrated = np.add(grass_calibrated,litter_calibrated)
    elif fuel_types == ["none"]:
        if keep_duet != "grass":
            # Use max/min from SB40 to calibrate grass values
            grass_max = np.max(rhof_arr[ftype_arr==1])
            grass_arr = rhof_arr[ftype_arr==1]
            grass_min = np.min(grass_arr[grass_arr>0])
            grass_calibrated = _calibrate_maxmin(duet_grass,grass_max,grass_min)
        if keep_duet != "litter":
            litter_max = np.max(rhof_arr[ftype_arr==-1])
            litter_arr = rhof_arr[ftype_arr==-1]
            litter_min = np.min(litter_arr[litter_arr>0])
            litter_calibrated = _calibrate_maxmin(duet_litter,litter_max,litter_min)
        if keep_duet == "grass":
            duet_calibrated = np.add(duet_grass,litter_calibrated)
        elif keep_duet == "litter":
            duet_calibrated = np.add(grass_calibrated,duet_litter)
        else:
            duet_calibrated = np.add(grass_calibrated,litter_calibrated)
    
    duet_calibrated = np.swapaxes(duet_calibrated,0,1) #need to to this or it doesn't match the uncalibrated duet outputs
    _write_np_array_to_dat(duet_calibrated, "surface_rhof_calibrated.dat",
                           output_dir, np.float32)
    print("Calibration Complete")


def replace_surface_fuels(zroot: zarr.hierarchy.Group,
                          duet_dir: Path | str,
                          quicfire_dir: Path | str,
                          calibrated: bool) -> None:
    """
    Replace surface fuel bulk density in quicfire output
    (from export_zarr_to_quicfire) with DUET output.

    Parameters
    ----------
    zroot: zarr.hierarchy.Group
        The root group of the zarr file.
    duet_dir: Path | str
        Directory where DUET .dat files are located.
    quicfire_dir: Path | str
        Directory where QUIO-Fire .dat files are located,
        and to where updated .dat files are written to.
    calibrated: bool
        Whether the DUET surface fuel loading has been
        calibrated using calibrate_duet.

    Returns
    -------
    None
        Modified bulk density array (treesrhof.dat) is written to the QUIC-Fire directory
    """
    duet_name = "surface_rhof_calibrated.dat" if calibrated else "surface_rhof.dat"
    nx = zroot.attrs['nx']
    ny = zroot.attrs['ny']
    nz = zroot.attrs['nz']-2 #ask about this
    qf_dim = (ny,nx,nz)
    duet_dim = (ny,nx) if calibrated else (2,ny,nx)
    qf_rhof = _read_dat_file(quicfire_dir, "treesrhof.dat", qf_dim)
    duet_rhof = _read_dat_file(duet_dir, duet_name, duet_dim, order="F")
    if calibrated == False:
        duet_rhof = np.add(duet_rhof[0,:,:],duet_rhof[1,:,:])
    qf_rhof[:,:,0] = duet_rhof
    _write_np_array_to_dat(qf_rhof, "treesrhof.dat", quicfire_dir, np.float32)


def _get_voxel_centers(nx: int, ny: int, nz: int, dx: float, dy: float,
                       dz: float):
    x_vec = np.linspace(dx / 2, nx * dx - dx / 2, nx)
    y_vec = np.linspace(dy / 2, ny * dy - dy / 2, ny)
    z_vec = np.linspace(dz / 2, nz * dz - dz / 2, nz)
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
    with FortranFile(Path(output_dir, dat_name), "w") as f:
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

def _read_dat_file(dir: Path | str,
                   filename: str,
                   arr_dim: tuple,
                   order: str = "C") -> np.array:
    """
    Read in a .dat file as a numpy array.

    Dimensions of the array must be known, and in the order (z,y,x)
    """
    # Convert the directory to a Path object if it is a string
    if isinstance(dir, str):
        dir = Path(dir)
    
    # Import and reshape .dat file
    arr =  FortranFile(Path(dir, filename),'r','uint32').read_ints('float32').T.reshape(arr_dim, order=order)
    
    return arr
    


def _query_landfire(zroot: zarr.hierarchy.Group,
                    output_dir: Path | str,
                    delete_files: bool = True) -> np.array:
    """
    Download a grid of SB40 fuel models from Landfire for the unit and convert to a numpy array

    Parameters
    ----------
    zroot : zarr.hierarchy.Group
        The root group of the zarr file.
    output_dir : Path | str
        The output directory to download Landfire data to.
    delete_files: bool = True
        Whether to delete intermediate tif files. Defaults to True

    Returns
    -------
    NumPy Array
        A numpy array of the SB40 FBFM keys for the site
    """
    
    # Name intermediate files
    temp = ["landfire_sb40.zip",
            "landfire_sb40.tif",
            "sb40_upsampled.tif",
            "sb40_cropped.tif"]

    # Create a bounding box from fuelgrid zarr
    coords = [   
            [zroot.attrs['xmin'], zroot.attrs['ymin']],
            [zroot.attrs['xmin'], zroot.attrs['ymax']],
            [zroot.attrs['xmax'], zroot.attrs['ymax']],
            [zroot.attrs['xmax'], zroot.attrs['ymin']],
            [zroot.attrs['xmin'], zroot.attrs['ymin']],
        ]
    poly = geojson.Polygon(coordinates=[coords],precision=8)
    bbox = get_bbox_from_polygon(aoi_polygon=poly, crs = 5070)

    # Download Landfire data to output directory
    lf = landfire.Landfire(bbox, output_crs = "5070")
    lf.request_data(layers = ["200F40_19"], output_path=Path(output_dir, "landfire_sb40.zip"))

    # Exctract tif from compressed download folder and rename
    with zipfile.ZipFile(Path(output_dir, "landfire_sb40.zip")) as zf:
        extension = '.tif'
        rename = 'landfire_sb40.tif'
        info = zf.infolist()
        for file in info:
            if file.filename.endswith(extension):
                file.filename = rename
                zf.extract(file, output_dir)
    
    # Upsample landfire raster to the quicfire resolution
    with rio.open(Path(output_dir, "landfire_sb40.tif")) as sb: 
        upscale_factor = 30/zroot.attrs['dx'] # lf res/qf res
        profile = sb.profile.copy()
        # resample data to target shape
        data = sb.read(
            out_shape=(
                sb.count,
                int(sb.height * upscale_factor),
                int(sb.width * upscale_factor)
            ),
            resampling=Resampling.nearest
        )
    
        # scale image transform
        transform = sb.transform * sb.transform.scale(
            (sb.width / data.shape[-1]),
            (sb.height / data.shape[-2])
        )
        profile.update({"height": data.shape[-2],
                    "width": data.shape[-1],
                   "transform": transform})
        with rio.open(Path(output_dir,"sb40_upsampled.tif"), "w", **profile) as dataset:
            dataset.write(data)
    
    # Crop the upsampled raster to the unit bounds
    with rio.open(Path(output_dir,"sb40_upsampled.tif"),"r+") as rst:
        out_image, out_transform = rasterio.mask.mask(rst,[poly],crop=True)
        out_meta = rst.meta
        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})
        with rio.open(Path(output_dir,"sb40_cropped.tif"), "w", **out_meta) as cropped:
            cropped.write(out_image)
    
    # Read in the cropped raster as a numpy array
    with rio.open(Path(output_dir,"sb40_cropped.tif")) as rst:
        arr = rst.read(1)
    
    if delete_files:
        [Path(output_dir,file).unlink() for file in temp if Path(output_dir,file).exists()]

    return arr[arr>0]
#TODO: fix rasterio cropping issue (grr) so that landfire raster is same size as fuelgrid

def _get_sb40_fuel_params(params: pd.DataFrame = None) -> dict:
    """
    Builds a dictionary of SB40 fuel parameter values and converts them to
    the official FastFuels units

    Returns:
        dict: SB40 parameters for each fuel model
    """
    # Load in the SB40 fuel parameters
    if params is not None:
        sb40_df = params.copy()
    else:
        fpath = Path("src", "data_module", "data", "sb40_parameters.csv")
        with open(fpath) as fin:
            sb40_df = pd.read_csv(fin)

    # Convert tons/ac-ft to kg/m^3
    sb40_df["1_hr_kg_per_m3"] = sb40_df["1_hr_t_per_ac"] * 0.22417
    sb40_df["10_hr_kg_per_m3"] = sb40_df["10_hr_t_per_ac"] * 0.22417
    sb40_df["100_hr_kg_per_m3"] = sb40_df["100_hr_t_per_ac"] * 0.22417
    sb40_df["live_herb_kg_per_m3"] = sb40_df["live_herb_t_per_ac"] * 0.22417
    sb40_df["live_woody_kg_per_m3"] = sb40_df["live_woody_t_per_ac"] * 0.22417

    # Convert inverse feet to meters
    sb40_df["dead_1_hr_sav_ratio_1_per_m"] = sb40_df["dead_1_hr_sav_ratio_1_per_ft"] * 3.2808
    sb40_df["live_herb_sav_ratio_1_per_m"] = sb40_df["live_herb_sav_ratio_1_per_ft"] * 3.2808
    sb40_df["live_wood_sav_ratio_1_per_m"] = sb40_df["live_wood_sav_ratio_1_per_ft"] * 3.2808

    # Convert percent to ratio
    sb40_df["dead_fuel_extinction_moisture"] /= 100

    # Convert feet to meters
    sb40_df["fuel_bed_depth_m"] = sb40_df["fuel_bed_depth_ft"] * 0.3048

    # Compute wet loading
    sb40_df["wet_load"] = sb40_df["1_hr_kg_per_m3"] + sb40_df["live_herb_kg_per_m3"]

    # Compute a live herb curing factor alpha as a function of wet loading.
    # This is kind of a B.S. approach raised by Rod on a phone call with
    # Anthony on 02/28/2023. I don't like this at all, but it is a temporary
    # Fix for the BP3D team to run some simulations.
    # low_load_fuel_models = [
    sb40_df["alpha"] = [0.5 if rho > 1 else 1.0 for rho in sb40_df["wet_load"]]

    # Compute dry loading
    sb40_df["dry_herb_load"] = sb40_df["live_herb_kg_per_m3"] * sb40_df["alpha"]
    sb40_df["dry_load"] = sb40_df["1_hr_kg_per_m3"] + sb40_df["dry_herb_load"]

    # Compute SAV
    sb40_df["sav_1hr_ratio"] = sb40_df["1_hr_kg_per_m3"] / sb40_df["dry_load"]
    sb40_df["sav_1hr"] = sb40_df["sav_1hr_ratio"] * sb40_df["dead_1_hr_sav_ratio_1_per_m"]
    sb40_df["sav_herb_ratio"] = sb40_df["dry_herb_load"] / sb40_df["dry_load"]
    sb40_df["sav_herb"] = sb40_df["sav_herb_ratio"] * sb40_df["live_herb_sav_ratio_1_per_m"]
    sb40_df["sav"] = sb40_df["sav_1hr"] + sb40_df["sav_herb"]

    # Convert nan to 0
    sb40_df.fillna(0, inplace=True)
    
    ## NIKO ADDITIONS
    # Create dictionary for assigning fuel types for DUET calibration
    duet_dict = {"NB" : 0, #0 = NEUTRAL, i.e. not predominantly grass or litter
                 "GR" : 1, #1 = GRASS predominantly
                 "GS" : 1,
                 "SH" : 1, #I am considering shrubs as grass
                 "TU" : 0,
                 "TL" : -1, #-1 = LITTER predominantly
                 "SB" : 0}
    
    # Add column to df with DUET designations
    pattern = r'[0-9]' #take out numbers from fbfm_type strings
    sb40_df["fbfm_cat"] = sb40_df["fbfm_code"].apply(lambda x: re.sub(pattern, '', x))
    sb40_df["duet_fuel_type"] = sb40_df["fbfm_cat"].apply(lambda x: duet_dict.get(x))
    ## END NIKO ADDITIONS

    # Build the dictionary with fuel parameters for the Scott and Burgan 40
    # fire behavior fuel models. Dict format: key ->
    # [name, loading (tons/ac), SAV (1/ft), ext. MC (percent), bed depth (ft)]
    # Note: Eventually we want to get rid of this and just use the dataframe.
    # This is legacy from the old parameter table json.
    sb40_dict = {}
    for key in sb40_df["key"]:
        row = sb40_df[sb40_df["key"] == key]
        sb40_dict[key] = [
            row["fbfm_code"].values[0],
            row["dry_load"].values[0],
            row["sav"].values[0],
            row["dead_fuel_extinction_moisture"].values[0],
            row["fuel_bed_depth_m"].values[0],
            row["duet_fuel_type"].values[0]
        ]

    return sb40_dict

def _get_sb40_arrays(sb40_keys: np.array, 
                     sb40_dict: dict) -> tuple:
    """
    Use a dictionary of bulk density and fuel types that correspond to SB40
    fuel models to assign those values across the study area.

    Fuel types are as follows:
    - 1: Predominantly grass. All cells with a GR, GS, or SH designation from SB40.
    - -1: Predominantly tree litter. All cells with a TL designation from SB40. 
    - 0: Neither predominantly grass or tree litter. All other SB40 designations.

    Returns:
        - np.array of fuel types
        - np.array of bulk density values as calculated by fastfuels
    """
    ftype_dict = {key:val[5] for key,val in sb40_dict.items()}
    ftype_arr = np.vectorize(ftype_dict.get)(sb40_keys)
    
    rhof_dict = {key:val[1] for key,val in sb40_dict.items()}
    rhof_arr = np.vectorize(rhof_dict.get)(sb40_keys)

    return ftype_arr, rhof_arr

def _calibrate_meansd(x: np.array,
                      mean: float | int,
                      sd: float | int) -> np.array:
    """
    Scales and shifts values in a numpy array based on an observed mean and standard deviation.
    Assumes data is normally distributed.
    """
    x1 = x[x>0]
    x2 = mean + (x1 - np.mean(x1)) * (sd/np.std(x1))
    xnew = x.copy()
    xnew[np.where(x>0)] = x2
    if np.min(xnew)<0:
        xnew = _truncate_at_0(xnew)
    return xnew

def _truncate_at_0(arr: np.array) -> np.array:
    """
    Artificially truncates data to positive values by scaling all values below the median
    to the range (0, mean), effectively "compressing" those values.
    """
    arr2 = arr.copy()
    bottom_half = arr2[arr2<np.median(arr2)]
    squeezed = (bottom_half-np.min(bottom_half))/(np.max(bottom_half)-np.min(bottom_half)) * (np.median(arr2)-0) + 0
    arr2[np.where(arr2<np.median(arr2))] = squeezed
    arr2[np.where(arr==0)] = 0
    return arr2

def _calibrate_maxmin(x: np.array,
                      max: float | int,
                      min: float | int) -> np.array:
    """
    Scales and shifts values in a numpy array based on an observed range. Does not assume
    data is normally distributed.
    """
    x1 = x[x>0]
    x2 = (x1-np.min(x1))/(np.max(x1)-np.min(x1))
    x3 = x2 * (max-min)
    x4 = x3 + min
    xnew = x.copy()
    xnew[np.where(x>0)] = x4
    return xnew