// src/components/StylePreferences.jsx
import React, { useState } from 'react';
import './StylesPreferences.css';

const StylePreferences = ({ onStyleChange }) => {
    const [style, setStyle] = useState('');

    // Handle style preference change
    const handleStyleChange = (event) => {
        setStyle(event.target.value);
        onStyleChange(event.target.value);  // Send style preference back to the parent component
    };

    return (
        <div>
            <h3>Enter Your Style Preference (e.g., casual, formal, athletic)</h3>
            <input
                type="text"
                value={style}
                onChange={handleStyleChange}
                placeholder="Style preference"
            />
        </div>
    );
};

export default StylePreferences;
