import json
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class WardrobeStorage:
    """Class for managing clothing item storage in a JSON-based wardrobe."""

    def __init__(self, storage_dir: str = None):
        """
        Initialize the wardrobe storage.

        Args:
            storage_dir: Directory to store wardrobe data and images
        """
        # Use default storage directory if not provided
        if storage_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            storage_dir = os.path.join(base_dir, "data")

        self.storage_dir = storage_dir
        self.wardrobe_file = os.path.join(storage_dir, "wardrobe.json")
        self.image_dir = os.path.join(storage_dir, "images")

        # Create directories if they don't exist
        os.makedirs(self.storage_dir, exist_ok=True)
        os.makedirs(self.image_dir, exist_ok=True)

        # Initialize wardrobe if it doesn't exist
        if not os.path.exists(self.wardrobe_file):
            self._save_wardrobe([])

    def _load_wardrobe(self) -> List[Dict]:
        """Load the wardrobe data from the JSON file."""
        try:
            with open(self.wardrobe_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_wardrobe(self, wardrobe: List[Dict]) -> None:
        """Save the wardrobe data to the JSON file."""
        with open(self.wardrobe_file, "w") as f:
            json.dump(wardrobe, f, indent=2)

    def add_item(
        self, item_data: Dict, image_data: bytes = None, image_path: str = None
    ) -> Dict:
        """
        Add a clothing item to the wardrobe.

        Args:
            item_data: Dictionary containing clothing item details
            image_data: Binary image data (optional)
            image_path: Path to the original image file (optional)

        Returns:
            Dict: The added item with ID
        """
        wardrobe = self._load_wardrobe()

        # Generate unique ID for the item
        item_id = str(uuid.uuid4())

        # Add metadata
        timestamp = datetime.now().isoformat()
        item_with_meta = {
            "id": item_id,
            "created_at": timestamp,
            "updated_at": timestamp,
            **item_data,
        }

        # Handle image storage
        if image_data is not None:
            # Generate a filename for the image
            extension = ".jpg"  # Default extension
            if image_path:
                extension = os.path.splitext(image_path)[1] or extension

            image_filename = f"{item_id}{extension}"
            stored_image_path = os.path.join(self.image_dir, image_filename)

            # Save the image
            with open(stored_image_path, "wb") as f:
                f.write(image_data)

            # Add image path to item data (relative path for portability)
            item_with_meta["image_path"] = f"images/{image_filename}"
        elif image_path and os.path.exists(image_path):
            # Copy the existing image file
            extension = os.path.splitext(image_path)[1]
            image_filename = f"{item_id}{extension}"
            stored_image_path = os.path.join(self.image_dir, image_filename)

            # Copy the file
            shutil.copy2(image_path, stored_image_path)

            # Add image path to item data (relative path for portability)
            item_with_meta["image_path"] = f"images/{image_filename}"

        # Add item to wardrobe
        wardrobe.append(item_with_meta)
        self._save_wardrobe(wardrobe)

        return item_with_meta

    def get_all_items(self) -> List[Dict]:
        """
        Get all clothing items in the wardrobe.

        Returns:
            List[Dict]: All clothing items
        """
        return self._load_wardrobe()

    def get_item(self, item_id: str) -> Optional[Dict]:
        """
        Get a specific clothing item by ID.

        Args:
            item_id: The ID of the item to retrieve

        Returns:
            Optional[Dict]: The item if found, None otherwise
        """
        wardrobe = self._load_wardrobe()
        for item in wardrobe:
            if item.get("id") == item_id:
                return item
        return None

    def update_item(self, item_id: str, updated_data: Dict) -> Optional[Dict]:
        """
        Update a clothing item in the wardrobe.

        Args:
            item_id: The ID of the item to update
            updated_data: Dictionary containing updated item details

        Returns:
            Optional[Dict]: The updated item if found, None otherwise
        """
        wardrobe = self._load_wardrobe()

        for i, item in enumerate(wardrobe):
            if item.get("id") == item_id:
                # Update the item
                updated_item = {**item, **updated_data}
                updated_item["updated_at"] = datetime.now().isoformat()

                # Don't allow updating the ID
                updated_item["id"] = item_id

                wardrobe[i] = updated_item
                self._save_wardrobe(wardrobe)
                return updated_item

        return None

    def delete_item(self, item_id: str) -> bool:
        """
        Delete a clothing item from the wardrobe.

        Args:
            item_id: The ID of the item to delete

        Returns:
            bool: True if the item was deleted, False otherwise
        """
        wardrobe = self._load_wardrobe()

        for i, item in enumerate(wardrobe):
            if item.get("id") == item_id:
                # Delete associated image if it exists
                if "image_path" in item:
                    # Convert relative path to absolute
                    rel_image_path = item["image_path"]
                    full_image_path = os.path.join(self.storage_dir, rel_image_path)
                    if os.path.exists(full_image_path):
                        os.remove(full_image_path)

                # Remove item from wardrobe
                wardrobe.pop(i)
                self._save_wardrobe(wardrobe)
                return True

        return False

    def get_image_path(self, item_id: str) -> Optional[str]:
        """
        Get the full path to an item's image.

        Args:
            item_id: The ID of the item

        Returns:
            Optional[str]: The full image path if found, None otherwise
        """
        item = self.get_item(item_id)
        if item and "image_path" in item:
            return os.path.join(self.storage_dir, item["image_path"])
        return None

    def filter_items(self, filter_criteria: Dict[str, Any]) -> List[Dict]:
        """
        Filter clothing items based on criteria.

        Args:
            filter_criteria: Dictionary with filter conditions

        Returns:
            List[Dict]: Filtered clothing items
        """
        wardrobe = self._load_wardrobe()
        filtered_items = []

        for item in wardrobe:
            matches = True

            for key, value in filter_criteria.items():
                # Handle nested attributes
                if "." in key:
                    parts = key.split(".")
                    item_value = item
                    for part in parts:
                        if part in item_value:
                            item_value = item_value[part]
                        else:
                            matches = False
                            break

                    if matches and item_value != value:
                        matches = False

                # Handle direct attributes
                elif key not in item or item[key] != value:
                    matches = False

            if matches:
                filtered_items.append(item)

        return filtered_items
