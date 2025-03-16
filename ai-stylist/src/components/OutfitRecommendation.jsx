import React from "react";

const OutfitRecommendation = ({ recommendation, getOutfitRecommendation, loading, error }) => {
    return (
        <div>
            {/* Button to get outfit recommendation */}
            <button onClick={getOutfitRecommendation} disabled={loading}>
                {loading ? "Loading..." : "Get Outfit Recommendation"}
            </button>

            {/* Show loading state */}
            {loading && <p>Loading...</p>}

            {/* Show error message */}
            {error && <p style={{ color: "red" }}>{error}</p>}

            {/* Show recommendation text */}
            {recommendation && (
                <div>
                    <h3>Outfit Recommendation</h3>
                    <ul>
                        {recommendation.recommendation.split("\n").map((line, index) => (
                            <li key={index}>{line}</li>
                        ))}
                    </ul>

                    {/* Display recommended images */}
                    {recommendation.recommended_images && recommendation.recommended_images.length > 0 ? (
                        <div>
                            <h3>Recommended Outfit Images</h3>
                            <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
                                {recommendation.recommended_images.map((imageUrl, index) => (
                                    <img
                                        key={index}
                                        src={`http://127.0.0.1:8000/data/${imageUrl}`}
                                        alt={`Outfit ${index + 1}`}
                                        style={{
                                            width: "150px",
                                            height: "150px",
                                            objectFit: "cover",
                                            borderRadius: "8px",
                                            border: "1px solid #ccc",
                                            boxShadow: "2px 2px 5px rgba(0,0,0,0.2)",
                                        }}
                                    />
                                ))}
                            </div>
                        </div>
                    ) : (
                        <p>No images available for this recommendation.</p>
                    )}
                </div>
            )}
        </div>
    );
};

export default OutfitRecommendation;
