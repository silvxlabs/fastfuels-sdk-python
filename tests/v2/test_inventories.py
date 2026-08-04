"""
tests/v2/test_inventories.py
"""

# Core imports
import json
from http import HTTPStatus
from types import SimpleNamespace
from uuid import uuid4

# Internal imports
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
    CategoricalColumnSummary,
    Column,
    ColumnType,
    ContinuousColumnSummary,
    FIASpeciesGroupShare,
    Inventory as InventoryModel,
    InventoryAttribute,
    InventoryDataResponse,
    InventoryJsonOrientation,
    InventoryModification,
    InventoryModificationAction,
    InventoryModificationCondition,
    InventorySource,
    InventoryType,
    JobStatus,
    Modifier,
    Operator,
    TreeForestryMetrics,
)
from fastfuels_sdk.v2.client_library.types import UNSET, Response
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


class TestForestryMetrics:
    @staticmethod
    def _model(forestry_metrics=UNSET):
        return InventoryModel(
            id="inventory-id",
            domain_id="domain-id",
            type_=InventoryType.TREE,
            status=JobStatus.COMPLETED,
            source=InventorySource(),
            forestry_metrics=forestry_metrics,
        )

    def test_wraps_metrics_record(self):
        metrics = TreeForestryMetrics(
            type_="tree",
            tree_count=120,
            basal_area_per_area=87.5,
            tree_density=240.0,
            quadratic_mean_diameter=9.4,
            dominant_species_groups=[
                FIASpeciesGroupShare(
                    spgrpcd=3,
                    name="Douglas-fir",
                    basal_area_share=0.62,
                )
            ],
        )

        inventory = Inventory._from_model(self._model(metrics))

        assert isinstance(inventory.forestry_metrics, TreeForestryMetrics)
        assert inventory.forestry_metrics.tree_count == 120
        assert inventory.forestry_metrics.dominant_species_groups[0].spgrpcd == 3

    def test_normalizes_missing_metrics_to_none(self):
        inventory = Inventory._from_model(self._model())

        assert inventory.forestry_metrics is None

    def test_completed_inventory_metrics_live(self, completed_tree_inventory):
        metrics = completed_tree_inventory.forestry_metrics

        assert isinstance(metrics, TreeForestryMetrics)
        assert metrics.type_ == "tree"
        assert (
            metrics.tree_count
            == completed_tree_inventory.get_data_metadata().total_rows
        )
        assert metrics.basal_area_per_area > 0
        assert metrics.tree_density > 0
        assert metrics.quadratic_mean_diameter > 0
        assert len(metrics.dominant_species_groups) > 0
        assert [
            group.basal_area_share for group in metrics.dominant_species_groups
        ] == (
            sorted(
                (group.basal_area_share for group in metrics.dominant_species_groups),
                reverse=True,
            )
        )


class TestColumnSummary:
    @staticmethod
    def _inventory_with_column(column):
        return Inventory(
            id="inventory-id",
            domain_id="domain-id",
            type_=InventoryType.TREE,
            status=JobStatus.COMPLETED,
            source=InventorySource(),
            columns=[column],
        )

    def test_returns_continuous_summary(self):
        summary = ContinuousColumnSummary(
            type_="continuous",
            count=10,
            null_count=0,
            min_=1.0,
            max_=5.0,
            mean=3.0,
            std=1.0,
        )
        inventory = self._inventory_with_column(
            Column(key="dbh", type_=ColumnType.CONTINUOUS, summary=summary)
        )

        assert inventory.column_summary("dbh") is summary
        assert inventory.column_summary("dbh").mean == 3.0

    def test_returns_categorical_summary(self):
        summary = CategoricalColumnSummary(
            type_="categorical", count=10, null_count=1, unique_count=3
        )
        inventory = self._inventory_with_column(
            Column(
                key="fia_species_code",
                type_=ColumnType.CATEGORICAL,
                summary=summary,
            )
        )

        assert inventory.column_summary("fia_species_code") is summary
        assert inventory.column_summary("fia_species_code").unique_count == 3

    def test_none_when_not_computed(self):
        inventory = self._inventory_with_column(
            Column(key="dbh", type_=ColumnType.CONTINUOUS)
        )

        assert inventory.column_summary("dbh") is None

    def test_unknown_column_raises(self):
        inventory = self._inventory_with_column(
            Column(key="dbh", type_=ColumnType.CONTINUOUS)
        )

        with pytest.raises(ValueError, match="no column"):
            inventory.column_summary("height")

    def test_summaries_live(self, completed_tree_inventory):
        dbh = completed_tree_inventory.column_summary("dbh")
        species = completed_tree_inventory.column_summary("fia_species_code")
        tree_count = completed_tree_inventory.get_data_metadata().total_rows

        assert isinstance(dbh, ContinuousColumnSummary)
        assert dbh.type_ == "continuous"
        assert dbh.count == tree_count
        assert dbh.null_count == 0
        assert dbh.mean > 0

        assert isinstance(species, CategoricalColumnSummary)
        assert species.type_ == "categorical"
        assert species.count == tree_count
        assert species.null_count == 0
        assert species.unique_count > 0


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
    def test_apply_modifications_rederives_in_place(self, throwaway_inventory):
        copy = throwaway_inventory
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
        assert copy.status == JobStatus.PENDING
        assert copy.modifications == []  # ledger grows only after completion
        assert copy.checksum != original_checksum  # rotates at dispatch
        copy.wait()
        assert copy.status == JobStatus.COMPLETED
        assert len(copy.modifications) == 1
        assert copy.checksum != original_checksum  # data was re-derived

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
        # Verify the builders independently through the create-time path. Use
        # the same seed as the unmodified fixture so removing dbh < 10 must
        # yield strictly fewer trees.
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
    @staticmethod
    def _inventory():
        return Inventory(
            id="inventory-id",
            domain_id="domain-id",
            type_=InventoryType.TREE,
            status=JobStatus.COMPLETED,
            source=InventorySource(),
        )

    def test_get_data_partition_passes_json_orientation(self, monkeypatch):
        captured = {}

        def fake_get(domain_id, inventory_id, partition_index, **kwargs):
            captured.update(
                domain_id=domain_id,
                inventory_id=inventory_id,
                partition_index=partition_index,
                **kwargs,
            )
            return Response(
                status_code=HTTPStatus.OK,
                content=b"",
                headers={},
                parsed=InventoryDataResponse(
                    partition=partition_index,
                    num_rows=1,
                    columns=["height"],
                    data=[{"height": 12.0}],
                ),
            )

        client = object()
        monkeypatch.setattr(
            "fastfuels_sdk.v2.inventories.ensure_client", lambda: client
        )
        monkeypatch.setattr(
            "fastfuels_sdk.v2.inventories.get_inventory_data_json.sync_detailed",
            fake_get,
        )

        partition = self._inventory().get_data_partition(
            2, columns=["height"], json_orientation="records"
        )

        assert partition.data == [{"height": 12.0}]
        assert captured == {
            "domain_id": "domain-id",
            "inventory_id": "inventory-id",
            "partition_index": 2,
            "client": client,
            "json_orientation": InventoryJsonOrientation.RECORDS,
            "columns": "height",
        }

    def test_get_data_partition_rejects_invalid_orientation(self):
        with pytest.raises(ValueError, match="not a valid InventoryJsonOrientation"):
            self._inventory().get_data_partition(0, json_orientation="columns")

    def test_to_dataframe_uses_csv_partitions(self, monkeypatch):
        inventory = self._inventory()
        metadata = SimpleNamespace(
            num_partitions=2, total_rows=3, columns=["x", "height"]
        )
        csv_partitions = [
            "x,height\n1.0,10.0\n2.0,20.0\n",
            "x,height\n3.0,30.0\n",
        ]
        captured = []

        def fake_csv(domain_id, inventory_id, partition_index, **kwargs):
            captured.append((domain_id, inventory_id, partition_index, kwargs))
            return Response(
                status_code=HTTPStatus.OK,
                content=csv_partitions[partition_index].encode(),
                headers={},
                parsed=csv_partitions[partition_index],
            )

        def fail_json(*args, **kwargs):
            raise AssertionError("to_dataframe must use the CSV endpoint")

        client = object()
        monkeypatch.setattr(inventory, "get_data_metadata", lambda: metadata)
        monkeypatch.setattr(
            "fastfuels_sdk.v2.inventories.ensure_client", lambda: client
        )
        monkeypatch.setattr(
            "fastfuels_sdk.v2.inventories.get_inventory_data_csv.sync_detailed",
            fake_csv,
        )
        monkeypatch.setattr(
            "fastfuels_sdk.v2.inventories.get_inventory_data_json.sync_detailed",
            fail_json,
        )

        trees = inventory.to_dataframe(columns=["x", "height"])

        assert trees.to_dict(orient="list") == {
            "x": [1.0, 2.0, 3.0],
            "height": [10.0, 20.0, 30.0],
        }
        assert [call[2] for call in captured] == [0, 1]
        assert all(
            call[3] == {"client": client, "columns": "x,height"} for call in captured
        )

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

    def test_get_data_partition_records(self, completed_tree_inventory):
        partition = completed_tree_inventory.get_data_partition(
            0, columns=["height"], json_orientation="records"
        )

        assert partition.columns == ["height"]
        assert len(partition.data) == partition.num_rows
        assert set(partition.data[0]) == {"height"}

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
