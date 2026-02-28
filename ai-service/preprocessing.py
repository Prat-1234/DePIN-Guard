# ai-service/preprocessing.py

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib


def preprocess_data(data_list):
    """
    Week 5: The Data Factory
    Takes a list of JSON dicts (raw sensor readings) and returns
    normalized (0-1 scaled) data ready for the AI model.

    Args:
        data_list: list of dicts, each with 'temperature', 'vibration', 'pressure'

    Returns:
        scaled_data: numpy array of shape (n_samples, 3) with values in [0, 1]
    """
    # Convert list of JSON dicts to DataFrame
    df = pd.DataFrame(data_list)

    # Select features
    features = df[['temperature', 'vibration', 'pressure']]

    # Scale Data
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(features)

    # Save the scaler so we can use it for the live app later!
    joblib.dump(scaler, 'scaler.save')

    return scaled_data


def get_preprocessed_data(df, seq_length=30):
    """
    Legacy helper: Scales data to [0,1] and converts to sequences of
    length `seq_length` for the LSTM Autoencoder (used in train.py).
    """
    # Normalization
    features = ['temperature', 'vibration']
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(df[features])

    # Sliding Window (Creating the 3D Tensor)
    xs = []
    for i in range(len(data_scaled) - seq_length):
        x = data_scaled[i:(i + seq_length)]
        xs.append(x)

    return np.array(xs), scaler