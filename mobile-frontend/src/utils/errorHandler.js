import { Alert } from 'react-native';

export const handleApiError = (error, customMessage = null) => {
    let errorMessage = customMessage || 'An error occurred. Please try again.';

    if (error.response) {
        // Server responded with error status
        errorMessage = error.response.data?.error || error.response.data?.message || errorMessage;
    } else if (error.request) {
        // Request made but no response received
        errorMessage = 'Network error. Please check your connection.';
    } else {
        // Something else happened
        errorMessage = error.message || errorMessage;
    }

    console.error('API Error:', error);
    return errorMessage;
};

export const showErrorAlert = (error, title = 'Error') => {
    const errorMessage = typeof error === 'string' ? error : handleApiError(error);
    Alert.alert(title, errorMessage);
};

export const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
};

export const validatePassword = (password) => {
    // At least 8 characters, 1 uppercase, 1 lowercase, 1 number
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
    return passwordRegex.test(password);
};

export const formatCurrency = (value, currency = 'USD') => {
    if (typeof value !== 'number') return 'N/A';
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency,
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    }).format(value);
};

export const formatNumber = (value, decimals = 2) => {
    if (typeof value !== 'number') return 'N/A';
    return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals,
    }).format(value);
};

export const formatPercentage = (value, decimals = 2) => {
    if (typeof value !== 'number') return 'N/A';
    return `${value >= 0 ? '+' : ''}${formatNumber(value, decimals)}%`;
};

export const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};
