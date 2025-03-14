# AI Stylist backend

A FastAPI-based backend for the AI Stylist application, providing clothing analysis, wardrobe management, and outfit recommendations.

## Features

- **Clothing Analysis**: Zero-shot classification of clothing items using CLIP (Contrastive Language-Image Pre-training)
- **Attribute Extraction**: Identification of color, pattern, material, and style attributes from clothing images
- **Wardrobe Management**: Storage and retrieval of analyzed clothing items
- **Outfit Recommendations**: LLM-powered outfit recommendations based on weather conditions
- **Weather Integration**: Weather data fetching for context-aware outfit suggestions

## Prerequisites

- Python 3.8+
- PyTorch
- Transformers library (Hugging Face)
- FastAPI
- Uvicorn

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ShreyaGudsurkar/AIStylist.git
   cd AIStylist/backend
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` in the backend directory:
   ```bash
   cp .env.example .env
   # Edit .env to add your API keys for huggingface and openweather
   ```

## Running the Server

1. Start the server:
   ```bash
   # Make sure you are in the backend directory
   # Use the run script
   python run.py
   ```

2. The API will be available at http://localhost:8000
3. Access the interactive API documentation at http://localhost:8000/docs

## API Endpoints

### Status

- `GET /`: Root endpoint to check if API is running
- `GET /status`: Show detailed status information

### Wardrobe Management

- `GET /wardrobe`: Get all wardrobe items
- `GET /wardrobe/{item_id}`: Get a specific item by ID
- `GET /wardrobe/{item_id}/image`: Get the image for a specific item
- `DELETE /wardrobe/{item_id}`: Delete an item from the wardrobe

### Clothing Analysis

- `POST /analyze`: Analyze a clothing image and optionally add it to the wardrobe

### Outfit Recommendations

- `POST /outfit/recommend`: Get an outfit recommendation based on wardrobe items and weather

### Weather

- `POST /weather/current`: Get current weather data for a location

## API Usage

For quick testing of the backend API:

### Analyze Clothing Image
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/image.jpg" \
  -F "add_to_wardrobe=true"
```

### Get Wardrobe Items
```bash
curl -X GET "http://localhost:8000/wardrobe" \
  -H "accept: application/json"
```

### Get Outfit Recommendation
```bash
curl -X POST "http://localhost:8000/outfit/recommend" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "wardrobe_ids": ["item1", "item2", "item3"],
    "location": "New York"
  }'
```

### Get Weather Data
```bash
curl -X POST "http://localhost:8000/weather/current" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "New York"
  }'
```

## LLM Integration Options

This backend supports multiple options for LLM-based outfit recommendations:

1. **Hugging Face Inference API** (default)
   - Requires a Hugging Face API key for the hosted model
   - Uses Mistral-7B-Instruct by default

2. **Ollama** (local option)
   - Requires Ollama to be running locally
   - No API key needed, runs completely locally
   - Set `OLLAMA_MODEL` in `.env` to choose model

3. **OpenAI-compatible API**
   - For any API that's compatible with OpenAI's chat completion API
   - Can be used with LocalAI, self-hosted models, or similar services
   - Configure with `OPENAI_COMPATIBLE_URL` and `OPENAI_COMPATIBLE_KEY` in `.env`

## Project Structure

- `main.py`: FastAPI application entry point
- `api/`: API routers and Pydantic models
- `models/`: Core functionality (clothing analysis, outfit recommendations)
- `utils/`: Utility functions (storage, helpers)
- `data/`: Storage for wardrobe data and images

## Integration with Frontend

This backend is designed to integrate with the React+Vite frontend located in the `ai-stylist` directory. The frontend can make API calls to this backend for all functionality.


## Legacy Backend (Flask)

The old Flask-based backend is still available:

```bash
cd backend/ai-stylist
sh configuration/setup.sh
python analyze.py
# Test with: curl -X POST -v -F "file=@image.png" http://127.0.0.1:5000/analyze
```