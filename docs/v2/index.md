# Welcome to the FastFuels Python SDK Documentation!

!!! warning "Beta"
    You are reading the documentation for the **v2 SDK**, which targets
    the FastFuels v2 API and is under active development. The v1 SDK
    remains the default — switch versions with the selector in the
    header. Import v2 explicitly from `fastfuels_sdk.v2`.

## What is FastFuels?

FastFuels is a cloud-based platform for generating forest inventory data. It
uses a combination of satellite imagery and machine learning to generate
tabular tree data and voxelized 3D fuel models. These data products can be used
to support wildfire risk assessment, fire behavior modeling, and other
applications.

The [FastFuels documentation](https://docs.fastfuels.silvxlabs.com) covers
the platform itself: the web application, the HTTP API, and explanations of
the core concepts (domains, grids, inventories, features). This site covers
how to work with FastFuels from Python.

## What is the FastFuels Python SDK?

The FastFuels Python SDK is a Python package that provides a convenient
interface for interacting with the FastFuels API. It can be used to create and
manage FastFuels resources. It can also be used to download and process
generated data products.

## Installation

The FastFuels Python SDK can be installed using `pip`:

```bash
pip install fastfuels-sdk
```

## Using the v2 SDK

The v1 and v2 APIs are separate live services, and the SDK ships both as
versioned subpackages, so you can use them side by side during migration:

```python
from fastfuels_sdk.v1 import Domain   # v1 (current default)
from fastfuels_sdk.v2 import Domain   # v2 (Beta)
```

Coming from v1? Start with [Migrating from v1](guides/migration.md).
