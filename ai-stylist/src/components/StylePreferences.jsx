import React from 'react';
import './StylesPreferences.css';

const StylePreferences = ({ style, onStyleChange }) => {
    return (
        <div>
            <h3>Enter Your Style Preference (e.g., casual, formal, athletic)</h3>
            <input
                type="text"
                value={style}
                onChange={(event) => onStyleChange(event.target.value)}
                placeholder="Style preference"
            />
        </div>
    );
};

export default StylePreferences;
