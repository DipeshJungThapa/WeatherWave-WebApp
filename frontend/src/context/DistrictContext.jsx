import React, { createContext, useState } from "react"; // React is needed for createContext and useState

export const DistrictContext = createContext(); // This is our "bulletin board"

export const DistrictProvider = ({ children }) => { // This is the part that "manages" the bulletin board
  const [district, setDistrict] = useState("Kathmandu"); // This is the actual data (current district)

  // The `value` is what's available to anyone "reading" from the bulletin board
  return (
    <DistrictContext.Provider value={{ district, setDistrict }}>
      {children} {/* This means any components inside DistrictProvider can access the context */}
    </DistrictContext.Provider>
  );
};