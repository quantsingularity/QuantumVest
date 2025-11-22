import React, { useState, useEffect, useCallback } from 'react';
import { View, StyleSheet, FlatList, Alert } from 'react-native';
import {
    Appbar,
    Card,
    Text,
    TextInput,
    Button,
    ActivityIndicator,
    List,
    Divider,
    useTheme,
    IconButton,
    Dialog,
    Portal,
} from 'react-native-paper';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios'; // Need axios for simple price endpoint

const COINGECKO_API_BASE_URL = 'https://api.coingecko.com/api/v3';
const WATCHLIST_STORAGE_KEY = '@QuantumVest:watchlist';

// Function to get simple price data from CoinGecko
const getSimplePrice = async (coinIds) => {
    if (!coinIds || coinIds.length === 0) {
        return {};
    }
    try {
        const response = await axios.get(`${COINGECKO_API_BASE_URL}/simple/price`, {
            params: {
                ids: coinIds.join(','),
                vs_currencies: 'usd',
            },
            headers: {
                Accept: 'application/json',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching simple price:', error);
        // Return empty object or throw error based on desired handling
        return {};
    }
};

const WatchlistScreen = ({ navigation }) => {
    const [watchlist, setWatchlist] = useState([]);
    const [watchlistData, setWatchlistData] = useState({}); // Store price data keyed by coinId
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [dialogVisible, setDialogVisible] = useState(false);
    const [newCoinId, setNewCoinId] = useState('');
    const theme = useTheme();

    const loadWatchlist = async () => {
        try {
            const storedWatchlist = await AsyncStorage.getItem(WATCHLIST_STORAGE_KEY);
            if (storedWatchlist !== null) {
                setWatchlist(JSON.parse(storedWatchlist));
            }
        } catch (e) {
            console.error('Failed to load watchlist.', e);
            Alert.alert('Error', 'Could not load watchlist from storage.');
        }
    };

    const saveWatchlist = async (newWatchlist) => {
        try {
            await AsyncStorage.setItem(WATCHLIST_STORAGE_KEY, JSON.stringify(newWatchlist));
        } catch (e) {
            console.error('Failed to save watchlist.', e);
            Alert.alert('Error', 'Could not save watchlist changes.');
        }
    };

    const fetchWatchlistData = useCallback(async (currentWatchlist) => {
        if (currentWatchlist.length === 0) {
            setWatchlistData({});
            setLoading(false);
            setRefreshing(false);
            return;
        }
        setLoading(true);
        const prices = await getSimplePrice(currentWatchlist);
        setWatchlistData(prices);
        setLoading(false);
        setRefreshing(false);
    }, []);

    useEffect(() => {
        const initialize = async () => {
            await loadWatchlist();
            // Fetch data after loading the watchlist state
        };
        initialize();
    }, []);

    // Fetch data whenever the watchlist state changes
    useEffect(() => {
        fetchWatchlistData(watchlist);
    }, [watchlist, fetchWatchlistData]);

    const handleAddCoin = async () => {
        const coinIdToAdd = newCoinId.trim().toLowerCase();
        if (!coinIdToAdd) {
            Alert.alert(
                'Input Error',
                'Please enter a valid CoinGecko coin ID (e.g., bitcoin, ethereum).',
            );
            return;
        }
        if (watchlist.includes(coinIdToAdd)) {
            Alert.alert('Duplicate', `${coinIdToAdd} is already in your watchlist.`);
            setNewCoinId('');
            setDialogVisible(false);
            return;
        }

        // Optional: Verify coin ID exists via CoinGecko API before adding
        // (Skipping for brevity, assuming user enters valid IDs)

        const newWatchlist = [...watchlist, coinIdToAdd];
        setWatchlist(newWatchlist);
        await saveWatchlist(newWatchlist);
        setNewCoinId('');
        setDialogVisible(false);
        // Data will refetch due to useEffect dependency on watchlist
    };

    const handleRemoveCoin = async (coinIdToRemove) => {
        const newWatchlist = watchlist.filter((id) => id !== coinIdToRemove);
        setWatchlist(newWatchlist);
        await saveWatchlist(newWatchlist);
        // Data will refetch due to useEffect dependency on watchlist
    };

    const onRefresh = useCallback(() => {
        setRefreshing(true);
        fetchWatchlistData(watchlist);
    }, [watchlist, fetchWatchlistData]);

    const renderWatchlistItem = ({ item: coinId }) => {
        const priceData = watchlistData[coinId];
        const currentPrice = priceData?.usd ?? 'Loading...';

        return (
            <Card style={styles.card} elevation={1}>
                <Card.Title
                    title={coinId.charAt(0).toUpperCase() + coinId.slice(1)} // Capitalize
                    subtitle={`Current Price: $${currentPrice}`}
                    subtitleStyle={styles.priceText}
                    left={(props) => <List.Icon {...props} icon="currency-usd" />} // Generic icon
                    right={(props) => (
                        <IconButton
                            {...props}
                            icon="delete"
                            onPress={() => handleRemoveCoin(coinId)}
                        />
                    )}
                />
            </Card>
        );
    };

    return (
        <View style={[styles.container, { backgroundColor: theme.colors.background }]}>
            <Appbar.Header>
                {navigation.canGoBack() && (
                    <Appbar.BackAction onPress={() => navigation.goBack()} />
                )}
                <Appbar.Content title="My Watchlist" />
                <Appbar.Action icon="plus" onPress={() => setDialogVisible(true)} />
                <Appbar.Action
                    icon="refresh"
                    onPress={onRefresh}
                    disabled={loading || refreshing}
                />
            </Appbar.Header>

            {loading && watchlist.length === 0 ? (
                <ActivityIndicator animating={true} size="large" style={styles.loader} />
            ) : (
                <FlatList
                    data={watchlist}
                    renderItem={renderWatchlistItem}
                    keyExtractor={(item) => item}
                    style={styles.list}
                    contentContainerStyle={styles.listContent}
                    ListEmptyComponent={
                        <Text style={styles.emptyText}>
                            Your watchlist is empty. Add coins using the '+' button.
                        </Text>
                    }
                    refreshing={refreshing}
                    onRefresh={onRefresh}
                    ItemSeparatorComponent={() => <Divider style={{ marginVertical: 5 }} />}
                />
            )}

            <Portal>
                <Dialog visible={dialogVisible} onDismiss={() => setDialogVisible(false)}>
                    <Dialog.Title>Add Coin to Watchlist</Dialog.Title>
                    <Dialog.Content>
                        <TextInput
                            label="CoinGecko Coin ID"
                            value={newCoinId}
                            onChangeText={setNewCoinId}
                            mode="outlined"
                            autoCapitalize="none"
                            placeholder="e.g., bitcoin, ethereum"
                        />
                        <Text style={styles.dialogHelperText}>Find IDs on CoinGecko.com</Text>
                    </Dialog.Content>
                    <Dialog.Actions>
                        <Button onPress={() => setDialogVisible(false)}>Cancel</Button>
                        <Button onPress={handleAddCoin}>Add</Button>
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
    loader: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    list: {
        flex: 1,
    },
    listContent: {
        padding: 15,
    },
    card: {
        marginBottom: 10,
    },
    priceText: {
        fontSize: 16,
        // color: theme.colors.primary // Example using theme
    },
    emptyText: {
        textAlign: 'center',
        marginTop: 50,
        fontSize: 16,
        color: 'grey',
    },
    dialogHelperText: {
        fontSize: 12,
        color: 'grey',
        marginTop: 5,
    },
});

export default WatchlistScreen;
