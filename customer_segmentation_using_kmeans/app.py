from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import csv
import os

app = Flask(__name__)

# Load model and scaler
with open(r'D:\customer_segmentation_using_kmeans\model\cluster_model.pkl', 'rb') as f:
    kmeans, scaler = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    segment = None
    label = None
    logs = []

    segment_labels = {
        0: "💸 High Income, High Spending",
        1: "🧍 Low Income, Low Spending",
        2: "📈 Average Income, Balanced Spending",
        3: "🎯 Target Customers (High Score, Moderate Income)",
        4: "👀 Low Income, High Spending (Risky)"
    }

    if request.method == 'POST':
        age = float(request.form['age'])
        income_inr = float(request.form['income'])
        income_k = income_inr / 1000
        score = float(request.form['score'])

        features = np.array([[age, income_k, score]])
        scaled_features = scaler.transform(features)
        segment = int(kmeans.predict(scaled_features)[0])
        label = segment_labels.get(segment, "Unknown Segment")

        os.makedirs('data', exist_ok=True)
        with open('data/predictions_log.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now(), age, income_inr, score, segment, label])

    # Load logs
    log_file = 'data/predictions_log.csv'
    if os.path.exists(log_file):
        with open(log_file, mode='r') as file:
            reader = csv.reader(file)
            logs = list(reader)[-10:]  # show last 10 predictions

    return render_template('index.html', segment=segment, label=label, logs=logs)

@app.route('/download_csv')
def download_csv():
    return send_file('data/predictions_log.csv', as_attachment=True)


@app.route('/clusters')
def clusters():
    df = pd.read_csv(r'D:\customer_segmentation_using_kmeans\dataset\Mall_Customers.csv')
    features = df[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']]
    scaled = scaler.transform(features)
    df['Cluster'] = kmeans.predict(scaled)

    # Save the cluster plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Annual Income (k$)', y='Spending Score (1-100)', hue='Cluster', palette='Set2')
    plt.title('Customer Segments')
    plt.savefig('static/cluster_plot.png')
    plt.close()

    # Generate segment-specific graphs
    for segment in df['Cluster'].unique():
        segment_df = df[df['Cluster'] == segment]
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=segment_df, x='Annual Income (k$)', y='Spending Score (1-100)', hue='Cluster', palette='Set2')
        plt.title(f'Segment {segment} Distribution')
        plt.savefig(f'static/segment_{segment}_plot.png')
        plt.close()

    return render_template('clusters.html', image='static/cluster_plot.png', segments=[0, 1, 2, 3, 4])


if __name__ == '__main__':
    app.run(debug=True)
