import React, { useState } from 'react';
import './App.css';
import UploadImage from './components/UploadImage.jsx';
import WeatherWidget from './components/WeatherWidget.jsx';
import StylePreferences from './components/StylePreferences.jsx';
import OutfitRecommendation from './components/OutfitRecommendation.jsx';
import axios from 'axios';

const App = () => {
    const [images, setImages] = useState([]); // Store uploaded wardrobe images
    const [style, setStyle] = useState(''); // Store user style preference
    const [weatherData, setWeatherData] = useState(null); // Store fetched weather data
    const [isDoneUploading, setIsDoneUploading] = useState(false);
    const [isWardrobeConfirmed, setIsWardrobeConfirmed] = useState(false);
    const [recommendation, setRecommendation] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Handle uploaded wardrobe images
    const handleImageUpload = (files) => {
        setImages(files);
    };

    // Handle user-selected style preference
    const handleStyleChange = (styleData) => {
        setStyle(styleData);
    };

    // Handle fetched weather data
    const handleWeatherChange = (weatherResponse) => {
        const processedWeather = {
            locationData: weatherResponse.name,
            temperature: weatherResponse.main.temp,
            temperature_feels_like: weatherResponse.main.feels_like,
            humidity: weatherResponse.main.humidity,
            description: weatherResponse.weather[0].description,
            wind_speed: weatherResponse.wind.speed,
            precipitation_chance: weatherResponse.rain ? weatherResponse.rain["1h"] || 0 : 0,
            weather_condition: getWeatherCondition(weatherResponse.main.temp),
        };

        setWeatherData(processedWeather);
    };

    // Categorize weather condition based on temperature
    const getWeatherCondition = (temp) => {
        if (temp <= 5) return "cold";
        if (temp > 5 && temp <= 18) return "cool";
        if (temp > 18 && temp <= 30) return "warm";
        return "hot";
    };

    // Confirm that the user is done uploading their wardrobe
    const handleDoneUploading = () => {
        setIsDoneUploading(true);
    };

    // Confirm if the user is ready to move on after wardrobe update
    const handleConfirmWardrobe = () => {
        setIsWardrobeConfirmed(true);
    };

    // Fetch Outfit Recommendation from Backend
    const getOutfitRecommendation = async () => {
        if (!weatherData || !style) {
            setError("Ensure your wardrobe is uploaded, style preference is set, and weather data is available.");
            console.error(" Missing data:", { weatherData, style, images });
            return;
        }

        setLoading(true);
        setError(null);

        const requestData = {
            wardrobe_ids: images.map(img => img.id || "default-wardrobe-id"), // Replace with actual wardrobe item IDs
            weather_data: weatherData,
            style_preference: style,
        };

        console.log("📡 [DEBUG] Sending request to /outfit/recommend:", requestData);

        try {
            const response = await axios.post("http://127.0.0.1:8000/outfit/recommend", requestData, {
                headers: { "Content-Type": "application/json" }
            });

            console.log("✅ [SUCCESS] Received response:", response.data);

            if (!response.data.success) {
                throw new Error("Failed to fetch outfit recommendation.");
            }

            setRecommendation(response.data);
        } catch (error) {
            console.error("Failed to fetch outfit recommendation:", error);
            setError("Failed to fetch outfit recommendation. Try again later.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <h1>AI Stylist</h1>

            {!isWardrobeConfirmed ? (
                <>
                    {/* Step 1: Upload Wardrobe */}
                    <UploadImage onImageUpload={handleImageUpload} />
                    {images.length > 0 && <p>Number of images uploaded: {images.length}</p>}

                    {/* Step 2: Confirmation prompt */}
                    <button onClick={handleDoneUploading}>I'm Done Updating My Wardrobe</button>

                    {isDoneUploading && (
                        <div>
                            <p>Are you done updating your wardrobe?</p>
                            <button onClick={handleConfirmWardrobe}>Yes, Proceed</button>
                            <button onClick={() => setIsDoneUploading(false)}>No, Upload More</button>
                        </div>
                    )}
                </>
            ) : (
                <>
                    {/* Step 3: Weather Widget */}
                    <WeatherWidget onWeatherChange={handleWeatherChange} />

                    {/* Step 4: Style Preferences */}
                    <StylePreferences style={style} onStyleChange={handleStyleChange} />
                    {style && <p>Your style preference: {style}</p>}

                    {/* Step 5: Outfit Recommendation */}
                    <OutfitRecommendation
                        weatherData={weatherData}
                        stylePreference={style}
                        wardrobeItems={images}
                        recommendation={recommendation}
                        getOutfitRecommendation={getOutfitRecommendation}
                        loading={loading}
                        error={error}
                    />
                </>
            )}
        </div>
    );
};

export default App;
