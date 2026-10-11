from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

API_KEY = "ak_z12wilxt7vvvlk42p60ju4f0"
EMAIL = "your-email@example.com"  # Replace with your actual login email

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analytics")
async def analytics(request: Request):
    key = request.headers.get("X-API-Key")

    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        body = await request.json()
        events = body["events"]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request body")

    total_events = len(events)
    users = set()
    positive_totals = {}

    revenue = 0.0

    for event in events:
        user = event.get("user")
        amount = event.get("amount", 0)

        users.add(user)

        if amount > 0:
            revenue += amount
            positive_totals[user] = positive_totals.get(user, 0) + amount

    top_user = max(positive_totals, key=positive_totals.get)

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": len(users),
        "revenue": revenue,
        "top_user": top_user,
    }