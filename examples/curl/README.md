# curl examples

End-to-end shell quickstarts for the Warp Freight API.

## Setup

```bash
# Get a sandbox key from https://www.wearewarp.com/agents/account
export WARP_KEY="wak_test_YOUR_SANDBOX_KEY"
```

## Run

```bash
chmod +x *.sh

./01-sandbox-key.sh    # mint a sandbox key from a wak_live_* (optional)
./02-ltl-quote.sh      # POST /ltl/quote -> returns quote_id
./03-book.sh <quote_id>     # POST /book -> returns shipment_id, tracking_number
./04-track.sh <booking_id>  # GET /track -> current status + events
```

Each script is `set -euo pipefail` and reads `$WARP_KEY` from the environment. Bookings made with a `wak_test_*` sandbox key are simulated — no card is charged.
