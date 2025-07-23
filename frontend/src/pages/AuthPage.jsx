// frontend/src/pages/AuthPage.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; 
import { useAuth } from '../context/AuthContext'; 

const AuthPage = () => {
    const { login, register, isAuthenticated } = useAuth(); 
    const navigate = useNavigate();

    const [isLoginView, setIsLoginView] = useState(true);
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState(''); 
    const [password, setPassword] = useState('');
    const [password2, setPassword2] = useState(''); 
    const [error, setError] = useState('');
    const [message, setMessage] = useState(''); 

    if (isAuthenticated) {
        navigate('/'); 
    }

    const handleLoginSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setMessage('');
        try {
            const response = await login(username, password);
            setMessage(response.message || 'Login successful!');
            navigate('/');
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
            const response = await register({ username, email, password, password2 });
            setMessage(response.message || 'Registration successful! You can now log in.');
            setIsLoginView(true);
            setUsername('');
            setEmail('');
            setPassword('');
            setPassword2('');
        } catch (err) {
            console.error("Registration Error:", err);
            let errorMessage = 'Registration failed.';
            if (err.response?.data) {
                errorMessage = Object.values(err.response.data).flat().join(' ');
            }
            setError(errorMessage);
        }
    };

    return (
        <div className="max-w-md mx-auto p-6 backdrop-blur-sm border border-opacity-10 rounded-lg shadow-lg">
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
                        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
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
                        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                    >
                        Register
                    </button>
                </form>
            )}

            <div className="mt-6 text-center">
                <button
                    onClick={() => setIsLoginView(!isLoginView)}
                    className="text-blue-600 hover:text-blue-800 hover:underline text-sm font-medium"
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