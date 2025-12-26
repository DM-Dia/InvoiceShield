import pandas as pd
from sklearn.cluster import DBSCAN

def cluster_vendor_prices(price_history, eps=0.5, min_samples=3):
    df = pd.DataFrame(price_history, columns=["price"])
    X = df["price"].values.reshape(-1, 1)

    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
    df["cluster"] = clustering.labels_

    normal_cluster = df["cluster"].value_counts().idxmax()
    df["is_anomaly"] = df["cluster"] != normal_cluster

    anomalies = df[df["is_anomaly"]]["price"].tolist()
    return {"anomaly_prices": anomalies}