"""
tests/v2/test_uploads.py

Unit tests for the shared signed-upload helper (no API).
"""

# Core imports
from types import SimpleNamespace

# Internal imports
from fastfuels_sdk.v2._uploads import put_upload
from fastfuels_sdk.v2.client_library.models import GridUploadSpecHeaders

# External imports
import pytest
import requests


def _spec(url, header_dict):
    """A minimal upload spec: a signed URL plus the server-provided headers."""
    headers = GridUploadSpecHeaders()
    for key, value in header_dict.items():
        headers[key] = value
    return SimpleNamespace(
        url=url, headers=headers, content_type=header_dict.get("Content-Type")
    )


class _FakeResponse:
    def __init__(self, status_code=200):
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(str(self.status_code))


def test_put_upload_echoes_server_headers(tmp_path, monkeypatch):
    # The signed URL covers BOTH Content-Type and the GCS content-length-range;
    # the PUT must send exactly the server-provided header set -- no more, no
    # less -- or GCS rejects it with 403.
    server_headers = {
        "Content-Type": "image/tiff",
        "x-goog-content-length-range": "0,1073741824",
    }
    spec = _spec("https://upload.example/signed", server_headers)
    path = tmp_path / "raster.tif"
    path.write_bytes(b"\x00\x01\x02data")

    captured = {}

    def fake_put(url, data=None, headers=None):
        captured["url"] = url
        captured["headers"] = headers
        captured["data"] = data.read()
        return _FakeResponse(200)

    monkeypatch.setattr(requests, "put", fake_put)

    put_upload(spec, str(path))

    assert captured["url"] == "https://upload.example/signed"
    assert captured["headers"] == server_headers  # incl. x-goog-content-length-range
    assert captured["data"] == b"\x00\x01\x02data"  # file streamed to the PUT


def test_put_upload_raises_on_http_error(tmp_path, monkeypatch):
    spec = _spec("https://upload.example/signed", {"Content-Type": "text/csv"})
    path = tmp_path / "trees.csv"
    path.write_text("x,y\n")

    monkeypatch.setattr(requests, "put", lambda *a, **k: _FakeResponse(403))

    with pytest.raises(requests.HTTPError):
        put_upload(spec, str(path))
