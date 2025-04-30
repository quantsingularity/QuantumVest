import React, { useState } from 'react';
import '../../styles/ThemeToggle.css';

const ThemeToggle = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  const toggleTheme = () => {
    const newMode = !isDarkMode;
    setIsDarkMode(newMode);
    
    // Apply theme to document
    document.documentElement.setAttribute('data-theme', newMode ? 'dark' : 'light');
    
    // Save preference to localStorage
    localStorage.setItem('theme', newMode ? 'dark' : 'light');
  };

  return (
    <div className="theme-toggle">
      <button 
        className={`toggle-button ${isDarkMode ? 'dark-mode' : 'light-mode'}`}
        onClick={toggleTheme}
        aria-label={`Switch to ${isDarkMode ? 'light' : 'dark'} mode`}
      >
        <div className="toggle-track">
          <div className="toggle-indicator">
            <span className="toggle-icon">
              {isDarkMode ? '🌙' : '☀️'}
            </span>
          </div>
        </div>
      </button>
    </div>
  );
};

export default ThemeToggle;
