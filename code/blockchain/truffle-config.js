module.exports = {
    networks: {
        development: {
            host: '127.0.0.1',
            port: 8545,
            network_id: '*',
        },
        bsc_testnet: {
            provider: () =>
                new HDWalletProvider(mnemonic, 'https://data-seed-prebsc-1-s1.binance.org:8545'),
            network_id: 97,
            confirmations: 2,
            timeoutBlocks: 200,
            gasPrice: 10000000000,
        },
    },
    compilers: {
        solc: {
            version: '0.8.0',
            settings: { optimizer: { enabled: true, runs: 200 } },
        },
    },
};
