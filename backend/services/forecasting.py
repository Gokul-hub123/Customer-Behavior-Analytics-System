from __future__ import annotations

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def calculate_rfm(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()

    max_date = df["date"].max()
    rfm = (
        df.groupby("customer_id")
        .agg(
            recency=("date", lambda x: (max_date - x.max()).days),
            frequency=("transaction_id", "nunique"),
            monetary=("total_amount", "sum"),
        )
        .reset_index()
    )
    return rfm.fillna(0)


def run_customer_segmentation(df: pd.DataFrame) -> dict:
    rfm = calculate_rfm(df)
    if rfm.empty:
        return {"message": "Not enough customer data for segmentation."}

    features = rfm[["recency", "frequency", "monetary"]]
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    model = KMeans(n_clusters=3, random_state=42, n_init=10)
    rfm["cluster"] = model.fit_predict(scaled)

    cluster_summary = (
        rfm.groupby("cluster")
        .agg(
            avg_recency=("recency", "mean"),
            avg_frequency=("frequency", "mean"),
            avg_monetary=("monetary", "mean"),
            customer_count=("customer_id", "count"),
        )
        .reset_index()
    )

    cluster_summary = cluster_summary.sort_values(["avg_monetary", "avg_frequency"], ascending=False)
    cluster_labels = {
        int(cluster_summary.iloc[0]["cluster"]): "High-value customers",
        int(cluster_summary.iloc[1]["cluster"]): "Regular customers",
        int(cluster_summary.iloc[2]["cluster"]): "Less-active customers",
    }

    rfm["cluster_label"] = rfm["cluster"].map(cluster_labels)
    cluster_summary["cluster_label"] = cluster_summary["cluster"].map(cluster_labels)

    return {
        "total_customers": int(rfm["customer_id"].nunique()),
        "cluster_summary": cluster_summary.to_dict(orient="records"),
        "segments": rfm[["customer_id", "recency", "frequency", "monetary", "cluster", "cluster_label"]].to_dict(orient="records"),
    }
