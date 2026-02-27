import React from "react";
import { View, StyleSheet } from "react-native";
import { Text, Button, useTheme } from "react-native-paper";
import Icon from "react-native-vector-icons/MaterialCommunityIcons";

const EmptyState = ({
  icon = "inbox",
  title = "No Data",
  message = "There is no data to display",
  actionLabel,
  onAction,
  iconSize = 64,
}) => {
  const theme = useTheme();

  return (
    <View
      style={[styles.container, { backgroundColor: theme.colors.background }]}
    >
      <Icon
        name={icon}
        size={iconSize}
        color={theme.colors.onSurfaceDisabled}
        style={styles.icon}
      />
      <Text
        variant="headlineSmall"
        style={[styles.title, { color: theme.colors.onSurface }]}
      >
        {title}
      </Text>
      <Text
        variant="bodyMedium"
        style={[styles.message, { color: theme.colors.onSurfaceVariant }]}
      >
        {message}
      </Text>
      {actionLabel && onAction && (
        <Button
          mode="contained"
          onPress={onAction}
          style={styles.button}
          icon={icon}
        >
          {actionLabel}
        </Button>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 24,
  },
  icon: {
    marginBottom: 16,
    opacity: 0.5,
  },
  title: {
    textAlign: "center",
    marginBottom: 8,
    fontWeight: "bold",
  },
  message: {
    textAlign: "center",
    marginBottom: 24,
    maxWidth: "80%",
  },
  button: {
    marginTop: 8,
  },
});

export default EmptyState;
