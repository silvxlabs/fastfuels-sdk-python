#!/usr/bin/env bash
# Regenerate the v2 client library (openapi-python-client).
# Run from this directory: bash generate_clients.sh
#
# Requirements: uv (openapi-python-client is run via uvx, no install needed)
set -euo pipefail

URL="https://api-v2-prod-782971006568.us-west1.run.app"
SPEC=$(mktemp /tmp/v2_openapi.XXXXXX.json)
PATCHED=$(mktemp /tmp/v2_openapi_patched.XXXXXX.json)

curl -s "$URL/openapi.json" > "$SPEC"

# The spec contains two schemas titled "Feature": the FastFuels feature
# resource and geojson_pydantic's GeoJSON Feature (auto-namespaced by
# FastAPI as geojson_pydantic__features__Feature, but with title "Feature").
# openapi-python-client names classes from titles and refuses duplicates,
# so re-title the GeoJSON one. Long-term fix: re-title the model in the
# FastFuels-API-v2 repo so the spec has no collision.
python3 - "$SPEC" "$PATCHED" <<'EOF'
import json, sys
spec = json.load(open(sys.argv[1]))
spec["components"]["schemas"]["geojson_pydantic__features__Feature"]["title"] = "GeoJsonFeature"
json.dump(spec, open(sys.argv[2], "w"))
EOF

uvx openapi-python-client generate \
  --path "$PATCHED" \
  --meta none \
  --output-path client_library \
  --overwrite

rm -f "$SPEC" "$PATCHED"
echo "Done."
