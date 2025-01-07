import React, { useState } from 'react';

const Slider = () => {
    const [timeConstraint, setTimeConstraint] = useState(0);
    const [risk, setRisk] = useState(0);
    const [importance, setImportance] = useState(0);

    return (
        <div className="sliders-container">
            <div className="slider-group">
                <label>Time Constraint: {timeConstraint}</label>
                <input 
                    type="range" 
                    min="0" 
                    max="1" 
                    step="0.1" 
                    value={timeConstraint}
                    onChange={(e) => setTimeConstraint(parseFloat(e.target.value))}
                />
            </div>

            <div className="slider-group">
                <label>Risk: {risk}</label>
                <input 
                    type="range" 
                    min="0" 
                    max="1" 
                    step="0.1" 
                    value={risk}
                    onChange={(e) => setRisk(parseFloat(e.target.value))}
                />
            </div>

            <div className="slider-group">
                <label>Importance: {importance}</label>
                <input 
                    type="range" 
                    min="0" 
                    max="1" 
                    step="0.1" 
                    value={importance}
                    onChange={(e) => setImportance(parseFloat(e.target.value))}
                />
            </div>
        </div>
    );
}

export default Slider;