# v2 Client Library Generator Comparison

> **Status: decision executed (2026-06-05).** openapi-python-client won;
> its output now lives at `fastfuels_sdk/v2/client_library/` and the
> `draft_*_opc.py` modules import from there. The openapi-generator tree
> and the `draft_*_oag.py` modules have been deleted (regenerable via the
> recipe below if the comparison ever needs to be revisited). This
> document is the record of the evaluation.

Two complete generated clients for the FastFuels v2 API (OpenAPI **3.1**,
FastAPI, pydantic/geojson-pydantic), each exercised through **four pairs of
draft wrapper modules** at v1-parity ergonomics, structured identically so
each `diff draft_X_oag.py draft_X_opc.py` reads as generator differences
only (`NOTE (comparison)` comments mark each forced divergence):

| Resource | Drafts | Endpoints covered |
|---|---|---|
| Domains | `draft_domains_{oag,opc}.py` | create (from_geojson / from_geodataframe / from_file), get, update, delete, list, to_geodataframe/to_json |
| Grids | `draft_grids_{oag,opc}.py` | LANDFIRE FBFM40, TreeMap (PIM), 3DEP topography/elevation; get, wait_until_completed, delete, list |
| Features | `draft_features_{oag,opc}.py` | OSM road, OSM water; get, wait_until_completed, update, delete, list |
| Inventories | `draft_inventories_{oag,opc}.py` | **PIM grid → tree inventory** (`create_from_pim_grid`); get, wait_until_completed, delete, list |

| | openapi-generator 7.22.0 | openapi-python-client 0.29.0 |
|---|---|---|
| Stack | pydantic v2 + urllib3 (same as v1) | attrs + httpx |
| Imports | absolute (fixed via dotted `--package-name`) | relative (relocatable as-is) |
| OpenAPI 3.1 support | "still in beta" (generator warning) | native |
| Generated size | 209 model files, **29 \*Api classes** (multi-tag operations duplicated into one class per tag) | 195 model files, 11 api/ packages (one per resource) |
| Functional against the live API | domains: **no** (broken geometry codegen); grids/features/inventories: yes (geometry-free payloads) | all resources: yes |

## Verdict: openapi-python-client

The deciding criterion is `anyOf` handling (next section): the v2 spec is
saturated with `anyOf`, openapi-generator's treatment of it ranges from
awkward (wrapper objects) to broken (geometry parsing crashes), and this
is structural to how FastAPI emits specs — not fixable by waiting.
openapi-generator's genuine advantages — typed exceptions and the
v1-familiar per-resource Api classes — are thin layers that the real v2
wrappers can recreate over opc (see Design notes).

## Why `anyOf` is the deciding criterion

The v2 spec contains **202 `anyOf` occurrences across 68 of 177 schemas
(38%)**. This is structural: FastAPI + pydantic v2 emit OpenAPI 3.1 where
every `Optional[X]` field becomes `anyOf: [X, null]`, and geojson-pydantic
contributes geometry unions and `Position2D | Position3D` coordinate
arrays. Four resource pairs gave a precise taxonomy of how each generator
copes:

| `anyOf` shape | Example | openapi-generator | openapi-python-client |
|---|---|---|---|
| `[X, null]` (nullable scalar/model) | `Feature.georeference`, `Grid.progress` | OK — `Optional[X]` | OK — `X \| None \| Unset` |
| `[X, Y, null]` (multi-model union) | `Grid.georeference` (2D/3D) | **wrapper dispatcher object** (`Georeference1(actual_instance=...)`) | native union — plain `Georeference` |
| union with plain values | `Domain.bbox` (4- or 6-tuple), `Band.nodata` | **wrapper models** (`Bbox(actual_instance=[...])`, `Nodata`) that reject plain values | plain `list[float]` / `int` |
| nested array unions (GeoJSON coordinates) | every geometry | **broken generated code** — `List[CoordinatesInner].from_dict(...)` raises `AttributeError`; the anyOf dispatcher only catches `ValidationError`, so parsing ANY domain crashes | parses to the right class (`Polygon`) |

Reproduce the domains blocker:

```python
from fastfuels_sdk.v2.draft_domains_oag import Domain
Domain.from_file("tests/data/blue_mtn.geojson")
# AttributeError: type object 'list' has no attribute 'from_dict'
# (crashes in the generated client before any API call is made)
```

The grids/features/inventories drafts sharpened the picture: their
payloads are geometry-free, so the oag client *parses them* — the hard
blocker is specifically geojson-pydantic's coordinate schemas, i.e.
exactly the schemas every Domain response contains.

## What writing every wrapper twice revealed

**546 of ~800 non-blank lines (≈ 68%) are identical across the four
pairs** (domains 187/287, grids 141/194, features 122/180, inventories
96/138). Everything that makes the SDK an SDK — geopandas conversions,
CRS forwarding, job polling, v1 ergonomics, docstrings — is
generator-independent. The differing third is plumbing:

| Aspect | openapi-generator (oag) | openapi-python-client (opc) |
|---|---|---|
| Client bootstrap | `Configuration` → `ApiClient` → one `*Api` object **per resource** (each draft repeats the bootstrap; a real impl needs a v1-style `api.py`) | one `AuthenticatedClient(base_url, token, prefix="", auth_header_name="api-key")` imported by every draft |
| Endpoint call | `get_grids_api().get_grid(domain_id, grid_id)` | `get_grid.sync(domain_id, grid_id, client=...)` — module-per-endpoint functions |
| Error handling | **typed exceptions raised natively** (`NotFoundException`, `UnprocessableEntityException`, `ServiceException`) — same as v1 | returns documented error models (a 422 is a returned `HTTPValidationError` object, even with `raise_on_unexpected_status=True`); drafts share a `_checked()` unwrapper |
| Model ↔ wrapper conversion | `cls.from_dict(model.to_dict())` — the v1 `cls(**model.model_dump())` pattern **breaks** on anyOf wrapper fields | `cls.from_dict(model.to_dict())` — `from_dict` constructs `cls`, so subclassing just works |
| Request body construction | `from_dict` only (kwargs construction rejects plain values for anyOf wrapper fields) | `from_dict` or kwargs both work |
| `to_dict()` output | **leaks enum objects** (`LandfireFbfm40Version.ENUM_2024`, `PointProcess.INHOMOGENEOUS_POISSON`) — not JSON-safe without `to_json()` | plain values (`"2024"`, `"inhomogeneous_poisson"`) |
| "absent field" sentinel | `None` — conflates *omit* with *set to null*; PATCH bodies rely on `to_dict()` dropping `None`s | explicit `UNSET` sentinel — omitted fields stay out of the PATCH body by construction |
| Field-copy idiom (in-place refresh) | `for f in Model.model_fields: setattr(...)` | `for f in attrs.fields(Model): setattr(...)` + `additional_properties` |
| Reserved-ish names | `type` | `type_` |
| Digit-leading op names | `create3dep_topography` | `create_3dep_topography` |
| API surface organization | 29 `*Api` classes for 11 resources (operations duplicated per tag: `create_osm_road_feature` lives in both `FeaturesApi` and `FeaturesRoadApi`) | 11 `api/<resource>/` packages, one module per operation |
| Async | none | free `asyncio`/`asyncio_detailed` variants of every endpoint |

Shared findings (identical code in both drafts):

- **v2 collapses v1's per-type resources** (surface/tree/topography grids;
  road/water features) into unified job-based resources distinguished by
  `source`/`type`. Grid, Feature, and Inventory all share the same
  `status`/`progress`/`error` lifecycle — `wait_until_completed` is
  line-identical across all six job-resource drafts, in both stacks
  (`JobStatus` is exported under the same name by both clients).
- The **PIM workflow** chains cleanly through the wrappers:
  `Grid.create_treemap(...)` → `wait_until_completed()` →
  `Inventory.create_from_pim_grid(domain_id, grid.id)` → `wait_until_completed()`.
- Spec details encoded in both drafts: creation `version` fields are
  *string* enums (`"2024"`); 3DEP `source_resolution` is an int enum
  (1/10/30); `Band` objects in responses vs band-name strings in requests;
  `FeatureGeoreference.bounds` is required.

## What openapi-python-client needed

1. **A spec patch**: the spec has two schemas titled `Feature`
   (the FastFuels feature resource and geojson-pydantic's GeoJSON
   Feature). opc names classes from titles and refuses duplicates —
   without the patch it silently drops every domain endpoint.
   `generate_client.sh` re-titles the GeoJSON one to `GeoJsonFeature`.
   The proper fix is in FastFuels-API-v2 (re-title the model) so the spec
   has no collision.
2. **Dependencies**: `httpx`, `attrs`, `python-dateutil` (currently in the
   dev group; move to runtime deps when v2 ships).

## Design notes for the real v2 wrappers (carried out of the drafts)

- **Shared job-resource base.** Grid/Feature/Inventory repeat identical
  `get`/`wait_until_completed`/`delete`/`_copy_fields_from` code — the
  real SDK should factor a `_JobResource` mixin (status polling, error
  raising, in-place refresh) used by all three.
- **`fastfuels_sdk/v2/exceptions.py`** translating opc's returned error
  models / `UnexpectedStatus` into typed SDK exceptions
  (`NotFoundException`, ...) — recreates v1 (and oag) ergonomics. The
  drafts' shared `_checked()` is the seed.
- **One cached `AuthenticatedClient`** (the drafts' `get_client()`)
  replaces v1's per-resource API singletons in `api.py`.
- The `Resource(GeneratedModel)` subclass pattern carries over from v1:
  opc's generated `from_dict` constructs `cls`, so classmethod
  constructors and in-place refresh work unchanged.
- `from_geodataframe` now forwards the GeoDataFrame CRS (v1 silently
  dropped it and relied on the EPSG:4326 default — latent bug for
  projected inputs).
- v1's `Domain.export()` has no v2 endpoint; v2-only endpoints
  (preview/reproject domain, domain lattice, feature/inventory data
  partitions, grid data/exports) are unwrapped so far.

## Regeneration

```bash
cd fastfuels_sdk/v2 && bash generate_client.sh   # regenerates client_library/
```

To reproduce the deleted openapi-generator client for re-evaluation:

```bash
openapi-generator generate -i <spec> -g python \
  --package-name fastfuels_sdk.v2.client_library_openapi_generator -o <tmp>
```

Remaining cleanup: the scratch `fastfuels_sdk/client_library_v2/` tree
(pre-dating this comparison) is fully superseded; the `draft_*_opc.py`
modules become the seeds of the real v2 wrappers.
