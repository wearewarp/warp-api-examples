#!/usr/bin/env bash
# Book a previously quoted shipment.
# Pass the quote_id (from ./02-ltl-quote.sh, or any /*/quote response) as $1.
#
# With a wak_test_* sandbox key the booking is simulated — no card is charged.
# With a wak_live_* production key the card on file is charged at the quoted rate.
set -euo pipefail

: "${WARP_KEY:?Set WARP_KEY to a wak_test_* or wak_live_* key}"

QUOTE_ID="${1:-}"
if [ -z "$QUOTE_ID" ]; then
  echo "Usage: $0 <quote_id>"
  exit 1
fi

curl -fsS -X POST https://www.wearewarp.com/api/v1/book \
  -H "Authorization: Bearer $WARP_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"quote_id\": \"$QUOTE_ID\",
    \"reference\": \"PO-DEMO-001\"
  }"
