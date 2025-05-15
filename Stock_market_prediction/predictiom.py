import numpy as np
import pandas as pd
import datetime
import os
import yfinance as yf
from tensorflow.keras.models import load_model
import joblib

def add_technical_indicators(df):
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI_14'] = 100 - (100 / (1 + rs))
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    return df

def predict_next():
    end = datetime.date.today() - datetime.timedelta(days=1)
    start = end - datetime.timedelta(days=365)

    try:
        df = yf.download('TSLA', start=start, end=end)
        if df.empty:
            raise ValueError("Empty dataframe from Yahoo")
        source = "Live data"
    except Exception as e:
        print(f"[WARNING] Live data fetch failed: {e}")
        print("[INFO] Falling back to local TSLA.csv")
        df = pd.read_csv(r'D:\Stock_market_prediction\Dataset\TSLA.csv')
        source = "CSV fallback"

    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    df = add_technical_indicators(df)
    df.dropna(inplace=True)

    if len(df) < 70:
        raise ValueError(f"{source}: Only {len(df)} valid rows after preprocessing. Need at least 70.")

    scaler = joblib.load('scaler.save')
    model = load_model('lstm_model.h5')

    scaled_data = scaler.transform(df)
    last_60 = scaled_data[-60:]
    X_test = np.reshape(last_60, (1, 60, last_60.shape[1]))

    prediction_scaled = model.predict(X_test)[0][0]
    close_index = 3
    close_min = scaler.data_min_[close_index]
    close_max = scaler.data_max_[close_index]
    predicted_close = prediction_scaled * (close_max - close_min) + close_min

    today = datetime.date.today()
    save_prediction(today, predicted_close)
    compare_with_actual(today - datetime.timedelta(days=1))

    return predicted_close

def save_prediction(date, predicted_price):
    log_file = 'prediction_log.csv'
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write('Date,Predicted_Price,Actual_Price,Error\n')

    df = pd.read_csv(log_file)
    date_str = str(date)

    if date_str not in df['Date'].values:
        with open(log_file, 'a') as f:
            f.write(f'{date},{predicted_price:.2f},,\n')

def compare_with_actual(yesterday):
    try:
        data = yf.download('TSLA', start=str(yesterday), end=str(yesterday + datetime.timedelta(days=1)))
        if data.empty:
            print(f"[INFO] No actual data available for {yesterday}")
            return

        actual_price = data['Close'].iloc[0]
        today_str = str(yesterday + datetime.timedelta(days=1))

        log_file = 'prediction_log.csv'
        df = pd.read_csv(log_file)

        mask = df['Date'] == today_str
        if mask.any():
            df.loc[mask, 'Actual_Price'] = actual_price
            df.loc[mask, 'Error'] = abs(df.loc[mask, 'Predicted_Price'] - actual_price)
            df.to_csv(log_file, index=False)
    except Exception as e:
        print(f"[WARNING] Failed to fetch actual price: {e}")
