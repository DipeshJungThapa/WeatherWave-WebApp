// frontend/src/components/ProtectedRoute.jsx
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // Import useAuth hook

const ProtectedRoute = () => {
    const { isAuthenticated, loading } = useAuth(); // Get isAuthenticated state and loading status

    // While authentication status is being loaded, you might want to show a loading spinner
    // or null to prevent flickering redirects.
    if (loading) {
        return (
            <div className="flex justify-center items-center h-screen text-xl text-foreground">
                Loading user data...
            </div>
        );
    }

    // If authenticated, render the child routes/components
    // Otherwise, redirect to the authentication page
    return isAuthenticated ? <Outlet /> : <Navigate to="/auth" replace />;
};

export default ProtectedRoute;