#!/usr/bin/env bash
# Get the current status and event timeline for a booked shipment.
# Pass the booking_id (returned from POST /book as shipment_id) as $1.
set -euo pipefail

: "${WARP_KEY:?Set WARP_KEY to a wak_test_* or wak_live_* key}"

BOOKING_ID="${1:-}"
if [ -z "$BOOKING_ID" ]; then
  echo "Usage: $0 <booking_id>"
  exit 1
fi

curl -fsS -G "https://www.wearewarp.com/api/v1/track" \
  --data-urlencode "booking_id=$BOOKING_ID" \
  -H "Authorization: Bearer $WARP_KEY"
