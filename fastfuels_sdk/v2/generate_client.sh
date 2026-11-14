#!/usr/bin/env bash
# Regenerate the v2 client library (fastfuels_sdk/v2/client_library/) from
# the live API spec. Run from this directory: bash generate_client.sh
#
# Generated code is committed — rerun this when the v2 API spec changes
# and commit the diff so API-surface changes are reviewable in PRs.
#
# client_templates/ overrides the generator's enum templates so a value this
# SDK version doesn't know parses as an UNKNOWN member instead of raising.
#
# Requirements: uv (openapi-python-client is run via uvx, no install
# needed). The generator version is pinned so regen diffs reflect API
# changes only; bump the pin deliberately.
set -euo pipefail

OPC_VERSION="0.29.0"

URL="https://api.fastfuels.silvxlabs.com"
SPEC=$(mktemp /tmp/v2_openapi.XXXXXX.json)

# OPENAPI_SPEC: read a local spec file instead of the live one.
if [ -n "${OPENAPI_SPEC:-}" ]; then
  cp "$OPENAPI_SPEC" "$SPEC"
else
  curl -fsS "$URL/v2/openapi.json" > "$SPEC"
fi

uvx "openapi-python-client@${OPC_VERSION}" generate \
  --path "$SPEC" \
  --meta none \
  --output-path client_library \
  --custom-template-path client_templates \
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

rm -f "$SPEC"
echo "Done."
