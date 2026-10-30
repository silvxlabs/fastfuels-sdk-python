"""
fastfuels_sdk/v2/inventories.py
"""

# Core imports
import json
from collections.abc import Mapping
from http import HTTPStatus
from io import StringIO
from pathlib import Path
from typing import List, Optional

# Internal imports
from fastfuels_sdk.v2._jobs import wait as _wait
from fastfuels_sdk.v2._uploads import put_upload
from fastfuels_sdk.v2.api import ensure_client
from fastfuels_sdk.v2.exceptions import expect
from fastfuels_sdk.v2.client_library.api.inventories import (
    apply_modifications as apply_modifications_endpoint,
    apply_treatments as apply_treatments_endpoint,
    create_chm_inventory,
    create_crown_base_height_inventory,
    create_gdam_inventory,
    create_inventory_export,
    create_inventory_upload,
    create_pim_chm_fusion_inventory,
    create_pim_inventory,
    delete_inventory,
    duplicate_inventory as duplicate_inventory_endpoint,
    get_inventory as get_inventory_endpoint,
    get_inventory_data_csv,
    get_inventory_data_json,
    get_inventory_data_metadata,
    list_inventories as list_inventories_endpoint,
    list_inventories_cross_domain,
    update_inventory,
)
from fastfuels_sdk.v2.client_library.models import (
    Inventory as InventoryModel,
    ApplyModificationsRequest,
    ApplyTreatmentsRequest,
    ChmInventoryCrownSegmentation,
    CreateChmInventoryRequest,
    CreateCrownBaseHeightInventoryRequest,
    CreateGdamInventoryRequest,
    CreateGdamInventoryRequestImputeColumnsItem,
    CreateInventoryUploadRequest,
    CreatePimChmFusionInventoryRequest,
    CreatePimInventoryRequest,
    CreateTreeInventoryRequest,
    CrownFeatureCrownGeometrySource,
    CrownProfileModel,
    DuplicateInventoryRequest,
    ExportInventoryRequest,
    FiaNationalLogit2026Model,
    GdamModel,
    InventoryColumnMapping,
    InventoryDataMetadata,
    InventoryDataResponse,
    InventoryExportFormat,
    InventoryJsonOrientation,
    InventorySortField,
    InventoryUploadFormat,
    JobStatus,
    ListInventoriesResponse,
    Monleon2004Eq1Model,
    Monleon2004Eq2Model,
    ParametricCrownGeometrySource,
    PointProcess,
    Randolph2010Model,
    ReimputationMethod,
    Resolution3D,
    SortOrder,
    ToneyReeves2009Model,
    TreeBand,
    UpdateInventoryRequestBody,
    Westfall2019Model,
)
from fastfuels_sdk.v2.client_library.types import UNSET

# External imports
import attrs
import pandas as pd

__all__ = [
    "Inventory",
    "create_tree_inventory_from_pim_grid",
    "create_tree_inventory_from_chm_grid",
    "create_tree_inventory_from_pim_chm_fusion",
    "create_tree_inventory_from_file",
    "create_tree_inventory_from_gdam",
    "create_tree_inventory_from_crown_base_height",
    "list_inventories",
    "get_inventory",
    "ChmInventoryCrownSegmentation",
    "CrownFeatureCrownGeometrySource",
    "ParametricCrownGeometrySource",
    "ReimputationMethod",
]

_UPLOAD_FORMATS = {
    ".csv": InventoryUploadFormat.CSV,
    ".geojson": InventoryUploadFormat.GEOJSON,
    ".json": InventoryUploadFormat.GEOJSON,
    ".gpkg": InventoryUploadFormat.GEOPACKAGE,
}


def _domain_id(domain) -> str:
    """Resolve a Domain object or a domain-id string to the id string."""
    return getattr(domain, "id", domain)


def _enum_list(values, enum_cls):
    """Coerce a list of strings/enum members to enum members, or UNSET."""
    if values is None:
        return UNSET
    return [v if isinstance(v, enum_cls) else enum_cls(v) for v in values]


def _opt(value):
    """Map ``None`` to the generated UNSET sentinel, else pass through."""
    return value if value is not None else UNSET


def _build_fusion_method(method):
    """Translate a fusion ``method`` kwarg into a method model or UNSET.

    - ``None`` -> ``UNSET`` (the API applies its default, reimputation).
    - a ``ReimputationMethod`` -> passed through unchanged.
    - a mapping -> a ``ReimputationMethod`` built from its fields.
    """
    if method is None:
        return UNSET
    if isinstance(method, ReimputationMethod):
        return method
    if isinstance(method, Mapping):
        return ReimputationMethod(**method)
    raise ValueError(
        "method must be a ReimputationMethod or a mapping of its fields, "
        f"got {method!r}."
    )


# Crown base height models by name. None takes parameters, so the name alone
# selects one; a prebuilt model instance is also accepted.
_CROWN_BASE_HEIGHT_MODELS = {
    "fia_national_logit_2026": FiaNationalLogit2026Model,
    "monleon_2004_eq1": Monleon2004Eq1Model,
    "monleon_2004_eq2": Monleon2004Eq2Model,
    "toney_reeves_2009": ToneyReeves2009Model,
    "randolph_2010": Randolph2010Model,
    "westfall_2019": Westfall2019Model,
    "gdam": GdamModel,
}


def _build_crown_base_height_model(model, kwarg: str):
    """Translate a crown base height model kwarg into a model or UNSET.

    - ``None`` -> ``UNSET`` (the API applies its default).
    - a model name, e.g. ``"gdam"`` -> that model.
    - a mapping with a ``name`` key, e.g. ``{"name": "gdam"}`` -> that model.
    - a model instance (e.g. ``GdamModel()``) -> passed through unchanged.
    """
    if model is None:
        return UNSET
    if isinstance(model, tuple(_CROWN_BASE_HEIGHT_MODELS.values())):
        return model
    if isinstance(model, Mapping):
        model_name = model.get("name")
    elif isinstance(model, str):
        model_name = model
    else:
        model_name = None
    factory = _CROWN_BASE_HEIGHT_MODELS.get(model_name)
    if factory is None:
        raise ValueError(
            f"{kwarg} must be one of {sorted(_CROWN_BASE_HEIGHT_MODELS)}, a "
            f"mapping with one of them as its name, or a crown base height "
            f"model object, got {model!r}."
        )
    return factory()


def _build_crown_segmentation(crown_segmentation):
    """Translate a CHM inventory ``crown_segmentation`` kwarg into a model or UNSET.

    - ``None`` -> ``UNSET`` (no segmentation, no ``crown_radius`` column).
    - a ``ChmInventoryCrownSegmentation`` -> passed through unchanged.
    - a mapping -> a ``ChmInventoryCrownSegmentation`` built from its fields
      (``{}`` segments with the API defaults).
    """
    if crown_segmentation is None:
        return UNSET
    if isinstance(crown_segmentation, ChmInventoryCrownSegmentation):
        return crown_segmentation
    if isinstance(crown_segmentation, Mapping):
        return ChmInventoryCrownSegmentation.from_dict(crown_segmentation)
    raise ValueError(
        "crown_segmentation must be a ChmInventoryCrownSegmentation or a "
        f"mapping of its fields, got {crown_segmentation!r}."
    )


def _build_crown_geometry_source(crown_geometry_source):
    """Translate a voxelize ``crown_geometry_source`` kwarg into a model or UNSET.

    - ``None`` -> ``UNSET`` (the API default, parametric crowns).
    - a ``ParametricCrownGeometrySource`` or
      ``CrownFeatureCrownGeometrySource`` -> passed through unchanged.
    - a crown ``Feature`` -> a crown-feature source for its id.
    - ``"parametric"`` -> ``ParametricCrownGeometrySource()``.
    - any other str -> a crown-feature source for that feature id.
    """
    if crown_geometry_source is None:
        return UNSET
    if isinstance(
        crown_geometry_source,
        (ParametricCrownGeometrySource, CrownFeatureCrownGeometrySource),
    ):
        return crown_geometry_source
    if crown_geometry_source == "parametric":
        return ParametricCrownGeometrySource()
    if isinstance(crown_geometry_source, str):
        return CrownFeatureCrownGeometrySource(feature_id=crown_geometry_source)
    # A Feature (or any object with a feature type): imported lazily so the
    # inventories module never imports features.
    feature_type = getattr(crown_geometry_source, "type_", None)
    if feature_type is not None:
        if getattr(feature_type, "value", feature_type) != "crown":
            raise ValueError(
                f"Feature {crown_geometry_source.id} has type "
                f"{getattr(feature_type, 'value', feature_type)!r}; "
                "crown_geometry_source requires a crown Feature."
            )
        return CrownFeatureCrownGeometrySource(feature_id=crown_geometry_source.id)
    raise ValueError(
        "crown_geometry_source must be a crown Feature, a feature id, a "
        "ParametricCrownGeometrySource, or a CrownFeatureCrownGeometrySource, "
        f"got {crown_geometry_source!r}."
    )


class Inventory(InventoryModel):
    """Inventory resource for the FastFuels v2 API.

    An inventory is a table of individual entities — trees — within a
    domain, generated from a PIM (TreeMap) grid, derived from a canopy
    height model, or uploaded from your own data. Inventories are
    asynchronous job resources — creation starts a background job and
    returns a *pending* record; call :meth:`wait` to block until it is
    ready.

    The tree records themselves are retrieved through the data methods
    (:meth:`get_data_metadata`, :meth:`get_data_partition`,
    :meth:`to_dataframe`) once the inventory is completed.

    Attributes
    ----------
    id : str
        Unique identifier for the inventory.
    domain_id : str
        Identifier of the domain the inventory belongs to.
    type_ : InventoryType
        Type of entities in the inventory (currently always "tree").
    status : JobStatus
        Job status: "pending", "running", "completed", or "failed".
    source : InventorySource
        Where the inventory data comes from (e.g. a PIM grid, a CHM
        grid, or an upload).
    name : str
        Human-readable name for the inventory.
    description : str
        Detailed description of the inventory.
    progress : JobProgress, optional
        Progress info while the job is running.
    checksum : str, optional
        Version marker for the inventory's content; changes each time
        the data is rebuilt, unaffected by metadata-only edits.
    modifications : List[InventoryModification], optional
        Cumulative modification rules applied to the inventory.
    treatments : list, optional
        Silvicultural treatments applied to the inventory.
    columns : List[Column], optional
        The columns of the inventory's tabular data.
    forestry_metrics : TreeForestryMetrics, optional
        Stand-level tree count, basal area per acre, trees per acre,
        quadratic mean diameter, and dominant FIA species groups. Populated
        when a tree inventory completes; ``None`` when unavailable.
    georeference : InventoryGeoreference, optional
        Spatial reference of the generated data; populated when the job
        completes.
    error : JobError, optional
        Error details if the job failed.
    tags : List[str], optional
        User-defined tags for organization.
    created_on : datetime
        When the inventory was created.
    modified_on : datetime
        When the inventory was last modified.

    Examples
    --------
    Create a tree inventory from a PIM grid and load it as a DataFrame:
    >>> import fastfuels_sdk as ff
    >>> pim = ff.grids.create_pim_grid_from_treemap(domain)
    >>> inventory = ff.inventories.create_tree_inventory_from_pim_grid(
    ...     domain, pim.wait()
    ... )
    >>> trees = inventory.wait().to_dataframe()

    Get an inventory by ID:
    >>> inventory = ff.get_inventory(domain, "abc123")

    See Also
    --------
    create_tree_inventory_from_pim_grid : Expand a PIM grid into trees.
    create_tree_inventory_from_chm_grid : Derive trees from a canopy height model.
    create_tree_inventory_from_file : Upload your own tree records.
    list_inventories : List inventories in a domain or across all domains.
    """

    @classmethod
    def _from_model(cls, model: InventoryModel) -> "Inventory":
        """Build an Inventory from a generated Inventory model instance.

        Round-trips through the generated to_dict/from_dict — from_dict
        constructs ``cls``, i.e. this subclass.
        """
        inventory = cls.from_dict(model.to_dict())
        if inventory.forestry_metrics is UNSET:
            inventory.forestry_metrics = None
        return inventory

    def _copy_fields_from(self, model: InventoryModel) -> "Inventory":
        """Copy all generated-model fields from `model` onto self (in-place)."""
        for field in attrs.fields(InventoryModel):
            if field.init:
                setattr(self, field.name, getattr(model, field.name))
        if self.forestry_metrics is UNSET:
            self.forestry_metrics = None
        self.additional_properties = dict(model.additional_properties)
        return self

    def _require_completed(self, action: str) -> None:
        """Raise if the inventory is not completed, before deriving from it."""
        if self.status != JobStatus.COMPLETED:
            raise ValueError(
                f"Cannot {action} an inventory with status '{self.status}'. "
                "Call .wait() until it completes first."
            )

    def _column(self, column: str):
        """Return the :class:`Column` with key ``column``, or raise if absent."""
        columns = [] if self.columns is UNSET or self.columns is None else self.columns
        for inventory_column in columns:
            if inventory_column.key == column:
                return inventory_column
        keys = [inventory_column.key for inventory_column in columns]
        raise ValueError(
            f"Inventory has no column {column!r}. Available columns: {keys}."
        )

    @classmethod
    def from_id(cls, domain_id: str, inventory_id: str) -> "Inventory":
        """Retrieve an existing Inventory resource by its ID.

        Parameters
        ----------
        domain_id : str
            The unique identifier of the domain the inventory belongs to.
        inventory_id : str
            The unique identifier of the inventory to retrieve.

        Returns
        -------
        Inventory
            The requested Inventory object.

        Raises
        ------
        NotFoundException
            If no inventory exists with the given IDs, or the user does not
            have access to it.
        """
        response = get_inventory_endpoint.sync_detailed(
            domain_id, inventory_id, client=ensure_client()
        )
        return cls._from_model(expect(response))

    def refresh(self) -> "Inventory":
        """Update this Inventory in place with the latest data from the API.

        Returns
        -------
        Inventory
            ``self``, updated with the latest data (so calls chain).

        Raises
        ------
        NotFoundException
            If the inventory no longer exists.
        """
        response = get_inventory_endpoint.sync_detailed(
            self.domain_id, self.id, client=ensure_client()
        )
        return self._copy_fields_from(expect(response))

    def wait(
        self, timeout: Optional[float] = None, verbose: bool = False
    ) -> "Inventory":
        """Poll the inventory job until it reaches a terminal status.

        Parameters
        ----------
        timeout : float, optional
            Maximum seconds to wait. ``None`` (default) waits indefinitely; the
            job runs server-side regardless, so a bounded wait is resumable.
        verbose : bool, optional
            If True, print the job status at each poll.

        Returns
        -------
        Inventory
            ``self``, updated to its terminal state (so calls chain).

        Raises
        ------
        TimeoutError
            If ``timeout`` is set and elapses before a terminal status.
        JobFailedError
            If the job finished with status "failed".
        """
        return _wait(self, timeout=timeout, verbose=verbose)

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> "Inventory":
        """Update the inventory's mutable metadata (name, description, tags) in place.

        Only provided fields are sent. If no fields are provided, no API call
        is made.

        Parameters
        ----------
        name : str, optional
            New name for the inventory.
        description : str, optional
            New description for the inventory.
        tags : List[str], optional
            New tags for the inventory (replaces existing tags).

        Returns
        -------
        Inventory
            ``self``, updated (so calls chain).

        Raises
        ------
        NotFoundException
            If the inventory no longer exists.
        """
        if name is None and description is None and tags is None:
            return self
        request_body = UpdateInventoryRequestBody(
            name=_opt(name), description=_opt(description), tags=_opt(tags)
        )
        response = update_inventory.sync_detailed(
            self.domain_id, self.id, client=ensure_client(), body=request_body
        )
        return self._copy_fields_from(expect(response))

    def delete(self) -> None:
        """Delete this inventory and its data.

        Raises
        ------
        NotFoundException
            If the inventory no longer exists.
        """
        response = delete_inventory.sync_detailed(
            self.domain_id, self.id, client=ensure_client()
        )
        expect(response, HTTPStatus.NO_CONTENT)

    def duplicate(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> "Inventory":
        """Create an independent copy of this inventory under a new ID.

        The copy is a true clone — the finished data is byte-copied, not
        regenerated — carrying over the source's ``source``,
        ``modifications``, ``treatments``, ``columns``, ``georeference``,
        and ``checksum`` verbatim. Use this to branch a scenario: duplicate,
        then modify the copy while the original stays untouched.

        Parameters
        ----------
        name : str, optional
            Name for the copy. Defaults to the source's name.
        description : str, optional
            Description for the copy. Defaults to the source's description.
        tags : List[str], optional
            Tags for the copy. Defaults to the source's tags.

        Returns
        -------
        Inventory
            The new Inventory object (job status "pending" while the data
            is copied; call :meth:`wait` before using it).

        Raises
        ------
        NotFoundException
            If the inventory no longer exists.
        UnprocessableEntityException
            If the inventory is not in "completed" status.
        """
        request_body = DuplicateInventoryRequest(
            name=_opt(name), description=_opt(description), tags=_opt(tags)
        )
        response = duplicate_inventory_endpoint.sync_detailed(
            self.domain_id, self.id, client=ensure_client(), body=request_body
        )
        return Inventory._from_model(expect(response, HTTPStatus.CREATED))

    def apply_modifications(self, modifications: list) -> "Inventory":
        """Apply modification rules to this inventory in place.

        The inventory keeps its ID; the submitted rules are queued while the
        tree data is re-derived as a background job. The inventory returns to
        "pending" status, and the rules are appended to its cumulative
        ``modifications`` list once processing completes. Call :meth:`wait`
        before using its data. To keep the original data, :meth:`duplicate`
        first and modify the copy.

        Parameters
        ----------
        modifications : list
            Modification rules (``InventoryModification``). Each rule
            filters trees by conditions (ANDed together) and applies
            actions — remove, multiply, divide, add, subtract, or
            replace — to the matching rows.

        Returns
        -------
        Inventory
            ``self``, updated (so calls chain).

        Raises
        ------
        NotFoundException
            If the inventory no longer exists.
        """
        self._require_completed("apply modifications to")
        request_body = ApplyModificationsRequest(modifications=list(modifications))
        response = apply_modifications_endpoint.sync_detailed(
            self.domain_id, self.id, client=ensure_client(), body=request_body
        )
        return self._copy_fields_from(expect(response))

    def apply_treatments(self, treatments: list) -> "Inventory":
        """Apply silvicultural treatments to this inventory in place.

        The inventory keeps its ID; the submitted treatments are queued while
        the tree data is re-derived as a background job. The inventory returns
        to "pending" status, and the treatments are appended to its cumulative
        ``treatments`` list once processing completes. Call :meth:`wait` before
        using its data. To keep the original data, :meth:`duplicate` first and
        treat the copy.

        Parameters
        ----------
        treatments : list
            Treatments thinning the stand to a target. Build them with
            :func:`fastfuels_sdk.v2.treatments.basal_area_treatment` (residual
            basal area) or
            :func:`fastfuels_sdk.v2.treatments.diameter_treatment` (diameter
            limit), available as ``ff.basal_area_treatment`` /
            ``ff.diameter_treatment``.

        Returns
        -------
        Inventory
            ``self``, updated (so calls chain).

        Raises
        ------
        NotFoundException
            If the inventory no longer exists.

        Examples
        --------
        >>> import fastfuels_sdk.v2 as ff
        >>> inventory.apply_treatments([ff.basal_area_treatment("from_below", 25.0)])
        >>> inventory.wait()
        """
        self._require_completed("apply treatments to")
        request_body = ApplyTreatmentsRequest(treatments=list(treatments))
        response = apply_treatments_endpoint.sync_detailed(
            self.domain_id, self.id, client=ensure_client(), body=request_body
        )
        return self._copy_fields_from(expect(response))

    def voxelize(
        self,
        horizontal_resolution_m: Optional[float] = None,
        vertical_resolution_m: Optional[float] = None,
        bands: Optional[list] = None,
        crown_profile_model: Optional[str] = None,
        biomass_source=None,
        max_crown_radius_source=None,
        moisture_model=None,
        seed: Optional[int] = None,
        name: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
        crown_geometry_source=None,
        max_bulk_density: Optional[float] = None,
    ):
        """Create a 3D voxelized tree fuel grid from this inventory.

        Distributes each tree's crown biomass into 3D cells, producing a
        voxel grid of canopy fuel properties.

        Parameters
        ----------
        horizontal_resolution_m : float, optional
            Horizontal (x and y) cell size in meters. Must be given
            together with ``vertical_resolution_m``; if both are omitted
            the API default resolution is used.
        vertical_resolution_m : float, optional
            Vertical (z) cell size in meters.
        bands : list, optional
            Voxel bands to produce (``TreeBand`` members or their string
            keys, e.g. "bulk_density.foliage.live", "fuel_moisture.dead",
            "savr.foliage", "spcd", "tree_id", "volume_fraction").
            Defaults to the API's standard band set.
        crown_profile_model : str, optional
            Crown shape model used to distribute biomass: "purves" (the API
            default), "beta", "cone", "cylinder", "single_ellipsoid",
            "dual_ellipsoid", "single_paraboloid", or "dual_paraboloid".
        biomass_source : AllometryBiomassSource or InventoryColumnsBiomassSource, optional
            Where crown biomass values come from: allometry equations or
            columns of this inventory.
        max_crown_radius_source : optional
            Where each tree's maximum crown radius comes from. Does not
            apply to measured crowns.
        moisture_model : MoistureModel, optional
            Fuel moisture values assigned to the voxelized fuels.
        seed : int, optional
            Random seed for reproducibility. Generated randomly if omitted.
        name, description : str, optional
            Metadata for the new grid.
        tags : List[str], optional
            Tags for the new grid.
        crown_geometry_source : Feature, str, ParametricCrownGeometrySource, or CrownFeatureCrownGeometrySource, optional
            Where crown shapes come from. The string ``"parametric"`` means
            ``ParametricCrownGeometrySource()``; any other string is a crown
            Feature id. Omitted (the default) or
            ``ParametricCrownGeometrySource()``: every crown is drawn from
            ``crown_profile_model`` and ``max_crown_radius_source``. A
            completed crown Feature (see
            :func:`fastfuels_sdk.v2.features.create_crown_feature_from_chm`),
            its id, or ``CrownFeatureCrownGeometrySource(feature_id=...)``:
            each tree with a crown in that Feature, matched by ``tree_id``,
            gets a measured crown. Its outline is the crown's CHM cells, its
            top is each cell's CHM height, and its bottom follows
            ``crown_profile_model`` up from the crown base. Trees with no
            crown in the Feature, whose crown does not contain their stem,
            or with no CHM height above their crown base are drawn
            parametrically. Every tree keeps the biomass ``biomass_source``
            gives it. Requires an inventory with a ``tree_id`` column; the
            CHM grid the Feature was built from must still exist.
        max_bulk_density : float, optional
            Upper limit on bulk density, in kg/m**3; must be greater than 0.
            In any voxel where a biomass component's bulk
            density, live and dead combined, exceeds the limit, that
            component's live and dead bulk density are scaled down to it,
            keeping their live/dead split, and ``leaf_area_density`` is
            scaled with foliage. Omitted (the default) applies no limit.

        Returns
        -------
        Grid
            The new (pending) 3D voxel Grid. Its ``source`` records the
            request, including ``crown_geometry_source`` and
            ``max_bulk_density``. With a crown Feature source,
            ``source["source_chm_grid_id"]`` and
            ``source["source_chm_grid_checksum"]`` record the Feature's CHM
            grid and its checksum at creation, and once the grid completes
            ``source["crown_geometry_counts"]`` gives the number of trees
            drawn with a measured crown (``"measured"``) and drawn
            parametrically because they had no crown in the Feature
            (``"parametric_no_crown"``), their crown did not contain their
            stem (``"parametric_stem_outside_crown"``), or they had no CHM
            height above their crown base (``"parametric_no_volume"``).

        Raises
        ------
        ValueError
            If only one of ``horizontal_resolution_m`` /
            ``vertical_resolution_m`` is given, the inventory is not
            completed, or ``crown_geometry_source`` is a Feature that is not
            a crown Feature.
        NotFoundException
            If the crown Feature does not exist in this domain.
        UnprocessableEntityException
            If ``max_bulk_density`` is not greater than 0, the Feature is not
            a completed crown Feature, the CHM grid it was built from no
            longer exists, or the inventory has no ``tree_id`` column or
            lacks the columns voxelization needs (``x``, ``y``, ``height``,
            ``dbh``, ``crown_base_height`` and ``fia_species_code``, with no
            empty values; see :func:`create_tree_inventory_from_gdam` and
            :func:`create_tree_inventory_from_crown_base_height`).

        Examples
        --------
        >>> inventory.wait()
        >>> voxels = inventory.voxelize(
        ...     horizontal_resolution_m=2.0, vertical_resolution_m=1.0
        ... )
        >>> voxels.wait()

        Draw measured crowns from a crown Feature and cap bulk density:

        >>> voxels = inventory.voxelize(
        ...     crown_geometry_source=crowns, max_bulk_density=2.0
        ... )
        >>> voxels.wait().source["crown_geometry_counts"]
        {'parametric_no_crown': 0, 'parametric_stem_outside_crown': 0, 'parametric_no_volume': 0, 'measured': 18218}
        """
        # Lazy import so the modules stay decoupled (grids never imports
        # inventories).
        from fastfuels_sdk.v2.client_library.api.grids import (
            create_tree_inventory_grid,
        )
        from fastfuels_sdk.v2.grids import Grid

        self._require_completed("voxelize")
        crown_geometry_source = _build_crown_geometry_source(crown_geometry_source)
        if (horizontal_resolution_m is None) != (vertical_resolution_m is None):
            raise ValueError(
                "horizontal_resolution_m and vertical_resolution_m must be "
                "given together."
            )
        if horizontal_resolution_m is not None:
            resolution = Resolution3D(
                horizontal=horizontal_resolution_m, vertical=vertical_resolution_m
            )
        else:
            resolution = UNSET
        request_body = CreateTreeInventoryRequest(
            source_inventory_id=self.id,
            resolution=resolution,
            bands=_enum_list(bands, TreeBand),
            crown_profile_model=(
                CrownProfileModel(crown_profile_model)
                if crown_profile_model is not None
                else UNSET
            ),
            biomass_source=_opt(biomass_source),
            max_crown_radius_source=_opt(max_crown_radius_source),
            crown_geometry_source=crown_geometry_source,
            max_bulk_density=_opt(max_bulk_density),
            moisture_model=_opt(moisture_model),
            seed=_opt(seed),
            name=name,
            description=description,
            tags=_opt(tags),
        )
        response = create_tree_inventory_grid.sync_detailed(
            self.domain_id, client=ensure_client(), body=request_body
        )
        return Grid._from_model(expect(response, HTTPStatus.CREATED))

    def export(
        self,
        format: str = "parquet",
        columns: Optional[List[str]] = None,
        expiration_days: int = 7,
        name: str = "",
        description: str = "",
        tags: Optional[List[str]] = None,
    ):
        """Export this inventory to a downloadable file format.

        Parameters
        ----------
        format : str, optional
            Export format: "parquet" (zipped, default), "csv", "geojson",
            or "geopackage".
        columns : List[str], optional
            Columns to include (default: all columns).
        expiration_days : int, optional
            Days until the signed download URL expires (max 7, default 7).
        name, description : str, optional
            Metadata for the export.
        tags : List[str], optional
            Tags for the export.

        Returns
        -------
        Export
            The created Export object (job status "pending"). Call
            :meth:`Export.wait` and then :meth:`Export.to_file` to download
            the file.

        Raises
        ------
        NotFoundException
            If the inventory no longer exists.
        UnprocessableEntityException
            If the inventory is not in "completed" status.
        """
        # Lazy import so the modules stay decoupled (exports never imports
        # inventories).
        from fastfuels_sdk.v2.exports import Export

        request_body = ExportInventoryRequest(
            columns=_opt(columns),
            expiration_days=expiration_days,
            name=name,
            description=description,
            tags=_opt(tags),
        )
        response = create_inventory_export.sync_detailed(
            self.domain_id,
            self.id,
            InventoryExportFormat(format),
            client=ensure_client(),
            body=request_body,
        )
        return Export._from_model(expect(response, HTTPStatus.CREATED))

    def get_data_metadata(self) -> InventoryDataMetadata:
        """Get the partition layout of the inventory's tree records.

        The tree records are served in fixed-size partitions. Use this to
        discover how many partitions exist before retrieving them with
        :meth:`get_data_partition` (or call :meth:`to_dataframe` to
        retrieve everything at once).

        Returns
        -------
        InventoryDataMetadata
            With attributes ``num_partitions``, ``total_rows``, ``columns``
            (column names), and ``partitions`` (per-partition row counts).
            An inventory with no data has ``num_partitions`` 0.

        Raises
        ------
        NotFoundException
            If the inventory no longer exists.
        UnprocessableEntityException
            If the inventory is not in "completed" status.

        Examples
        --------
        >>> metadata = inventory.get_data_metadata()
        >>> metadata.num_partitions
        1
        """
        response = get_inventory_data_metadata.sync_detailed(
            self.domain_id, self.id, client=ensure_client()
        )
        return expect(response)

    def column_summary(self, column: str):
        """Return summary statistics for one column without downloading records.

        The server computes a per-column summary when an inventory completes,
        so this provides a cheap overview without fetching the inventory's tree
        records (unlike :meth:`to_dataframe`).

        Parameters
        ----------
        column : str
            The column key to summarize (see :attr:`columns` for available
            keys).

        Returns
        -------
        ContinuousColumnSummary or CategoricalColumnSummary or None
            The column's summary, discriminated by its ``type_``:
            ``"continuous"`` carries ``count``, ``null_count``, ``min_``,
            ``max_``, ``mean``, and ``std``; ``"categorical"`` carries
            ``count``, ``null_count``, and ``unique_count``. ``None`` until
            the inventory completes (call :meth:`wait` first).

        Raises
        ------
        ValueError
            If ``column`` is not one of the inventory's columns.

        Examples
        --------
        >>> inventory = ff.get_inventory(domain, "abc123").wait()
        >>> inventory.column_summary("dbh").type_
        'continuous'
        """
        summary = self._column(column).summary
        return None if summary is UNSET else summary

    def get_data_partition(
        self,
        partition_index: int,
        columns: Optional[List[str]] = None,
        json_orientation: str = "split",
    ) -> InventoryDataResponse:
        """Get one partition of the inventory's tree records.

        Parameters
        ----------
        partition_index : int
            Zero-indexed partition number. Must be less than the
            ``num_partitions`` reported by :meth:`get_data_metadata`.
        columns : List[str], optional
            Column subset to retrieve (default: all columns).
        json_orientation : {"split", "records"}, optional
            JSON layout. ``"split"`` (default) returns rows as lists of
            values in ``partition.columns`` order; ``"records"`` returns
            self-describing row mappings.

        Returns
        -------
        InventoryDataResponse
            With attributes ``partition``, ``num_rows``, ``columns``
            (column names), and ``data`` (row lists for ``"split"`` or row
            mappings for ``"records"``).

        Raises
        ------
        NotFoundException
            If the inventory no longer exists.
        UnprocessableEntityException
            If ``partition_index`` is past the last partition, or the
            inventory is not in "completed" status.
        ValueError
            If ``json_orientation`` is not ``"split"`` or ``"records"``.

        Examples
        --------
        >>> partition = inventory.get_data_partition(0)
        >>> partition.num_rows
        1392
        """
        orientation = InventoryJsonOrientation(json_orientation)
        response = get_inventory_data_json.sync_detailed(
            self.domain_id,
            self.id,
            partition_index,
            client=ensure_client(),
            json_orientation=orientation,
            columns=",".join(columns) if columns is not None else UNSET,
        )
        return expect(response)

    def to_dataframe(self, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """Retrieve the inventory's tree records as a pandas DataFrame.

        Retrieves every partition as CSV, parses it with :func:`pandas.read_csv`,
        and concatenates the partitions into a single DataFrame with one row
        per tree, preserving source order.

        Parameters
        ----------
        columns : List[str], optional
            Column subset to retrieve (default: all columns).

        Returns
        -------
        pd.DataFrame
            DataFrame with one row per tree. Empty if the inventory
            contains no trees.

        Raises
        ------
        NotFoundException
            If the inventory no longer exists.
        UnprocessableEntityException
            If the inventory is not in "completed" status.

        Examples
        --------
        >>> inventory.wait()
        >>> trees = inventory.to_dataframe()
        """
        metadata = self.get_data_metadata()
        frames = []
        for partition_index in range(metadata.num_partitions):
            response = get_inventory_data_csv.sync_detailed(
                self.domain_id,
                self.id,
                partition_index,
                client=ensure_client(),
                columns=",".join(columns) if columns is not None else UNSET,
            )
            frames.append(pd.read_csv(StringIO(expect(response))))
        if not frames:
            return pd.DataFrame(columns=columns or metadata.columns)
        return pd.concat(frames, ignore_index=True)

    def to_json(self) -> str:
        """Serialize the complete Inventory object to a JSON string.

        Returns
        -------
        str
            The Inventory as a pretty-printed JSON string.
        """
        return json.dumps(self.to_dict(), default=str, indent=2)


# ---------------------------------------------------------------------------
# Create inventories (module-level functions)
# ---------------------------------------------------------------------------


def create_tree_inventory_from_pim_grid(
    domain,
    pim_grid,
    seed: Optional[int] = None,
    point_process: Optional[str] = None,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
    treatments: Optional[list] = None,
) -> Inventory:
    """Create a tree inventory by expanding a PIM (TreeMap) grid.

    Each pixel of the completed PIM grid imputes an FIA plot; expansion
    generates individual tree records from those plots and assigns each
    tree a coordinate with a spatial point process.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the inventory in.
    pim_grid : Grid or str
        A completed PIM grid (or its id) to expand. See
        :func:`fastfuels_sdk.v2.grids.create_pim_grid_from_treemap`.
    seed : int, optional
        Random seed for reproducibility. Generated randomly if omitted.
    point_process : str, optional
        Spatial point process for tree coordinate assignment
        (``PointProcess`` member or its string key, e.g.
        "inhomogeneous_poisson").
    name, description : str, optional
        Metadata for the inventory.
    tags : List[str], optional
        Tags for the inventory.
    modifications : list, optional
        Modification rules (``InventoryModification``) applied after
        expansion.
    treatments : list, optional
        Silvicultural treatments (``InventoryBasalAreaTreatment`` or
        ``InventoryDiameterTreatment``) applied after modifications.

    Returns
    -------
    Inventory
        The created Inventory object (job status "pending" or "running").

    Examples
    --------
    >>> import fastfuels_sdk as ff
    >>> pim = ff.grids.create_pim_grid_from_treemap(domain)
    >>> inventory = ff.inventories.create_tree_inventory_from_pim_grid(
    ...     domain, pim.wait(), seed=42
    ... )
    >>> inventory.wait()
    """
    request_body = CreatePimInventoryRequest(
        source_pim_grid_id=_domain_id(pim_grid),
        seed=_opt(seed),
        point_process=(
            PointProcess(point_process) if point_process is not None else UNSET
        ),
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
        treatments=_opt(treatments),
    )
    response = create_pim_inventory.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Inventory._from_model(expect(response, HTTPStatus.CREATED))


def create_tree_inventory_from_chm_grid(
    domain,
    chm_grid,
    algorithm=None,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
    treatments: Optional[list] = None,
    crown_segmentation=None,
) -> Inventory:
    """Create a tree inventory by isolating stems in a canopy height model.

    Detects individual trees in a completed canopy height model (CHM)
    grid and derives a tree record from each detected stem. Each tree gets
    a ``tree_id``. To outline each detected tree's crown as a crown
    Feature for measured-crown voxelization, pass this inventory and the
    same CHM grid to
    :func:`fastfuels_sdk.v2.features.create_crown_feature_from_chm`.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the inventory in.
    chm_grid : Grid or str
        A completed canopy height model grid (or its id). See
        :func:`fastfuels_sdk.v2.grids.create_canopy_height_grid_from_meta`
        and
        :func:`fastfuels_sdk.v2.grids.create_canopy_height_grid_from_naip_chm`.
    algorithm : StemIsolationLmf or StemIsolationVwf, optional
        Stem isolation algorithm and its parameters: local maximum
        filtering (``StemIsolationLmf``) or variable window filtering
        (``StemIsolationVwf``). Defaults to the API's standard algorithm.
        ``StemIsolationVwf()`` without arguments uses ``crown_ratio=0.05``
        and ``crown_offset=3.0``: the search window diameter in meters is
        ``crown_offset + crown_ratio * height``.
    name, description : str, optional
        Metadata for the inventory.
    tags : List[str], optional
        Tags for the inventory.
    modifications : list, optional
        Modification rules (``InventoryModification``) applied after stem
        isolation.
    treatments : list, optional
        Silvicultural treatments (``InventoryBasalAreaTreatment`` or
        ``InventoryDiameterTreatment``) applied after modifications.
    crown_segmentation : ChmInventoryCrownSegmentation or Mapping, optional
        Segment each detected tree's crown on the CHM and add a
        ``crown_radius`` column (m). Pass a ``ChmInventoryCrownSegmentation``
        or a mapping of its fields (``method``, ``min_relative_height``,
        ``min_relative_crown_height``, ``max_crown_radius``,
        ``radius_estimator``); ``{}`` segments with the API defaults.
        Requires a CHM cell size of 2 m or finer. Omitted (the default)
        skips segmentation.

    Returns
    -------
    Inventory
        The created Inventory object (job status "pending" or "running").

    Raises
    ------
    ValueError
        If ``crown_segmentation`` is neither a
        ``ChmInventoryCrownSegmentation`` nor a mapping.
    UnprocessableEntityException
        If ``crown_segmentation`` is given and the CHM cell size is coarser
        than 2 m.

    Examples
    --------
    >>> import fastfuels_sdk as ff
    >>> chm = ff.grids.create_canopy_height_grid_from_meta(domain)
    >>> inventory = ff.inventories.create_tree_inventory_from_chm_grid(
    ...     domain, chm.wait()
    ... )
    >>> inventory.wait()

    Add a measured ``crown_radius`` column:

    >>> inventory = ff.inventories.create_tree_inventory_from_chm_grid(
    ...     domain, chm, crown_segmentation={}
    ... )
    """
    request_body = CreateChmInventoryRequest(
        source_chm_grid_id=_domain_id(chm_grid),
        algorithm=_opt(algorithm),
        crown_segmentation=_build_crown_segmentation(crown_segmentation),
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
        treatments=_opt(treatments),
    )
    response = create_chm_inventory.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Inventory._from_model(expect(response, HTTPStatus.CREATED))


def create_tree_inventory_from_pim_chm_fusion(
    domain,
    pim_grid,
    chm_grid,
    method=None,
    seed: Optional[int] = None,
    point_process: Optional[str] = None,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    modifications: Optional[list] = None,
    treatments: Optional[list] = None,
) -> Inventory:
    """Create a tree inventory by fusing a PIM grid with a canopy height model.

    Expands the plots of a completed PIM grid into individual trees, as
    :func:`create_tree_inventory_from_pim_grid` does, but conditioned on a
    completed canopy height model (CHM) grid: the PIM is resampled to the
    method's ``resolution``, each resampled cell keeps its plot only where
    the CHM's canopy cover (the fraction of CHM cells taller than
    ``min_height``) exceeds ``cover_threshold``, and the surviving plots are
    expanded. The result has the same columns as a PIM-expanded inventory.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the inventory in.
    pim_grid : Grid or str
        A completed PIM grid (or its id) to expand. See
        :func:`fastfuels_sdk.v2.grids.create_pim_grid_from_treemap`.
    chm_grid : Grid or str
        A completed canopy height model grid (or its id) with a ``chm`` band
        in meters, used to condition the PIM. See
        :func:`fastfuels_sdk.v2.grids.create_canopy_height_grid_from_meta`,
        :func:`fastfuels_sdk.v2.grids.create_canopy_height_grid_from_naip_chm`,
        and
        :func:`fastfuels_sdk.v2.grids.create_canopy_height_grid_from_point_cloud`.
    method : ReimputationMethod or Mapping, optional
        Fusion algorithm and its parameters. ``None`` (the default) applies
        the API's default, reimputation with ``resolution=7.5`` m,
        ``min_height=2.0`` m, and ``cover_threshold=0.2``; a
        ``ReimputationMethod`` or a mapping of its fields (``resolution``,
        ``min_height``, ``cover_threshold``) sets them explicitly. The
        resolution must be no finer than the CHM cell and no coarser than
        the PIM cell.
    seed : int, optional
        Random seed for reproducibility. Generated randomly if omitted.
    point_process : str, optional
        Spatial point process for tree coordinate assignment
        (``PointProcess`` member or its string key, e.g.
        "inhomogeneous_poisson").
    name, description : str, optional
        Metadata for the inventory.
    tags : List[str], optional
        Tags for the inventory.
    modifications : list, optional
        Modification rules (``InventoryModification``) applied after
        expansion.
    treatments : list, optional
        Silvicultural treatments (``InventoryBasalAreaTreatment`` or
        ``InventoryDiameterTreatment``) applied after modifications.

    Returns
    -------
    Inventory
        The created Inventory object (job status "pending" or "running").

    Raises
    ------
    ValueError
        If ``method`` is neither a ``ReimputationMethod`` nor a mapping.

    Examples
    --------
    >>> import fastfuels_sdk.v2 as ff
    >>> pim = ff.grids.create_pim_grid_from_treemap(domain, output_resolution_m=30)
    >>> chm = ff.grids.create_canopy_height_grid_from_meta(domain, output_resolution_m=1)
    >>> ff.wait_all([pim, chm])
    >>> inventory = ff.inventories.create_tree_inventory_from_pim_chm_fusion(
    ...     domain, pim, chm, seed=42
    ... )
    >>> inventory.wait()

    Keep plots only where at least 30% of the cell is canopy:

    >>> inventory = ff.inventories.create_tree_inventory_from_pim_chm_fusion(
    ...     domain, pim, chm, method={"cover_threshold": 0.3}, seed=42
    ... )
    """
    request_body = CreatePimChmFusionInventoryRequest(
        source_pim_grid_id=_domain_id(pim_grid),
        source_chm_grid_id=_domain_id(chm_grid),
        method=_build_fusion_method(method),
        seed=_opt(seed),
        point_process=(
            PointProcess(point_process) if point_process is not None else UNSET
        ),
        name=name,
        description=description,
        tags=_opt(tags),
        modifications=_opt(modifications),
        treatments=_opt(treatments),
    )
    response = create_pim_chm_fusion_inventory.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Inventory._from_model(expect(response, HTTPStatus.CREATED))


def create_tree_inventory_from_file(
    domain,
    path: str,
    format: Optional[str] = None,
    columns=None,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
) -> Inventory:
    """Create a tree inventory by uploading your own tree records.

    Creates the inventory resource, uploads the file to the returned
    signed URL, and returns the (pending) Inventory. Coordinates must be
    in the domain's CRS.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the inventory in.
    path : str
        Path to the local file: ``.csv``, ``.geojson``/``.json``, or
        ``.gpkg``.
    format : str, optional
        Upload format: "csv", "geojson", or "geopackage". Inferred from
        the file extension if omitted.
    columns : dict or InventoryColumnMapping, optional
        Mapping from the standard column roles to your file's column
        names, e.g. ``{"x": "X_UTM", "y": "Y_UTM", "dbh": "DBH_CM"}``.
        Roles: "tree_id", "x", "y", "height", "dbh", "crown_ratio",
        "crown_base_height", "crown_radius", "fia_species_code",
        "fia_status_code", "fia_crown_class_code". Columns whose names
        already match need no mapping. ``crown_ratio`` is the FIA compacted
        live crown ratio (0-1). ``crown_base_height`` is the height of the
        lowest live foliage in meters (at least 0 and at most ``height``).
        ``crown_radius`` is a measured crown radius in meters (> 0 and
        <= 20; null for trees without a measurement).
    name, description : str, optional
        Metadata for the inventory.
    tags : List[str], optional
        Tags for the inventory.

    Returns
    -------
    Inventory
        The created Inventory object (job status "pending"). Call
        :meth:`Inventory.wait` to block until the uploaded file is
        processed.

    Raises
    ------
    ValueError
        If ``format`` is omitted and the file extension is not one of
        ``.csv``, ``.geojson``, ``.json``, or ``.gpkg``.

    Examples
    --------
    >>> import fastfuels_sdk as ff
    >>> inventory = ff.inventories.create_tree_inventory_from_file(
    ...     domain, "plot_trees.csv", columns={"x": "X_UTM", "y": "Y_UTM"}
    ... )
    >>> inventory.wait()
    """
    if format is not None:
        upload_format = InventoryUploadFormat(format)
    else:
        suffix = Path(path).suffix.lower()
        if suffix not in _UPLOAD_FORMATS:
            raise ValueError(
                f"Cannot infer the upload format from {suffix!r}. Pass "
                'format="csv", "geojson", or "geopackage".'
            )
        upload_format = _UPLOAD_FORMATS[suffix]
    if isinstance(columns, dict):
        columns = InventoryColumnMapping(**columns)
    request_body = CreateInventoryUploadRequest(
        format_=upload_format,
        columns=_opt(columns),
        name=name,
        description=description,
        tags=_opt(tags),
    )
    response = create_inventory_upload.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    created = expect(response, HTTPStatus.CREATED)
    put_upload(created.upload, path)
    return Inventory._from_model(created.inventory)


def create_tree_inventory_from_gdam(
    domain,
    source_inventory,
    impute_columns: Optional[list] = None,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
    crown_base_height_model=None,
    overwrite: bool = False,
) -> Inventory:
    """Create a tree inventory by imputing morphology with GDAM allometry.

    GDAM fills in per-tree morphology — diameter at breast height, FIA
    compacted crown ratio, FIA species code, and crown base height — for a
    completed source tree inventory with a position and height for every tree
    (for example one uploaded with coordinates and heights only). GDAM
    conditions its predictions on whichever of these columns the source
    already has. The result is a new inventory; the source is left unchanged.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the inventory in.
    source_inventory : Inventory or str
        A completed tree inventory (or its id) with ``x``, ``y`` and
        ``height`` for every tree, whose morphology columns GDAM will fill in.
    impute_columns : list, optional
        Which morphology columns to impute
        (``CreateGdamInventoryRequestImputeColumnsItem`` members or their
        string keys: "dbh", "crown_ratio", "fia_species_code",
        "crown_base_height"). Defaults to all four. Narrow it to impute fewer
        columns; columns left out keep the source's values.
    name, description : str, optional
        Metadata for the inventory.
    tags : List[str], optional
        Tags for the inventory.
    crown_base_height_model : str, Mapping, or crown base height model, optional
        The model that gives ``crown_base_height``, by name: "gdam",
        "fia_national_logit_2026", "monleon_2004_eq1", "monleon_2004_eq2",
        "toney_reeves_2009", "randolph_2010", or "westfall_2019" (a mapping
        such as ``{"name": "gdam"}`` or a model object such as
        ``GdamModel()`` is also accepted). Omitted (the default) uses
        "gdam", which predicts it with the other columns. Any other model
        computes it from each tree's species, dbh, crown ratio and height
        after GDAM fills them, so each of those must be imputed or be a
        column of the source inventory.
    overwrite : bool, optional
        ``False`` (the default) keeps existing values and fills only empty
        cells of ``impute_columns``. ``True`` replaces every tree's value in
        ``impute_columns``; the old values are not given to GDAM.

    Returns
    -------
    Inventory
        The created Inventory object (job status "pending"). Call
        :meth:`Inventory.wait` to block until imputation finishes. Its
        ``source`` records ``impute_columns``, ``overwrite``,
        ``crown_base_height_model``, and the source columns GDAM conditioned
        on (``conditioned_columns``).

    Raises
    ------
    ValueError
        If ``crown_base_height_model`` is not a known model name, a mapping
        naming one, or a crown base height model object.
    UnprocessableEntityException
        If the source inventory is missing, or has empty values in, ``x``,
        ``y`` or ``height``, or ``crown_base_height_model`` is an equation
        whose inputs are neither imputed nor columns of the source.

    Examples
    --------
    >>> import fastfuels_sdk as ff
    >>> sparse = ff.inventories.create_tree_inventory_from_file(
    ...     domain, "stems.csv"  # x, y, height only
    ... )
    >>> sparse.wait()
    >>> full = ff.inventories.create_tree_inventory_from_gdam(domain, sparse)
    >>> full.wait()

    Compute crown base heights with an equation instead of GDAM:

    >>> full = ff.inventories.create_tree_inventory_from_gdam(
    ...     domain, sparse, crown_base_height_model="fia_national_logit_2026"
    ... )
    """
    request_body = CreateGdamInventoryRequest(
        source_tree_inventory_id=_domain_id(source_inventory),
        impute_columns=_enum_list(
            impute_columns, CreateGdamInventoryRequestImputeColumnsItem
        ),
        overwrite=overwrite,
        crown_base_height_model=_build_crown_base_height_model(
            crown_base_height_model, "crown_base_height_model"
        ),
        name=name,
        description=description,
        tags=_opt(tags),
    )
    response = create_gdam_inventory.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Inventory._from_model(expect(response, HTTPStatus.CREATED))


def create_tree_inventory_from_crown_base_height(
    domain,
    source_inventory,
    model=None,
    overwrite: bool = False,
    name: str = "",
    description: str = "",
    tags: Optional[List[str]] = None,
) -> Inventory:
    """Create a tree inventory with each tree's crown base height computed.

    Computes ``crown_base_height`` (m) for a completed source tree inventory
    with a crown base height model and copies every other column unchanged.
    The equation models compute it from each tree's species, dbh, FIA
    compacted crown ratio and height; species a model does not cover get no
    crown base height. The "gdam" model predicts it with GDAM from position
    and height, conditioned on whichever of species, dbh, crown ratio and
    crown base height the tree has. Use it for a tree inventory without a
    crown base height, such as an uploaded inventory, before voxelizing it or
    building canopy grids from it. The result is a new inventory; the source
    is left unchanged.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) to create the inventory in.
    source_inventory : Inventory or str
        A completed tree inventory (or its id) with ``x``, ``y`` and
        ``height`` for every tree, and ``fia_species_code``, ``dbh`` and
        ``crown_ratio`` for every tree unless ``model`` is "gdam". To fill
        those columns and the crown base height in one request, use
        :func:`create_tree_inventory_from_gdam` instead.
    model : str, Mapping, or crown base height model, optional
        The crown base height model, by name: "fia_national_logit_2026",
        "monleon_2004_eq1", "monleon_2004_eq2", "toney_reeves_2009",
        "randolph_2010", "westfall_2019", or "gdam" (a mapping such as
        ``{"name": "gdam"}`` or a model object such as ``GdamModel()`` is also
        accepted). Omitted (the default) uses "fia_national_logit_2026".
    overwrite : bool, optional
        ``False`` (the default) keeps existing crown base heights and fills
        only empty cells. ``True`` recomputes every tree's crown base height
        with ``model``; "gdam" is not given the old values.
    name, description : str, optional
        Metadata for the inventory.
    tags : List[str], optional
        Tags for the inventory.

    Returns
    -------
    Inventory
        The created Inventory object (job status "pending"). Call
        :meth:`Inventory.wait` to block until the crown base heights are
        computed. Its ``source`` records ``model`` and ``overwrite``.

    Raises
    ------
    ValueError
        If ``model`` is not a known model name, a mapping naming one, or a
        crown base height model object.
    UnprocessableEntityException
        If the source inventory is missing, or has empty values in, a column
        ``model`` needs, or ``overwrite`` is ``False`` and every tree already
        has a crown base height.

    Examples
    --------
    >>> import fastfuels_sdk as ff
    >>> trees = ff.inventories.create_tree_inventory_from_file(
    ...     domain, "plot_trees.csv"  # x, y, height, dbh, crown_ratio, species
    ... )
    >>> trees.wait()
    >>> inventory = ff.inventories.create_tree_inventory_from_crown_base_height(
    ...     domain, trees
    ... )
    >>> inventory.wait()

    Recompute every tree's crown base height with a regional equation:

    >>> inventory = ff.inventories.create_tree_inventory_from_crown_base_height(
    ...     domain, trees, model="toney_reeves_2009", overwrite=True
    ... )
    """
    request_body = CreateCrownBaseHeightInventoryRequest(
        source_tree_inventory_id=_domain_id(source_inventory),
        model=_build_crown_base_height_model(model, "model"),
        overwrite=overwrite,
        name=name,
        description=description,
        tags=_opt(tags),
    )
    response = create_crown_base_height_inventory.sync_detailed(
        _domain_id(domain), client=ensure_client(), body=request_body
    )
    return Inventory._from_model(expect(response, HTTPStatus.CREATED))


# ---------------------------------------------------------------------------
# Top-level fetch / list helpers
# ---------------------------------------------------------------------------


def list_inventories(
    domain=None,
    page: int = 0,
    size: int = 100,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
    source: Optional[str] = None,
    tag: Optional[str] = None,
) -> List[Inventory]:
    """List inventories in a domain, or across all domains (single page).

    Parameters
    ----------
    domain : Domain or str, optional
        The domain (or its id) to list inventories in. If omitted,
        inventories from all the user's domains are listed.
    page : int, optional
        The page number to retrieve, zero-indexed (default 0).
    size : int, optional
        The number of inventories per page (default 100).
    sort_by : str, optional
        Field to sort by: "name", "created_on", or "modified_on".
    sort_order : str, optional
        Sort direction: "ascending" or "descending".
    source : str, optional
        Only return inventories from this source (e.g. "pim").
    tag : str, optional
        Only return inventories carrying this tag.

    Returns
    -------
    List[Inventory]
        The requested page of Inventory objects.
    """
    kwargs = dict(
        client=ensure_client(),
        page=page,
        size=size,
        sort_by=InventorySortField(sort_by) if sort_by else UNSET,
        sort_order=SortOrder(sort_order) if sort_order else UNSET,
        source=_opt(source),
        tag=_opt(tag),
    )
    if domain is None:
        response = list_inventories_cross_domain.sync_detailed(**kwargs)
    else:
        response = list_inventories_endpoint.sync_detailed(_domain_id(domain), **kwargs)
    list_response: ListInventoriesResponse = expect(response)
    return [Inventory._from_model(i) for i in list_response.inventories]


def get_inventory(domain, inventory_id: str) -> Inventory:
    """Retrieve a single inventory by its ID.

    Parameters
    ----------
    domain : Domain or str
        The domain (or its id) the inventory belongs to.
    inventory_id : str
        The unique identifier of the inventory.

    Returns
    -------
    Inventory
        The requested Inventory object.

    Raises
    ------
    NotFoundException
        If no inventory exists with the given IDs, or the user does not have
        access.
    """
    return Inventory.from_id(_domain_id(domain), inventory_id)
