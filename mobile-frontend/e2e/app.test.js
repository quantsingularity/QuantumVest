describe('QuantumVest Mobile App E2E Tests', () => {
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
            await expect(element(by.text('Sign In'))).toBeVisible();
        });

        it('should allow guest access', async () => {
            await element(by.text('Continue as Guest')).tap();
            await expect(element(by.text('QuantumVest Dashboard'))).toBeVisible();
        });

        it('should navigate to register screen', async () => {
            await element(by.text("Don't have an account? Register")).tap();
            await expect(element(by.text('Create Account'))).toBeVisible();
            await element(by.text('Already have an account? Sign In')).tap();
            await expect(element(by.text('Welcome to QuantumVest'))).toBeVisible();
        });
    });

    describe('Dashboard Flow', () => {
        beforeEach(async () => {
            // Access app as guest
            await element(by.text('Continue as Guest')).tap();
            await waitFor(element(by.text('QuantumVest Dashboard')))
                .toBeVisible()
                .withTimeout(5000);
        });

        it('should display dashboard with market data', async () => {
            await expect(element(by.text('QuantumVest Dashboard'))).toBeVisible();
            await expect(element(by.text(/Backend API Status:/))).toBeVisible();
        });

        it('should navigate to News screen', async () => {
            await element(by.text('News')).tap();
            await expect(element(by.text('Crypto News'))).toBeVisible();
        });

        it('should navigate to Watchlist screen', async () => {
            await element(by.text('Watchlist')).tap();
            await expect(element(by.text('My Watchlist'))).toBeVisible();
        });

        it('should navigate to Prediction screen', async () => {
            await element(by.text('Predictions')).tap();
            await expect(element(by.text('Market Predictions'))).toBeVisible();
        });

        it('should navigate to Portfolio screen', async () => {
            await element(by.text('Portfolio')).tap();
            await expect(element(by.text('Portfolio Optimization'))).toBeVisible();
        });
    });

    describe('Watchlist Flow', () => {
        beforeEach(async () => {
            await element(by.text('Continue as Guest')).tap();
            await waitFor(element(by.text('QuantumVest Dashboard')))
                .toBeVisible()
                .withTimeout(5000);
            await element(by.text('Watchlist')).tap();
        });

        it('should add coin to watchlist', async () => {
            await element(by.id('add-coin-button')).tap();
            await expect(element(by.text('Add Coin to Watchlist'))).toBeVisible();
            await element(by.id('coin-id-input')).typeText('bitcoin');
            await element(by.text('Add')).tap();
            await expect(element(by.text('Bitcoin'))).toBeVisible();
        });

        it('should remove coin from watchlist', async () => {
            // First add a coin
            await element(by.id('add-coin-button')).tap();
            await element(by.id('coin-id-input')).typeText('ethereum');
            await element(by.text('Add')).tap();

            // Then remove it
            await element(by.id('delete-ethereum')).tap();
            await expect(element(by.text('Ethereum'))).not.toBeVisible();
        });
    });

    describe('Prediction Flow', () => {
        beforeEach(async () => {
            await element(by.text('Continue as Guest')).tap();
            await waitFor(element(by.text('QuantumVest Dashboard')))
                .toBeVisible()
                .withTimeout(5000);
            await element(by.text('Predictions')).tap();
        });

        it('should get prediction for an asset', async () => {
            await element(by.id('asset-input')).clearText();
            await element(by.id('asset-input')).typeText('BTC');
            await element(by.id('timeframe-input')).clearText();
            await element(by.id('timeframe-input')).typeText('7d');
            await element(by.id('current-price-input')).clearText();
            await element(by.id('current-price-input')).typeText('50000');

            await element(by.text('Get Prediction')).tap();

            await waitFor(element(by.text('Prediction Result')))
                .toBeVisible()
                .withTimeout(10000);
            await expect(element(by.text(/Predicted Price:/))).toBeVisible();
        });
    });

    describe('Portfolio Optimization Flow', () => {
        beforeEach(async () => {
            await element(by.text('Continue as Guest')).tap();
            await waitFor(element(by.text('QuantumVest Dashboard')))
                .toBeVisible()
                .withTimeout(5000);
            await element(by.text('Portfolio')).tap();
        });

        it('should optimize portfolio', async () => {
            await element(by.id('assets-input')).clearText();
            await element(by.id('assets-input')).typeText('BTC,ETH,ADA');
            await element(by.id('risk-tolerance-input')).clearText();
            await element(by.id('risk-tolerance-input')).typeText('0.5');

            await element(by.text('Optimize Portfolio')).tap();

            await waitFor(element(by.text('Optimization Result')))
                .toBeVisible()
                .withTimeout(10000);
            await expect(element(by.text(/Expected Return:/))).toBeVisible();
        });
    });

    describe('News Flow', () => {
        beforeEach(async () => {
            await element(by.text('Continue as Guest')).tap();
            await waitFor(element(by.text('QuantumVest Dashboard')))
                .toBeVisible()
                .withTimeout(5000);
            await element(by.text('News')).tap();
        });

        it('should display news articles', async () => {
            await waitFor(element(by.id('news-list')))
                .toBeVisible()
                .withTimeout(5000);
        });

        it('should refresh news on pull-to-refresh', async () => {
            await element(by.id('news-list')).swipe('down', 'fast');
            await waitFor(element(by.id('news-list')))
                .toBeVisible()
                .withTimeout(5000);
        });
    });

    describe('Settings Flow', () => {
        beforeEach(async () => {
            await element(by.text('Continue as Guest')).tap();
            await waitFor(element(by.text('QuantumVest Dashboard')))
                .toBeVisible()
                .withTimeout(5000);
            await element(by.id('settings-button')).tap();
        });

        it('should display settings screen', async () => {
            await expect(element(by.text('Settings'))).toBeVisible();
            await expect(element(by.text('Appearance'))).toBeVisible();
        });

        it('should toggle dark mode', async () => {
            await element(by.id('dark-mode-switch')).tap();
            // Visual verification would be needed here
        });
    });
});
