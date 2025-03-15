from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator


class WeatherCondition(str, Enum):
    HOT = "hot"
    WARM = "warm"
    MILD = "mild"
    COOL = "cool"
    COLD = "cold"
    RAINY = "rainy"
    SNOWY = "snowy"


class ClothingType(str, Enum):
    TSHIRT = "t-shirt"
    DRESS = "dress"
    PANTS = "pants"
    JEANS = "jeans"
    SKIRT = "skirt"
    BLOUSE = "blouse"
    SWEATER = "sweater"
    JACKET = "jacket"
    COAT = "coat"
    SHORTS = "shorts"
    HOODIE = "hoodie"
    SWEATSHIRT = "sweatshirt"
    TANKTOP = "tank top"


class WeatherData(BaseModel):
    temperature: float
    temperature_feels_like: Optional[float] = None
    humidity: Optional[float] = None
    description: str
    wind_speed: Optional[float] = None
    precipitation_chance: Optional[float] = None
    weather_condition: Optional[str] = None


class ClothingAttributes(BaseModel):
    color: Dict[str, float]
    pattern: Dict[str, float]
    material: Dict[str, float]
    style: Dict[str, float]


class TopAttributes(BaseModel):
    color: str
    pattern: str
    material: str
    style: str


class ClothingAnalysisResponse(BaseModel):
    image_path: Optional[str] = None
    clothing_type: str
    clothing_type_scores: Dict[str, float]
    attributes: ClothingAttributes
    top_attributes: TopAttributes
    success: bool = True
    error: Optional[str] = None


class ClothingItem(BaseModel):
    id: Optional[str] = None
    clothing_type: str
    clothing_type_scores: Optional[Dict[str, float]] = None
    attributes: Optional[Dict[str, Dict[str, float]]] = None
    top_attributes: Dict[str, str]
    image_path: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class WardrobeResponse(BaseModel):
    items: List[ClothingItem]
    count: int
    success: bool = True
    error: Optional[str] = None


class WeatherRequest(BaseModel):
    location: str = Field(..., description="City name or coordinates for weather data")


class OutfitRequest(BaseModel):
    wardrobe_ids: Optional[List[str]] = Field(
        None, description="List of wardrobe item IDs to include in recommendation"
    )
    location: Optional[str] = Field(None, description="City name or coordinates")
    weather_data: Optional[WeatherData] = Field(
        None, description="Manual weather data override"
    )
    style_preference: Optional[str] = Field(
        None, description="Style preference for outfit recommendation"
    )



class OutfitRecommendation(BaseModel):
    recommendation: str
    weather_data: WeatherData
    wardrobe_summary: Optional[Dict[str, int]] = None
    success: bool = True
    error: Optional[str] = None


class ErrorResponse(BaseModel):
    detail: str
    success: bool = False


class StatusResponse(BaseModel):
    status: str
    version: str
    success: bool = True
