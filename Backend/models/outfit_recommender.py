import datetime
import json
import os
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class OutfitRecommender:
    def __init__(self, api_type="huggingface"):
        """
        Initialize the LLM-based outfit recommender.

        Args:
            api_type: Type of LLM API to use ("huggingface", "ollama", or "openai-compatible")
        """
        self.api_type = api_type

        # Set up the appropriate API based on type
        if api_type == "huggingface":
            # For Hugging Face Inference API (free tier)
            self.api_key = os.getenv("HUGGINGFACE_API_KEY", "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")
            self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

        elif api_type == "ollama":
            # For local Ollama API (completely free, runs locally)
            self.api_url = "http://localhost:11434/api/generate"
            self.model_name = os.getenv(
                "OLLAMA_MODEL", "llama2:7b"
            )  # or mistral:7b, gemma:7b, etc.
            self.headers = {"Content-Type": "application/json"}

        elif api_type == "openai-compatible":
            # For OpenAI-compatible APIs like LocalAI, llama.cpp servers, etc.
            self.api_url = os.getenv(
                "OPENAI_COMPATIBLE_URL", "http://localhost:8080/v1/chat/completions"
            )
            self.api_key = os.getenv("OPENAI_COMPATIBLE_KEY", "")
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

        else:
            raise ValueError(f"Unsupported API type: {api_type}")

    def _build_prompt(self, wardrobe_items: List[Dict], weather_data: Dict, ) -> str:
        """
        Build a prompt for the LLM with clear instructions for logical outfit recommendations.

        Args:
            wardrobe_items: List of clothing items with attributes
            weather_data: Dictionary containing weather information

        Returns:
            str: Formatted prompt for the LLM
        """
        # Format wardrobe items with numbers and clear categories
        wardrobe_text = "My wardrobe contains the following items:\n"

        # Group items by category
        tops = []
        bottoms = []
        dresses = []
        outerwear = []

        for i, item in enumerate(wardrobe_items, 1):
            category = item["clothing_type"]
            desc = f"{i}. {category}: {item['top_attributes']['color']} {item['top_attributes']['pattern']}, style: {item['top_attributes']['style']}, material: {item['top_attributes']['material']}, image_path:{item['image_path']}"

            if category in [
                "t-shirt",
                "blouse",
                "sweater",
                "hoodie",
                "sweatshirt",
                "tank top",
            ]:
                tops.append((i, desc))
            elif category in ["pants", "jeans", "skirt", "shorts"]:
                bottoms.append((i, desc))
            elif category in ["dress"]:
                dresses.append((i, desc))
            elif category in ["jacket", "coat"]:
                outerwear.append((i, desc))

        # Add items by category
        if tops:
            wardrobe_text += "\nTops:\n" + "\n".join([desc for _, desc in tops])
        if bottoms:
            wardrobe_text += "\n\nBottoms:\n" + "\n".join([desc for _, desc in bottoms])
        if dresses:
            wardrobe_text += "\n\nDresses:\n" + "\n".join([desc for _, desc in dresses])
        if outerwear:
            wardrobe_text += "\n\nOuterwear:\n" + "\n".join(
                [desc for _, desc in outerwear]
            )

        # Format weather data
        weather_text = f"Current weather conditions: {weather_data['description']}, temperature: {weather_data['temperature']}°C ({weather_data.get('temperature_feels_like', weather_data['temperature'])}°C feels like), humidity: {weather_data.get('humidity', 'N/A')}%, precipitation: {weather_data.get('precipitation_chance', 'N/A')}%, wind: {weather_data.get('wind_speed', 'N/A')} km/h"

        # Build the full prompt with clearer instructions
        prompt = f"""Given my wardrobe and current weather conditions, recommend an appropriate outfit for today.

{wardrobe_text}

{weather_text}

IMPORTANT OUTFIT RULES:
1. You must create ONE logical outfit that follows normal clothing combinations
2. Choose EITHER a dress OR a top + bottom combination (never both)
3. Only add outerwear (jacket/coat) if the weather requires it
4. Do NOT recommend wearing multiple bottoms together (no jeans+skirt)
5. Do NOT recommend wearing a dress over or under other clothing

Please consider:
1. Weather appropriateness (temperature, precipitation, wind)
2. Color coordination and style matching
3. Appropriate layering if needed

Your recommendation should follow the format:
1. List each recommended item by its number and description and do not miss image_path
2. Explain why this outfit is suitable for today's weather
3. Explain how the pieces work together (color coordination, style)

Recommended outfit:"""

        return prompt

    def _call_huggingface_api(self, prompt: str) -> str:
        """Call Hugging Face Inference API to generate an outfit recommendation."""
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 600,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True,
            },
        }

        try:
            response = requests.post(
                self.api_url, headers=self.headers, json=payload, timeout=60
            )
            if response.status_code == 200:
                response_json = response.json()
                print(response_json)
                generated_text = response_json[0]["generated_text"]
                final_response = generated_text.replace(prompt, "").strip()
                return final_response
            else:
                error_msg = f"API call failed with status code {response.status_code}: {response.text}"
                print(error_msg)
                return f"Error generating recommendation: {error_msg}"
        except Exception as e:
            error_msg = f"Exception during API call: {str(e)}"
            print(error_msg)
            return f"Error generating recommendation: {error_msg}"

    def _call_ollama_api(self, prompt: str) -> str:
        """Call local Ollama API to generate an outfit recommendation."""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 600,
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            if response.status_code == 200:
                return response.json()["response"].strip()
            else:
                error_msg = f"API call failed with status code {response.status_code}: {response.text}"
                print(error_msg)
                return f"Error generating recommendation: {error_msg}"
        except Exception as e:
            error_msg = f"Exception during API call: {str(e)}"
            print(error_msg)
            return f"Error generating recommendation: {error_msg}"

    def _call_openai_compatible_api(self, prompt: str) -> str:
        """Call OpenAI-compatible API to generate an outfit recommendation."""
        payload = {
            "model": "gpt-3.5-turbo",  # Typically ignored by compatible APIs, uses whatever model is running
            "messages": [
                {
                    "role": "system",
                    "content": "You are a fashion assistant that helps recommend outfits based on weather conditions.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 600,
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"].strip()
            else:
                error_msg = f"API call failed with status code {response.status_code}: {response.text}"
                print(error_msg)
                return f"Error generating recommendation: {error_msg}"
        except Exception as e:
            error_msg = f"Exception during API call: {str(e)}"
            print(error_msg)
            return f"Error generating recommendation: {error_msg}"
    '''
   ''''''' def fetch_weather_data(self, location: str) -> Dict:
        """
        Fetch current weather data for a given location using a free weather API.

        Args:
            location: City name or coordinates

        Returns:
            Dict: Weather data
        """
        # OpenWeatherMap API (free tier)
        api_key = os.getenv("OPENWEATHER_API_KEY", "")
        if not api_key:
            # Return mock weather data if no API key
            return self._get_mock_weather_data(location)

        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

                # Format the response into a standardized structure
                weather_data = {
                    "temperature": data["main"]["temp"],
                    "temperature_feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"],
                    # "precipitation_chance": 0,  # Not directly available in this API
                    "weather_condition": data["weather"][0]["main"].lower(),
                }

                return weather_data
            else:
                print(
                    f"Weather API call failed: {response.status_code} - {response.text}"
                )
                return self._get_mock_weather_data(location)

        except Exception as e:
            print(f"Error fetching weather data: {str(e)}")
            return self._get_mock_weather_data(location)

    def _get_mock_weather_data(self, location: str) -> Dict:
        """Generate mock weather data when API access is not available."""
        # Get the current month to make the mock weather seasonally appropriate
        current_month = datetime.datetime.now().month

        # Seasonal temperature ranges (approximate, for northern hemisphere)
        if current_month in [12, 1, 2]:  # Winter
            temp = round(
                float(5 + 10 * (0.5 - abs(0.5 - (datetime.datetime.now().day / 31)))), 1
            )
            condition = (
                "cloudy"
                if datetime.datetime.now().day % 3 == 0
                else "snowy" if datetime.datetime.now().day % 4 == 0 else "clear"
            )
        elif current_month in [3, 4, 5]:  # Spring
            temp = round(
                float(15 + 10 * (0.5 - abs(0.5 - (datetime.datetime.now().day / 31)))),
                1,
            )
            condition = (
                "rainy"
                if datetime.datetime.now().day % 3 == 0
                else (
                    "partly cloudy" if datetime.datetime.now().day % 4 == 0 else "clear"
                )
            )
        elif current_month in [6, 7, 8]:  # Summer
            temp = round(
                float(25 + 10 * (0.5 - abs(0.5 - (datetime.datetime.now().day / 31)))),
                1,
            )
            condition = (
                "thunderstorm"
                if datetime.datetime.now().day % 7 == 0
                else (
                    "partly cloudy" if datetime.datetime.now().day % 3 == 0 else "clear"
                )
            )
        else:  # Fall
            temp = round(
                float(15 + 10 * (0.5 - abs(0.5 - (datetime.datetime.now().day / 31)))),
                1,
            )
            condition = (
                "rainy"
                if datetime.datetime.now().day % 4 == 0
                else "cloudy" if datetime.datetime.now().day % 3 == 0 else "clear"
            )

        return {
            "temperature": temp,
            "temperature_feels_like": (
                temp - 2 if condition in ["rainy", "cloudy", "snowy"] else temp
            ),
            "humidity": 65 + (15 if condition in ["rainy", "snowy"] else 0),
            "description": condition,
            "wind_speed": 5 + (10 if condition in ["rainy", "thunderstorm"] else 0),
            # "precipitation_chance": (
            #     80
            #     if condition in ["rainy", "snowy", "thunderstorm"]
            #     else 20 if condition == "partly cloudy" else 0
            # ),
            "weather_condition": condition,
        }
    '''
    def recommend_outfit(
        self,
        wardrobe_items: List[Dict],
        location: str = None,
        weather_data: Optional[Dict] = None,
        
    ) -> Dict:
        """
        Generate an outfit recommendation based on wardrobe items and weather.

        Args:
            wardrobe_items: List of clothing items with attributes
            location: City name or coordinates (optional if weather_data is provided)
            weather_data: Weather data dictionary (optional, will be fetched if not provided)

        Returns:
            Dict: Recommended outfit with explanation
        """
        # If no wardrobe items, return an error
        if not wardrobe_items:
            return {"error": "No wardrobe items provided", "success": False}


        # If no weather data provided, fetch it
        
        if weather_data is None:
            if location:
                weather_data = self.fetch_weather_data(location)
            else:
                # Use a default location or mock data
                weather_data = self._get_mock_weather_data("Default Location")
        
        # Build prompt
        prompt = self._build_prompt(wardrobe_items, weather_data)
        print("🖼️ Prompt is:", prompt)
        # Call the appropriate API based on type
        if self.api_type == "huggingface":
            response_text = self._call_huggingface_api(prompt)
            print("Response Text:", response_text)
        elif self.api_type == "ollama":
            response_text = self._call_ollama_api(prompt)
        elif self.api_type == "openai-compatible":
            response_text = self._call_openai_compatible_api(prompt)
        else:
            response_text = "Unsupported API type"

        if "Error generating recommendation" in response_text:
            return {"error": response_text, "success": False}
        
        
        recommended_images = [
        item["image_path"]
        for item in wardrobe_items
        if item["image_path"] in response_text
        ]

        print("Image Path:",recommended_images)


        # Format the response
        return {
            "success": True,
            "recommendation": response_text,
            "weather_data": weather_data,
            "recommended_images": recommended_images, 
            "wardrobe_summary": {
                "total_items": len(wardrobe_items),
                "tops": sum(
                    1
                    for item in wardrobe_items
                    if item["clothing_type"]
                    in [
                        "t-shirt",
                        "blouse",
                        "sweater",
                        "hoodie",
                        "sweatshirt",
                        "tank top",
                    ]
                ),
                "bottoms": sum(
                    1
                    for item in wardrobe_items
                    if item["clothing_type"] in ["pants", "jeans", "skirt", "shorts"]
                ),
                "dresses": sum(
                    1 for item in wardrobe_items if item["clothing_type"] in ["dress"]
                ),
                "outerwear": sum(
                    1
                    for item in wardrobe_items
                    if item["clothing_type"] in ["jacket", "coat"]
                ),
            },
        }
        
 