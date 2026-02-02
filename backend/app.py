"""
FastAPI application for audio fingerprinting service.

Main entry point for the backend API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routes import router
from service import get_service


# Create FastAPI app
app = FastAPI(
    title="Shazam Clone API",
    description="Audio fingerprinting and recognition API using classical DSP",
    version="1.0.0"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # React/Next.js dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Initialize service on startup."""
    print("=" * 60)
    print("Starting Shazam Clone API")
    print("=" * 60)
    service = get_service()
    print(f"Database loaded: {len(service.metadata)} songs, {len(service.db)} hashes")
    print("=" * 60)


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "message": "Shazam Clone API",
        "version": "1.0.0",
        "endpoints": {
            "add_song": "POST /api/songs/add",
            "recognize": "POST /api/songs/recognize",
            "list_songs": "GET /api/songs/list",
            "health": "GET /api/health"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
