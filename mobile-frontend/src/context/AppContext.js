import React, { createContext, useState, useContext, useCallback } from "react";

const AppContext = createContext(null);

export const AppProvider = ({ children }) => {
  const [theme, setTheme] = useState("light");
  const [currency, setCurrency] = useState("usd");
  const [notifications, setNotifications] = useState([]);
  const [networkStatus, setNetworkStatus] = useState("online");

  const toggleTheme = useCallback(() => {
    setTheme((prevTheme) => (prevTheme === "light" ? "dark" : "light"));
  }, []);

  const addNotification = useCallback((notification) => {
    const newNotification = {
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
      ...notification,
    };
    setNotifications((prev) => [newNotification, ...prev].slice(0, 50)); // Keep last 50
  }, []);

  const clearNotification = useCallback((id) => {
    setNotifications((prev) => prev.filter((notif) => notif.id !== id));
  }, []);

  const clearAllNotifications = useCallback(() => {
    setNotifications([]);
  }, []);

  const value = {
    theme,
    currency,
    notifications,
    networkStatus,
    toggleTheme,
    setCurrency,
    addNotification,
    clearNotification,
    clearAllNotifications,
    setNetworkStatus,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useApp must be used within an AppProvider");
  }
  return context;
};

export default AppContext;
