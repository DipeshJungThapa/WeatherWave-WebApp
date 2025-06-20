// src/context/DistrictContext.jsx
import React, { createContext, useContext, useState } from "react"; // <--- NEW: useContext imported here

export const DistrictContext = createContext();

export const DistrictProvider = ({ children }) => {
  const [district, setDistrict] = useState("Kathmandu"); // Default district

  return (
    <DistrictContext.Provider value={{ district, setDistrict }}>
      {children}
    </DistrictContext.Provider>
  );
};

// <--- NEW: Helper hook to consume the DistrictContext cleanly
export const useDistrict = () => {
  const context = useContext(DistrictContext);
  if (context === undefined) {
    throw new Error('useDistrict must be used within a DistrictProvider');
  }
  return context;
};