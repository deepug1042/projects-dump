import pickle
from sklearn.cluster import KMeans
from model.preprocess import load_and_preprocess

data, scaler = load_and_preprocess(r'D:\customer_segmentation_using_kmeans\dataset\Mall_Customers.csv')
kmeans = KMeans(n_clusters=5, random_state=42)
kmeans.fit(data)

with open(r'D:\customer_segmentation_using_kmeans\model\cluster_model.pkl', 'wb') as f:
    pickle.dump((kmeans, scaler), f)
