#!/usr/bin/env python3
"""
Entry point script for running the AI Stylist Backend.
This script ensures proper imports by adding the current directory to the Python path.
"""
import os
import sys

import uvicorn

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Run the application with uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
