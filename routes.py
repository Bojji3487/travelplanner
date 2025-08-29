from fastapi import APIRouter
from models import TripRequest

router = APIRouter()

@router.post("/plan-trip")
async def plan_trip(trip: TripRequest):
    return {
        "message": "Trip planned successfully!",
        "destination": trip.destination,
        "days": trip.days,
        "budget": trip.budget,
        "itinerary": [
            "Day 1: Arrival & local exploration",
            "Day 2: City Tour & activities",
            "Day 3: Relax & Departure"
        ]
    }
