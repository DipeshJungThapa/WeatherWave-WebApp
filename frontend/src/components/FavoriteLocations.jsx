// frontend/src/components/FavoriteLocations.jsx
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { ListIcon, XCircle } from 'lucide-react'; // Importing icons
import { Skeleton } from './ui/skeleton'; // For loading state

const FavoriteLocations = ({ onSelectFavorite, onFavoriteRemoved }) => {
    const { token, isAuthenticated } = useAuth();
    const [favorites, setFavorites] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchFavorites = async () => {
        if (!isAuthenticated || !token) {
            setFavorites([]);
            setLoading(false);
            return;
        }

        setLoading(true);
        setError(null);
        try {
            const response = await fetch('http://127.0.0.1:8000/api/favorites/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,
                },
            });

            if (response.ok) {
                const data = await response.json();
                setFavorites(data);
            } else if (response.status === 401) {
                setError("You are not authorized to view favorites. Please log in.");
                setFavorites([]);
            } else {
                const errorData = await response.json();
                setError(`Failed to fetch favorites: ${response.status} - ${JSON.stringify(errorData)}`);
                setFavorites([]);
            }
        } catch (err) {
            console.error("Network or parsing error fetching favorites:", err);
            setError("An unexpected error occurred while fetching favorites.");
            setFavorites([]);
        } finally {
            setLoading(false);
        }
    };

    const handleRemoveFavorite = async (favoriteId, cityName) => {
        if (!isAuthenticated || !token) {
            alert("You must be logged in to remove favorites!");
            return;
        }

        if (!confirm(`Are you sure you want to remove ${cityName} from your favorites?`)) {
            return;
        }

        try {
            const response = await fetch(`http://127.0.0.1:8000/api/favorites/${favoriteId}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Token ${token}`,
                },
            });

            if (response.status === 204) {
                alert(`${cityName} removed from favorites!`);
                fetchFavorites(); // Re-fetch the list to update the UI
                if (onFavoriteRemoved) {
                    onFavoriteRemoved(cityName); // Notify parent component if needed
                }
            } else if (response.status === 404) {
                alert(`${cityName} not found in your favorites or already removed.`);
                fetchFavorites(); // Re-fetch in case of desync
            } else {
                const errorData = await response.json();
                console.error('Failed to remove favorite:', response.status, errorData);
                alert(`Failed to remove favorite: ${response.status} - ${JSON.stringify(errorData)}`);
            }
        } catch (err) {
            console.error('Network error during favorite removal:', err);
            alert('An unexpected error occurred while removing favorite.');
        }
    };

    useEffect(() => {
        fetchFavorites();
    }, [isAuthenticated, token]); // Re-fetch when auth status or token changes

    if (loading) {
        return (
            <Card className="w-full">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2"><ListIcon className="h-5 w-5"/> My Favorites</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-2">
                        <Skeleton className="h-8 w-3/4" />
                        <Skeleton className="h-8 w-2/3" />
                        <Skeleton className="h-8 w-1/2" />
                    </div>
                </CardContent>
            </Card>
        );
    }

    if (error) {
        return (
            <Card className="w-full border-red-500">
                <CardHeader>
                    <CardTitle className="text-red-500 flex items-center gap-2"><XCircle className="h-5 w-5"/> Error Loading Favorites</CardTitle>
                </CardHeader>
                <CardContent>
                    <CardDescription className="text-red-400">{error}</CardDescription>
                    <Button onClick={fetchFavorites} className="mt-4">Retry</Button>
                </CardContent>
            </Card>
        );
    }

    if (!isAuthenticated) {
        return (
            <Card className="w-full">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2"><ListIcon className="h-5 w-5"/> My Favorites</CardTitle>
                </CardHeader>
                <CardContent>
                    <CardDescription>Please log in to view your favorited locations.</CardDescription>
                </CardContent>
            </Card>
        );
    }

    return (
        <Card className="w-full">
            <CardHeader>
                <CardTitle className="flex items-center gap-2">
                    <ListIcon className="h-5 w-5"/> My Favorites
                    {favorites.length > 0 && ` (${favorites.length})`}
                </CardTitle>
                <CardDescription>Your saved weather locations.</CardDescription>
            </CardHeader>
            <CardContent>
                {favorites.length === 0 ? (
                    <p className="text-muted-foreground">You haven't added any favorites yet.</p>
                ) : (
                    <ul className="space-y-2">
                        {favorites.map((fav) => (
                            <li key={fav.id} className="flex items-center justify-between p-2 border rounded-md hover:bg-accent hover:text-accent-foreground transition-colors">
                                <Button
                                    variant="link"
                                    className="text-lg font-semibold p-0 h-auto"
                                    onClick={() => onSelectFavorite(fav.city_name)}
                                >
                                    {fav.city_name}
                                </Button>
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    onClick={() => handleRemoveFavorite(fav.id, fav.city_name)}
                                    className="text-muted-foreground hover:text-red-500"
                                    title={`Remove ${fav.city_name} from favorites`}
                                >
                                    <XCircle className="h-4 w-4" />
                                </Button>
                            </li>
                        ))}
                    </ul>
                )}
            </CardContent>
        </Card>
    );
};

export default FavoriteLocations;