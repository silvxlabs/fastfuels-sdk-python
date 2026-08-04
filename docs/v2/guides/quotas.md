# How to Check Usage and Handle Quota Rejections

!!! warning "Beta"
    The v2 SDK targets the FastFuels v2 API and is under active
    development. The v1 SDK remains the default — import v2 explicitly
    from `fastfuels_sdk.v2`.

## Prerequisites

- The FastFuels SDK installed: `pip install fastfuels-sdk`
- A FastFuels API key in the `FASTFUELS_API_KEY` environment variable

Use this guide to inspect the current owner's limits and usage and to handle
quota rejections from SDK resource creators.

## Check your limits

Call `get_quotas` to retrieve the limits resolved for the owner authenticated
by the current API key:

```python
import fastfuels_sdk.v2 as ff

quotas = ff.get_quotas()

print(quotas.max_active_grids)
print(quotas.max_weekly_grid_dispatches)
print(quotas.max_grid_storage_bytes)
```

## Check your current usage

Call `get_usage` to compare current usage with the corresponding limits:

```python
usage = ff.get_usage()

print(usage.grids.active.usage, usage.grids.active.limit)
print(usage.grids.total.usage, usage.grids.total.limit)
print(usage.grids.storage.usage_bytes, usage.grids.storage.limit_bytes)
```

Count-only resources are available through `usage.domains`,
`usage.applications`, and `usage.api_keys`. The active, total, and storage
fields are also available for exports, inventories, features, and point
clouds.

Inspect `usage.lifecycle` for the resource-retention policy currently applied
to the owner:

```python
print(usage.lifecycle.resource_ttl_days)
print(usage.lifecycle.failed_resource_ttl_days)
print(usage.lifecycle.next_expiry_on)
```

## Handle a quota rejection

Catch `QuotaExceededException` around any operation that creates or re-derives
a resource:

```python
import fastfuels_sdk.v2 as ff
from fastfuels_sdk.v2.exceptions import QuotaExceededException

try:
    grid = ff.grids.create_topography_grid_from_3dep(
        domain,
        output_resolution_m=30,
    )
except QuotaExceededException as exc:
    print(exc.quota, exc.current, exc.limit)
    print(exc.message)
    if exc.retry_after is not None:
        print(f"Retry in {exc.retry_after} seconds")
```

For an active-job limit, `retry_after` contains the number of seconds the API
recommends waiting before another attempt.

For a weekly dispatch limit, `window_reset_on` contains the reset time. Count
and storage limits provide neither retry field; delete unneeded resources or
request a higher limit before retrying.
