import requests, redis, json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Connect to Redis (the hostname 'redis' will be defined in Kubernetes later)
r = redis.Redis(host='redis', port=6379, db=0)

@app.get("/api/iss")
def get_iss():
    cached = r.get("iss_loc")
    if cached:
        return json.loads(cached)
    
    res = requests.get("http://api.open-notify.org/iss-now.json").json()
    loc = {"lat": res["iss_position"]["latitude"], "lon": res["iss_position"]["longitude"]}
    r.setex("iss_loc", 2, json.dumps(loc)) # Cache for 2 seconds
    return loc