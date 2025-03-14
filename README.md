# AI Stylist

A smart fashion assistant that analyzes your clothing items and provides personalized outfit recommendations based on weather conditions.

## Features

- **Clothing Analysis**: Zero-shot classification of clothing types and attributes using CLIP
- **Attribute Extraction**: Identification of color, pattern, material, and style
- **Wardrobe Management**: Storage and retrieval of your clothing items
- **Weather Integration**: Context-aware outfit recommendations based on current weather
- **Personalized Recommendations**: LLM-powered outfit suggestions with explanations

## Project Structure

This project consists of two main components:

1. **Frontend**: React-based UI for user interactions
2. **Backend**: FastAPI-based server for image analysis and outfit recommendations

## Getting Started

### Backend Setup

See README under [backend](/AIStylist/backend) directory.

The API server will be available at http://localhost:8000 with interactive docs at http://localhost:8000/docs

### Frontend Setup

1. Navigate to the ai-stylist directory:
   ```bash
   cd ai-stylist
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at http://localhost:5173