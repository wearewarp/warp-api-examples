// Warp Freight API — TypeScript quickstart (Node ≥18, native fetch).
//
// End-to-end flow: quote an LTL shipment, book it, track it.
//
// Setup:
//   npm install
//   export WARP_KEY="wak_test_YOUR_SANDBOX_KEY"   # from /agents/account
//
// Run:
//   npm start

const API_BASE = 'https://www.wearewarp.com/api/v1';

interface QuoteResponse {
  quote_id: string;
  lane_id?: string;
  mode: 'van' | 'box_truck' | 'ftl' | 'ltl';
  price_usd: number;
  currency: string;
  transit_days?: number;
  pickup_date: string;
  delivery_date?: string;
  expires_at: string;
  quote_tier: 'firm' | 'indicative';
  service?: Record<string, unknown>;
  missing_for_ship?: string[];
  booking_url?: string;
}

interface BookingResponse {
  booked: boolean;
  shipment_id: string;
  shipment_number: string;
  tracking_number: string;
  lane_id?: string;
  service?: Record<string, unknown>;
}

const apiKey = process.env.WARP_KEY;
if (!apiKey) {
  console.error('Set WARP_KEY to a wak_test_* or wak_live_* key. Get one at https://www.wearewarp.com/agents/account.');
  process.exit(1);
}

async function call<T>(method: 'GET' | 'POST', path: string, body?: unknown): Promise<T> {
  const init: RequestInit = {
    method,
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
  };
  if (body !== undefined) init.body = JSON.stringify(body);

  const response = await fetch(`${API_BASE}${path}`, init);
  if (!response.ok) {
    throw new Error(`${method} ${path} → ${response.status}: ${await response.text()}`);
  }
  return (await response.json()) as T;
}

async function main(): Promise<void> {
  const pickupDate = new Date(Date.now() + 7 * 86400 * 1000).toISOString().slice(0, 10);

  const quote = await call<QuoteResponse>('POST', '/ltl/quote', {
    origin_zip: '90012',
    destination_zip: '94105',
    pickup_date: pickupDate,
    pallets: 2,
    weight_lbs_per_pallet: 800,
    commodity: 'auto parts',
  });
  console.log(`Quote: ${quote.quote_id} — $${quote.price_usd} (${quote.transit_days ?? '?'} days, ${quote.quote_tier} tier)`);

  const booking = await call<BookingResponse>('POST', '/book', {
    quote_id: quote.quote_id,
    reference: 'PO-DEMO-001',
  });
  console.log(`Booked: ${booking.shipment_id} (tracking ${booking.tracking_number})`);

  const status = await call<unknown>('GET', `/track?booking_id=${encodeURIComponent(booking.shipment_id)}`);
  console.log('Status:', status);
}

main().catch((err: Error) => {
  console.error(err.message);
  process.exit(1);
});
