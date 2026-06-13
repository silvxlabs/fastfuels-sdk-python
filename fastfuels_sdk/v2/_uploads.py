"""
fastfuels_sdk/v2/_uploads.py

Shared helper for uploading a local file to a signed upload URL. Used by every
upload creator (grids, inventories, point clouds) so the signed-header contract
lives in exactly one place.
"""

# External imports
import requests


def put_upload(spec, path: str) -> None:
    """Upload a local file to a signed upload URL with HTTP PUT.

    The API signs the upload URL against a specific set of headers -- the
    ``Content-Type`` and a GCS ``x-goog-content-length-range`` -- and returns
    them in ``spec.headers``. The PUT must echo those headers *exactly* (no
    more, no less) or GCS rejects it with 403, so this sends the server-provided
    set verbatim rather than reconstructing it.

    Parameters
    ----------
    spec : upload spec
        An upload spec carrying ``url`` and ``headers`` (a
        ``*UploadSpecHeaders`` model), as returned by the create endpoints.
    path : str
        Path to the local file to upload.

    Raises
    ------
    requests.HTTPError
        If the signed PUT returns a non-2xx status.
    """
    headers = dict(spec.headers.to_dict())
    with open(path, "rb") as file_obj:
        response = requests.put(spec.url, data=file_obj, headers=headers)
    response.raise_for_status()
