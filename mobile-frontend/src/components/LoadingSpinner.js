import React from 'react';
import { View, StyleSheet } from 'react-native';
import { ActivityIndicator, Text } from 'react-native-paper';

const LoadingSpinner = ({ message = 'Loading...', size = 'large' }) => {
    return (
        <View style={styles.container}>
            <ActivityIndicator animating={true} size={size} />
            {message && (
                <Text variant="bodyMedium" style={styles.text}>
                    {message}
                </Text>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
    },
    text: {
        marginTop: 15,
        color: '#666',
    },
});

export default LoadingSpinner;
