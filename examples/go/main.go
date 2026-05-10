// Warp Freight API — Go quickstart (standard library only).
//
// End-to-end flow: quote an LTL shipment, book it, track it.
//
// Setup:
//   export WARP_KEY="wak_test_YOUR_SANDBOX_KEY"   # from /agents/account
//
// Run:
//   go run main.go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"time"
)

const apiBase = "https://www.wearewarp.com/api/v1"

type quoteResponse struct {
	QuoteID      string  `json:"quote_id"`
	Mode         string  `json:"mode"`
	PriceUSD     float64 `json:"price_usd"`
	Currency     string  `json:"currency"`
	TransitDays  int     `json:"transit_days"`
	PickupDate   string  `json:"pickup_date"`
	DeliveryDate string  `json:"delivery_date,omitempty"`
	ExpiresAt    string  `json:"expires_at"`
	QuoteTier    string  `json:"quote_tier"`
}

type bookingResponse struct {
	Booked         bool   `json:"booked"`
	ShipmentID     string `json:"shipment_id"`
	ShipmentNumber string `json:"shipment_number"`
	TrackingNumber string `json:"tracking_number"`
}

func call(apiKey, method, path string, body any, out any) error {
	var reqBody io.Reader
	if body != nil {
		buf, err := json.Marshal(body)
		if err != nil {
			return err
		}
		reqBody = bytes.NewReader(buf)
	}
	req, err := http.NewRequest(method, apiBase+path, reqBody)
	if err != nil {
		return err
	}
	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{Timeout: 30 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	respBody, _ := io.ReadAll(resp.Body)
	if resp.StatusCode >= 400 {
		return fmt.Errorf("%s %s → %d: %s", method, path, resp.StatusCode, string(respBody))
	}
	return json.Unmarshal(respBody, out)
}

func main() {
	apiKey := os.Getenv("WARP_KEY")
	if apiKey == "" {
		fmt.Fprintln(os.Stderr, "Set WARP_KEY to a wak_test_* or wak_live_* key. Get one at https://www.wearewarp.com/agents/account.")
		os.Exit(1)
	}

	pickupDate := time.Now().AddDate(0, 0, 7).Format("2006-01-02")

	// POST /ltl/quote
	var quote quoteResponse
	err := call(apiKey, "POST", "/ltl/quote", map[string]any{
		"origin_zip":            "90012",
		"destination_zip":       "94105",
		"pickup_date":           pickupDate,
		"pallets":               2,
		"weight_lbs_per_pallet": 800,
		"commodity":             "auto parts",
	}, &quote)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Printf("Quote: %s — $%.2f (%d days, %s tier)\n",
		quote.QuoteID, quote.PriceUSD, quote.TransitDays, quote.QuoteTier)

	// POST /book
	var booking bookingResponse
	err = call(apiKey, "POST", "/book", map[string]any{
		"quote_id":  quote.QuoteID,
		"reference": "PO-DEMO-001",
	}, &booking)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Printf("Booked: %s (tracking %s)\n", booking.ShipmentID, booking.TrackingNumber)

	// GET /track?booking_id=...
	var status map[string]any
	q := url.Values{"booking_id": []string{booking.ShipmentID}}
	err = call(apiKey, "GET", "/track?"+q.Encode(), nil, &status)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println("Status:", status)
}
