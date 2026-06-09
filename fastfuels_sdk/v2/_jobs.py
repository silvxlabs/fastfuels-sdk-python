"""
fastfuels_sdk/v2/_jobs.py

Shared polling helpers for job-based v2 resources (Feature, Grid,
Inventory). Private module: each resource exposes its own documented
``wait`` method that delegates to :func:`wait` here. :func:`wait_all` and
:class:`JobFailedError` are re-exported at the package top level.
"""

import time

from fastfuels_sdk.v2.client_library.models import JobStatus
from fastfuels_sdk.v2.client_library.types import Unset

_TERMINAL_STATUSES = (JobStatus.COMPLETED, JobStatus.FAILED)

# Server-side poll interval. Not user-tunable: the job runs server-side
# regardless of how often we poll, so the interval is an implementation
# detail rather than part of the wait contract.
_POLL_SECONDS = 5


class JobFailedError(Exception):
    """Raised when a job-based resource reaches the ``failed`` status.

    Attributes
    ----------
    code : str or None
        Machine-readable error code reported by the API (``None`` when the
        API returned no error detail).
    message : str or None
        Human-readable error message reported by the API.
    suggestion : str or None
        Actionable advice reported by the API, when present.
    """

    def __init__(self, display, *, code=None, message=None, suggestion=None):
        self.code = code
        self.message = message
        self.suggestion = suggestion
        super().__init__(display)


def _job_failed_error(resource, error) -> JobFailedError:
    """Build a :class:`JobFailedError` from a generated ``JobError``."""
    label = f"{type(resource).__name__} {resource.id}"
    if error is None or isinstance(error, Unset):
        return JobFailedError(f"{label} failed (no error detail returned).")
    suggestion = getattr(error, "suggestion", None)
    if isinstance(suggestion, Unset):
        suggestion = None
    display = f"{label} failed [{error.code}]: {error.message}"
    if suggestion:
        display += f" Suggestion: {suggestion}"
    return JobFailedError(
        display, code=error.code, message=error.message, suggestion=suggestion
    )


def wait(resource, timeout=None, verbose=False):
    """Poll a job resource until it reaches a terminal status.

    Duck-typed on the resource wrapper: requires ``refresh()``, ``status``,
    ``error``, and ``id``. Updates the resource in place on every poll and
    returns it, so calls chain.

    Parameters
    ----------
    resource
        A job-based resource wrapper (Feature, Grid, ...).
    timeout : float, optional
        Maximum seconds to wait. ``None`` (default) waits indefinitely; the
        job runs server-side regardless, so a bounded wait is resumable.
    verbose : bool, optional
        Print status updates while polling.

    Raises
    ------
    TimeoutError
        If ``timeout`` is set and elapsed before a terminal status.
    JobFailedError
        If the job reaches the ``failed`` status.
    """
    elapsed = 0.0
    resource.refresh()
    while resource.status not in _TERMINAL_STATUSES:
        if timeout is not None and elapsed >= timeout:
            raise TimeoutError(
                f"{type(resource).__name__} {resource.id} did not complete "
                f"within {timeout} seconds"
            )
        time.sleep(_POLL_SECONDS)
        elapsed += _POLL_SECONDS
        resource.refresh()
        if verbose:
            print(
                f"{type(resource).__name__} {resource.id}: "
                f"{resource.status} ({elapsed:.0f}s)"
            )
    if resource.status == JobStatus.FAILED:
        raise _job_failed_error(resource, resource.error)
    return resource


def wait_all(resources, timeout=None, verbose=False):
    """Wait for several job resources to reach a terminal status.

    Jobs run server-side in parallel, so creating resources without waiting
    and then joining them here runs the work concurrently. Resources are
    joined in iteration order; the first one to be found ``failed`` raises
    its :class:`JobFailedError`.

    Parameters
    ----------
    resources : iterable
        Job-based resource wrappers to wait on.
    timeout : float, optional
        Per-resource timeout in seconds (``None`` waits indefinitely).
    verbose : bool, optional
        Print status updates while polling.

    Returns
    -------
    list
        The resources, each updated in place to its terminal state.
    """
    resources = list(resources)
    for resource in resources:
        wait(resource, timeout=timeout, verbose=verbose)
    return resources
