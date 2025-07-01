// src/components/Navbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from './ui/button';
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from './ui/command';
import { Popover, PopoverContent, PopoverTrigger } from './ui/popover';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from './ui/dropdown-menu'; // Corrected import for DropdownMenu components

import { nepalLocations } from '../data/nepalLocations';
import { Moon, Sun, Monitor, Thermometer } from 'lucide-react'; // Corrected: Using generic Thermometer icon
import { useTheme } from 'next-themes'; // Hook from next-themes

const Navbar = () => {
  const [openLocationPicker, setOpenLocationPicker] = React.useState(false);
  const [selectedLocation, setSelectedLocation] = React.useState(null);

  const [geolocation, setGeolocation] = React.useState({ latitude: null, longitude: null, error: null });
  const [isGeoLoading, setIsGeoLoading] = React.useState(false);

  // State for Unit Toggle
  const [unit, setUnit] = React.useState('celsius'); // 'celsius' or 'fahrenheit'

  // Hook for Theme Toggle
  const { setTheme } = useTheme();

  const handleLocationSelect = (location) => {
    setSelectedLocation(location);
    setOpenLocationPicker(false);
    console.log("Selected Location from dropdown (Navbar):", location.label);
  };

  const getCurrentLocation = () => {
    if (!navigator.geolocation) {
      setGeolocation(prev => ({ ...prev, error: "Geolocation is not supported by your browser." }));
      alert("Geolocation is not supported by your browser.");
      return;
    }

    setIsGeoLoading(true);
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setGeolocation({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          error: null,
        });
        setIsGeoLoading(false);
        console.log("Current Geolocation (Navbar):", position.coords.latitude, position.coords.longitude);
        setSelectedLocation({ value: 'current', label: 'Current Location' });
      },
      (geoError) => {
        setGeolocation(prev => ({ ...prev, error: geoError.message }));
        setIsGeoLoading(false);
        console.error("Geolocation error (Navbar):", geoError.message);
        alert(`Geolocation Error: ${geoError.message}.`);
      },
      {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0,
      }
    );
  };

  return (
    <header className="bg-primary text-primary-foreground p-4 flex justify-between items-center shadow-md">
      {/* Left side: App Name/Logo */}
      <Link to="/" className="flex items-center space-x-2 text-2xl font-bold">
        <img src="/weatherwave-logo.png" alt="WeatherWave Logo" className="h-8 w-8" />
        <span>WeatherWave</span>
      </Link>

      {/* Right side: Location Selector, Toggles & Login Button */}
      <div className="flex items-center space-x-4">
        {/* Location Selector */}
        <div className="flex flex-col md:flex-row items-center space-y-2 md:space-y-0 md:space-x-2">
          <Popover open={openLocationPicker} onOpenChange={setOpenLocationPicker}>
            <PopoverTrigger asChild>
              <Button
                variant="outline"
                role="combobox"
                aria-expanded={openLocationPicker}
                className="w-full md:w-[250px] justify-between text-left flex items-center space-x-2 bg-popover text-popover-foreground hover:bg-popover/90"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-search h-4 w-4 text-muted-foreground"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                <span className="flex-grow">
                  {selectedLocation ? selectedLocation.label : "Select location..."}
                </span>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-chevrons-up-down ml-2 h-4 w-4 shrink-0 opacity-50"><path d="m7 15 5 5 5-5"/><path d="m7 9 5-5 5 5"/></svg>
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-[250px] p-0 z-50">
              <Command>
                <CommandInput placeholder="Search district or city..." className="h-9" />
                <CommandList>
                  <CommandEmpty>No location found.</CommandEmpty>
                  <CommandGroup>
                    {nepalLocations.map((location) => (
                      <CommandItem
                        key={location.value}
                        value={location.label}
                        onSelect={() => handleLocationSelect(location)}
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
            className="flex items-center space-x-2 bg-popover text-popover-foreground hover:bg-popover/90"
            onClick={getCurrentLocation}
            disabled={isGeoLoading}
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-map-pin h-4 w-4"><path d="M12 12.75a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"/><path d="M12 21.35V22m0-19v-1m9 9h1m-19 0H2m13.788 5.788 1.414 1.414M6.798 6.798 5.384 5.384m0 9.899-1.414 1.414M17.202 6.798l1.414-1.414M12 22a8 8 0 1 0 0-16 8 8 0 0 0 0 16Z"/></svg>
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
          <DropdownMenuContent align="end">
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

        {/* Unit Toggle */}
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="icon" className="text-primary-foreground hover:bg-primary/80">
              {/* Using generic Thermometer icon as specific ones are not direct exports */}
              <Thermometer className="h-5 w-5" />
              <span className="sr-only">Toggle unit</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={() => setUnit('celsius')}>
              <Thermometer className="mr-2 h-4 w-4" /> Celsius
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => setUnit('fahrenheit')}>
              <Thermometer className="mr-2 h-4 w-4" /> Fahrenheit
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        {/* Original Login Button */}
        <Button asChild>
          <Link to="/auth">Login</Link>
        </Button>
      </div>
    </header>
  );
};

export default Navbar;