import React, { useState, useEffect } from "react";
import { View, StyleSheet, FlatList, Alert, Dimensions } from "react-native";
import {
  Appbar,
  Card,
  Text,
  Button,
  ActivityIndicator,
  List,
  Divider,
  useTheme,
} from "react-native-paper";
import { LineChart } from "react-native-chart-kit";
// Import the new CoinGecko function and the health check
import { checkApiHealth, getCoinMarketChart } from "../services/api";

const screenWidth = Dimensions.get("window").width;

// Chart configuration (can be customized further)
const chartConfig = {
  backgroundColor: "#1E2923",
  backgroundGradientFrom: "#08130D",
  backgroundGradientTo: "#1A2F2B",
  decimalPlaces: 2, // optional, defaults to 2dp
  color: (opacity = 1) => `rgba(26, 255, 146, ${opacity})`,
  labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
  style: {
    borderRadius: 16,
  },
  propsForDots: {
    r: "4",
    strokeWidth: "1",
    stroke: "#ffa726",
  },
};

const DashboardScreen = ({ navigation }) => {
  const [apiStatus, setApiStatus] = useState("Checking...");
  const [btcChartData, setBtcChartData] = useState({
    labels: [],
    datasets: [{ data: [] }],
  });
  const [ethChartData, setEthChartData] = useState({
    labels: [],
    datasets: [{ data: [] }],
  });
  const [loading, setLoading] = useState(true);
  const theme = useTheme();

  // Updated function to format data from CoinGecko's market_chart endpoint
  const formatCoinGeckoChartData = (apiResponse) => {
    const prices = apiResponse?.data?.prices;
    if (!prices || prices.length === 0) {
      return { labels: [], datasets: [{ data: [] }] };
    }

    // CoinGecko returns [timestamp, price]
    const labels = prices.map((item) =>
      new Date(item[0]).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
      }),
    );
    const data = prices.map((item) => item[1]);

    // Ensure we have at least one data point
    if (data.length === 0) {
      return { labels: [], datasets: [{ data: [] }] };
    }

    // Keep labels concise if there are many points (e.g., show every Nth label)
    const step = Math.max(1, Math.floor(labels.length / 7)); // Aim for ~7 labels
    const filteredLabels = labels.filter((_, index) => index % step === 0);
    const filteredData = data; // Keep all data points for the line

    return {
      labels: filteredLabels,
      datasets: [
        {
          data: filteredData,
        },
      ],
    };
  };

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      let backendHealthy = false;
      try {
        // Check Backend API Health first
        const healthResponse = await checkApiHealth();
        setApiStatus(
          healthResponse.data.status === "healthy" ? "Online" : "Offline",
        );
        backendHealthy = healthResponse.data.status === "healthy";
      } catch (error) {
        console.error("Error checking backend health:", error);
        setApiStatus("Error");
        // Don't alert here, let CoinGecko calls proceed if possible
      }

      try {
        // Fetch Real Data from CoinGecko (e.g., last 7 days)
        // Use CoinGecko IDs: 'bitcoin', 'ethereum'
        const btcResponse = await getCoinMarketChart("bitcoin", "7");
        setBtcChartData(formatCoinGeckoChartData(btcResponse));

        const ethResponse = await getCoinMarketChart("ethereum", "7");
        setEthChartData(formatCoinGeckoChartData(ethResponse));
      } catch (error) {
        console.error("Error fetching CoinGecko data:", error);
        // Only alert if backend is also down, otherwise maybe CoinGecko is temp unavailable
        if (!backendHealthy) {
          Alert.alert(
            "API Error",
            "Failed to fetch data from backend and CoinGecko. Please check connections.",
          );
        } else {
          Alert.alert(
            "CoinGecko Error",
            "Failed to fetch market data from CoinGecko.",
          );
        }
        // Set empty data for charts to show 'Not enough data' message
        setBtcChartData({ labels: [], datasets: [{ data: [] }] });
        setEthChartData({ labels: [], datasets: [{ data: [] }] });
      }
      setLoading(false);
    };

    fetchData();
  }, []);

  const renderChart = (chartData, title) => {
    if (
      !chartData ||
      !chartData.datasets ||
      chartData.datasets.length === 0 ||
      chartData.datasets[0].data.length < 1
    ) {
      return (
        <Text style={styles.emptyListText}>
          Not enough data to display {title} chart.
        </Text>
      );
    }
    return (
      <View style={styles.chartContainer}>
        <Text style={[styles.sectionTitle, { color: theme.colors.onSurface }]}>
          {title} Price Trend (Last 7 Days)
        </Text>
        <LineChart
          data={chartData}
          width={screenWidth - 30} // Adjust width as needed
          height={220}
          yAxisLabel="$"
          yAxisInterval={1} // Adjust interval based on data range if needed
          chartConfig={chartConfig}
          bezier // Use bezier curves for smoother lines
          style={styles.chartStyle}
        />
      </View>
    );
  };

  return (
    <View
      style={[styles.container, { backgroundColor: theme.colors.background }]}
    >
      <Appbar.Header>
        <Appbar.Content title="QuantumVest Dashboard" />
      </Appbar.Header>

      <View style={styles.contentContainer}>
        <Text
          style={[styles.statusText, { color: theme.colors.onSurfaceVariant }]}
          variant="titleMedium"
        >
          Backend API Status:{" "}
          <Text
            style={{
              color:
                apiStatus === "Online"
                  ? "green"
                  : apiStatus === "Offline"
                    ? "orange"
                    : "red",
              fontWeight: "bold",
            }}
          >
            {apiStatus}
          </Text>
        </Text>

        {loading ? (
          <ActivityIndicator
            animating={true}
            size="large"
            style={styles.loader}
          />
        ) : (
          <FlatList
            data={[{ key: "btcChart" }, { key: "ethChart" }]} // Structure data for sections
            renderItem={({ item }) => {
              if (item.key === "btcChart") {
                return renderChart(btcChartData, "Bitcoin (BTC)");
              } else if (item.key === "ethChart") {
                return renderChart(ethChartData, "Ethereum (ETH)");
              }
            }}
            keyExtractor={(item) => item.key}
            ItemSeparatorComponent={() => (
              <Divider
                style={{
                  marginVertical: 15,
                  backgroundColor: theme.colors.outlineVariant,
                }}
              />
            )}
            style={styles.listContainer}
            ListFooterComponent={
              <View style={styles.buttonContainer}>
                <Button
                  mode="contained"
                  icon="newspaper-variant-multiple" // Icon for News
                  onPress={() => navigation.navigate("News")}
                  style={styles.button}
                >
                  News
                </Button>
                <Button
                  mode="contained"
                  icon="playlist-check" // Icon for Watchlist
                  onPress={() => navigation.navigate("Watchlist")}
                  style={styles.button}
                >
                  Watchlist
                </Button>
                <Button
                  mode="contained"
                  icon="chart-line"
                  onPress={() => navigation.navigate("Prediction")}
                  style={styles.button}
                >
                  Predictions
                </Button>
                <Button
                  mode="contained"
                  icon="briefcase-check"
                  onPress={() => navigation.navigate("Portfolio")}
                  style={styles.button}
                >
                  Portfolio
                </Button>
              </View>
            }
          />
        )}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  contentContainer: {
    flex: 1,
  },
  statusText: {
    textAlign: "center",
    marginVertical: 15,
  },
  loader: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  listContainer: {
    flex: 1,
  },
  chartContainer: {
    alignItems: "center",
    marginVertical: 10,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 10,
    textAlign: "center",
  },
  chartStyle: {
    marginVertical: 8,
    borderRadius: 16,
  },
  emptyListText: {
    textAlign: "center",
    marginTop: 20,
    fontStyle: "italic",
    paddingHorizontal: 15,
  },
  buttonContainer: {
    paddingVertical: 15, // Use vertical padding
    flexDirection: "row",
    justifyContent: "space-around",
    borderTopWidth: 1,
    borderTopColor: "#eee", // Consider using theme color theme.colors.outlineVariant
    paddingHorizontal: 15,
    marginTop: 15,
  },
  button: {
    flex: 1, // Buttons share space equally
    marginHorizontal: 5, // Add space between buttons
  },
});

export default DashboardScreen;
