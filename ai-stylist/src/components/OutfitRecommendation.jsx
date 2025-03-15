import React from "react";

const OutfitRecommendation = ({recommendation, getOutfitRecommendation, loading, error }) => {
    return (
        <div>

            <button onClick={getOutfitRecommendation} disabled={loading}>Get Outfit Recommendation</button>

            {loading && <p>Loading...</p>}
            {error && <p style={{ color: "red" }}>{error}</p>}

            {recommendation && recommendation.recommendation && (
                <div>
                    <h3>Outfit Recommendation</h3>
                    <ul>
                        {recommendation.recommendation.split("\n").map((line, index) => (
                            <li key={index}>{line}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default OutfitRecommendation;
