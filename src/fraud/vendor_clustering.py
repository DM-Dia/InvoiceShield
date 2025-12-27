import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

def cluster_vendors(df: pd.DataFrame):
    """
    Clusters vendors based on average invoice amount and invoice count.
    Returns dataframe with cluster labels.
    """

    vendor_features = (
        df.groupby("vendor")
        .agg(
            avg_amount=("amount", "mean"),
            invoice_count=("amount", "count")
        )
        .reset_index()
    )

    scaler = StandardScaler()
    X = scaler.fit_transform(
        vendor_features[["avg_amount", "invoice_count"]]
    )

    dbscan = DBSCAN(eps=0.8, min_samples=2)
    vendor_features["cluster"] = dbscan.fit_predict(X)

    return vendor_features
