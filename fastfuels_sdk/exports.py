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
import warnings


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


class DuetCalibrator:
    #TODO: Instead of saving just the most recent array to self.calibrated_array, append to a list or a dict of calibrated arrays, so that you can access a bunch without reading in dat files
    def __init__(self, zroot, output_dir, param_dir=None):
        self.zroot = zroot
        self.output_dir = Path(output_dir)
        self.param_dir = Path(param_dir) if param_dir else None
        self.calibrated = False
        self.calibrated_array = None
        self.calibrated_fuel_type = []
        self.calibration_method = []
        self.saved_files = []
        self.original_duet_array = self._read_original_duet()
        self.duet_dict = self._get_input_array()
            
    def calibrate_max_min(self,
                          fuel_type: str | list,
                          max_val: float | list,
                          min_val: float | list) -> None:
        """
        Calibrate the values of the surface bulk density output from DUET by setting the
        range (maximum and minimum).

        Parameters
        ----------

        fuel_type : str | list
            Fuel type(s) to calibrate. May be one of "total", "grass", or "litter" given 
            as a string, or both "grass" and "litter" given as a list. When "total", both
            fuel types are calibrated based on one set of inputs. When "litter" or "grass",
            the given fuel type is calibrated, the other is left unchanged and added to the 
            calibrated fuel type to produce the final array. When ["grass","litter"] or 
            ["litter","grass"] both fuel types are calibrated based on their respective inputs.
        
        max_val : float | list
            Target maximim value for calibration. If multiple values are given for multiple fuel
            types, the position of each value in the list must match the position of their
            corresponding fuel type.
        
        min_val : float | list
            Target minimum value for calibration. If multiple values are given for multiple 
            fuel types, the position of each value in the list must match the position of their
            corresponding fuel type.
            
        Returns
        -------
        None
            Calibrated array of DUET surface bulk density is saved to the output directory.
            Filename indicates the fuel type and the max/min calibration method, and is 
            incremented if previous calibrations of the same fuel type and method have been
            conducted.

        """
        self._validate_inputs(fuel_type,max_val,min_val)
        if isinstance(fuel_type, str):
            fuel_type = [fuel_type]
        if isinstance(max_val, int) or isinstance(max_val, float):
            max_val = [max_val]
        if isinstance(min_val, int) or isinstance(min_val, float):
            min_val = [min_val]
        calibrated = {}
        for f in range(len(fuel_type)):
            arr = self.duet_dict[fuel_type[f]]
            calibrated[fuel_type[f]] = self._maxmin_calibration(arr, max_val[f], min_val[f])
        self.calibrated_array = self._combine_fuel_types(calibrated_dict = calibrated)
        self.calibrated = True
        self.calibrated_fuel_type.append(fuel_type)
        self.calibrated_fuel_type = self._flatten(self.calibrated_fuel_type)
        self.calibration_method.append("maxmin")
        self.duet_dict = self._get_input_array()


    def calibrate_mean_sd(self,
                            fuel_type: str | list,
                            mean_val: float | list,
                            sd_val: float | list) -> None:
        """
        Calibrate the values of the surface bulk density output from DUET by setting the
        center and spread (mean and standard deviation).

        Parameters
        ----------

        fuel_type : str | list
            Fuel type(s) to calibrate. May be one of "total", "grass", or "litter" given 
            as a string, or both "grass" and "litter" given as a list. When "total", both
            fuel types are calibrated based on one set of inputs. When "litter" or "grass",
            the given fuel type is calibrated, the other is left unchanged and added to the 
            calibrated fuel type to produce the final array. When ["grass","litter"] or 
            ["litter","grass"] both fuel types are calibrated based on their respective inputs.
        
        mean_val : float | list
            Target mean value for calibration. If multiple values are given for multiple fuel
            types, the position of each value in the list must match the position of their
            corresponding fuel type.
        
        sd_val : float | list
            Target standard deviation for calibration. If multiple values are given for multiple 
            fuel types, the position of each value in the list must match the position of their
            corresponding fuel type.
        
        Returns
        -------
        None
            Calibrated array of DUET surface bulk density is saved to the output directory.
            Filename indicates the fuel type and the max/min calibration method, and is 
            incremented if previous calibrations of the same fuel type and method have been
            conducted.

        """
        self._validate_inputs(fuel_type,mean_val,sd_val)
        if isinstance(fuel_type, str):
            fuel_type = [fuel_type]
        if isinstance(mean_val, int) or isinstance(mean_val, float):
            mean_val = [mean_val]
        if isinstance(sd_val, int) or isinstance(sd_val, float):
            sd_val = [sd_val]
        calibrated = {}
        for f in range(len(fuel_type)):
            arr = self.duet_dict[fuel_type[f]]
            calibrated[fuel_type[f]] = self._meansd_calibration(arr, mean_val[f], sd_val[f])
        self.calibrated_array = self._combine_fuel_types(calibrated_dict = calibrated)
        self.calibrated = True
        self.calibrated_fuel_type.append(fuel_type)
        self.calibrated_fuel_type = self._flatten(self.calibrated_fuel_type)
        self.calibration_method.append("meansd")
        self.duet_dict = self._get_input_array()

    
    def calibrate_with_sb40(self,
                            fuel_type: str | list) -> None:
        self._validate_inputs(fuel_type)
        print("Querying LandFire...\n")
        # Query Landfire and return array of SB40 keys
        sb40_arr = self._query_landfire()
        # Import SB40 FBFM parameters table
        param_dir = self.output_dir if self.param_dir == None else self.param_dir
        sb40_params = pd.read_csv(Path(param_dir,"sb40_parameters.csv"))
        # Generate dict of fastfuels bulk density values and apply to Landfire query
        sb40_dict = self._get_sb40_fuel_params(sb40_params)
        sb40_ftype, sb40_rhof = self._get_sb40_arrays(sb40_arr, sb40_dict)
        if isinstance(fuel_type, str):
            fuel_type = [fuel_type]
        calibrated = {}
        for f in fuel_type:
            if f == "grass":
                max_val = np.max(sb40_rhof[sb40_ftype==1])
                grass_arr = sb40_rhof[sb40_ftype==1]
                min_val = np.min(grass_arr[grass_arr>0])
            elif f == "litter":
                max_val = np.max(sb40_rhof[sb40_ftype==-1])
                litter_arr = sb40_rhof[sb40_ftype==-1]
                min_val = np.min(litter_arr[litter_arr>0])
            else:
                max_val = np.max(sb40_rhof)
                min_val = np.min(sb40_rhof[sb40_rhof>0])
            calibrated[f] = self._maxmin_calibration(self.duet_dict[f], max_val, min_val)
        self.calibrated_array = self._combine_fuel_types(calibrated_dict = calibrated)
        self.calibrated = True
        self.calibrated_fuel_type.append(fuel_type)
        self.calibrated_fuel_type = self._flatten(self.calibrated_fuel_type)
        self.calibration_method.append("sb40")
        self.duet_dict = self._get_input_array()


    def revert_to_original_duet(self, 
                                delete_files: bool = False) -> None:
        """
        Ensure that the next calibration will be conducted on the original DUET output and
        optionally delete all files saved from previous calibrations of the DuetCalibrator
        instance.

        Parameters
        ----------

        delete_files : bool
            Whether to delete the previously saved .dat files. Default is False, 
            meaning files will not be deleted and any subsequent calibrations of the 
            same method and fuel type will be saved with incremented filenames.
        
        """
        if delete_files:
            [Path(self.output_dir,self.saved_files[file]).unlink() for file in range(len(self.saved_files)) if Path(self.output_dir,self.saved_files[file]).exists()]
            self.saved_files = []
        self.calibrated = False
        self.calibrated_array = None
        self.calibrated_fuel_type = []
        self.calibration_method = []
        self.original_duet_array = self._read_original_duet()
        self.duet_dict = self._get_input_array()

    def to_file(self) -> None:
        """
        Write the most recently calibrated surface fuel array to a .dat file.
        File will be saved to the output directory of the DuetCalibrator instance.
        """
        if self.calibrated:
            arr_name = self._name_calibrated_file()
            _write_np_array_to_dat(self.calibrated_array, arr_name, self.output_dir)
            self.saved_files.append(arr_name)
        else:
            raise Exception("Must calibrate array before writing to file.")
    

    def replace_quicfire_surface_fuels(self):
        """
        Replace surface fuel bulk density in quicfire output
        (from export_zarr_to_quicfire) with DUET output.

        Parameters
        ----------
        quicfire_dir: Path | str
            Directory where QUIO-Fire .dat files are located,
            and to where updated .dat files are written to.

        Returns
        -------
        None
            Modified bulk density array (treesrhof.dat) is written to the QUIC-Fire directory
        """
        nx = self.zroot.attrs['nx']
        ny = self.zroot.attrs['ny']
        nz = self.zroot.attrs['nz']
        qf_dim = (ny,nx,nz)
        with open(Path(self.output_dir, "treesrhof.dat"), "rb") as fin:
            qf_arr = FortranFile(fin).read_reals(dtype="float32").reshape((nz, ny, nx), order = "C")
        if self.calibrated:
            tag = "calibrated"
            duet_arr = np.add(self.calibrated_array[0,:,:],self.calibrated_array[1,:,:])
        else:
            tag = "unmodified"
            duet_arr = np.add(self.original_duet_array[0,:,:],self.original_duet_array[1,:,:])
        qf_arr[0,:,:] = duet_arr
        _write_np_array_to_dat(qf_arr, "treesrhof.dat", self.output_dir, np.float32, reshape = False)
        print("Replaced FastFuels surface fuel layer with {} DUET surface fuels".format(tag))

    def _validate_inputs(self, fuel_type, val1=None, val2=None):
        # Validate fuel types
        valid_ftypes = ['litter','grass','total',['litter','grass'],['grass','litter']]
        if fuel_type not in valid_ftypes:
            raise ValueError("Invalid fuel type. Must be one of {}.".format(valid_ftypes))
        if fuel_type == "total" and self.calibrated == True:
            raise ValueError("Invalide fuel type: 'total' fuel calibration cannot be applied to a previously calibrated array. Choose a different fuel type or use revert_to_original_duet() before calibrating total fuels.")
        if fuel_type in self.calibrated_fuel_type:
            warnings.warn("Fuel type '{}' already calibrated. Replacing previous calibrated values.".format(fuel_type))

        # Validate fuel summary arguments
        if val1 is not None:
            if isinstance(fuel_type, list):
                if not isinstance(val1, list) or not isinstance(val2, list):
                    raise TypeError("Fuel input values must be provided as a list when fuel_type is a list.")
                if len(fuel_type) != len(val1) | len(val2):
                    raise ValueError("Number of fuel value inputs must match number of fuel types ({} fuel inputs for fuel_type = {}).".format(len(fuel_type), fuel_type))
            

    def _maxmin_calibration(self,
                            x: np.array,
                            max_val: float | int,
                            min_val: float | int) -> np.array:
        """
        Scales and shifts values in a numpy array based on an observed range. Does not assume
        data is normally distributed.
        """
        x1 = x[x>0]
        x2 = (x1-np.min(x1))/(np.max(x1)-np.min(x1))
        x3 = x2 * (max_val-min_val)
        x4 = x3 + min_val
        xnew = x.copy()
        xnew[np.where(x>0)] = x4
        return xnew
    

    def _meansd_calibration(self,
                            x: np.array,
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
            xnew = self._truncate_at_0(xnew)
        return xnew
    
    def _truncate_at_0(self, arr: np.array) -> np.array:
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


    def _query_landfire(self,
                        delete_files: bool = True) -> np.array:
        """
        Download a grid of SB40 fuel models from Landfire for the unit and convert to a numpy array

        Parameters
        ----------
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
                [self.zroot.attrs['xmin'], self.zroot.attrs['ymin']],
                [self.zroot.attrs['xmin'], self.zroot.attrs['ymax']],
                [self.zroot.attrs['xmax'], self.zroot.attrs['ymax']],
                [self.zroot.attrs['xmax'], self.zroot.attrs['ymin']],
                [self.zroot.attrs['xmin'], self.zroot.attrs['ymin']],
            ]
        poly = geojson.Polygon(coordinates=[coords],precision=8)
        bbox = get_bbox_from_polygon(aoi_polygon=poly, crs = 5070)

        # Download Landfire data to output directory
        lf = landfire.Landfire(bbox, output_crs = "5070")
        lf.request_data(layers = ["200F40_19"], output_path=Path(self.output_dir, "landfire_sb40.zip"))

        # Exctract tif from compressed download folder and rename
        with zipfile.ZipFile(Path(self.output_dir, "landfire_sb40.zip")) as zf:
            extension = '.tif'
            rename = 'landfire_sb40.tif'
            info = zf.infolist()
            for file in info:
                if file.filename.endswith(extension):
                    file.filename = rename
                    zf.extract(file, self.output_dir)
        
        # Upsample landfire raster to the quicfire resolution
        with rio.open(Path(self.output_dir, "landfire_sb40.tif")) as sb: 
            upscale_factor = 30/self.zroot.attrs['dx'] # lf res/qf res
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
            with rio.open(Path(self.output_dir,"sb40_upsampled.tif"), "w", **profile) as dataset:
                dataset.write(data)
        
        # Crop the upsampled raster to the unit bounds
        with rio.open(Path(self.output_dir,"sb40_upsampled.tif"),"r+") as rst:
            out_image, out_transform = rasterio.mask.mask(rst,[poly],crop=True)
            out_meta = rst.meta
            out_meta.update({"driver": "GTiff",
                            "height": out_image.shape[1],
                            "width": out_image.shape[2],
                            "transform": out_transform})
            with rio.open(Path(self.output_dir,"sb40_cropped.tif"), "w", **out_meta) as cropped:
                cropped.write(out_image)
        
        # Read in the cropped raster as a numpy array
        with rio.open(Path(self.output_dir,"sb40_cropped.tif")) as rst:
            arr = rst.read(1)
        
        if delete_files:
            [Path(self.output_dir,file).unlink() for file in temp if Path(self.output_dir,file).exists()]

        return arr[arr>0]
    #TODO: fix rasterio cropping issue (grr) so that landfire raster is same size as fuelgrid

    def _get_sb40_fuel_params(self, params: pd.DataFrame = None) -> dict:
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

    def _get_sb40_arrays(self,
                         sb40_keys: np.array, 
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

    def _combine_fuel_types(self, 
                            calibrated_dict) -> np.array:
        calibrated_duet = np.zeros((2,self.zroot.attrs["ny"],self.zroot.attrs["nx"]))
        if len(calibrated_dict.keys()) == 1:
            ftype = list(calibrated_dict.keys())[0]
            if ftype == "grass":
                calibrated_duet[0,:,:] = calibrated_dict["grass"]
                calibrated_duet[1,:,:] = self.duet_dict["litter"]
            elif ftype == "litter":
                calibrated_duet[0,:,:] = self.duet_dict["grass"]
                calibrated_duet[1,:,:] = calibrated_dict["litter"]
            else:
                grass_weights = self.duet_dict["grass"]/self.duet_dict["total"]
                litter_weights = self.duet_dict["litter"]/self.duet_dict["total"]
                calibrated_duet[0,:,:][np.where(self.original_duet_array[0,:,:]>0)] = (calibrated_dict["total"]*grass_weights)[np.where(self.original_duet_array[0,:,:]>0)]
                calibrated_duet[1,:,:][np.where(self.original_duet_array[0,:,:]>0)] = (calibrated_dict["total"]*litter_weights)[np.where(self.original_duet_array[0,:,:]>0)]
        else:
            calibrated_duet[0,:,:] = calibrated_dict["grass"]
            calibrated_duet[1,:,:] = calibrated_dict["litter"]
        return calibrated_duet

    def _read_original_duet(self):
        nx = self.zroot.attrs["nx"]
        ny = self.zroot.attrs["ny"]
        nz = 2 # number of duet layers, right now grass and litter. Will be number of tree species + 1
        with open(Path(self.output_dir, "surface_rhof.dat"), "rb") as fin:
            duet_rhof = FortranFile(fin).read_reals(dtype="float32").reshape((nz, ny, nx), order="F")
        return duet_rhof


    def _get_input_array(self):
        duet_dict = {}
        if self.calibrated:
            duet_dict["grass"] = self.calibrated_array[0,:,:]
            duet_dict["litter"] = self.calibrated_array[1,:,:]
            duet_dict["total"] = np.add(self.calibrated_array[0,:,:],self.calibrated_array[1,:,:])
        else:
            duet_dict["grass"] = self.original_duet_array[0,:,:]
            duet_dict["litter"] = self.original_duet_array[1,:,:]
            duet_dict["total"] = np.add(self.original_duet_array[0,:,:],self.original_duet_array[1,:,:])
        return duet_dict


    def _name_calibrated_file(self) -> str:
        delim = "_"
        ftype_str = self.calibrated_fuel_type[0] if len(self.calibrated_fuel_type)==1 else delim.join([str(ele) for ele in self.calibrated_fuel_type])
        method_str = self.calibration_method[0] if len(self.calibration_method)==1 else delim.join([str(ele) for ele in self.calibration_method])
        arr_name = delim.join(["surface_rhof_calibrated",ftype_str,"{}.dat".format(method_str)])
        if Path(self.output_dir, arr_name).exists():
            i = 2
            while Path(self.output_dir, delim.join(["surface_rhof_calibrated",ftype_str,method_str,"%s.dat" % i])).exists():
                i += 1
            arr_name = delim.join(["surface_rhof_calibrated",ftype_str,method_str,"%s.dat" % i])
        return arr_name
    
    def _flatten(self, A):
        rt = []
        for i in A:
            if isinstance(i,list): rt.extend(self._flatten(i))
            else: rt.append(i)
        return rt


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


def _write_np_array_to_dat(array: np.ndarray, dat_name: str,
                           output_dir: Path, dtype: type = np.float32,
                           reshape: bool = True) -> None:
    """
    Write a numpy array to a fortran binary file. Array must be cast to the
    appropriate data type before calling this function. If the array is 3D,
    the array will be reshaped from (y, x, z) to (z, y, x) for fortran.
    """
    # Reshape array from (y, x, z) to (z, y, x) (also for fortran)
    if reshape:
        if len(array.shape) == 3:
            array = np.moveaxis(array, 2, 0).astype(dtype)
        else:
            array = array.astype(dtype)
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
