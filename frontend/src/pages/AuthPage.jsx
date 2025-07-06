// frontend/src/pages/AuthPage.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // For redirection after login/register
import { useAuth } from '../context/AuthContext'; // Import the useAuth hook

const AuthPage = () => {
    const { login, register, isAuthenticated } = useAuth(); // Get auth functions and state from context
    const navigate = useNavigate();

    const [isLoginView, setIsLoginView] = useState(true); // Toggle between login/register views
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState(''); // For registration
    const [password, setPassword] = useState('');
    const [password2, setPassword2] = useState(''); // For registration (confirm password)
    const [error, setError] = useState('');
    const [message, setMessage] = useState(''); // For success messages

    // Redirect if already authenticated
    if (isAuthenticated) {
        navigate('/'); // Redirect to dashboard if already logged in
    }

    const handleLoginSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setMessage('');
        try {
            // Call the login function from AuthContext
            const response = await login(username, password);
            setMessage(response.message || 'Login successful!');
            navigate('/'); // Redirect to dashboard on successful login
        } catch (err) {
            console.error("Login Error:", err);
            setError(err.response?.data?.error || err.response?.data?.detail || 'Login failed. Please check your credentials.');
        }
    };

    const handleRegisterSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setMessage('');

        if (password !== password2) {
            setError("Passwords do not match.");
            return;
        }

        try {
            // Call the register function from AuthContext
            const response = await register({ username, email, password, password2 });
            setMessage(response.message || 'Registration successful! You can now log in.');
            // Optionally, switch to login view after successful registration
            setIsLoginView(true);
            setUsername('');
            setEmail('');
            setPassword('');
            setPassword2('');
        } catch (err) {
            console.error("Registration Error:", err);
            // Handle specific errors returned from Django serializer if available
            let errorMessage = 'Registration failed.';
            if (err.response?.data) {
                // Assuming Django serializer sends validation errors as an object
                errorMessage = Object.values(err.response.data).flat().join(' ');
            }
            setError(errorMessage);
        }
    };

    return (
        <div className="max-w-md mx-auto p-6 bg-card rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold text-center mb-6">
                {isLoginView ? 'Login' : 'Register'}
            </h2>

            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
                    <strong className="font-bold">Error! </strong>
                    <span className="block sm:inline">{error}</span>
                </div>
            )}
            {message && (
                <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative mb-4" role="alert">
                    <strong className="font-bold">Success! </strong>
                    <span className="block sm:inline">{message}</span>
                </div>
            )}

            {isLoginView ? (
                <form onSubmit={handleLoginSubmit} className="space-y-4">
                    <div>
                        <label htmlFor="login-username" className="block text-sm font-medium text-foreground">
                            Username:
                        </label>
                        <input
                            type="text"
                            id="login-username"
                            className="mt-1 block w-full px-3 py-2 border border-input rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm bg-background text-foreground"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div>
                        <label htmlFor="login-password" className="block text-sm font-medium text-foreground">
                            Password:
                        </label>
                        <input
                            type="password"
                            id="login-password"
                            className="mt-1 block w-full px-3 py-2 border border-input rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm bg-background text-foreground"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                    >
                        Login
                    </button>
                </form>
            ) : (
                <form onSubmit={handleRegisterSubmit} className="space-y-4">
                    <div>
                        <label htmlFor="register-username" className="block text-sm font-medium text-foreground">
                            Username:
                        </label>
                        <input
                            type="text"
                            id="register-username"
                            className="mt-1 block w-full px-3 py-2 border border-input rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm bg-background text-foreground"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div>
                        <label htmlFor="register-email" className="block text-sm font-medium text-foreground">
                            Email:
                        </label>
                        <input
                            type="email"
                            id="register-email"
                            className="mt-1 block w-full px-3 py-2 border border-input rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm bg-background text-foreground"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div>
                        <label htmlFor="register-password" className="block text-sm font-medium text-foreground">
                            Password:
                        </label>
                        <input
                            type="password"
                            id="register-password"
                            className="mt-1 block w-full px-3 py-2 border border-input rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm bg-background text-foreground"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <div>
                        <label htmlFor="register-password2" className="block text-sm font-medium text-foreground">
                            Confirm Password:
                        </label>
                        <input
                            type="password"
                            id="register-password2"
                            className="mt-1 block w-full px-3 py-2 border border-input rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm bg-background text-foreground"
                            value={password2}
                            onChange={(e) => setPassword2(e.target.value)}
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                    >
                        Register
                    </button>
                </form>
            )}

            <div className="mt-6 text-center">
                <button
                    onClick={() => setIsLoginView(!isLoginView)}
                    className="text-primary hover:underline text-sm"
                >
                    {isLoginView
                        ? "Don't have an account? Register"
                        : "Already have an account? Login"}
                </button>
            </div>
        </div>
    );
};

export default AuthPage;