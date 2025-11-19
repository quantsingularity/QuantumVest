import React from 'react';

// Utility function to create a context hook with error handling
export const createContextHook = (context, hookName) => {
  return () => {
    const ctx = React.useContext(context);
    if (ctx === undefined) {
      throw new Error(`use${hookName} must be used within a ${hookName}Provider`);
    }
    return ctx;
  };
};

// Format currency values
export const formatCurrency = (value, currency = 'USD', locale = 'en-US') => {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: currency,
  }).format(value);
};

// Format percentage values
export const formatPercentage = (value, decimals = 2, locale = 'en-US') => {
  return new Intl.NumberFormat(locale, {
    style: 'percent',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value / 100);
};

// Format date values
export const formatDate = (date, options = {}, locale = 'en-US') => {
  const defaultOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  };

  return new Date(date).toLocaleDateString(
    locale,
    { ...defaultOptions, ...options }
  );
};

// Truncate text with ellipsis
export const truncateText = (text, maxLength) => {
  if (text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

// Generate random color
export const generateRandomColor = () => {
  return `#${Math.floor(Math.random() * 16777215).toString(16)}`;
};

// Debounce function for performance optimization
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

// Local storage helpers
export const storage = {
  get: (key, defaultValue = null) => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
      console.error(`Error getting item ${key} from localStorage:`, error);
      return defaultValue;
    }
  },
  set: (key, value) => {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (error) {
      console.error(`Error setting item ${key} in localStorage:`, error);
      return false;
    }
  },
  remove: (key) => {
    try {
      window.localStorage.removeItem(key);
      return true;
    } catch (error) {
      console.error(`Error removing item ${key} from localStorage:`, error);
      return false;
    }
  }
};
