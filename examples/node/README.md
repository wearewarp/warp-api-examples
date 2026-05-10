# Node.js examples

Single-file quickstart using native `fetch` (Node 18+). No `npm install` needed.

## Setup

```bash
export WARP_KEY="wak_test_YOUR_SANDBOX_KEY"   # from /agents/account
```

## Run

```bash
node quickstart.mjs
```

Quotes an LTL shipment LA → SF, books it, and prints the tracking status. With a `wak_test_*` sandbox key the booking is simulated and no card is charged.
