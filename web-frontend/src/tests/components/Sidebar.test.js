import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Sidebar from '../../components/layout/Sidebar';

describe('Sidebar Component', () => {
    test('renders sidebar with logo and navigation links', () => {
        render(
            <BrowserRouter>
                <Sidebar />
            </BrowserRouter>,
        );

        // Check for logo
        expect(screen.getByText('QuantumVest')).toBeInTheDocument();

        // Check for navigation links
        expect(screen.getByText('Dashboard')).toBeInTheDocument();
        expect(screen.getByText('Predictions')).toBeInTheDocument();
        expect(screen.getByText('Portfolio')).toBeInTheDocument();
        expect(screen.getByText('Analytics')).toBeInTheDocument();
        expect(screen.getByText('Settings')).toBeInTheDocument();
    });

    test('navigation links have correct hrefs', () => {
        render(
            <BrowserRouter>
                <Sidebar />
            </BrowserRouter>,
        );

        const dashboardLink = screen.getByText('Dashboard').closest('a');
        const predictionsLink = screen.getByText('Predictions').closest('a');
        const portfolioLink = screen.getByText('Portfolio').closest('a');
        const analyticsLink = screen.getByText('Analytics').closest('a');
        const settingsLink = screen.getByText('Settings').closest('a');

        expect(dashboardLink).toHaveAttribute('href', '/');
        expect(predictionsLink).toHaveAttribute('href', '/predictions');
        expect(portfolioLink).toHaveAttribute('href', '/optimize');
        expect(analyticsLink).toHaveAttribute('href', '/analytics');
        expect(settingsLink).toHaveAttribute('href', '/settings');
    });

    test('active link has active class', () => {
        // Mock window.location
        Object.defineProperty(window, 'location', {
            value: {
                pathname: '/predictions',
            },
            writable: true,
        });

        render(
            <BrowserRouter>
                <Sidebar />
            </BrowserRouter>,
        );

        const predictionsLink = screen.getByText('Predictions').closest('a');
        expect(predictionsLink).toHaveClass('active');

        // Other links should not have active class
        const dashboardLink = screen.getByText('Dashboard').closest('a');
        expect(dashboardLink).not.toHaveClass('active');
    });

    test('displays user information in footer', () => {
        render(
            <BrowserRouter>
                <Sidebar />
            </BrowserRouter>,
        );

        const userSection = document.querySelector('.user-info');
        expect(userSection).toBeInTheDocument();

        // Check for user avatar and details
        expect(document.querySelector('.user-avatar')).toBeInTheDocument();
        expect(screen.getByText(/John Doe/)).toBeInTheDocument();
        expect(screen.getByText(/Pro Plan/)).toBeInTheDocument();
    });
});
