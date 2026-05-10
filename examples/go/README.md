# Go examples

Single-file quickstart using the Go standard library — `net/http`, `encoding/json`. No external dependencies.

## Setup

```bash
export WARP_KEY="wak_test_YOUR_SANDBOX_KEY"   # from /agents/account
```

## Run

```bash
go run main.go
```

Quotes an LTL shipment LA → SF, books it, and prints the tracking status. With a `wak_test_*` sandbox key the booking is simulated and no card is charged.
