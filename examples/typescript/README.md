# TypeScript examples

Single-file quickstart with response types. Native `fetch` (Node 18+), `tsx` for execution.

## Setup

```bash
npm install
export WARP_KEY="wak_test_YOUR_SANDBOX_KEY"   # from /agents/account
```

## Run

```bash
npm start
```

Quotes an LTL shipment LA → SF, books it, and prints the tracking status. With a `wak_test_*` sandbox key the booking is simulated and no card is charged.
