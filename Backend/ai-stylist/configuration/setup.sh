#!/bin/bash

# Define Python version
PYTHON_VERSION="python3"

echo "Setting up Flask Backend with AI Model"

# Check if Python is installed
if ! command -v $PYTHON_VERSION &> /dev/null
then
    echo "Python is not installed. Please install Python 3 and try again."
    exit 1

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install required backend dependencies
echo "Installing Flask and dependencies..."
pip install flask flask-cors opencv-python numpy werkzeug

# Install AI model dependencies 
echo "Installing AI model dependencies..."
pip install torch torchvision # PyTorch
pip install tensorflow  # TensorFlow 
pip install scikit-learn pandas  # Scikit-Learn & Pandas
pip install timm

# Create required folders
echo "Creating 'uploads' folder..."
mkdir -p uploads

