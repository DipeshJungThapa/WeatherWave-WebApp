// src/components/DistrictSelector.jsx
import React from 'react';
import './DistrictSelector.css'; // Import the new CSS file

export default function DistrictSelector({ district, onChange }) {
  return (
    <div className="district-selector-container">
      <label htmlFor="district-select" className="district-selector-label">Select District:</label>
      <select
        id="district-select"
        value={district}
        onChange={e => onChange(e.target.value)}
        className="district-selector-dropdown"
      >
        <option value="">Select District</option>
        <option value="Kathmandu">Kathmandu</option>
        <option value="Pokhara">Pokhara</option>
        <option value="Lalitpur">Lalitpur</option>
        {/* Add more districts as needed */}
      </select>
    </div>
  );
}