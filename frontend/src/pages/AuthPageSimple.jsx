// Simple AuthPage - Login and Register only
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Alert, AlertDescription } from '../components/ui/alert';
import { Eye, EyeOff, Mail, Lock, User, Loader2 } from 'lucide-react';

const AuthPageSimple = ({ mode = 'login' }) => {
    const { login, register, isAuthenticated } = useAuth();
    const navigate = useNavigate();

    // Form state
    const [currentMode, setCurrentMode] = useState(mode);
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
    });
    
    // UI state
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    // Redirect if already authenticated
    useEffect(() => {
        if (isAuthenticated) {
            navigate('/dashboard');
        }
    }, [isAuthenticated, navigate]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
        
        // Clear error when user starts typing
        if (error) setError('');
        if (success) setSuccess('');
    };

    const validateForm = () => {
        if (!formData.username.trim()) {
            setError('Username is required');
            return false;
        }

        if (currentMode === 'register' && !formData.email.trim()) {
            setError('Email is required');
            return false;
        }

        if (currentMode === 'register' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
            setError('Please enter a valid email address');
            return false;
        }

        if (!formData.password) {
            setError('Password is required');
            return false;
        }

        if (formData.password.length < 8) {
            setError('Password must be at least 8 characters');
            return false;
        }

        if (currentMode === 'register' && formData.password !== formData.confirmPassword) {
            setError('Passwords do not match');
            return false;
        }

        return true;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!validateForm()) return;

        setIsLoading(true);
        setError('');
        setSuccess('');

        try {
            if (currentMode === 'login') {
                await login(formData.username, formData.password);
                setSuccess('Login successful! Redirecting...');
                setTimeout(() => navigate('/dashboard'), 1500);
            } else {
                await register({
                    username: formData.username,
                    email: formData.email,
                    password: formData.password
                });
                setSuccess('Registration successful! Please login.');
                setTimeout(() => setCurrentMode('login'), 2000);
            }
        } catch (err) {
            setError(err.response?.data?.message || err.message || 'Authentication failed');
        } finally {
            setIsLoading(false);
        }
    };

    const toggleMode = () => {
        setCurrentMode(currentMode === 'login' ? 'register' : 'login');
        setFormData({ username: '', email: '', password: '', confirmPassword: '' });
        setError('');
        setSuccess('');
    };

    return (
        <div className="min-h-screen flex items-center justify-center p-4" style={{
            background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(147, 197, 253, 0.1) 50%, rgba(219, 234, 254, 0.1) 100%)',
            backdropFilter: 'blur(10px)'
        }}>
            <div className="w-full max-w-md">
                <Card className="shadow-2xl border border-white/20 bg-white/10 dark:bg-gray-900/10 backdrop-blur-xl">
                    <CardHeader className="text-center">
                        <CardTitle className="text-2xl font-bold text-black dark:text-white">
                            {currentMode === 'login' ? 'Welcome Back' : 'Create Account'}
                        </CardTitle>
                        <CardDescription className="text-gray-700 dark:text-gray-300">
                            {currentMode === 'login' 
                                ? 'Sign in to your WeatherWave account' 
                                : 'Join WeatherWave for personalized weather forecasts'
                            }
                        </CardDescription>
                    </CardHeader>

                    <CardContent className="space-y-4">
                        {/* Alerts */}
                        {error && (
                            <Alert variant="destructive" className="border-red-300/50 bg-red-100/20 dark:bg-red-900/20 backdrop-blur-sm">
                                <AlertDescription className="text-red-800 dark:text-red-200">
                                    {error}
                                </AlertDescription>
                            </Alert>
                        )}

                        {success && (
                            <Alert className="border-green-300/50 bg-green-100/20 dark:bg-green-900/20 backdrop-blur-sm">
                                <AlertDescription className="text-green-800 dark:text-green-200">
                                    {success}
                                </AlertDescription>
                            </Alert>
                        )}

                        <form onSubmit={handleSubmit} className="space-y-4">
                            {/* Username Field */}
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-black dark:text-white">
                                    Username
                                </label>
                                <div className="relative">
                                    <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                                    <Input
                                        type="text"
                                        name="username"
                                        value={formData.username}
                                        onChange={handleInputChange}
                                        className="pl-10 text-black dark:text-white bg-white/20 dark:bg-gray-900/20 border-white/30 dark:border-gray-600/30 backdrop-blur-sm"
                                        placeholder="Enter your username"
                                        required
                                    />
                                </div>
                            </div>

                            {/* Email Field (Register only) */}
                            {currentMode === 'register' && (
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-black dark:text-white">
                                        Email
                                    </label>
                                    <div className="relative">
                                        <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                                        <Input
                                            type="email"
                                            name="email"
                                            value={formData.email}
                                            onChange={handleInputChange}
                                            className="pl-10 text-black dark:text-white bg-white/20 dark:bg-gray-900/20 border-white/30 dark:border-gray-600/30 backdrop-blur-sm"
                                            placeholder="Enter your email"
                                            required
                                        />
                                    </div>
                                </div>
                            )}

                            {/* Password Field */}
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-black dark:text-white">
                                    Password
                                </label>
                                <div className="relative">
                                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                                    <Input
                                        type={showPassword ? 'text' : 'password'}
                                        name="password"
                                        value={formData.password}
                                        onChange={handleInputChange}
                                        className="pl-10 pr-10 text-black dark:text-white bg-white/20 dark:bg-gray-900/20 border-white/30 dark:border-gray-600/30 backdrop-blur-sm"
                                        placeholder="Enter your password"
                                        required
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowPassword(!showPassword)}
                                        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                                    >
                                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                    </button>
                                </div>
                            </div>

                            {/* Confirm Password Field (Register only) */}
                            {currentMode === 'register' && (
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-black dark:text-white">
                                        Confirm Password
                                    </label>
                                    <div className="relative">
                                        <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                                        <Input
                                            type={showConfirmPassword ? 'text' : 'password'}
                                            name="confirmPassword"
                                            value={formData.confirmPassword}
                                            onChange={handleInputChange}
                                            className="pl-10 pr-10 text-black dark:text-white bg-white/20 dark:bg-gray-900/20 border-white/30 dark:border-gray-600/30 backdrop-blur-sm"
                                            placeholder="Confirm your password"
                                            required
                                        />
                                        <button
                                            type="button"
                                            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                                            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                                        >
                                            {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                        </button>
                                    </div>
                                </div>
                            )}

                            {/* Submit Button */}
                            <Button
                                type="submit"
                                disabled={isLoading}
                                className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white"
                            >
                                {isLoading ? (
                                    <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                        {currentMode === 'login' ? 'Signing In...' : 'Creating Account...'}
                                    </>
                                ) : (
                                    currentMode === 'login' ? 'Sign In' : 'Create Account'
                                )}
                            </Button>
                        </form>

                        {/* Toggle Mode */}
                        <div className="text-center pt-4 border-t border-white/20 dark:border-gray-600/20">
                            <p className="text-sm text-gray-700 dark:text-gray-300">
                                {currentMode === 'login' ? "Don't have an account?" : "Already have an account?"}
                                <button
                                    type="button"
                                    onClick={toggleMode}
                                    className="ml-2 text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 font-medium"
                                >
                                    {currentMode === 'login' ? 'Sign up' : 'Sign in'}
                                </button>
                            </p>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

export default AuthPageSimple;
