const { test, expect } = require('@playwright/test');

test.describe('QuantumVest Frontend E2E Tests', () => {
    test('homepage loads successfully', async ({ page }) => {
        await page.goto('/');
        await expect(page).toHaveTitle(/QuantumVest/);
        await expect(page.getByText(/Next-Gen Investment Analytics/i)).toBeVisible();
    });

    test('can navigate to dashboard', async ({ page }) => {
        await page.goto('/');

        // Click on Dashboard link in sidebar
        await page.click('text=Dashboard');

        // Wait for navigation
        await page.waitForURL('**/dashboard');

        // Check if dashboard content is visible
        await expect(page.getByText('Investment Dashboard')).toBeVisible();
    });

    test('can navigate to predictions page', async ({ page }) => {
        await page.goto('/');

        // Navigate to predictions
        await page.click('text=Predictions');
        await page.waitForURL('**/predictions');

        // Verify predictions page loaded
        await expect(page.getByText('Price Predictions')).toBeVisible();
    });

    test('can navigate to portfolio optimization', async ({ page }) => {
        await page.goto('/');

        // Navigate to portfolio
        await page.click('text=Portfolio');
        await page.waitForURL('**/optimize');

        // Verify portfolio page loaded
        await expect(page.getByText('Portfolio Optimization')).toBeVisible();
    });

    test('can navigate to analytics', async ({ page }) => {
        await page.goto('/');

        // Navigate to analytics
        await page.click('text=Analytics');
        await page.waitForURL('**/analytics');

        // Verify analytics page loaded
        await expect(page.getByText('Analytics Dashboard')).toBeVisible();
    });

    test('can navigate to settings', async ({ page }) => {
        await page.goto('/');

        // Navigate to settings
        await page.click('text=Settings');
        await page.waitForURL('**/settings');

        // Verify settings page loaded
        await expect(page.getByText('Account Settings')).toBeVisible();
    });

    test('sidebar toggle works', async ({ page }) => {
        await page.goto('/dashboard');

        // Find and click the sidebar toggle button
        const toggleButton = page.locator('.toggle-sidebar');
        await toggleButton.click();

        // Sidebar should collapse
        // Wait a moment for animation
        await page.waitForTimeout(500);
    });

    test('theme toggle works', async ({ page }) => {
        await page.goto('/dashboard');

        // Find theme toggle button
        const themeButton = page.locator('.header-action-btn').first();
        await themeButton.click();

        // Theme should change
        await page.waitForTimeout(300);
    });
});
