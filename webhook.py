from fastapi import FastAPI, Request, Response, HTTPException
import json

app = FastAPI()

@app.post("/paystack-webhook")
async def paystack_webhook(request: Request):
    # Fetch raw data payload
    payload_bytes = await request.body()
    payload = json.loads(payload_bytes.decode("utf-8"))
    
    # 1. Fetch event type
    event_type = payload.get("event")
    
    # 2. Process only successful checkouts
    if event_type == "charge.success":
        data = payload.get("data", {})
        reference = data.get("reference")
        amount = data.get("amount") / 100  # Convert back from Kobo/Cents
        customer_email = data.get("customer", {}).get("email")
        
        print("\n" + "="*40)
        print("🚨 SUCCESSFUL WEBHOOK RECEIVED FROM PAYSTACK 🚨")
        print(f"Customer:  {customer_email}")
        print(f"Amount:    {amount}")
        print(f"Reference: {reference}")
        print("="*40 + "\n")
        
        # Insert your internal order processing or database state changes here.

    # 3. Always return an absolute HTTP 200 OK immediately to satisfy Paystack
    return Response(status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
