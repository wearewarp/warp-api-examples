// Warp Freight API — Node.js quickstart (Node ≥18, native fetch, zero deps).
//
// End-to-end flow: quote an LTL shipment, book it, track it.
//
// Setup:
//   export WARP_KEY="wak_test_YOUR_SANDBOX_KEY"   # from /agents/account
//
// Run:
//   node quickstart.mjs

const API_BASE = 'https://www.wearewarp.com/api/v1';

const apiKey = process.env.WARP_KEY;
if (!apiKey) {
  console.error('Set WARP_KEY to a wak_test_* or wak_live_* key. Get one at https://www.wearewarp.com/agents/account.');
  process.exit(1);
}

const headers = {
  Authorization: `Bearer ${apiKey}`,
  'Content-Type': 'application/json',
};

async function call(method, path, body) {
  const init = { method, headers };
  if (body !== undefined) init.body = JSON.stringify(body);
  const response = await fetch(`${API_BASE}${path}`, init);
  if (!response.ok) {
    throw new Error(`${method} ${path} → ${response.status}: ${await response.text()}`);
  }
  return response.json();
}

async function main() {
  const pickupDate = new Date(Date.now() + 7 * 86400 * 1000).toISOString().slice(0, 10);

  // POST /ltl/quote
  const quote = await call('POST', '/ltl/quote', {
    origin_zip: '90012',
    destination_zip: '94105',
    pickup_date: pickupDate,
    pallets: 2,
    weight_lbs_per_pallet: 800,
    commodity: 'auto parts',
    length_in: 48,
    width_in: 40,
    height_in: 48,
  });
  console.log(`Quote: ${quote.quote_id} — $${quote.price_usd} (${quote.transit_days ?? '?'} days, ${quote.quote_tier} tier)`);

  // POST /book
  const booking = await call('POST', '/book', {
    quote_id: quote.quote_id,
    reference: 'PO-DEMO-001',
  });
  console.log(`Booked: ${booking.shipment_id} (tracking ${booking.tracking_number})`);

  // GET /track?booking_id=...
  const status = await call('GET', `/track?booking_id=${encodeURIComponent(booking.shipment_id)}`);
  console.log('Status:', status);
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
