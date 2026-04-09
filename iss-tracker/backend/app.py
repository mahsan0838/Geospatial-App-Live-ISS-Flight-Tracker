import requests, redis, json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Connect to Redis
r = redis.Redis(host='redis', port=6379, db=0)

@app.get("/api/iss")
def get_iss():
    cached = r.get("iss_loc")
    if cached:
        return json.loads(cached)
    
    res = requests.get("http://api.open-notify.org/iss-now.json").json()
    loc = {"lat": res["iss_position"]["latitude"], "lon": res["iss_position"]["longitude"]}
    r.setex("iss_loc", 2, json.dumps(loc))
    return loc

@app.get("/api/flights")
def get_flights():
    cached = r.get("flights")
    if cached:
        return json.loads(cached)
    
    # Get flights over USA (bounding box)
    url = "https://opensky-network.org/api/states/all"
    params = {"lamin": 24, "lomin": -125, "lamax": 49, "lomax": -65}  # Continental US
    res = requests.get(url, params=params).json()
    
    flights = []
    for state in res.get("states", [])[:20]:  # Limit to 20 flights
        if state[5] and state[6]:  # Check if lat/lon exist
            flights.append({
                "callsign": state[1].strip(),
                "lat": state[6],
                "lon": state[5],
                "altitude": state[7],
                "velocity": state[9]
            })
    
    r.setex("flights", 10, json.dumps(flights))  # Cache for 10 seconds
    return flights