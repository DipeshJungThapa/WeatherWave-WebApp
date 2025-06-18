// src/App.jsx
import { Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard'; // Import your Dashboard page
import Login from './pages/Login';       // Import your Login page

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<Dashboard />} />
    </Routes>
  );
}