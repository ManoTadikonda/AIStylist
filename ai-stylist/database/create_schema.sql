-- Step 1: Create a new database
CREATE DATABASE IF NOT EXISTS ai_stylist;

-- Step 2: Use the newly created database
USE ai_stylist;

-- Step 3: Create the 'wardrobe' table
CREATE TABLE IF NOT EXISTS wardrobe (
    id INT AUTO_INCREMENT PRIMARY KEY,       -- Unique identifier for each wardrobe item
    image_path VARCHAR(255) NOT NULL,         -- Path to the uploaded image
    category VARCHAR(50) NOT NULL,           -- Category (e.g., Jeans, Shirt)
    color VARCHAR(50) NOT NULL,              -- Color (e.g., Blue, Red)
    style VARCHAR(50) NOT NULL,              -- Style (e.g., Casual, Formal)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp for when the record was created
);

