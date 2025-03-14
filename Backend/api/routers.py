import io
import os
import shutil
import sys
import tempfile
from typing import Any, Dict, List, Optional

from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
)
from fastapi.responses import FileResponse
from PIL import Image
from utils.storage import WardrobeStorage

from models.clothing_analyzer import ClothingAnalyzer
from models.outfit_recommender import OutfitRecommender

from . import models

# Create routers
wardrobe_router = APIRouter(prefix="/wardrobe", tags=["wardrobe"])
analysis_router = APIRouter(prefix="/analyze", tags=["analyze"])
outfit_router = APIRouter(prefix="/outfit", tags=["outfit"])
weather_router = APIRouter(prefix="/weather", tags=["weather"])


def get_analyzer():
    """Dependency to get clothing analyzer instance."""
    return ClothingAnalyzer()


def get_recommender():
    """Dependency to get outfit recommender instance."""
    return OutfitRecommender(api_type="huggingface")  # Default to huggingface


def get_storage():
    """Dependency to get wardrobe storage instance."""
    return WardrobeStorage()


# Wardrobe Endpoints
@wardrobe_router.get(
    "", response_model=models.WardrobeResponse, summary="Get all wardrobe items"
)
async def get_wardrobe(
    storage: WardrobeStorage = Depends(get_storage),
    clothing_type: Optional[str] = Query(None, description="Filter by clothing type"),
):
    """Get all clothing items in the wardrobe, with optional filtering."""
    try:
        if clothing_type:
            items = storage.filter_items({"clothing_type": clothing_type})
        else:
            items = storage.get_all_items()

        return {"items": items, "count": len(items), "success": True}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving wardrobe: {str(e)}"
        )


@wardrobe_router.get(
    "/{item_id}", response_model=models.ClothingItem, summary="Get wardrobe item"
)
async def get_wardrobe_item(
    item_id: str,
    storage: WardrobeStorage = Depends(get_storage),
):
    """Get a specific clothing item by ID."""
    item = storage.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
    return item


@wardrobe_router.get(
    "/{item_id}/image", response_class=FileResponse, summary="Get item image"
)
async def get_item_image(
    item_id: str,
    storage: WardrobeStorage = Depends(get_storage),
):
    """Get the image for a specific clothing item."""
    image_path = storage.get_image_path(item_id)
    if not image_path or not os.path.exists(image_path):
        raise HTTPException(
            status_code=404, detail=f"Image for item {item_id} not found"
        )

    return FileResponse(image_path)


@wardrobe_router.delete(
    "/{item_id}", response_model=Dict[str, Any], summary="Delete wardrobe item"
)
async def delete_wardrobe_item(
    item_id: str,
    storage: WardrobeStorage = Depends(get_storage),
):
    """Delete a clothing item from the wardrobe."""
    success = storage.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")

    return {"success": True, "message": f"Item {item_id} deleted successfully"}


# Analysis Endpoints
@analysis_router.post(
    "", response_model=models.ClothingAnalysisResponse, summary="Analyze clothing image"
)
async def analyze_clothing(
    file: UploadFile = File(...),
    analyzer: ClothingAnalyzer = Depends(get_analyzer),
    storage: Optional[WardrobeStorage] = Depends(get_storage),
    add_to_wardrobe: bool = Form(False),
):
    """
    Analyze a clothing image and optionally add it to the wardrobe.

    - **file**: The image file to analyze
    - **add_to_wardrobe**: Whether to add the analyzed item to the wardrobe
    """
    try:
        # Read the file contents
        contents = await file.read()

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
            temp.write(contents)
            temp_path = temp.name

        # Analyze the image
        analysis_result = analyzer.analyze_image(temp_path)

        # Add to wardrobe if requested
        if add_to_wardrobe and analysis_result:
            storage.add_item(
                analysis_result, image_data=contents, image_path=file.filename
            )

        # Clean up the temporary file
        os.remove(temp_path)

        if not analysis_result:
            return {"success": False, "error": "Failed to analyze image"}

        return {**analysis_result, "success": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing image: {str(e)}")


# Outfit Endpoints
@outfit_router.post(
    "/recommend",
    response_model=models.OutfitRecommendation,
    summary="Get outfit recommendation",
)
async def recommend_outfit(
    request: models.OutfitRequest,
    recommender: OutfitRecommender = Depends(get_recommender),
    storage: WardrobeStorage = Depends(get_storage),
):
    """
    Get an outfit recommendation based on wardrobe items and weather.

    Either provide:
    - wardrobe_ids: List of wardrobe item IDs to use for the recommendation
    - location: City name for weather data
    - weather_data: Manual weather data
    """
    try:
        # Get wardrobe items
        if request.wardrobe_ids:
            items = [
                storage.get_item(item_id)
                for item_id in request.wardrobe_ids
                if storage.get_item(item_id)
            ]
        else:
            items = storage.get_all_items()

        # Check if we have items to work with
        if not items:
            raise HTTPException(
                status_code=400, detail="No wardrobe items available for recommendation"
            )

        # Generate recommendation
        result = recommender.recommend_outfit(
            wardrobe_items=items,
            location=request.location,
            weather_data=request.weather_data.dict() if request.weather_data else None,
        )

        if not result.get("success", False):
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Failed to generate recommendation"),
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating outfit recommendation: {str(e)}"
        )


# Weather Endpoints
@weather_router.post(
    "/current", response_model=models.WeatherData, summary="Get current weather data"
)
async def get_weather(
    request: models.WeatherRequest,
    recommender: OutfitRecommender = Depends(get_recommender),
):
    """
    Get current weather data for a location.

    - **location**: City name or coordinates
    """
    try:
        weather_data = recommender.fetch_weather_data(request.location)
        return weather_data
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching weather data: {str(e)}"
        )
