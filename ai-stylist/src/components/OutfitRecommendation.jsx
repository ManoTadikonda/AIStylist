import React from "react";

const OutfitRecommendation = ({ weatherData, stylePreference,recommendation, getOutfitRecommendation, loading, error }) => {
    return (
        <div>
            <h2>Get Outfit Recommendation</h2>

            {weatherData && (
                <div>
                    <h4>Weather Data</h4>
                    <p><strong>Temperature:</strong> {weatherData.temperature}°C</p>
                    <p><strong>Feels Like:</strong> {weatherData.temperature_feels_like}°C</p>
                    <p><strong>Humidity:</strong> {weatherData.humidity}%</p>
                    <p><strong>Wind Speed:</strong> {weatherData.wind_speed} m/s</p>
                    <p><strong>Description:</strong> {weatherData.description}</p>
                    <p><strong>Weather Condition:</strong> {weatherData.weather_condition}</p>
                </div>
            )}

            {stylePreference && <p><strong>Selected Style:</strong> {stylePreference}</p>}

            <button onClick={getOutfitRecommendation} disabled={loading}>Get Outfit Recommendation</button>

            {loading && <p>Loading...</p>}
            {error && <p style={{ color: "red" }}>{error}</p>}

            {recommendation && (
                <div>
                    <h3>Outfit Recommendation</h3>
                    <pre>{JSON.stringify(recommendation, null, 2)}</pre>
                </div>
            )}
        </div>
    );
};

export default OutfitRecommendation;
