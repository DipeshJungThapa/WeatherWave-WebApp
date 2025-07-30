// Simple and clean ProfilePage

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { useAuth } from '../context/AuthContext';
import { User, Mail, LogOut } from 'lucide-react';

const ProfilePage = ({ user }) => {
    const { isAuthenticated, logout } = useAuth();

    if (!isAuthenticated) {
        return (
            <div className="container mx-auto p-4 max-w-2xl">
                <Card>
                    <CardHeader>
                        <CardTitle className="text-black dark:text-white">Access Denied</CardTitle>
                        <CardDescription className="text-black dark:text-white">
                            Please log in to view your profile.
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <Button 
                            onClick={() => window.location.href = '/login'} 
                            className="bg-blue-600 hover:bg-blue-700 text-white"
                        >
                            Go to Login
                        </Button>
                    </CardContent>
                </Card>
            </div>
        );
    }

    const handleLogout = async () => {
        try {
            await logout();
            window.location.href = '/';
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    return (
        <div className="container mx-auto p-4 max-w-2xl">
            <Card>
                <CardHeader>
                    <CardTitle className="text-black dark:text-white">User Profile</CardTitle>
                    <CardDescription className="text-black dark:text-white">
                        View your account details
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                    {user ? (
                        <>
                            {/* Username Display */}
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-black dark:text-white flex items-center gap-2">
                                    <User className="h-4 w-4" />
                                    Username
                                </label>
                                <div className="p-3 bg-gray-50 dark:bg-gray-700 rounded-md border">
                                    <p className="text-black dark:text-white font-medium">
                                        {user.username}
                                    </p>
                                </div>
                            </div>

                            {/* Email Display */}
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-black dark:text-white flex items-center gap-2">
                                    <Mail className="h-4 w-4" />
                                    Email
                                </label>
                                <div className="p-3 bg-gray-50 dark:bg-gray-700 rounded-md border">
                                    <p className="text-black dark:text-white font-medium">
                                        {user.email}
                                    </p>
                                </div>
                            </div>

                            {/* Logout Button */}
                            <div className="pt-4 border-t">
                                <Button 
                                    onClick={handleLogout}
                                    variant="destructive"
                                    className="bg-red-600 hover:bg-red-700 text-white"
                                >
                                    <LogOut className="mr-2 h-4 w-4" />
                                    Logout
                                </Button>
                            </div>
                        </>
                    ) : (
                        <div className="text-center py-4">
                            <p className="text-black dark:text-white">Loading user data...</p>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
};

export default ProfilePage;