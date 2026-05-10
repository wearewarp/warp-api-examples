#!/usr/bin/env bash
# Mint a sandbox (wak_test_*) key from a production (wak_live_*) key.
# Sandbox keys can quote and simulate bookings without charging the card on file.
#
# To get a wak_live_* key in the first place, sign up at:
#   https://www.wearewarp.com/agents/account
set -euo pipefail

: "${WARP_LIVE_KEY:?Set WARP_LIVE_KEY to a wak_live_* key}"

curl -fsS -X POST https://www.wearewarp.com/api/v1/agents/sandbox-key \
  -H "Authorization: Bearer $WARP_LIVE_KEY" \
  -H "Content-Type: application/json"
