# How to Check Usage and Handle Quota Rejections

This guide shows how to inspect the limits and usage of the account behind
your API key and how to handle quota rejections from SDK resource creators.
For how quotas and resource retention work, see
[About quotas](https://docs.fastfuels.silvxlabs.com/v2/api/explanation/quotas/)
in the FastFuels documentation.

## Prerequisites

- The FastFuels SDK installed: `pip install fastfuels-sdk`
- A FastFuels API key in the `FASTFUELS_API_KEY` environment variable

## Check your limits

To retrieve the limits that apply to the account behind the current API key,
call `get_quotas`:

```python
import fastfuels_sdk.v2 as ff

quotas = ff.get_quotas()

print(quotas.max_active_grids)
print(quotas.max_weekly_grid_dispatches)
print(quotas.max_grid_storage_bytes)
```

## Check your current usage

To compare current usage with the corresponding limits, call `get_usage`:

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

To see the resource-retention policy applied to the account, inspect
`usage.lifecycle`:

```python
print(usage.lifecycle.resource_ttl_days)
print(usage.lifecycle.failed_resource_ttl_days)
print(usage.lifecycle.next_expiry_on)
```

## Handle a quota rejection

To handle a rejection, catch `QuotaExceededException` around any operation
that creates or re-derives a resource:

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
