import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, appointments, insects, locations
from dependencies.dbclients import init_db
import logging
import os
import sentry_sdk

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
)

app = FastAPI(
    title="Rentokil Self Service API",
    description="API for insect extermination appointments",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOW_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
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


@app.get("/sentry-debug")
async def trigger_error():
    raise Exception("New Insect Exception V2")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, server_header=False)  # nosec B104
