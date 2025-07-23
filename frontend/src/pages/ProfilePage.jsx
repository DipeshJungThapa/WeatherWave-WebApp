// frontend/src/pages/ProfilePage.jsx

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { useAuth } from '../context/AuthContext'; // Import useAuth to check authentication status

const ProfilePage = ({ user }) => { // onSelectFavorite and onFavoriteRemoved are no longer needed here
    const { isAuthenticated, logout } = useAuth(); // Get logout from context

    if (!isAuthenticated) {
        return (
            <div className="container mx-auto p-4 max-w-2xl backdrop-blur-sm border border-opacity-10 rounded-md">
                <Card>
                    <CardHeader>
                        <CardTitle>Access Denied</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <CardDescription>Please log in to view your profile.</CardDescription>
                        {/* You might add a link to login here */}
                    </CardContent>
                </Card>
            </div>
        );
    }

    return (
        <div className="container mx-auto p-4 max-w-2xl backdrop-blur-sm border border-opacity-10 rounded-md">
            <Card>
                <CardHeader>
                    <CardTitle>User Profile</CardTitle>
                    <CardDescription>View and manage your account details.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    {user ? (
                        <>
                            <p><strong>Username:</strong> {user.username}</p>
                            <p><strong>Email:</strong> {user.email}</p>
                            {/* Add other user details you have, if any */}
                        </>
                    ) : (
                        <p>Loading user data...</p>
                    )}

                    {/* You can keep logout here, or primarily in Navbar dropdown. Having it in both is fine. */}
                    <Button onClick={logout} variant="destructive" className="text-white bg-red-600 hover:bg-red-700 border-0">
                        Logout
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
};

export default ProfilePage;