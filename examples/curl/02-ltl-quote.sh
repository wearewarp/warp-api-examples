#!/usr/bin/env bash
# Quote an LTL shipment from Los Angeles to San Francisco.
# Pickup is 7 days from now. Returns a quote_id you pass to ./03-book.sh.
set -euo pipefail

: "${WARP_KEY:?Set WARP_KEY to a wak_test_* or wak_live_* key}"

# Pickup date 7 days from now (works on macOS and GNU date)
PICKUP_DATE=$(date -v+7d +%Y-%m-%d 2>/dev/null || date -d '+7 days' +%Y-%m-%d)

curl -fsS -X POST https://www.wearewarp.com/api/v1/ltl/quote \
  -H "Authorization: Bearer $WARP_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"origin_zip\": \"90012\",
    \"destination_zip\": \"94105\",
    \"pickup_date\": \"$PICKUP_DATE\",
    \"pallets\": 2,
    \"weight_lbs_per_pallet\": 800,
    \"commodity\": \"auto parts\"
  }"
