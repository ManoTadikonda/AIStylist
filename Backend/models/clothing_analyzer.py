import os
import tempfile
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor


class ClothingAnalyzer:
    def __init__(self):
        """Initialize the clothing analyzer with CLIP model."""
        # Load CLIP model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(
            self.device
        )
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        # Define clothing types
        self.clothing_types = [
            "t-shirt",
            "dress",
            "pants",
            "jeans",
            "skirt",
            "blouse",
            "sweater",
            "jacket",
            "coat",
            "shorts",
            "hoodie",
            "sweatshirt",
            "tank top",
        ]

        # Define attributes
        self.colors = [
            "red",
            "blue",
            "green",
            "yellow",
            "purple",
            "pink",
            "orange",
            "black",
            "white",
            "gray",
            "brown",
            "beige",
            "navy",
            "teal",
            "maroon",
        ]

        self.patterns = [
            "solid",
            "striped",
            "floral",
            "plaid",
            "checkered",
            "dotted",
            "geometric",
            "animal print",
            "tie-dye",
            "camouflage",
            "abstract",
        ]

        self.materials = [
            "cotton",
            "silk",
            "wool",
            "linen",
            "polyester",
            "denim",
            "leather",
            "suede",
            "velvet",
            "knit",
            "cashmere",
            "satin",
            "lace",
            "chiffon",
        ]

        self.styles = [
            "casual",
            "formal",
            "business",
            "sporty",
            "vintage",
            "bohemian",
            "preppy",
            "streetwear",
            "minimalist",
            "elegant",
            "punk",
            "athleisure",
        ]

        # Weather appropriateness mapping
        self.weather_appropriateness = {
            "hot": {
                "appropriate": ["t-shirt", "shorts", "skirt", "dress", "tank top"],
                "inappropriate": ["coat", "sweater", "jacket", "hoodie", "sweatshirt"],
            },
            "warm": {
                "appropriate": [
                    "t-shirt",
                    "shorts",
                    "skirt",
                    "dress",
                    "pants",
                    "jeans",
                    "blouse",
                    "tank top",
                ],
                "inappropriate": ["coat", "sweater", "jacket"],
            },
            "mild": {
                "appropriate": [
                    "t-shirt",
                    "pants",
                    "jeans",
                    "blouse",
                    "skirt",
                    "dress",
                    "light sweater",
                    "light jacket",
                ],
                "inappropriate": ["coat", "heavy sweater", "tank top", "shorts"],
            },
            "cool": {
                "appropriate": [
                    "pants",
                    "jeans",
                    "sweater",
                    "jacket",
                    "hoodie",
                    "sweatshirt",
                    "blouse",
                ],
                "inappropriate": ["shorts", "tank top"],
            },
            "cold": {
                "appropriate": [
                    "coat",
                    "sweater",
                    "jacket",
                    "pants",
                    "jeans",
                    "hoodie",
                    "sweatshirt",
                ],
                "inappropriate": ["shorts", "t-shirt", "tank top", "skirt", "dress"],
            },
            "rainy": {
                "appropriate": ["jacket", "pants", "jeans", "hoodie", "sweatshirt"],
                "inappropriate": ["light colored clothing", "suede"],
            },
            "snowy": {
                "appropriate": [
                    "coat",
                    "sweater",
                    "jacket",
                    "pants",
                    "jeans",
                    "hoodie",
                    "sweatshirt",
                ],
                "inappropriate": ["shorts", "t-shirt", "tank top", "skirt", "dress"],
            },
        }

    def classify_clothing(self, image: Image.Image) -> Dict[str, float]:
        """Identify the clothing type using CLIP."""
        try:
            # Create prompts for clothing types
            prompts = [f"a {clothing} photo" for clothing in self.clothing_types]

            # Process image and text
            inputs = self.processor(
                text=prompts, images=image, return_tensors="pt", padding=True
            ).to(self.device)

            # Forward pass
            with torch.no_grad():
                outputs = self.model(**inputs)

            # Calculate similarities
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1).cpu().numpy()[0]

            # Create result dictionary
            results = {
                self.clothing_types[i]: float(probs[i])
                for i in range(len(self.clothing_types))
            }

            return results

        except Exception as e:
            print(f"Error in classify_clothing: {str(e)}")
            return {}

    def extract_attributes(self, image: Image.Image) -> Dict[str, Dict[str, float]]:
        """Extract attributes such as color, pattern, material, and style."""
        try:
            attribute_categories = {
                "color": self.colors,
                "pattern": self.patterns,
                "material": self.materials,
                "style": self.styles,
            }

            results = {}

            # Process each attribute category
            for category, attributes in attribute_categories.items():
                # Create prompts
                prompts = [f"a {attr} {category}" for attr in attributes]

                # Process image and text
                inputs = self.processor(
                    text=prompts, images=image, return_tensors="pt", padding=True
                ).to(self.device)

                # Forward pass
                with torch.no_grad():
                    outputs = self.model(**inputs)

                # Calculate similarities
                logits_per_image = outputs.logits_per_image
                probs = logits_per_image.softmax(dim=1).cpu().numpy()[0]

                # Add to results
                results[category] = {
                    attributes[i]: float(probs[i]) for i in range(len(attributes))
                }

            return results

        except Exception as e:
            print(f"Error in extract_attributes: {str(e)}")
            return {}

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """Perform complete analysis of clothing image."""
        try:
            # Load image
            image = Image.open(image_path).convert("RGB")

            # Classify clothing type
            clothing_types = self.classify_clothing(image)
            top_clothing_type = max(clothing_types.items(), key=lambda x: x[1])[0]

            # Extract attributes
            attributes = self.extract_attributes(image)

            # Get top attributes for each category
            top_attributes = {}
            for category, attrs in attributes.items():
                top_attributes[category] = max(attrs.items(), key=lambda x: x[1])[0]

            # Combine results
            results = {
                "image_path": image_path,
                "clothing_type": top_clothing_type,
                "clothing_type_scores": clothing_types,
                "attributes": attributes,
                "top_attributes": top_attributes,
            }

            return results

        except Exception as e:
            print(f"Error in analyze_image: {str(e)}")
            return {}

    def analyze_image_from_bytes(
        self, image_bytes: bytes, filename: str = None
    ) -> Dict[str, Any]:
        """Analyze clothing image from bytes."""
        try:
            # Create a temporary file to save the image
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file.write(image_bytes)
                temp_path = temp_file.name

            # Analyze the image
            image = Image.open(temp_path).convert("RGB")

            # Classify clothing type
            clothing_types = self.classify_clothing(image)
            top_clothing_type = max(clothing_types.items(), key=lambda x: x[1])[0]

            # Extract attributes
            attributes = self.extract_attributes(image)

            # Get top attributes for each category
            top_attributes = {}
            for category, attrs in attributes.items():
                top_attributes[category] = max(attrs.items(), key=lambda x: x[1])[0]

            # Use the provided filename or the temp path
            image_path = filename if filename else temp_path

            # Combine results
            results = {
                "image_path": image_path,
                "clothing_type": top_clothing_type,
                "clothing_type_scores": clothing_types,
                "attributes": attributes,
                "top_attributes": top_attributes,
            }

            # Clean up
            os.unlink(temp_path)

            return results

        except Exception as e:
            print(f"Error in analyze_image_from_bytes: {str(e)}")
            return {}

    def is_weather_appropriate(
        self, clothing_type: str, weather: str
    ) -> Optional[bool]:
        """Check if a clothing type is appropriate for given weather."""
        if weather not in self.weather_appropriateness:
            return None

        if clothing_type in self.weather_appropriateness[weather]["appropriate"]:
            return True
        elif clothing_type in self.weather_appropriateness[weather]["inappropriate"]:
            return False
        else:
            # For items not explicitly categorized, we'll consider them neutral
            return None
