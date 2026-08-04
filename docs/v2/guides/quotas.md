# How to Handle Quota Rejections

!!! warning "Beta"
    The v2 SDK targets the FastFuels v2 API and is under active
    development. The v1 SDK remains the default — import v2 explicitly
    from `fastfuels_sdk.v2`.

## Prerequisites

- The FastFuels SDK installed: `pip install fastfuels-sdk`
- A FastFuels API key in the `FASTFUELS_API_KEY` environment variable

Use this guide to handle quota rejections from SDK resource creators.

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
