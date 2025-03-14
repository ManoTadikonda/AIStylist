import React, { useState } from "react";
import "./UploadImage.css";

const UploadImage = () => {
    const [images, setImages] = useState([]); // Store wardrobe image previews
    const [imageFiles, setImageFiles] = useState([]); // Store actual files for upload
    const [message, setMessage] = useState("");
    const [analysisResults, setAnalysisResults] = useState({}); // Store parsed backend results

    // Handle multiple image selection
    const handleImageChange = (event) => {
        const files = Array.from(event.target.files);
        const imageURLs = files.map(file => URL.createObjectURL(file));

        setImages(prevImages => [...prevImages, ...imageURLs]); // Store previews
        setImageFiles(prevFiles => [...prevFiles, ...files]); // Store files for backend
    };

    // Upload and analyze each image
    const handleUpload = async () => {
        if (imageFiles.length === 0) {
            setMessage("Please select images first.");
            return;
        }

        setMessage("Uploading images...");

        const results = {};

        for (const file of imageFiles) {
            const formData = new FormData();
            formData.append("file", file);

            try {
                const response = await fetch("http://127.0.0.1:5000/analyze", {
                    method: "POST",
                    body: formData,
                });

                const result = await response.json();

                if (response.ok) {
                    // Parse the "results" field from the backend response
                    const parsedResults = JSON.parse(result.results);

                    results[file.name] = {
                        clothing_type: parsedResults.clothing_type.type,
                        confidence: parsedResults.clothing_type.confidence.toFixed(2),
                        dominant_colors: parsedResults.dominant_colors.map(color => `${color.color} (${color.percentage}%)`).join(", "),
                        seasonal_suitability: parsedResults.seasonal_suitability.map(season => `${season.season} (${season.probability}%)`).join(", ")
                    };
                } else {
                    setMessage(`Error analyzing ${file.name}: ${result.error}`);
                }
            } catch (error) {
                setMessage(`Error uploading ${file.name}`);
            }
        }

        setAnalysisResults(results);
        setMessage("All images uploaded and analyzed successfully!");
    };

    return (
        <div>
            <h3>Upload Clothing Images</h3>
            <input type="file" multiple onChange={handleImageChange} />

            <div className="image-preview">
                {images.map((image, index) => {
                    const fileName = imageFiles[index]?.name;
                    const result = analysisResults[fileName];

                    return (
                        <div key={index} className="image-item">
                            <img src={image} alt={`Wardrobe Item ${index + 1}`} width="100" />
                            {result && (
                                <div className="analysis-results">
                                    <p><strong>Clothing Type:</strong> {result.clothing_type} (Confidence: {result.confidence}%)</p>
                                    <p><strong>Dominant Colors:</strong> {result.dominant_colors}</p>
                                    <p><strong>Seasonal Suitability:</strong> {result.seasonal_suitability}</p>
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>

            {imageFiles.length > 0 && (
                <button onClick={handleUpload}>Upload & Analyze</button>
            )}

            {message && <p>{message}</p>}
        </div>
    );
};

export default UploadImage;
