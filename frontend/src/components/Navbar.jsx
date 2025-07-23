// src/components/Navbar.jsx
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from './ui/button';
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from './ui/command';
import { Popover, PopoverContent, PopoverTrigger } from './ui/popover';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from './ui/dropdown-menu';

import { nepalLocations } from '../data/nepalLocations';
import { Moon, Sun, Monitor, Thermometer } from 'lucide-react';
import { useTheme } from 'next-themes';

// Import authentication specific icons and hook
import { CgProfile } from 'react-icons/cg';
import { TbLogout } from 'react-icons/tb';
import { Heart } from 'lucide-react'; // <--- NEW: Import Heart icon for Favorites
import { useAuth } from '../context/AuthContext';

// Navbar now accepts props: onLocationChange (function) and currentDistrict (string or object)
const Navbar = ({ onLocationChange, currentDistrict, unit, toggleUnit }) => { // Added unit and toggleUnit props
    const navigate = useNavigate();
    const { isAuthenticated, user, logout } = useAuth(); // Get auth state and logout function from context

    const [openLocationPicker, setOpenLocationPicker] = useState(false);

    const [displayLocationLabel, setDisplayLocationLabel] = useState(() => {
        if (typeof currentDistrict === 'string') {
            return currentDistrict;
        } else if (currentDistrict && currentDistrict.latitude && currentDistrict.longitude) {
            return "Current Location";
        }
        return "Kathmandu"; // Fallback default
    });

    const [geolocation, setGeolocation] = useState({ latitude: null, longitude: null, error: null });
    const [isGeoLoading, setIsGeoLoading] = useState(false);

    const { setTheme } = useTheme(); // Hook for Theme Toggle

    // Effect to update displayLocationLabel when currentDistrict prop changes
    useEffect(() => {
        if (typeof currentDistrict === 'string') {
            setDisplayLocationLabel(currentDistrict);
        } else if (currentDistrict && currentDistrict.latitude && currentDistrict.longitude) {
            setDisplayLocationLabel("Current Location");
        } else {
            setDisplayLocationLabel("Kathmandu");
        }
    }, [currentDistrict]);

    const handleLocationSelect = (location) => {
        setDisplayLocationLabel(location.label);
        setOpenLocationPicker(false);
        if (onLocationChange) {
            onLocationChange(location.label);
        }
        console.log("Selected Location from dropdown (Navbar):", location.label);
    };

    const getCurrentLocation = () => {
        if (!navigator.geolocation) {
            setGeolocation(prev => ({ ...prev, error: "Geolocation is not supported by your browser." }));
            console.warn("Geolocation is not supported by your browser.");
            alert("Geolocation is not supported by your browser."); // Added alert for immediate feedback
            return;
        }

        setIsGeoLoading(true);
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const newGeoLoc = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    error: null,
                };
                setGeolocation(newGeoLoc);
                setIsGeoLoading(false);
                setDisplayLocationLabel("Current Location");
                if (onLocationChange) {
                    onLocationChange(newGeoLoc);
                }
                console.log("Current Geolocation (Navbar):", position.coords.latitude, position.coords.longitude);
            },
            (geoError) => {
                setGeolocation(prev => ({ ...prev, error: geoError.message }));
                setIsGeoLoading(false);
                console.error("Geolocation error (Navbar):", geoError.message);
                alert(`Unable to retrieve your location: ${geoError.message}. Please enable location services or select a city manually.`); // Added alert
            },
            {
                enableHighAccuracy: true,
                timeout: 5000,
                maximumAge: 0,
            }
        );
        setOpenLocationPicker(false); // Close popover after trying to get location
    };

    // New handleLogout function
    const handleLogout = async () => {
        try {
            await logout(); // Call the logout function from AuthContext
            navigate('/login'); // Redirect to login page after logout (or '/')
            // Consider showing a toast/notification instead of alert for better UX
            // alert('Logged out successfully!');
        } catch (error) {
            console.error("Logout failed:", error);
            // alert('Logout failed. Please try again.'); // Only alert if backend explicitly failed
        }
    };


    return (
        <header className="bg-primary/30 backdrop-blur-md text-primary-foreground p-4 flex justify-between items-center shadow-md border-b border-opacity-20">
            {/* Left side: App Name/Logo */}
            <Link to="/" className="flex items-center space-x-2 text-2xl font-bold">
                {/* Assuming you have weatherwave-logo.png in your public folder */}
                <img src="/weatherwave-logo.png" alt="WeatherWave Logo" className="h-8 w-8" />
                <span>WeatherWave</span>
            </Link>

            {/* Right side: Location Selector, Toggles & Auth Buttons */}
            <div className="flex items-center space-x-4">
                {/* Location Selector */}
                <div className="flex flex-col md:flex-row items-center space-y-2 md:space-y-0 md:space-x-2">
                    <Popover open={openLocationPicker} onOpenChange={setOpenLocationPicker}>
                        <PopoverTrigger asChild>
                            <Button
                                variant="outline"
                                role="combobox"
                                aria-expanded={openLocationPicker}
                                className="w-full md:w-[250px] justify-between text-left flex items-center space-x-2 bg-popover/30 backdrop-blur-md text-popover-foreground hover:bg-popover/50"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-search h-4 w-4 text-muted-foreground"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                                <span className="flex-grow">
                                    {displayLocationLabel}
                                </span>
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-chevrons-up-down ml-2 h-4 w-4 shrink-0 opacity-50"><path d="m7 15 5 5 5-5"/><path d="m7 9 5-5 5 5"/></svg>
                            </Button>
                        </PopoverTrigger>
                        <PopoverContent className="w-[250px] p-0 z-50 bg-popover/30 backdrop-blur-md">
                            <Command>
                                <CommandInput placeholder="Search district or city..." className="h-9" />
                                <CommandList className="bg-transparent">
                                    <CommandEmpty>No location found.</CommandEmpty>
                                    <CommandGroup>
                                        {nepalLocations.map((location) => (
                                            <CommandItem
                                                key={location.value}
                                                value={location.label}
                                                onSelect={() => handleLocationSelect(location)}
                                                className="data-[selected=true]:bg-primary/50"
                                            >
                                                {location.label}
                                            </CommandItem>
                                        ))}
                                    </CommandGroup>
                                </CommandList>
                            </Command>
                        </PopoverContent>
                    </Popover>

                    <Button
                        variant="outline"
                        className="flex items-center space-x-2 bg-popover/30 backdrop-blur-md text-popover-foreground hover:bg-popover/50"
                        onClick={getCurrentLocation}
                        disabled={isGeoLoading}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-map-pin h-4 w-4"><path d="M12 12.75a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M12 22a8 8 0 1 0 0-16 8 8 0 0 0 0 16Z"/></svg>
                        <span>{isGeoLoading ? 'Locating...' : 'Use Location'}</span>
                    </Button>
                </div>

                {/* Theme Toggle */}
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon" className="text-primary-foreground hover:bg-primary/80">
                            <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
                            <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
                            <span className="sr-only">Toggle theme</span>
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end" className="bg-popover/30 backdrop-blur-md">
                        <DropdownMenuItem onClick={() => setTheme("light")}>
                            <Sun className="mr-2 h-4 w-4" /> Light
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => setTheme("dark")}>
                            <Moon className="mr-2 h-4 w-4" /> Dark
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => setTheme("system")}>
                            <Monitor className="mr-2 h-4 w-4" /> System
                        </DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>

                {/* Unit Toggle (currently local to Navbar) */}
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon" className="text-primary-foreground hover:bg-primary/80" onClick={toggleUnit}>
                            <Thermometer className="h-5 w-5" />
                            <span className="sr-only">Toggle unit</span>
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end" className="bg-popover/30 backdrop-blur-md">
                        <DropdownMenuItem onClick={() => toggleUnit()}>
                            <Thermometer className="mr-2 h-4 w-4" /> Celsius
                        </DropdownMenuItem>
                        <DropdownMenuItem onClick={() => toggleUnit()}>
                            <Thermometer className="mr-2 h-4 w-4" /> Fahrenheit
                        </DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>

                {/* Conditional rendering for Login/Logout/Profile/Favorites */}
                {isAuthenticated ? (
                    <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="text-primary-foreground hover:bg-primary/80 flex items-center space-x-1">
                                <CgProfile className="h-5 w-5" />
                                <span>{user?.username || 'Profile'}</span>
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end" className="bg-popover/30 backdrop-blur-md">
                            {/* "My Profile" menu item */}
                            <DropdownMenuItem onClick={() => navigate('/profile')}>
                                <CgProfile className="mr-2 h-4 w-4" /> My Profile
                            </DropdownMenuItem>
                            {/* "My Favorites" menu item <--- NEW ITEM */}
                            <DropdownMenuItem onClick={() => navigate('/favorites')}>
                                <Heart className="mr-2 h-4 w-4" /> My Favorites
                            </DropdownMenuItem>
                            {/* "Logout" menu item */}
                            <DropdownMenuItem onClick={handleLogout}>
                                <TbLogout className="mr-2 h-4 w-4" /> Logout
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                ) : (
                    // Link to Login page when not authenticated
                    <Link to="/login">
                        <Button variant="ghost" className="text-primary-foreground hover:bg-primary/80 flex items-center space-x-1">
                            <CgProfile className="h-5 w-5" />
                            <span>Login</span>
                        </Button>
                    </Link>
                )}
            </div>
        </header>
    );
};

export default Navbar;