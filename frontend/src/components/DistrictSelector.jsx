// src/components/DistrictSelector.jsx
import React, { useContext } from "react"; 
import { DistrictContext } from "../context/DistrictContext"; 
import './DistrictSelector.css';
const DistrictSelector = () => {
  const { district, setDistrict } = useContext(DistrictContext);

  const handleChange = (e) => {
    setDistrict(e.target.value); 
  };

  return (
    <div className="district-selector-container">
      <label className="district-selector-label">Select District:</label>
      <select value={district} onChange={handleChange} className="district-selector-dropdown">
        <option value="Kathmandu">Kathmandu</option>
        <option value="Pokhara">Pokhara</option>
        <option value="Lalitpur">Lalitpur</option>
        
      </select>
    </div>
  );
};

export default DistrictSelector;