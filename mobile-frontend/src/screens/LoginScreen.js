import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';
import { TextInput, Button, Text, useTheme, Card } from 'react-native-paper';
import { useAuth } from '../context/AuthContext';
import { showErrorAlert, validateEmail } from '../utils/errorHandler';

const LoginScreen = ({ navigation }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const { login } = useAuth();
    const theme = useTheme();

    const handleLogin = async () => {
        if (!username.trim() || !password.trim()) {
            showErrorAlert('Please enter both username/email and password', 'Validation Error');
            return;
        }

        setLoading(true);
        try {
            const result = await login(username.trim(), password);
            if (!result.success) {
                showErrorAlert(result.error || 'Login failed', 'Login Error');
            }
        } catch (error) {
            showErrorAlert(error, 'Login Error');
        } finally {
            setLoading(false);
        }
    };

    const handleRegisterNavigation = () => {
        navigation.navigate('Register');
    };

    const handleGuestAccess = () => {
        navigation.replace('Main');
    };

    return (
        <KeyboardAvoidingView
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            style={[styles.container, { backgroundColor: theme.colors.background }]}
        >
            <ScrollView
                contentContainerStyle={styles.scrollContent}
                keyboardShouldPersistTaps="handled"
            >
                <Card style={styles.card}>
                    <Card.Content>
                        <Text variant="headlineMedium" style={styles.title}>
                            Welcome to QuantumVest
                        </Text>
                        <Text variant="bodyMedium" style={styles.subtitle}>
                            Sign in to access your investment portfolio
                        </Text>

                        <TextInput
                            label="Username or Email"
                            value={username}
                            onChangeText={setUsername}
                            mode="outlined"
                            style={styles.input}
                            autoCapitalize="none"
                            autoCorrect={false}
                            left={<TextInput.Icon icon="account" />}
                            disabled={loading}
                        />

                        <TextInput
                            label="Password"
                            value={password}
                            onChangeText={setPassword}
                            mode="outlined"
                            style={styles.input}
                            secureTextEntry={!showPassword}
                            autoCapitalize="none"
                            left={<TextInput.Icon icon="lock" />}
                            right={
                                <TextInput.Icon
                                    icon={showPassword ? 'eye-off' : 'eye'}
                                    onPress={() => setShowPassword(!showPassword)}
                                />
                            }
                            disabled={loading}
                        />

                        <Button
                            mode="contained"
                            onPress={handleLogin}
                            loading={loading}
                            disabled={loading}
                            style={styles.button}
                            icon="login"
                        >
                            Sign In
                        </Button>

                        <Button
                            mode="text"
                            onPress={handleRegisterNavigation}
                            disabled={loading}
                            style={styles.textButton}
                        >
                            Don't have an account? Register
                        </Button>

                        <Button
                            mode="outlined"
                            onPress={handleGuestAccess}
                            disabled={loading}
                            style={styles.guestButton}
                            icon="account-arrow-right"
                        >
                            Continue as Guest
                        </Button>
                    </Card.Content>
                </Card>
            </ScrollView>
        </KeyboardAvoidingView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    scrollContent: {
        flexGrow: 1,
        justifyContent: 'center',
        padding: 20,
    },
    card: {
        elevation: 4,
    },
    title: {
        textAlign: 'center',
        marginBottom: 8,
        fontWeight: 'bold',
    },
    subtitle: {
        textAlign: 'center',
        marginBottom: 24,
        color: '#666',
    },
    input: {
        marginBottom: 16,
    },
    button: {
        marginTop: 8,
        paddingVertical: 6,
    },
    textButton: {
        marginTop: 8,
    },
    guestButton: {
        marginTop: 16,
    },
});

export default LoginScreen;
