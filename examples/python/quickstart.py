"""
Warp Freight API — Python quickstart.

End-to-end flow: quote an LTL shipment, book it, track it.

Setup:
    pip install -r requirements.txt
    export WARP_KEY="wak_test_YOUR_SANDBOX_KEY"   # from /agents/account

Run:
    python quickstart.py
"""

import os
import sys
from datetime import date, timedelta

import requests

API_BASE = "https://www.wearewarp.com/api/v1"


def quote_ltl(api_key: str) -> dict:
    """POST /ltl/quote — request a self-serve LTL quote."""
    pickup_date = (date.today() + timedelta(days=7)).isoformat()
    response = requests.post(
        f"{API_BASE}/ltl/quote",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "origin_zip": "90012",
            "destination_zip": "94105",
            "pickup_date": pickup_date,
            "pallets": 2,
            "weight_lbs_per_pallet": 800,
            "commodity": "auto parts",
            "length_in": 48,
            "width_in": 40,
            "height_in": 48,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def book(api_key: str, quote_id: str) -> dict:
    """POST /book — turn a quote into a shipment.

    With a wak_test_* key the booking is simulated; with wak_live_* the card on
    file is charged at the quoted rate.
    """
    response = requests.post(
        f"{API_BASE}/book",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"quote_id": quote_id, "reference": "PO-DEMO-001"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def track(api_key: str, booking_id: str) -> dict:
    """GET /track — current status and event history."""
    response = requests.get(
        f"{API_BASE}/track",
        headers={"Authorization": f"Bearer {api_key}"},
        params={"booking_id": booking_id},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    api_key = os.environ.get("WARP_KEY")
    if not api_key:
        sys.exit("Set WARP_KEY to a wak_test_* or wak_live_* key. "
                 "Get one at https://www.wearewarp.com/agents/account.")

    quote = quote_ltl(api_key)
    print(f"Quote: {quote['quote_id']} — ${quote['price_usd']} "
          f"({quote.get('transit_days', '?')} days, {quote.get('quote_tier', '?')} tier)")

    booking = book(api_key, quote["quote_id"])
    print(f"Booked: {booking['shipment_id']} (tracking {booking['tracking_number']})")

    status = track(api_key, booking["shipment_id"])
    print(f"Status: {status}")


if __name__ == "__main__":
    main()
