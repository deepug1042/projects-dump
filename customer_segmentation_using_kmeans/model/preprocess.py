import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_and_preprocess(file_path):
    df = pd.read_csv(file_path)
    df = df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']]
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df)
    return scaled, scaler
