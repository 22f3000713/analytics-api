from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

API_KEY = "ak_z12wilxt7vvvlk42p60ju4f0"
EMAIL = "22f3000713@ds.study.iitm.ac.in"  # Replace with your real email

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analytics")
async def analytics(request: Request):
    # Check authentication FIRST
    key = request.headers.get("x-api-key")

    if key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized"}
        )

    # Only parse the body after authentication succeeds
    try:
        body = await request.json()
        events = body.get("events", [])
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid JSON body"}
        )

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
