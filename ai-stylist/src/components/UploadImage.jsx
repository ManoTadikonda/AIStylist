import React, { useState } from "react";
import "./UploadImage.css";

const UploadImage = () => {
    const [images, setImages] = useState([]); // Store wardrobe image previews
    const [imageFiles, setImageFiles] = useState([]); // Store actual files for upload
    const [message, setMessage] = useState("");
    const [analysisResults, setAnalysisResults] = useState({}); // Store parsed backend results
    const [loading, setLoading] = useState(false); // Loading state

    // Handle multiple image selection
    const handleImageChange = (event) => {
        const files = Array.from(event.target.files);

        // Free old image URLs to prevent memory leaks
        images.forEach(url => URL.revokeObjectURL(url));

        const imageURLs = files.map(file => URL.createObjectURL(file));

        setImages(imageURLs); // Store previews
        setImageFiles(files); // Store files for backend
    };

    // Upload and analyze each image
    const handleUpload = async () => {
        if (imageFiles.length === 0) {
            setMessage("Please select images first.");
            return;
        }

        setLoading(true);
        setMessage("Uploading images...");

        const results = {};

        for (const file of imageFiles) {
            const formData = new FormData();
            formData.append("file", file);
            formData.append("add_to_wardrobe", "true");

            try {
                const response = await fetch("http://127.0.0.1:8000/analyze", {
                    method: "POST",
                    body: formData,
                    headers: {
                        "Accept": "application/json",
                    },
                });

                if (!response.ok) {
                    const errorResult = await response.json();
                    setMessage(`Error analyzing ${file.name}: ${errorResult.detail || "Unknown error"}`);
                    continue;
                }

                const result = await response.json();

                // Ensure result is valid and successful
                if (!result.success) {
                    setMessage(`Analysis failed for ${file.name}: ${result.error || "Unknown error"}`);
                    continue;
                }

                // Store the extracted attributes
                results[file.name] = {
                    clothing_type: result.clothing_type || "Unknown",
                    dominant_color: result.top_attributes?.color || "Unknown",
                    pattern: result.top_attributes?.pattern || "Unknown",
                    material: result.top_attributes?.material || "Unknown",
                    style: result.top_attributes?.style || "Unknown",
                    confidence: (result.clothing_type_scores?.[result.clothing_type] * 100).toFixed(2) || "N/A",
                };
            } catch (error) {
                setMessage(`Network error while uploading ${file.name}`);
            }
        }

        setAnalysisResults(results);
        setMessage("All images uploaded and analyzed successfully!");
        setLoading(false);
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
                                    <p><strong>Dominant Color:</strong> {result.dominant_color}</p>
                                    <p><strong>Pattern:</strong> {result.pattern}</p>
                                    <p><strong>Material:</strong> {result.material}</p>
                                    <p><strong>Style:</strong> {result.style}</p>
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>

            {imageFiles.length > 0 && (
                <button onClick={handleUpload} disabled={loading}>
                    {loading ? "Uploading..." : "Upload & Analyze"}
                </button>
            )}

            {message && <p className="status-message">{message}</p>}
        </div>
    );
};

export default UploadImage;
