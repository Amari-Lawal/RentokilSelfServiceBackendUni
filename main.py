import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, appointments, insects, locations
from dependencies.dbclients import init_db
import logging

app = FastAPI(
    title="Rentokil Self Service API",
    description="API for insect extermination appointments"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

# Initialize DB
init_db()


app.include_router(auth.router)
app.include_router(appointments.router)
app.include_router(insects.router)
app.include_router(locations.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
