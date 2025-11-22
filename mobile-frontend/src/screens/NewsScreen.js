import React, { useState, useEffect, useCallback } from 'react';
import { View, StyleSheet, FlatList, Alert, Linking } from 'react-native';
import {
    Appbar,
    Card,
    Text,
    ActivityIndicator,
    List,
    Divider,
    useTheme,
    Chip,
    Button,
} from 'react-native-paper';
import { getCryptoNews } from '../services/api';

const NewsScreen = ({ navigation }) => {
    const [newsArticles, setNewsArticles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [page, setPage] = useState(1);
    const [loadingMore, setLoadingMore] = useState(false);
    const [isListEnd, setIsListEnd] = useState(false); // To prevent loading more when end is reached
    const theme = useTheme();

    const fetchNews = useCallback(
        async (pageNum = 1, refreshing = false) => {
            if (loadingMore || (pageNum > 1 && isListEnd)) return; // Prevent multiple simultaneous loads or loading past end

            if (pageNum > 1) setLoadingMore(true);
            else if (refreshing) setRefreshing(true);
            else setLoading(true);

            try {
                const response = await getCryptoNews(pageNum);
                const newArticles = response.data?.data || [];

                if (newArticles.length === 0) {
                    setIsListEnd(true); // No more articles found
                } else {
                    setIsListEnd(false);
                    if (pageNum === 1) {
                        setNewsArticles(newArticles);
                    } else {
                        setNewsArticles((prevArticles) => [...prevArticles, ...newArticles]);
                    }
                }
            } catch (error) {
                console.error('Error fetching crypto news:', error);
                // Check if the error is due to the placeholder token
                if (error.config?.params?.token === 'YOUR_CRYPTONEWS_API_TOKEN') {
                    Alert.alert(
                        'API Token Missing',
                        'Please set your CryptoNews API token in src/services/api.js to fetch news.',
                    );
                    setNewsArticles([]); // Clear articles if token is missing
                    setIsListEnd(true); // Prevent further loading attempts
                } else {
                    Alert.alert(
                        'Error',
                        'Failed to fetch news articles. Please check your connection or API configuration.',
                    );
                }
            }

            if (pageNum > 1) setLoadingMore(false);
            else if (refreshing) setRefreshing(false);
            else setLoading(false);
        },
        [loadingMore, isListEnd],
    );

    useEffect(() => {
        fetchNews(1); // Initial load
    }, [fetchNews]);

    const handleRefresh = () => {
        setPage(1);
        setIsListEnd(false);
        fetchNews(1, true); // Fetch page 1 and indicate refreshing
    };

    const handleLoadMore = () => {
        if (!loading && !loadingMore && !isListEnd) {
            const nextPage = page + 1;
            setPage(nextPage);
            fetchNews(nextPage);
        }
    };

    const openArticle = (url) => {
        Linking.canOpenURL(url).then((supported) => {
            if (supported) {
                Linking.openURL(url);
            } else {
                Alert.alert('Error', `Cannot open URL: ${url}`);
            }
        });
    };

    const renderNewsItem = ({ item }) => (
        <Card style={styles.card} onPress={() => openArticle(item.news_url)} elevation={1}>
            {item.image_url && <Card.Cover source={{ uri: item.image_url }} />}
            <Card.Content>
                <Text variant="titleMedium" style={styles.titleText}>
                    {item.title}
                </Text>
                <Text variant="bodySmall" style={styles.sourceText}>
                    {item.source_name} - {new Date(item.date).toLocaleString()}
                </Text>
                <Text variant="bodyMedium" style={styles.contentText} numberOfLines={3}>
                    {item.text}
                </Text>
                <View style={styles.chipContainer}>
                    {item.tickers.map((ticker) => (
                        <Chip key={ticker} style={styles.chip} mode="outlined">
                            {ticker}
                        </Chip>
                    ))}
                    <Chip
                        style={styles.chip}
                        icon={
                            item.sentiment === 'Positive'
                                ? 'thumb-up'
                                : item.sentiment === 'Negative'
                                  ? 'thumb-down'
                                  : 'neutral'
                        }
                    >
                        {item.sentiment}
                    </Chip>
                </View>
            </Card.Content>
        </Card>
    );

    const renderFooter = () => {
        if (!loadingMore) return null;
        return <ActivityIndicator animating={true} size="small" style={{ marginVertical: 20 }} />;
    };

    return (
        <View style={[styles.container, { backgroundColor: theme.colors.background }]}>
            <Appbar.Header>
                {navigation.canGoBack() && (
                    <Appbar.BackAction onPress={() => navigation.goBack()} />
                )}
                <Appbar.Content title="Crypto News" />
                <Appbar.Action
                    icon="refresh"
                    onPress={handleRefresh}
                    disabled={loading || refreshing}
                />
            </Appbar.Header>

            {loading && page === 1 ? (
                <ActivityIndicator animating={true} size="large" style={styles.loader} />
            ) : (
                <FlatList
                    data={newsArticles}
                    renderItem={renderNewsItem}
                    keyExtractor={(item, index) => item.news_url + index} // Use URL + index as key
                    style={styles.list}
                    contentContainerStyle={styles.listContent}
                    ListEmptyComponent={
                        <Text style={styles.emptyText}>
                            No news articles found. Check API token or try refreshing.
                        </Text>
                    }
                    refreshing={refreshing}
                    onRefresh={handleRefresh}
                    onEndReached={handleLoadMore}
                    onEndReachedThreshold={0.5} // Load more when halfway through the last item
                    ListFooterComponent={renderFooter}
                    ItemSeparatorComponent={() => <Divider style={{ marginVertical: 8 }} />}
                />
            )}
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
        marginBottom: 15,
    },
    titleText: {
        marginBottom: 5,
        fontWeight: 'bold',
    },
    sourceText: {
        color: 'grey',
        marginBottom: 10,
        fontSize: 12,
    },
    contentText: {
        marginBottom: 10,
    },
    chipContainer: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        marginTop: 5,
    },
    chip: {
        marginRight: 5,
        marginBottom: 5,
    },
    emptyText: {
        textAlign: 'center',
        marginTop: 50,
        fontSize: 16,
        color: 'grey',
    },
});

export default NewsScreen;
