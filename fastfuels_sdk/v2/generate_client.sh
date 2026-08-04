#!/usr/bin/env bash
# Regenerate the v2 client library (fastfuels_sdk/v2/client_library/) from
# the live API spec. Run from this directory: bash generate_client.sh
#
# Generated code is committed — rerun this when the v2 API spec changes
# and commit the diff so API-surface changes are reviewable in PRs.
#
# Requirements: uv (openapi-python-client is run via uvx, no install
# needed). The generator version is pinned so regen diffs reflect API
# changes only; bump the pin deliberately.
set -euo pipefail

OPC_VERSION="0.29.0"

URL="https://api-v2-prod-782971006568.us-west1.run.app"
SPEC=$(mktemp /tmp/v2_openapi.XXXXXX.json)
PATCHED=$(mktemp /tmp/v2_openapi_patched.XXXXXX.json)

curl -s "$URL/openapi.json" > "$SPEC"

# openapi-python-client names classes from schema titles and refuses
# duplicates, dropping the endpoints that reference the loser. The spec has
# two such collisions, so re-title one side of each. Long-term fix: re-title
# the models in the FastFuels-API-v2 repo so the spec has no collision.
#
#   "Feature" — the FastFuels feature resource vs geojson_pydantic's GeoJSON
#   Feature (auto-namespaced by FastAPI, but still titled "Feature").
#
#   "ThreeDepCoverageResponse" — the point cloud 3DEP pre-flight check
#   (point count / budget) vs the topography one (tiles / resolution).
python3 - "$SPEC" "$PATCHED" <<'EOF'
import json, sys
spec = json.load(open(sys.argv[1]))
schemas = spec["components"]["schemas"]
schemas["geojson_pydantic__features__Feature"]["title"] = "GeoJsonFeature"
schemas["ThreeDepCoverageResponse"]["title"] = "PointCloudThreeDepCoverageResponse"
json.dump(spec, open(sys.argv[2], "w"))
EOF

uvx "openapi-python-client@${OPC_VERSION}" generate \
  --path "$PATCHED" \
  --meta none \
  --output-path client_library \
  --overwrite

# openapi-python-client embeds no server URL (the spec has no `servers`
# entry, and the generated client takes base_url at construction time), so
# record the deployment URL this client was generated against. api.py
# imports it as the SDK default — this script is the single source of
# truth for the URL.
cat > client_library/base_url.py <<EOF
"""Deployment URL of the FastFuels v2 API this client was generated against.

Written by generate_client.sh (the OpenAPI spec carries no \`servers\`
entry and openapi-python-client takes base_url at construction time, so
the regen script records the URL alongside the client it generates).
"""

DEFAULT_BASE_URL = "$URL"
EOF

rm -f "$SPEC" "$PATCHED"
echo "Done."
