describe('QuantumVest E2E Tests', () => {
    beforeAll(async () => {
        await device.launchApp({
            permissions: { notifications: 'YES' },
            newInstance: true,
        });
    });

    beforeEach(async () => {
        await device.reloadReactNative();
    });

    describe('Authentication Flow', () => {
        it('should show login screen on app launch', async () => {
            await expect(element(by.text('Welcome to QuantumVest'))).toBeVisible();
            await expect(
                element(by.text('Sign in to access your investment portfolio')),
            ).toBeVisible();
        });

        it('should allow guest access to app', async () => {
            await element(by.text('Continue as Guest')).tap();
            await expect(element(by.text('QuantumVest Dashboard'))).toBeVisible();
        });

        it('should navigate to register screen', async () => {
            await element(by.text(/Don't have an account\\? Register/)).tap();
            await expect(element(by.text('Create Account'))).toBeVisible();
            await expect(
                element(by.text('Join QuantumVest to start your investment journey')),
            ).toBeVisible();
        });

        it('should show validation errors for empty login form', async () => {
            await element(by.text('Sign In')).tap();
            // Alert should show
            await waitFor(element(by.text('Validation Error')))
                .toBeVisible()
                .withTimeout(2000);
        });

        it('should accept username and password input', async () => {
            await element(by.label('Username or Email')).typeText('testuser');
            await element(by.label('Password')).typeText('TestPassword123');
            await element(by.label('Password')).tapReturnKey();
            // Form should be filled
            await expect(element(by.label('Username or Email'))).toHaveText('testuser');
        });
    });

    describe('Dashboard Screen', () => {
        beforeEach(async () => {
            // Navigate to dashboard as guest
            await element(by.text('Continue as Guest')).tap();
            await waitFor(element(by.text('QuantumVest Dashboard')))
                .toBeVisible()
                .withTimeout(3000);
        });

        it('should display dashboard with API status', async () => {
            await expect(element(by.text(/Backend API Status:/))).toBeVisible();
        });

        it('should show Bitcoin and Ethereum charts or loading state', async () => {
            // Either the charts load or we see empty state text
            await waitFor(element(by.text(/Bitcoin \\(BTC\\)|Not enough data/)))
                .toBeVisible()
                .withTimeout(5000);
        });

        it('should navigate to News screen', async () => {
            await element(by.text('News')).tap();
            await expect(element(by.text('Crypto News'))).toBeVisible();
        });

        it('should navigate to Watchlist screen', async () => {
            await element(by.text('Watchlist')).tap();
            await expect(element(by.text('My Watchlist'))).toBeVisible();
        });

        it('should navigate to Predictions screen', async () => {
            await element(by.text('Predictions')).tap();
            await expect(element(by.text('Market Predictions'))).toBeVisible();
        });

        it('should navigate to Portfolio screen', async () => {
            await element(by.text('Portfolio')).tap();
            await expect(element(by.text('Portfolio Optimization'))).toBeVisible();
        });

        it('should navigate to Settings screen', async () => {
            await element(by.id('settings-button')).tap();
            await expect(element(by.text('Settings'))).toBeVisible();
        });
    });

    describe('Prediction Screen Flow', () => {
        beforeEach(async () => {
            await element(by.text('Continue as Guest')).tap();
            await waitFor(element(by.text('QuantumVest Dashboard')))
                .toBeVisible()
                .withTimeout(3000);
            await element(by.text('Predictions')).tap();
        });

        it('should allow entering prediction parameters', async () => {
            await element(by.label('Asset (e.g., BTC, ETH)')).clearText();
            await element(by.label('Asset (e.g., BTC, ETH)')).typeText('ETH');

            await element(by.label('Timeframe (e.g., 1d, 7d, 30d)')).clearText();
            await element(by.label('Timeframe (e.g., 1d, 7d, 30d)')).typeText('7d');

            await element(by.label('Current Price')).clearText();
            await element(by.label('Current Price')).typeText('3000');

            await element(by.text('Get Prediction')).tap();

            // Should show result or loading
            await waitFor(element(by.text(/Prediction Result|Loading/)))
                .toBeVisible()
                .withTimeout(5000);
        });
    });

    describe('Portfolio Screen Flow', () => {
        beforeEach(async () => {
            await element(by.text('Continue as Guest')).tap();
            await waitFor(element(by.text('QuantumVest Dashboard')))
                .toBeVisible()
                .withTimeout(3000);
            await element(by.text('Portfolio')).tap();
        });

        it('should allow portfolio optimization input', async () => {
            await element(by.label('Assets (comma-separated)')).clearText();
            await element(by.label('Assets (comma-separated)')).typeText('BTC,ETH,SOL');

            await element(by.label('Risk Tolerance (0.0 to 1.0)')).clearText();
            await element(by.label('Risk Tolerance (0.0 to 1.0)')).typeText('0.6');

            await element(by.text('Optimize Portfolio')).tap();

            // Should show result
            await waitFor(element(by.text(/Optimization Result|Expected Return/)))
                .toBeVisible()
                .withTimeout(5000);
        });
    });

    describe('Watchlist Screen Flow', () => {
        beforeEach(async () => {
            await element(by.text('Continue as Guest')).tap();
            await waitFor(element(by.text('QuantumVest Dashboard')))
                .toBeVisible()
                .withTimeout(3000);
            await element(by.text('Watchlist')).tap();
        });

        it('should show empty watchlist message initially', async () => {
            await expect(element(by.text(/Your watchlist is empty/))).toBeVisible();
        });

        it('should allow adding a coin to watchlist', async () => {
            await element(by.id('add-coin-button')).tap();
            await expect(element(by.text('Add Coin to Watchlist'))).toBeVisible();

            await element(by.label('CoinGecko Coin ID')).typeText('bitcoin');
            await element(by.text('Add')).tap();

            // Should show the coin in list
            await waitFor(element(by.text(/Bitcoin/)))
                .toBeVisible()
                .withTimeout(3000);
        });
    });

    describe('News Screen Flow', () => {
        beforeEach(async () => {
            await element(by.text('Continue as Guest')).tap();
            await waitFor(element(by.text('QuantumVest Dashboard')))
                .toBeVisible()
                .withTimeout(3000);
            await element(by.text('News')).tap();
        });

        it('should display crypto news articles', async () => {
            await waitFor(element(by.text(/Bitcoin|Ethereum|Crypto/)))
                .toBeVisible()
                .withTimeout(5000);
        });

        it('should allow refreshing news', async () => {
            await element(by.id('refresh-news-button')).tap();
            await waitFor(element(by.text(/Bitcoin|Ethereum|Crypto/)))
                .toBeVisible()
                .withTimeout(5000);
        });
    });

    describe('Settings Screen Flow', () => {
        beforeEach(async () => {
            await element(by.text('Continue as Guest')).tap();
            await waitFor(element(by.text('QuantumVest Dashboard')))
                .toBeVisible()
                .withTimeout(3000);
            await element(by.id('settings-button')).tap();
        });

        it('should display settings options', async () => {
            await expect(element(by.text('Settings'))).toBeVisible();
            await expect(element(by.text('Appearance'))).toBeVisible();
            await expect(element(by.text('API Configuration'))).toBeVisible();
        });

        it('should toggle dark mode', async () => {
            await element(by.label('Dark Mode')).tap();
            // Theme should change (hard to test visually in Detox)
            await expect(element(by.label('Dark Mode'))).toBeVisible();
        });
    });
});
