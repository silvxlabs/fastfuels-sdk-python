"""
tests/test_top_level_namespace.py

Offline tests for the lazy v1 re-export in ``fastfuels_sdk/__init__.py``.
No API key or network needed.
"""

import subprocess
import sys

import pytest

import fastfuels_sdk
import fastfuels_sdk.v1


def _run(code: str) -> str:
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


@pytest.mark.parametrize(
    "statement", ["import fastfuels_sdk.v2", "from fastfuels_sdk import v2"]
)
def test_importing_v2_does_not_load_v1(statement):
    out = _run(
        f"import sys; {statement}; "
        "print(any(m == 'fastfuels_sdk.v1' or m.startswith('fastfuels_sdk.v1.') "
        "for m in sys.modules))"
    )
    assert out == "False"


def test_top_level_access_loads_v1_lazily():
    out = _run(
        "import sys, fastfuels_sdk; "
        "before = 'fastfuels_sdk.v1' in sys.modules; "
        "from fastfuels_sdk import Domain; "
        "import fastfuels_sdk.v1 as v1; "
        "print(before, Domain is v1.Domain)"
    )
    assert out == "False True"


@pytest.mark.parametrize("name", fastfuels_sdk.v1.__all__)
def test_v1_names_are_exposed_at_top_level(name):
    assert getattr(fastfuels_sdk, name) is getattr(fastfuels_sdk.v1, name)


def test_star_import_matches_v1_all():
    namespace = {}
    exec("from fastfuels_sdk import *", namespace)
    namespace.pop("__builtins__")
    assert set(namespace) == set(fastfuels_sdk.v1.__all__)


def test_all_matches_v1_all():
    assert list(fastfuels_sdk.__all__) == list(fastfuels_sdk.v1.__all__)


def test_dir_lists_public_names():
    assert set(fastfuels_sdk.v1.__all__) <= set(dir(fastfuels_sdk))


def test_unknown_attribute_raises_attribute_error():
    with pytest.raises(AttributeError, match="no attribute 'NotAThing'"):
        fastfuels_sdk.NotAThing
    with pytest.raises(ImportError):
        from fastfuels_sdk import NotAThing  # noqa: F401
