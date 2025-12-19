import React, { createContext, useState, useContext, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

const AuthContext = createContext(null);

const AUTH_TOKEN_KEY = '@QuantumVest:auth_token';
const REFRESH_TOKEN_KEY = '@QuantumVest:refresh_token';
const USER_DATA_KEY = '@QuantumVest:user_data';

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Load saved auth state on mount
    useEffect(() => {
        loadAuthState();
    }, []);

    const loadAuthState = async () => {
        try {
            const [savedToken, savedUser] = await Promise.all([
                AsyncStorage.getItem(AUTH_TOKEN_KEY),
                AsyncStorage.getItem(USER_DATA_KEY),
            ]);

            if (savedToken && savedUser) {
                setToken(savedToken);
                setUser(JSON.parse(savedUser));
            }
        } catch (error) {
            console.error('Failed to load auth state:', error);
        } finally {
            setLoading(false);
        }
    };

    const saveAuthState = async (authToken, userData) => {
        try {
            await Promise.all([
                AsyncStorage.setItem(AUTH_TOKEN_KEY, authToken),
                AsyncStorage.setItem(USER_DATA_KEY, JSON.stringify(userData)),
            ]);
        } catch (error) {
            console.error('Failed to save auth state:', error);
        }
    };

    const clearAuthState = async () => {
        try {
            await Promise.all([
                AsyncStorage.removeItem(AUTH_TOKEN_KEY),
                AsyncStorage.removeItem(REFRESH_TOKEN_KEY),
                AsyncStorage.removeItem(USER_DATA_KEY),
            ]);
        } catch (error) {
            console.error('Failed to clear auth state:', error);
        }
    };

    const login = async (username, password) => {
        try {
            setLoading(true);
            setError(null);

            const response = await axios.post('http://localhost:5000/api/v1/auth/login', {
                username,
                password,
            });

            if (response.data.success) {
                const { access_token, refresh_token, user: userData } = response.data;
                setToken(access_token);
                setUser(userData);
                await saveAuthState(access_token, userData);
                if (refresh_token) {
                    await AsyncStorage.setItem(REFRESH_TOKEN_KEY, refresh_token);
                }
                return { success: true };
            } else {
                setError(response.data.error || 'Login failed');
                return { success: false, error: response.data.error };
            }
        } catch (error) {
            const errorMessage = error.response?.data?.error || 'Network error. Please try again.';
            setError(errorMessage);
            return { success: false, error: errorMessage };
        } finally {
            setLoading(false);
        }
    };

    const register = async (userData) => {
        try {
            setLoading(true);
            setError(null);

            const response = await axios.post(
                'http://localhost:5000/api/v1/auth/register',
                userData,
            );

            if (response.data.success) {
                // Auto-login after registration
                return await login(userData.username, userData.password);
            } else {
                setError(response.data.error || 'Registration failed');
                return { success: false, error: response.data.error };
            }
        } catch (error) {
            const errorMessage = error.response?.data?.error || 'Network error. Please try again.';
            setError(errorMessage);
            return { success: false, error: errorMessage };
        } finally {
            setLoading(false);
        }
    };

    const logout = async () => {
        setUser(null);
        setToken(null);
        await clearAuthState();
    };

    const refreshAccessToken = async () => {
        try {
            const refreshToken = await AsyncStorage.getItem(REFRESH_TOKEN_KEY);
            if (!refreshToken) {
                throw new Error('No refresh token available');
            }

            const response = await axios.post('http://localhost:5000/api/v1/auth/refresh', {
                refresh_token: refreshToken,
            });

            if (response.data.success) {
                const { access_token } = response.data;
                setToken(access_token);
                await AsyncStorage.setItem(AUTH_TOKEN_KEY, access_token);
                return access_token;
            } else {
                throw new Error('Token refresh failed');
            }
        } catch (error) {
            console.error('Failed to refresh token:', error);
            await logout();
            throw error;
        }
    };

    const value = {
        user,
        token,
        loading,
        error,
        login,
        register,
        logout,
        refreshAccessToken,
        isAuthenticated: !!user && !!token,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

export default AuthContext;
