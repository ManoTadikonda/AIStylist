import React, { useState } from 'react';
import './App.css';
import UploadImage from './components/UploadImage.jsx';
import WeatherWidget from './components/WeatherWidget.jsx';
import StylePreferences from './components/StylePreferences.jsx';

const App = () => {
    const [images, setImages] = useState([]);
    const [style, setStyle] = useState('');
    const [isDoneUploading, setIsDoneUploading] = useState(false);
    const [isWardrobeConfirmed, setIsWardrobeConfirmed] = useState(false);

    // Handle image files passed from UploadImage
    const handleImageUpload = (files) => {
        setImages(files);
    };

    // Handle style input passed from StylePreferences
    const handleStyleChange = (styleData) => {
        setStyle(styleData);
    };

    // Confirm that the user is done uploading their wardrobe
    const handleDoneUploading = () => {
        setIsDoneUploading(true);
    };

    // Confirm if the user is ready to move on after wardrobe update
    const handleConfirmWardrobe = () => {
        setIsWardrobeConfirmed(true);
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
                    <WeatherWidget city="New York" />

                    {/* Step 4: Style Preferences */}
                    <StylePreferences onStyleChange={handleStyleChange} />
                    {style && <p>Your style preference: {style}</p>}

                    {/* Step 5: Outfit Recommendation */}
                    <p>Here is your recommended outfit based on your wardrobe, style, and today's weather.</p>
                    {/* Add logic to display the recommended outfit */}
                </>
            )}
        </div>
    );
};

export default App;
