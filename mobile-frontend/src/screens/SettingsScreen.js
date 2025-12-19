import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, Alert } from 'react-native';
import {
    Appbar,
    Card,
    List,
    Divider,
    Switch,
    useTheme,
    Text,
    Button,
    Dialog,
    Portal,
    TextInput,
} from 'react-native-paper';
import { useAuth } from '../context/AuthContext';
import { useApp } from '../context/AppContext';
import { saveCryptoNewsApiToken, getCryptoNewsApiToken } from '../services/api';

const SettingsScreen = ({ navigation }) => {
    const { user, isAuthenticated, logout } = useAuth();
    const { theme: appTheme, toggleTheme } = useApp();
    const theme = useTheme();
    const [tokenDialogVisible, setTokenDialogVisible] = useState(false);
    const [newToken, setNewToken] = useState('');
    const [isDarkMode, setIsDarkMode] = useState(appTheme === 'dark');

    const handleLogout = () => {
        Alert.alert('Logout', 'Are you sure you want to logout?', [
            { text: 'Cancel', style: 'cancel' },
            {
                text: 'Logout',
                style: 'destructive',
                onPress: async () => {
                    await logout();
                    navigation.replace('Login');
                },
            },
        ]);
    };

    const handleToggleTheme = () => {
        setIsDarkMode(!isDarkMode);
        toggleTheme();
    };

    const handleSaveToken = async () => {
        if (!newToken.trim()) {
            Alert.alert('Error', 'Please enter a valid token');
            return;
        }

        const saved = await saveCryptoNewsApiToken(newToken.trim());
        if (saved) {
            Alert.alert('Success', 'CryptoNews API token saved successfully');
            setTokenDialogVisible(false);
            setNewToken('');
        } else {
            Alert.alert('Error', 'Failed to save token');
        }
    };

    const handleOpenTokenDialog = async () => {
        const currentToken = await getCryptoNewsApiToken();
        if (currentToken && currentToken !== 'YOUR_CRYPTONEWS_API_TOKEN') {
            setNewToken(currentToken);
        }
        setTokenDialogVisible(true);
    };

    return (
        <View style={[styles.container, { backgroundColor: theme.colors.background }]}>
            <Appbar.Header>
                {navigation.canGoBack() && (
                    <Appbar.BackAction onPress={() => navigation.goBack()} />
                )}
                <Appbar.Content title="Settings" />
            </Appbar.Header>

            <ScrollView style={styles.scrollView}>
                {/* User Information */}
                {isAuthenticated && user && (
                    <Card style={styles.card}>
                        <Card.Content>
                            <Text variant="titleMedium" style={styles.cardTitle}>
                                Account Information
                            </Text>
                            <List.Item
                                title="Username"
                                description={user.username || 'N/A'}
                                left={(props) => <List.Icon {...props} icon="account" />}
                            />
                            <List.Item
                                title="Email"
                                description={user.email || 'N/A'}
                                left={(props) => <List.Icon {...props} icon="email" />}
                            />
                            <List.Item
                                title="Name"
                                description={
                                    `${user.first_name || ''} ${user.last_name || ''}`.trim() ||
                                    'N/A'
                                }
                                left={(props) => <List.Icon {...props} icon="account-circle" />}
                            />
                        </Card.Content>
                    </Card>
                )}

                {/* App Settings */}
                <Card style={styles.card}>
                    <Card.Content>
                        <Text variant="titleMedium" style={styles.cardTitle}>
                            Appearance
                        </Text>
                        <List.Item
                            title="Dark Mode"
                            description="Switch between light and dark theme"
                            left={(props) => <List.Icon {...props} icon="theme-light-dark" />}
                            right={() => (
                                <Switch value={isDarkMode} onValueChange={handleToggleTheme} />
                            )}
                        />
                    </Card.Content>
                </Card>

                {/* API Configuration */}
                <Card style={styles.card}>
                    <Card.Content>
                        <Text variant="titleMedium" style={styles.cardTitle}>
                            API Configuration
                        </Text>
                        <List.Item
                            title="CryptoNews API Token"
                            description="Configure your CryptoNews API token for live news"
                            left={(props) => <List.Icon {...props} icon="key" />}
                            onPress={handleOpenTokenDialog}
                        />
                        <Text variant="bodySmall" style={styles.helperText}>
                            Get your free token from https://cryptonews-api.com/
                        </Text>
                    </Card.Content>
                </Card>

                {/* About */}
                <Card style={styles.card}>
                    <Card.Content>
                        <Text variant="titleMedium" style={styles.cardTitle}>
                            About
                        </Text>
                        <List.Item
                            title="Version"
                            description="1.0.0"
                            left={(props) => <List.Icon {...props} icon="information" />}
                        />
                        <List.Item
                            title="QuantumVest"
                            description="AI-Powered Investment Analytics Platform"
                            left={(props) => <List.Icon {...props} icon="chart-line" />}
                        />
                    </Card.Content>
                </Card>

                {/* Logout Button */}
                {isAuthenticated && (
                    <Button
                        mode="contained"
                        onPress={handleLogout}
                        style={styles.logoutButton}
                        icon="logout"
                        buttonColor={theme.colors.error}
                    >
                        Logout
                    </Button>
                )}

                <View style={styles.bottomSpacer} />
            </ScrollView>

            {/* Token Dialog */}
            <Portal>
                <Dialog visible={tokenDialogVisible} onDismiss={() => setTokenDialogVisible(false)}>
                    <Dialog.Title>CryptoNews API Token</Dialog.Title>
                    <Dialog.Content>
                        <TextInput
                            label="API Token"
                            value={newToken}
                            onChangeText={setNewToken}
                            mode="outlined"
                            autoCapitalize="none"
                            placeholder="Enter your CryptoNews API token"
                        />
                        <Text variant="bodySmall" style={styles.dialogHelperText}>
                            Register at https://cryptonews-api.com/ to get your free API token
                        </Text>
                    </Dialog.Content>
                    <Dialog.Actions>
                        <Button onPress={() => setTokenDialogVisible(false)}>Cancel</Button>
                        <Button onPress={handleSaveToken}>Save</Button>
                    </Dialog.Actions>
                </Dialog>
            </Portal>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    scrollView: {
        flex: 1,
    },
    card: {
        margin: 15,
        marginBottom: 0,
    },
    cardTitle: {
        marginBottom: 10,
        fontWeight: 'bold',
    },
    helperText: {
        marginTop: 5,
        marginLeft: 16,
        color: '#666',
        fontSize: 12,
    },
    dialogHelperText: {
        marginTop: 10,
        color: '#666',
        fontSize: 12,
    },
    logoutButton: {
        margin: 15,
        marginTop: 20,
    },
    bottomSpacer: {
        height: 20,
    },
});

export default SettingsScreen;
