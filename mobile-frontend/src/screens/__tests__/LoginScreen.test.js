import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import LoginScreen from '../LoginScreen';
import { AuthProvider } from '../../context/AuthContext';
import { AppProvider } from '../../context/AppContext';
import { ThemeProvider } from '../../theme/ThemeProvider';

// Mock navigation
const mockNavigate = jest.fn();
const mockReplace = jest.fn();
const navigation = {
    navigate: mockNavigate,
    replace: mockReplace,
};

// Wrapper component with all providers
const AllTheProviders = ({ children }) => {
    return (
        <AppProvider>
            <ThemeProvider>
                <AuthProvider>{children}</AuthProvider>
            </ThemeProvider>
        </AppProvider>
    );
};

const renderWithProviders = (component) => {
    return render(component, { wrapper: AllTheProviders });
};

describe('LoginScreen', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('renders correctly', () => {
        const { getByText, getByPlaceholderText } = renderWithProviders(
            <LoginScreen navigation={navigation} />,
        );

        expect(getByText('Welcome to QuantumVest')).toBeTruthy();
        expect(getByText('Sign in to access your investment portfolio')).toBeTruthy();
    });

    it('allows users to enter username and password', () => {
        const { getByLabelText } = renderWithProviders(<LoginScreen navigation={navigation} />);

        const usernameInput = getByLabelText(/Username or Email/i);
        const passwordInput = getByLabelText(/Password/i);

        fireEvent.changeText(usernameInput, 'testuser');
        fireEvent.changeText(passwordInput, 'testpassword123');

        expect(usernameInput.props.value).toBe('testuser');
        expect(passwordInput.props.value).toBe('testpassword123');
    });

    it('shows guest access button', () => {
        const { getByText } = renderWithProviders(<LoginScreen navigation={navigation} />);

        const guestButton = getByText('Continue as Guest');
        expect(guestButton).toBeTruthy();
    });

    it('navigates to register screen', () => {
        const { getByText } = renderWithProviders(<LoginScreen navigation={navigation} />);

        const registerButton = getByText(/Don't have an account\\? Register/i);
        fireEvent.press(registerButton);

        expect(mockNavigate).toHaveBeenCalledWith('Register');
    });

    it('handles guest access', () => {
        const { getByText } = renderWithProviders(<LoginScreen navigation={navigation} />);

        const guestButton = getByText('Continue as Guest');
        fireEvent.press(guestButton);

        expect(mockReplace).toHaveBeenCalledWith('Main');
    });

    it('shows loading state while logging in', async () => {
        const { getByText, getByLabelText } = renderWithProviders(
            <LoginScreen navigation={navigation} />,
        );

        const usernameInput = getByLabelText(/Username or Email/i);
        const passwordInput = getByLabelText(/Password/i);
        const loginButton = getByText('Sign In');

        fireEvent.changeText(usernameInput, 'testuser');
        fireEvent.changeText(passwordInput, 'testpassword123');
        fireEvent.press(loginButton);

        // The button should show loading state
        await waitFor(() => {
            expect(loginButton.props.accessibilityState.disabled).toBe(true);
        });
    });
});
