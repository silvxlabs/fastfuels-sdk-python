"""
fastfuels_sdk/v2/_jobs.py

Shared polling helper for job-based v2 resources (Feature, Grid,
Inventory). Private module: each resource exposes its own documented
``wait_until_completed`` method that delegates here.
"""

import time

from fastfuels_sdk.v2.client_library.models import JobStatus
from fastfuels_sdk.v2.client_library.types import Unset

_TERMINAL_STATUSES = (JobStatus.COMPLETED, JobStatus.FAILED)


def _format_job_error(resource, error) -> str:
    """Build a human-readable message from a generated JobError."""
    label = f"{type(resource).__name__} {resource.id}"
    if error is None or isinstance(error, Unset):
        return f"{label} failed (no error detail returned)."
    message = f"{label} failed [{error.code}]: {error.message}"
    suggestion = getattr(error, "suggestion", None)
    if suggestion and not isinstance(suggestion, Unset):
        message += f" Suggestion: {suggestion}"
    return message


def wait_until_completed(
    resource,
    step: float = 5,
    timeout: float = 600,
    in_place: bool = True,
    verbose: bool = False,
):
    """Poll a job resource until it reaches a terminal status.

    Duck-typed on the resource wrapper: requires ``get()``, ``status``,
    ``error``, ``id``, and ``_copy_fields_from()``.
    """
    elapsed = 0.0
    latest = resource.get()
    while latest.status not in _TERMINAL_STATUSES:
        if elapsed >= timeout:
            raise TimeoutError(
                f"{type(resource).__name__} {resource.id} did not complete "
                f"within {timeout} seconds"
            )
        time.sleep(step)
        elapsed += step
        latest = resource.get()
        if verbose:
            print(
                f"{type(resource).__name__} {resource.id}: "
                f"{latest.status} ({elapsed:.0f}s)"
            )
    if latest.status == JobStatus.FAILED:
        raise RuntimeError(_format_job_error(resource, latest.error))
    if in_place:
        return resource._copy_fields_from(latest)
    return latest
