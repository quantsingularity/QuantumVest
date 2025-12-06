import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential


def train_model() -> Any:
    data = pd.read_csv("../../resources/datasets/market_data.csv")
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data["price"].values.reshape(-1, 1))
    X, y = ([], [])
    for i in range(60, len(scaled_data)):
        X.append(scaled_data[i - 60 : i, 0])
        y.append(scaled_data[i, 0])
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mean_squared_error")
    model.fit(np.array(X), np.array(y), epochs=25, batch_size=32)
    joblib.dump((model, scaler), "../../prediction_model.pkl")
