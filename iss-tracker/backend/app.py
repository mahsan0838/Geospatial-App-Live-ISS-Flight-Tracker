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
    
    try:
        # Use anonymous access (no auth) - limits 100/day
        url = "https://opensky-network.org/api/states/all"
        params = {"lamin": 24, "lomin": -125, "lamax": 49, "lomax": -65}
        res = requests.get(url, params=params, timeout=5)
        
        if res.status_code != 200:
            return []
            
        flights = []
        for state in res.json().get("states", [])[:20]:
            if state[5] and state[6] and state[1]:
                flights.append({
                    "callsign": state[1].strip(),
                    "lat": state[6],
                    "lon": state[5],
                    "altitude": state[7] or 0,
                    "velocity": state[9] or 0
                })
        
        # Cache for 60 seconds (reduces API calls)
        r.setex("flights", 60, json.dumps(flights))
        return flights
    except Exception as e:
        print(f"Flight API error: {e}")
        return []