// src/routes/AppRouter.jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "../pages/Dashboard"; // We'll create this soon
import AuthPage from "../pages/AuthPage";   // We'll create this soon

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/auth" element={<AuthPage />} />
        {/* Add more routes here as needed */}
      </Routes>
    </BrowserRouter>
  );
}