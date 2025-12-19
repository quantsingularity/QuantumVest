import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import LoginScreen from '../LoginScreen';
import { useAuth } from '../../context/AuthContext';

const mockNavigation = {
    navigate: jest.fn(),
    replace: jest.fn(),
};

jest.mock('../../context/AuthContext', () => ({
    useAuth: jest.fn(),
}));

describe('LoginScreen', () => {
    const mockLogin = jest.fn();

    beforeEach(() => {
        useAuth.mockReturnValue({
            login: mockLogin,
        });
        mockLogin.mockReset();
        mockNavigation.navigate.mockReset();
        mockNavigation.replace.mockReset();
    });

    test('renders login form correctly', () => {
        const { getByText, getByPlaceholderText } = render(
            <LoginScreen navigation={mockNavigation} />,
        );

        expect(getByText('Welcome to QuantumVest')).toBeTruthy();
        expect(getByText('Sign in to access your investment portfolio')).toBeTruthy();
        expect(getByText('Sign In')).toBeTruthy();
    });

    test('allows input in username and password fields', () => {
        const { getByLabelText } = render(<LoginScreen navigation={mockNavigation} />);

        const usernameInput = getByLabelText('Username or Email');
        const passwordInput = getByLabelText('Password');

        fireEvent.changeText(usernameInput, 'testuser');
        fireEvent.changeText(passwordInput, 'password123');

        expect(usernameInput.props.value).toBe('testuser');
        expect(passwordInput.props.value).toBe('password123');
    });

    test('calls login function with correct credentials', async () => {
        mockLogin.mockResolvedValue({ success: true });

        const { getByLabelText, getByText } = render(<LoginScreen navigation={mockNavigation} />);

        const usernameInput = getByLabelText('Username or Email');
        const passwordInput = getByLabelText('Password');
        const signInButton = getByText('Sign In');

        fireEvent.changeText(usernameInput, 'testuser');
        fireEvent.changeText(passwordInput, 'password123');
        fireEvent.press(signInButton);

        await waitFor(() => {
            expect(mockLogin).toHaveBeenCalledWith('testuser', 'password123');
        });
    });

    test('toggles password visibility', () => {
        const { getByLabelText } = render(<LoginScreen navigation={mockNavigation} />);

        const passwordInput = getByLabelText('Password');

        // Initially password should be hidden
        expect(passwordInput.props.secureTextEntry).toBe(true);
    });

    test('navigates to Register screen when register button is pressed', () => {
        const { getByText } = render(<LoginScreen navigation={mockNavigation} />);

        const registerButton = getByText("Don't have an account? Register");
        fireEvent.press(registerButton);

        expect(mockNavigation.navigate).toHaveBeenCalledWith('Register');
    });

    test('navigates to Main screen when guest access is pressed', () => {
        const { getByText } = render(<LoginScreen navigation={mockNavigation} />);

        const guestButton = getByText('Continue as Guest');
        fireEvent.press(guestButton);

        expect(mockNavigation.replace).toHaveBeenCalledWith('Main');
    });
});
