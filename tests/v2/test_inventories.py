"""
tests/v2/test_inventories.py
"""

# Core imports
import json
from uuid import uuid4

# Internal imports
from fastfuels_sdk.v2._jobs import JobFailedError
from fastfuels_sdk.v2.grids import Grid
from fastfuels_sdk.v2.inventories import (
    Inventory,
    create_tree_inventory_from_file,
    create_tree_inventory_from_gdam,
    create_tree_inventory_from_pim_grid,
    get_inventory,
    list_inventories,
)
from fastfuels_sdk.v2.treatments import basal_area_treatment, diameter_treatment
from fastfuels_sdk.v2.modifications import remove_trees, tree_attribute
from fastfuels_sdk.v2.client_library.models import (
    InventoryAttribute,
    InventoryModification,
    InventoryModificationAction,
    InventoryModificationCondition,
    JobStatus,
    Modifier,
    Operator,
)
from fastfuels_sdk.v2.exceptions import NotFoundException

# External imports
import numpy as np
import pandas as pd
import pytest

# The test_domain, completed_pim_grid, and completed_tree_inventory fixtures
# are session-scoped and shared across modules (tests/v2/conftest.py). They
# are READ-ONLY: tests that mutate or delete create throwaways (duplicates).


@pytest.fixture(scope="class")
def throwaway_inventory(completed_tree_inventory):
    """A mutable copy of the shared inventory (the fixtures are read-only)."""
    inventory = completed_tree_inventory.duplicate(name="throwaway_copy")
    inventory.wait()
    yield inventory
    inventory.delete()


class TestCreateTreeInventoryFromPimGrid:
    def test_create(self, test_domain, completed_pim_grid):
        inventory = create_tree_inventory_from_pim_grid(
            test_domain,
            completed_pim_grid,
            seed=42,
            name="throwaway_pim_inventory",
        )
        assert len(inventory.id) > 0
        assert inventory.domain_id == test_domain.id
        assert inventory.status in (JobStatus.PENDING, JobStatus.RUNNING)
        inventory.delete()

    def test_accepts_grid_id_string(self, test_domain, completed_pim_grid):
        inventory = create_tree_inventory_from_pim_grid(
            test_domain, completed_pim_grid.id, seed=42
        )
        assert inventory.domain_id == test_domain.id
        inventory.delete()

    def test_completed_fixture(self, completed_tree_inventory):
        assert completed_tree_inventory.status == JobStatus.COMPLETED
        assert completed_tree_inventory.georeference is not None
        assert completed_tree_inventory.checksum


class TestCreateTreeInventoryFromFile:
    def test_unknown_extension_raises(self, test_domain):
        with pytest.raises(ValueError, match="upload format"):
            create_tree_inventory_from_file(test_domain, "trees.parquet")

    def test_create_from_csv(self, test_domain, tmp_path):
        # Tree records at the center of the domain, in the domain CRS
        x_center = (test_domain.bbox[0] + test_domain.bbox[2]) / 2
        y_center = (test_domain.bbox[1] + test_domain.bbox[3]) / 2
        trees = pd.DataFrame(
            {
                "x": [x_center, x_center + 10],
                "y": [y_center, y_center + 10],
                "height": [12.0, 8.5],
                "dbh": [25.0, 18.0],
                "crown_ratio": [0.4, 0.5],
                "fia_species_code": [122, 122],
                "fia_status_code": [1, 1],
            }
        )
        path = tmp_path / "trees.csv"
        trees.to_csv(path, index=False)

        inventory = create_tree_inventory_from_file(
            test_domain, str(path), name="throwaway_upload"
        )
        assert len(inventory.id) > 0
        assert inventory.domain_id == test_domain.id
        # Processing the uploaded file runs as a background job
        inventory.wait()
        assert inventory.status == JobStatus.COMPLETED
        assert len(inventory.to_dataframe()) == 2
        inventory.delete()


class TestCreateTreeInventoryFromGdam:
    def test_create_returns_new_pending_inventory(
        self, test_domain, completed_tree_inventory
    ):
        imputed = create_tree_inventory_from_gdam(
            test_domain,
            completed_tree_inventory,
            impute_columns=["dbh", "crown_ratio"],
            name="throwaway_gdam",
        )
        assert isinstance(imputed, Inventory)
        assert imputed.id != completed_tree_inventory.id
        assert imputed.domain_id == test_domain.id
        assert imputed.status in (JobStatus.PENDING, JobStatus.RUNNING)
        imputed.delete()

    def test_accepts_inventory_id_string(self, test_domain, completed_tree_inventory):
        imputed = create_tree_inventory_from_gdam(
            test_domain, completed_tree_inventory.id
        )
        assert imputed.domain_id == test_domain.id
        imputed.delete()


class TestFromId:
    def test_success(self, test_domain, completed_tree_inventory):
        inventory = Inventory.from_id(test_domain.id, completed_tree_inventory.id)
        assert inventory.id == completed_tree_inventory.id
        assert inventory.domain_id == test_domain.id

    def test_not_found(self, test_domain):
        with pytest.raises(NotFoundException):
            Inventory.from_id(test_domain.id, uuid4().hex)


class TestGetInventory:
    def test_get_inventory_returns_new_instance(
        self, test_domain, completed_tree_inventory
    ):
        inventory = get_inventory(test_domain, completed_tree_inventory.id)
        assert inventory.id == completed_tree_inventory.id
        assert inventory is not completed_tree_inventory


class TestRefreshInventory:
    def test_refresh_returns_self(self, completed_tree_inventory):
        refreshed = completed_tree_inventory.refresh()
        assert refreshed is completed_tree_inventory
        assert refreshed.id == completed_tree_inventory.id


class TestUpdateInventory:
    def test_update_name(self, test_domain, throwaway_inventory):
        # update() mutates in place and returns self (chains)
        updated = throwaway_inventory.update(name="updated_name")
        assert updated is throwaway_inventory
        assert throwaway_inventory.name == "updated_name"
        assert get_inventory(test_domain, throwaway_inventory.id).name == "updated_name"

    def test_update_tags(self, throwaway_inventory):
        throwaway_inventory.update(tags=["updated"])
        assert throwaway_inventory.tags == ["updated"]

    def test_update_no_fields_makes_no_api_call(self, throwaway_inventory):
        assert throwaway_inventory.update() is throwaway_inventory


class TestDuplicate:
    def test_duplicate_is_a_clone(self, completed_tree_inventory):
        copy = completed_tree_inventory.duplicate(name="duplicate_test")
        assert copy.id != completed_tree_inventory.id
        assert copy.name == "duplicate_test"
        # The copy job byte-copies the data rather than re-deriving it, so
        # the finished copy carries the source's checksum verbatim
        copy.wait()
        assert copy.status == JobStatus.COMPLETED
        assert copy.checksum == completed_tree_inventory.checksum
        copy.delete()


class TestApplyModifications:
    @pytest.mark.xfail(
        reason="v2 API bug: the in-place modifications job fails at the save "
        "step (module-level gcsfs client is not fork-safe in standgen) — "
        "FastFuels-API-v2#333",
        raises=JobFailedError,
        strict=True,
    )
    def test_apply_modifications_rederives_in_place(self, completed_tree_inventory):
        # Mutating, so work on a duplicate — the shared fixture is read-only
        copy = completed_tree_inventory.duplicate(name="modify_test")
        copy.wait()
        # Rules need at least one condition; height > 0 matches every tree
        modification = InventoryModification(
            conditions=[
                InventoryModificationCondition(
                    attribute=InventoryAttribute.HEIGHT,
                    operator=Operator.GT,
                    value=0,
                )
            ],
            actions=[
                InventoryModificationAction(
                    attribute=InventoryAttribute.HEIGHT,
                    modifier=Modifier.MULTIPLY,
                    value=0.9,
                )
            ],
        )
        original_checksum = copy.checksum

        modified = copy.apply_modifications([modification])

        assert modified is copy  # in place: same object, same id
        assert len(copy.modifications) == 1
        copy.wait()
        assert copy.status == JobStatus.COMPLETED
        assert copy.checksum != original_checksum  # data was re-derived
        copy.delete()

    def test_requires_completed_source(self, test_domain, completed_pim_grid):
        inventory = create_tree_inventory_from_pim_grid(
            test_domain, completed_pim_grid, seed=42
        )
        if inventory.status == JobStatus.COMPLETED:
            inventory.delete()
            pytest.skip("inventory completed too quickly to test the guard")
        with pytest.raises(ValueError, match="apply modifications"):
            inventory.apply_modifications([])
        inventory.delete()


class TestApplyTreatments:
    def test_apply_treatments_rederives_in_place(self, completed_tree_inventory):
        # Mutating, so work on a duplicate — the shared fixture is read-only
        copy = completed_tree_inventory.duplicate(name="treat_test")
        copy.wait()
        original_checksum = copy.checksum

        treated = copy.apply_treatments([basal_area_treatment("from_below", 25.0)])

        assert treated is copy  # in place: same object, same id
        assert len(copy.treatments) == 1
        copy.wait()
        assert copy.status == JobStatus.COMPLETED
        assert copy.checksum != original_checksum  # data was re-derived
        copy.delete()

    def test_requires_completed_source(self, test_domain, completed_pim_grid):
        inventory = create_tree_inventory_from_pim_grid(
            test_domain, completed_pim_grid, seed=42
        )
        if inventory.status == JobStatus.COMPLETED:
            inventory.delete()
            pytest.skip("inventory completed too quickly to test the guard")
        with pytest.raises(ValueError, match="apply treatments"):
            inventory.apply_treatments([diameter_treatment("from_below", 10.0)])
        inventory.delete()


class TestModificationBuilders:
    def test_remove_trees_at_creation(
        self, test_domain, completed_pim_grid, completed_tree_inventory
    ):
        # In-place apply_modifications is #333-blocked, so verify the builders
        # via the create-time path (which works). Same seed as the unmodified
        # fixture, so removing dbh < 10 must yield strictly fewer trees.
        modified = create_tree_inventory_from_pim_grid(
            test_domain,
            completed_pim_grid,
            seed=42,
            modifications=[remove_trees(tree_attribute("dbh", "<", 10))],
            name="throwaway_modified",
        )
        modified.wait()
        assert modified.status == JobStatus.COMPLETED
        assert (
            0
            < len(modified.to_dataframe())
            < len(completed_tree_inventory.to_dataframe())
        )
        modified.delete()


class TestVoxelize:
    def test_voxelize_returns_new_pending_grid(self, completed_tree_inventory):
        voxels = completed_tree_inventory.voxelize(
            horizontal_resolution_m=2.0,
            vertical_resolution_m=1.0,
            name="throwaway_voxels",
        )
        assert isinstance(voxels, Grid)
        assert voxels.domain_id == completed_tree_inventory.domain_id
        assert voxels.status in (JobStatus.PENDING, JobStatus.RUNNING)
        voxels.delete()

    def test_resolution_args_must_be_given_together(self, completed_tree_inventory):
        with pytest.raises(ValueError, match="together"):
            completed_tree_inventory.voxelize(horizontal_resolution_m=2.0)

    def test_requires_completed_source(self, test_domain, completed_pim_grid):
        inventory = create_tree_inventory_from_pim_grid(
            test_domain, completed_pim_grid, seed=42
        )
        if inventory.status == JobStatus.COMPLETED:
            inventory.delete()
            pytest.skip("inventory completed too quickly to test the guard")
        with pytest.raises(ValueError, match="voxelize"):
            inventory.voxelize()
        inventory.delete()


class TestExport:
    def test_export_returns_pending_export(self, completed_tree_inventory):
        export = completed_tree_inventory.export(format="csv")
        assert len(export.id) > 0
        assert export.domain_id == completed_tree_inventory.domain_id
        assert export.status in (
            JobStatus.PENDING,
            JobStatus.RUNNING,
            JobStatus.COMPLETED,
        )

    def test_invalid_format(self, completed_tree_inventory):
        with pytest.raises(ValueError):
            completed_tree_inventory.export(format="shapefile")


class TestInventoryData:
    def test_get_data_metadata(self, completed_tree_inventory):
        metadata = completed_tree_inventory.get_data_metadata()
        assert metadata.inventory_id == completed_tree_inventory.id
        assert metadata.num_partitions >= 1
        assert metadata.total_rows > 0
        assert len(metadata.columns) > 0

    def test_get_data_partition(self, completed_tree_inventory):
        # metadata.columns can carry a __null_dask_index__ backend artifact
        # that the partition responses correctly omit, so compare as subset
        metadata = completed_tree_inventory.get_data_metadata()
        partition = completed_tree_inventory.get_data_partition(0)
        assert partition.partition == 0
        assert partition.num_rows == metadata.partitions[0].num_rows
        assert set(partition.columns) <= set(metadata.columns)
        assert "height" in partition.columns
        assert len(partition.data) == partition.num_rows

    def test_to_dataframe(self, completed_tree_inventory):
        metadata = completed_tree_inventory.get_data_metadata()
        trees = completed_tree_inventory.to_dataframe()
        assert isinstance(trees, pd.DataFrame)
        assert len(trees) == metadata.total_rows
        assert set(trees.columns) <= set(metadata.columns)
        assert {"x", "y", "height"} <= set(trees.columns)

    def test_to_dataframe_column_subset(self, completed_tree_inventory):
        metadata = completed_tree_inventory.get_data_metadata()
        subset = metadata.columns[:2]
        trees = completed_tree_inventory.to_dataframe(columns=subset)
        assert list(trees.columns) == subset

    @pytest.fixture(scope="class")
    def completed_csv_export(self, completed_tree_inventory):
        """A completed CSV export of the shared tree inventory."""
        export = completed_tree_inventory.export(format="csv", tags=["test"])
        export.wait()
        return export

    def test_to_dataframe_matches_csv_export(
        self, completed_tree_inventory, completed_csv_export, tmp_path
    ):
        # Ground-truth check for to_dataframe: the records it loads from the
        # data partitions must match the same inventory the server renders to
        # a CSV and we read back with pandas. Row order is not guaranteed and
        # the CSV round-trips floats through text, so compare order- and
        # precision-independently: equal row count, shared columns, and the
        # same multiset of values per column. Reuses the export fixture.
        path = completed_csv_export.to_file(tmp_path / "trees.csv")
        from_csv = pd.read_csv(path)
        from_api = completed_tree_inventory.to_dataframe()

        shared = sorted(set(from_api.columns) & set(from_csv.columns))
        assert {"x", "y", "height"} <= set(shared)
        assert len(from_api) == len(from_csv)

        for column in shared:
            api_values = from_api[column].to_numpy()
            if not np.issubdtype(api_values.dtype, np.number):
                continue  # presence is already asserted via `shared`
            assert np.allclose(
                np.sort(api_values.astype(float)),
                np.sort(from_csv[column].to_numpy(dtype=float)),
                rtol=1e-4,
                atol=1e-4,
                equal_nan=True,
            )


class TestListInventories:
    def test_list_in_domain(self, test_domain, completed_tree_inventory):
        inventory_ids = [i.id for i in list_inventories(test_domain)]
        assert completed_tree_inventory.id in inventory_ids

    def test_list_cross_domain(self, completed_tree_inventory):
        # No domain: list inventories across all the user's domains
        inventory_ids = [i.id for i in list_inventories()]
        assert completed_tree_inventory.id in inventory_ids

    def test_filter_by_tag(self, test_domain, completed_tree_inventory):
        tagged = list_inventories(test_domain, tag="test")
        assert completed_tree_inventory.id in [i.id for i in tagged]

    def test_invalid_sort_field(self):
        with pytest.raises(ValueError):
            list_inventories(sort_by="not_a_field")


class TestToJson:
    def test_to_json(self, completed_tree_inventory):
        inventory_dict = json.loads(completed_tree_inventory.to_json())
        assert inventory_dict["id"] == completed_tree_inventory.id
        assert inventory_dict["domain_id"] == completed_tree_inventory.domain_id


class TestDeleteInventory:
    def test_delete(self, test_domain, completed_tree_inventory):
        inventory = completed_tree_inventory.duplicate(name="delete_test")
        inventory.delete()

        with pytest.raises(NotFoundException):
            Inventory.from_id(test_domain.id, inventory.id)

        with pytest.raises(NotFoundException):
            inventory.delete()
