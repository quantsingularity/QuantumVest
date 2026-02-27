import React, { useState, useEffect } from "react";
import { Snackbar } from "react-native-paper";

// Simple network status component without native dependencies
// In a real implementation, you would use @react-native-community/netinfo
const NetworkStatus = () => {
  const [visible, setVisible] = useState(false);
  const [isConnected, setIsConnected] = useState(true);

  // Placeholder for network monitoring
  // In production, this would use NetInfo.addEventListener
  useEffect(() => {
    // Network monitoring would go here
    // For now, this is a placeholder component
  }, []);

  if (!visible) {
    return null;
  }

  return (
    <Snackbar
      visible={visible}
      onDismiss={() => setVisible(false)}
      duration={3000}
      style={{
        backgroundColor: isConnected ? "#4caf50" : "#f44336",
      }}
    >
      {isConnected ? "Back online" : "No internet connection"}
    </Snackbar>
  );
};

export default NetworkStatus;
