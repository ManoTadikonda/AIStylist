import os
import sys

import torch
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Add the current directory to the path so imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.models import StatusResponse
from api.routers import analysis_router, outfit_router, wardrobe_router, weather_router

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Stylist API",
    description="Backend API for the AI Stylist application.",
    version="0.1.0",
)

# Set up CORS middleware to allow React app to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create data directory if it doesn't exist
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
images_dir = os.path.join(data_dir, "images")
os.makedirs(data_dir, exist_ok=True)
os.makedirs(images_dir, exist_ok=True)

# Mount static files directory for serving saved images
app.mount("/data/images", StaticFiles(directory=images_dir), name="images")

# Include routers
app.include_router(wardrobe_router)
app.include_router(analysis_router)
app.include_router(outfit_router)
app.include_router(weather_router)


@app.get("/", response_model=StatusResponse, tags=["status"])
async def root():
    """Root endpoint to check if API is running."""
    device = "CUDA" if torch.cuda.is_available() else "CPU"
    return {
        "status": "AI Stylist API is running",
        "version": "0.1.0",
        "success": True,
    }


async def status():
    """Check API status and environment information."""
    try:
        device = "CUDA" if torch.cuda.is_available() else "CPU"
        return {
            "status": f"Running on {device}",
            "version": "0.1.0",
            "success": True,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking status: {str(e)}")


if __name__ == "__main__":
    # Run the application with uvicorn when script is executed directly
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
