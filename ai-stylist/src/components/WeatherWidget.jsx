import React, { useState } from 'react';
import axios from 'axios';
import './WeatherWidget.css';

const WeatherWidget = ({ onWeatherChange }) => {
    const [city, setCity] = useState('');
    const [weather, setWeather] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const apiKey = "";  // Replace with your OpenWeather API key

    const fetchWeather = async () => {
        if (city === '') {
            setError("Please enter a city name.");
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;
            const response = await axios.get(url,{
                maxContentLength: 5 * 1024 * 1024,  
                maxBodyLength: 5 * 1024 * 1024      
              });

            if (response.data.cod !== 200) {
                throw new Error("Invalid city name or other issue");
            }

            setWeather(response.data);
            onWeatherChange(response.data);
            setLoading(false);
        } catch (error) {
            setError("Failed to fetch weather data. Please check the city name.");
        }
        finally {
                setLoading(false);
        }
    };



    const handleCityChange = (event) => {
        setCity(event.target.value);
    };

    const handleCitySubmit = (event) => {
        event.preventDefault();
        fetchWeather();
    };

    return (
        <div className="widget-card">
            <h3>Weather Widget</h3>
            <form onSubmit={handleCitySubmit}>
                <label>
                    Enter city:
                    <input
                        type="text"
                        value={city}
                        onChange={handleCityChange}
                        placeholder="Enter city name"
                    />
                </label>
                <button type="submit">Get Weather</button>
            </form>

            {loading && <div className="loading">Loading weather...</div>}
            {error && <div className="error">{error}</div>}
            {weather && (
                <div className="weather-info">
                    <h4>Weather in {weather.name}</h4>
                    <p>Temperature: {weather.main.temp}°C</p>
                    <p>Condition: {weather.weather[0].description}</p>
                    <p>Humidity: {weather.main.humidity}%</p>
                    <p>Wind Speed: {weather.wind.speed} m/s</p>
                </div>
            )}
        </div>
    );
};

export default WeatherWidget;
