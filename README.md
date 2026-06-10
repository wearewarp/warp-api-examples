# Warp Freight API examples

Code samples and the OpenAPI 3.1 spec for the [Warp Freight API](https://www.wearewarp.com/freight-api). Quote, book, and track LTL, FTL, cargo van, box truck, and multi-stop FTL shipments through one Bearer-token REST API.

- **Live API docs:** https://www.wearewarp.com/freight-api
- **OpenAPI 3.1 spec:** [`openapi.yaml`](./openapi.yaml) (mirrored from production)
- **Postman collection:** [`postman/warp-freight-api.postman_collection.json`](./postman/warp-freight-api.postman_collection.json) — drag-and-drop import into Postman, Insomnia, or Bruno
- **Sandbox keys:** free, instant, no card. Sign up at https://www.wearewarp.com/agents/account
- **MCP server for AI agents:** [`warp-agent-mcp`](https://www.npmjs.com/package/warp-agent-mcp)
- **CLI:** [`@warpfreight/cli-agent`](https://www.npmjs.com/package/@warpfreight/cli-agent)
- **License:** [Apache-2.0](./LICENSE)

## Quickstart (60 seconds)

```bash
# 1. Get a sandbox key from https://www.wearewarp.com/agents/account
#    (or POST /api/v1/agents/sandbox-key with a wak_live_* key)
export WARP_KEY="wak_test_YOUR_SANDBOX_KEY"

# 2. Quote an LTL shipment
curl -X POST https://www.wearewarp.com/api/v1/ltl/quote \
  -H "Authorization: Bearer $WARP_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "origin_zip": "90012",
    "destination_zip": "94105",
    "pickup_date": "2026-05-15",
    "pallets": 2,
    "weight_lbs_per_pallet": 800,
    "commodity": "auto parts",
    "length_in": 48,
    "width_in": 40,
    "height_in": 48
  }'

# Response includes a quote_id. Pass it to POST /book to confirm.
```

## What's in this repo

| Path | What it is |
|---|---|
| [`openapi.yaml`](./openapi.yaml) | OpenAPI 3.1 spec, mirrored from production |
| [`postman/warp-freight-api.postman_collection.json`](./postman/warp-freight-api.postman_collection.json) | Postman collection v2.1.0 — drag-and-drop import into Postman, Insomnia, or Bruno. Generated from `openapi.yaml` via `npx openapi-to-postmanv2`. |
| [`scripts/mirror.py`](./scripts/mirror.py) | Re-mirrors `openapi.yaml` from the production spec and regenerates the Postman collection. Run `python3 scripts/mirror.py` (needs PyYAML and Node). |
| [`examples/curl/`](./examples/curl) | bash + curl quickstarts: sandbox key, quote, book, track |
| [`examples/python/`](./examples/python) | Python via `requests`, end-to-end quote → book → track |
| [`examples/node/`](./examples/node) | Node.js (≥18) using native `fetch`, no dependencies |
| [`examples/typescript/`](./examples/typescript) | TypeScript with response types |
| [`examples/go/`](./examples/go) | Go using the standard library |

## Modes

| Mode | When to use | Endpoint |
|---|---|---|
| Cargo van | Up to 3 pallets, 3,500 lbs total. Same-day or next-day metros. | `POST /van/quote` |
| Box truck | 26ft straight truck. Up to ~12 pallets, regional. | `POST /box-truck/quote` |
| LTL | 1–24 pallets, shared trailer, national. FAK-rated (no class needed). | `POST /ltl/quote` |
| FTL | Full 53ft dry van, dedicated, fastest direct. | `POST /ftl/quote` |
| Multi-stop FTL | One trailer, several pickups or deliveries. | `POST /multistop/quote` |

After any quote, pass the returned `quote_id` to `POST /book`.

## Authentication

Every request needs `Authorization: Bearer <key>`.

- `wak_test_*` — sandbox keys. Free quotes, simulated bookings, no card charges.
- `wak_live_*` — production keys. Bookings charge the card on file.

Get a sandbox key at https://www.wearewarp.com/agents/account.

## Pricing

Rates are all-inclusive — the price you see at quote is the price on the invoice. No fuel surcharges added later, no per-pallet upcharges, no accessorial surprises beyond what you book.

## Tested against the live API

The [`validate-openapi`](./.github/workflows/validate-openapi.yml) workflow runs daily. It re-fetches the live OpenAPI spec and re-runs every example against a sandbox account. If the API shape changes, these samples break before yours do.

## Use Warp from an AI agent

If you're wiring Warp into a Claude / GPT / Gemini agent rather than calling the REST API directly:

- **MCP** — install [`warp-agent-mcp`](https://www.npmjs.com/package/warp-agent-mcp) for any MCP-compatible client (Claude Desktop, Cursor, Claude Code).
- **CLI** — `npx @warpfreight/cli-agent` for shell-based agents.
- **LangChain / LlamaIndex** — see https://www.wearewarp.com/freight-api for current upstream tool packages.

## About Warp

Warp is a freight network for shippers and AI agents. It runs its own cross-dock terminals across the contiguous US and connects to FAK-rated legacy carriers (ODFL, FedEx Freight, XPO, Saia) for full coverage. Every shipment is scanned at every dock — chain of custody from pickup to delivery, exposed in the API.

## Contributing

PRs welcome for new languages, fixes, or improved error handling. See [`CONTRIBUTING.md`](./CONTRIBUTING.md).

## License

Apache-2.0. See [`LICENSE`](./LICENSE).
