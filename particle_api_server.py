from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

# Enable CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Particle API. Use /particles to get particle data."}

@app.get("/particles")
def get_particles(n: int = 10):
    particles = [
        {
            "x": random.uniform(-50, 50),
            "y": random.uniform(-50, 50),
            "z": random.uniform(20, 70)
        }
        for _ in range(n)
    ]
    return {"particles": particles}