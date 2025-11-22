// Test script for QuantumVest application
const testBackendConnection = async () => {
    try {
        console.log('Testing backend connection...');
        const response = await fetch('http://localhost:5000/api/health');

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Backend health check response:', data);
        return { success: true, message: 'Backend connection successful', data };
    } catch (error) {
        console.error('Backend connection test failed:', error);
        return {
            success: false,
            message: `Backend connection failed: ${error.message}`,
        };
    }
};

const testPredictionEndpoint = async () => {
    try {
        console.log('Testing prediction endpoint...');
        const testData = {
            open: 45000,
            high: 46000,
            low: 44000,
            close: 45500,
            volume: 1000000,
            market_cap: 850000000000,
            timestamp: new Date().toISOString(),
        };

        const response = await fetch('http://localhost:5000/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(testData),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Prediction endpoint response:', data);
        return {
            success: true,
            message: 'Prediction endpoint test successful',
            data,
        };
    } catch (error) {
        console.error('Prediction endpoint test failed:', error);
        return {
            success: false,
            message: `Prediction endpoint test failed: ${error.message}`,
        };
    }
};

const testOptimizationEndpoint = async () => {
    try {
        console.log('Testing portfolio optimization endpoint...');
        const testData = {
            assets: ['BTC', 'ETH', 'SOL', 'ADA', 'DOT'],
            returns: [0.05, 0.07, 0.09, 0.04, 0.06],
            volatilities: [0.2, 0.25, 0.3, 0.18, 0.22],
            risk_tolerance: 0.5,
        };

        const response = await fetch('http://localhost:5000/api/optimize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(testData),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Optimization endpoint response:', data);
        return {
            success: true,
            message: 'Optimization endpoint test successful',
            data,
        };
    } catch (error) {
        console.error('Optimization endpoint test failed:', error);
        return {
            success: false,
            message: `Optimization endpoint test failed: ${error.message}`,
        };
    }
};

const runAllTests = async () => {
    console.log('Starting QuantumVest application tests...');

    const results = {
        backendConnection: await testBackendConnection(),
        predictionEndpoint: await testPredictionEndpoint(),
        optimizationEndpoint: await testOptimizationEndpoint(),
    };

    console.log('\nTest Results Summary:');
    console.log('=====================');

    for (const [testName, result] of Object.entries(results)) {
        console.log(
            `${testName}: ${result.success ? '✅ PASSED' : '❌ FAILED'} - ${result.message}`,
        );
    }

    const allPassed = Object.values(results).every((result) => result.success);
    console.log(
        `\nOverall Test Result: ${allPassed ? '✅ ALL TESTS PASSED' : '❌ SOME TESTS FAILED'}`,
    );

    return { results, allPassed };
};

// Run tests when script is executed directly
if (typeof window !== 'undefined') {
    console.log('Run this test in Node.js environment or from the browser console');
} else {
    runAllTests();
}

// Export functions for use in other scripts
module.exports = {
    testBackendConnection,
    testPredictionEndpoint,
    testOptimizationEndpoint,
    runAllTests,
};
