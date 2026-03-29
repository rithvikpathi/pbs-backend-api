from fastapi import FastAPI
from routers import relay
from fastapi.middleware.cors import CORSMiddleware

# --- APP INITIALIZATION ---
app = FastAPI(
    title="Indy Relay Super Backend",
    description="Real-time Pacers Bikeshare GBFS data + Smart Relay Routing.",
    version="3.0"
)

# Plug in all the API routes we just built
app.include_router(relay.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://your-production-url.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Indy Relay API is firing on all cylinders. Hit /docs to view the dashboard."}

    ## python -m uvicorn main:app --reload to run