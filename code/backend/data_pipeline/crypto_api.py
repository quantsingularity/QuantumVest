"""
Cryptocurrency API Module
Fetches cryptocurrency data from public APIs
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

import pandas as pd
import requests

from .data_fetcher import DataFetcher, DataValidator

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class CryptoDataFetcher(DataFetcher):
    """Fetches cryptocurrency data from CoinGecko API"""

    def __init__(self, cache_dir: str = "../../resources/data_cache"):
        """
        Initialize the crypto data fetcher

        Args:
            cache_dir: Directory to cache fetched data
        """
        super().__init__(cache_dir)
        self.base_url = "https://api.coingecko.com/api/v3"

    def fetch_data(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        interval: str = "daily",
    ) -> pd.DataFrame:
        """
        Fetch cryptocurrency data for the given symbol

        Args:
            symbol: The cryptocurrency symbol (e.g., 'bitcoin', 'ethereum')
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            interval: Data interval ('daily', 'hourly')

        Returns:
            DataFrame with the fetched cryptocurrency data
        """
        # Check cache first
        cached_data = self._load_from_cache(symbol, interval)
        if cached_data is not None:
            logger.info(f"Loaded cached data for {symbol}")
            return cached_data

        # Set default dates if not provided
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if start_date is None:
            # Default to 1 year of data
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

        logger.info(
            f"Fetching crypto data for {symbol} from {start_date} to {end_date}"
        )

        try:
            # Convert dates to UNIX timestamps
            from_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
            to_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())

            # Map interval to API parameter
            days = "1" if interval == "daily" else "0"

            # Construct API URL
            url = f"{self.base_url}/coins/{symbol}/market_chart/range"
            params = {
                "vs_currency": "usd",
                "from": from_timestamp,
                "to": to_timestamp,
                "days": days,
            }

            # Make API request
            response = self.session.get(url, params=params)
            self._handle_request_error(response, symbol)

            data = response.json()

            # Process the response
            if "prices" in data and "market_caps" in data and "total_volumes" in data:
                # Extract price, market cap, and volume data
                prices = data["prices"]
                market_caps = data["market_caps"]
                volumes = data["total_volumes"]

                # Create DataFrame
                df = pd.DataFrame(prices, columns=["timestamp", "close"])
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

                # Add market cap and volume
                df["market_cap"] = [item[1] for item in market_caps]
                df["volume"] = [item[1] for item in volumes]

                # Add symbol column
                df["symbol"] = symbol

                # Add placeholder columns for OHLC data (CoinGecko only provides close prices)
                df["open"] = df["close"].shift(1)
                df["high"] = df["close"]
                df["low"] = df["close"]

                # Fill first row's open price
                if not df.empty:
                    df.loc[0, "open"] = df.loc[0, "close"]

                # Validate and clean data
                df = DataValidator.validate_dataframe(df, symbol)

                # Cache the result
                self._save_to_cache(df, symbol, interval)

                return df
            else:
                logger.error(f"Invalid response format for {symbol}")
                return pd.DataFrame()

        except Exception as e:
            logger.error(f"Error fetching crypto data for {symbol}: {e}")
            return pd.DataFrame()

    def fetch_current_price(self, symbols: List[str]) -> Dict[str, float]:
        """
        Fetch current prices for multiple cryptocurrencies

        Args:
            symbols: List of cryptocurrency symbols

        Returns:
            Dictionary mapping symbols to their current prices
        """
        try:
            # Construct API URL
            url = f"{self.base_url}/simple/price"
            params = {"ids": ",".join(symbols), "vs_currencies": "usd"}

            # Make API request
            response = self.session.get(url, params=params)
            self._handle_request_error(response, ",".join(symbols))

            data = response.json()

            # Extract prices
            prices = {}
            for symbol in symbols:
                if symbol in data and "usd" in data[symbol]:
                    prices[symbol] = data[symbol]["usd"]
                else:
                    prices[symbol] = None

            return prices

        except Exception as e:
            logger.error(f"Error fetching current prices: {e}")
            return {symbol: None for symbol in symbols}

    def fetch_multiple_cryptos(
        self, symbols: List[str], interval: str = "daily"
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple cryptocurrency symbols

        Args:
            symbols: List of cryptocurrency symbols
            interval: Data interval

        Returns:
            Dictionary mapping symbols to their respective DataFrames
        """
        results = {}
        for symbol in symbols:
            results[symbol] = self.fetch_data(symbol, interval=interval)
        return results
