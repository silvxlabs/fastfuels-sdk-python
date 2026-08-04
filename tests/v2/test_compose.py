"""Tests for v2 grid-compose builders and creator."""

from http import HTTPStatus

import numpy as np
import pytest

from fastfuels_sdk.v2 import compose, grids
from fastfuels_sdk.v2.client_library.models import (
    Band,
    BandType,
    ComposeComparisonOperator,
    ComposeCompute,
    ComposeLiteral,
    ComposeOperator,
    ComposeSelect,
    GridSource,
    InlineCompute,
    JobStatus,
)
from fastfuels_sdk.v2.client_library.types import Response
from fastfuels_sdk.v2.grids import (
    Grid,
    create_fuel_grid_from_fbfm40_lookup,
    create_grid_from_compose,
)


def _grid(
    id_="source-grid",
    domain_id="domain-id",
    status=JobStatus.COMPLETED,
    bands=None,
):
    return Grid(
        id=id_,
        domain_id=domain_id,
        status=status,
        source=GridSource(),
        bands=bands
        or [
            Band(
                key="fuel_load.1hr",
                type_=BandType.CONTINUOUS,
                index=0,
                unit="kg/m**2",
            ),
            Band(
                key="fuel_depth",
                type_=BandType.CONTINUOUS,
                index=1,
                unit="m",
            ),
        ],
    )


class TestComposeBuilders:
    def test_select(self):
        operation = compose.select("fuel_depth", "fuels.fuel_depth")

        assert isinstance(operation, ComposeSelect)
        assert operation.to_dict() == {
            "output": "fuel_depth",
            "from": "fuels.fuel_depth",
        }

    def test_compute(self):
        operation = compose.compute(
            "fuel_load.1hr",
            "multiply",
            ["fuels.fuel_load.1hr", 0.5],
            unit="kg/m**2",
        )

        assert isinstance(operation, ComposeCompute)
        assert operation.operator == ComposeOperator.MULTIPLY
        assert operation.to_dict() == {
            "operator": "multiply",
            "operands": ["fuels.fuel_load.1hr", 0.5],
            "output": "fuel_load.1hr",
            "unit": "kg/m**2",
        }

    def test_conditional_typed_literal_fallback(self):
        where = compose.condition("fuels.fbfm", "in", ["GR1", "GR2"])
        fallback = compose.literal(0, unit="kg/m**2")
        operation = compose.select(
            "fuel_load.1hr",
            "fuels.fuel_load.1hr",
            conditions=[where],
            else_=fallback,
        )

        assert where.operator == ComposeComparisonOperator.IN
        assert isinstance(fallback, ComposeLiteral)
        assert operation.to_dict()["conditions"] == [
            {
                "band": "fuels.fbfm",
                "operator": "in",
                "value": ["GR1", "GR2"],
            }
        ]
        assert operation.to_dict()["else"] == {
            "type": "literal",
            "value": 0,
            "unit": "kg/m**2",
        }

    def test_inline_compute(self):
        fallback = compose.inline_compute(
            "average",
            ["base.fuel_load.1hr", "alternate.fuel_load.1hr"],
        )

        assert isinstance(fallback, InlineCompute)
        assert fallback.to_dict() == {
            "operator": "average",
            "operands": [
                "base.fuel_load.1hr",
                "alternate.fuel_load.1hr",
            ],
        }

    @pytest.mark.parametrize(
        "operator,operands",
        [
            ("add", ["fuels.fuel_load.1hr"]),
            ("subtract", ["fuels.fuel_load.1hr", 1, 2]),
            ("divide", [1, 2]),
        ],
    )
    def test_compute_rejects_invalid_operands(self, operator, operands):
        with pytest.raises(ValueError):
            compose.compute("output", operator, operands)

    def test_condition_in_requires_list(self):
        with pytest.raises(ValueError, match="requires a list"):
            compose.condition("fuels.fbfm", "in", "GR1")

    def test_condition_ordering_requires_scalar(self):
        with pytest.raises(ValueError, match="requires a scalar"):
            compose.condition("fuels.fuel_depth", "gt", [0, 1])

    def test_conditions_require_fallback(self):
        with pytest.raises(ValueError, match="else_"):
            compose.select(
                "fuel_depth",
                "fuels.fuel_depth",
                conditions=[compose.condition("fuels.fuel_depth", "gt", 0)],
            )

    def test_string_literal_cannot_have_unit(self):
        with pytest.raises(ValueError, match="cannot carry a unit"):
            compose.literal("GR1", unit="kg/m**2")


class TestCreateGridFromCompose:
    def test_builds_request(self, monkeypatch):
        source = _grid()
        created = _grid(id_="composed-grid", status=JobStatus.PENDING)
        captured = {}

        def fake_create(domain_id, *, client, body):
            captured.update(domain_id=domain_id, client=client, body=body)
            return Response(
                status_code=HTTPStatus.CREATED,
                content=b"",
                headers={},
                parsed=created,
            )

        client = object()
        monkeypatch.setattr(grids, "ensure_client", lambda: client)
        monkeypatch.setattr(
            grids.create_compose_grid,
            "sync_detailed",
            fake_create,
        )

        result = create_grid_from_compose(
            {"fuels": source},
            select=[compose.select("fuel_depth", "fuels.fuel_depth")],
            compute=[
                compose.compute(
                    "fuel_load.1hr",
                    "multiply",
                    ["fuels.fuel_load.1hr", 0.5],
                )
            ],
            name="Composed fuels",
            tags=["test"],
        )

        assert result.id == "composed-grid"
        assert captured["domain_id"] == "domain-id"
        assert captured["client"] is client
        assert [item.to_dict() for item in captured["body"].inputs] == [
            {"grid_id": "source-grid", "alias": "fuels"}
        ]
        assert captured["body"].select[0].output == "fuel_depth"
        assert captured["body"].compute[0].operator == ComposeOperator.MULTIPLY
        assert captured["body"].name == "Composed fuels"
        assert captured["body"].tags == ["test"]

    @pytest.mark.parametrize(
        "inputs,match,error",
        [
            ([], "mapping", TypeError),
            ({}, "at least one", ValueError),
            ({"1bad": _grid()}, "Invalid compose alias", ValueError),
            (
                {"a": _grid(status=JobStatus.PENDING)},
                "Cannot compose",
                ValueError,
            ),
            (
                {"a": _grid(), "b": _grid()},
                "more than one alias",
                ValueError,
            ),
            (
                {"a": _grid(), "b": _grid(id_="other", domain_id="other")},
                "same domain",
                ValueError,
            ),
        ],
    )
    def test_rejects_invalid_inputs(self, inputs, match, error):
        with pytest.raises(error, match=match):
            create_grid_from_compose(
                inputs,
                select=[compose.select("fuel_depth", "a.fuel_depth")],
            )

    def test_requires_an_operation(self):
        with pytest.raises(ValueError, match="At least one"):
            create_grid_from_compose({"fuels": _grid()})

    def test_rejects_duplicate_outputs(self):
        with pytest.raises(ValueError, match="must be unique"):
            create_grid_from_compose(
                {"fuels": _grid()},
                select=[compose.select("fuel", "fuels.fuel_depth")],
                compute=[
                    compose.compute(
                        "fuel",
                        "multiply",
                        ["fuels.fuel_load.1hr", 0.5],
                    )
                ],
            )

    def test_rejects_empty_output(self):
        with pytest.raises(ValueError, match="nonempty output"):
            create_grid_from_compose(
                {"fuels": _grid()},
                select=[ComposeSelect(output="", from_="fuels.fuel_depth")],
            )

    @pytest.mark.parametrize(
        "reference,match",
        [
            ("other.fuel_depth", "Unknown compose band reference"),
            ("fuels.unknown", "has no 'unknown' band"),
        ],
    )
    def test_rejects_unknown_references(self, reference, match):
        with pytest.raises(ValueError, match=match):
            create_grid_from_compose(
                {"fuels": _grid()},
                select=[compose.select("fuel_depth", reference)],
            )

    def test_create_live(self, completed_fbfm40_grid):
        fuel_grid = create_fuel_grid_from_fbfm40_lookup(
            completed_fbfm40_grid,
            bands=["fuel_load.1hr", "fuel_depth"],
            name="test_compose_source",
            tags=["test"],
        )
        composed = None
        try:
            fuel_grid.wait()
            composed = create_grid_from_compose(
                {"fuels": fuel_grid},
                select=[compose.select("fuel_depth", "fuels.fuel_depth")],
                compute=[
                    compose.compute(
                        "fuel_load.1hr",
                        "multiply",
                        ["fuels.fuel_load.1hr", 0.5],
                        conditions=[compose.condition("fuels.fuel_load.1hr", "gt", 0)],
                        else_=compose.literal(0, unit="kg/m**2"),
                    )
                ],
                name="test_composed_fuels",
                tags=["test"],
            )
            composed.wait()
            assert composed.status == JobStatus.COMPLETED
            assert [band.key for band in composed.bands] == [
                "fuel_depth",
                "fuel_load.1hr",
            ]
            fuel_load = composed.to_numpy("fuel_load.1hr")
            assert fuel_load.ndim == 2
            assert np.isfinite(fuel_load).any()
        finally:
            if composed is not None:
                composed.delete()
            fuel_grid.delete()
