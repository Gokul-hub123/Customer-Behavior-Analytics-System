from __future__ import annotations

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def calculate_rfm(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()

    if "customer_id" not in df.columns or "date" not in df.columns:
        return pd.DataFrame()

    cleaned = df.copy()
    cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")
    cleaned = cleaned.dropna(subset=["customer_id", "date"])

    if cleaned.empty:
        return pd.DataFrame()

    max_date = cleaned["date"].max()
    rfm = (
        cleaned.groupby("customer_id")
        .agg(
            recency=("date", lambda values: (max_date - values.max()).days),
            frequency=("transaction_id", "nunique") if "transaction_id" in cleaned.columns else ("customer_id", "count"),
            monetary=("total_amount", "sum") if "total_amount" in cleaned.columns else ("unit_price", "sum"),
        )
        .reset_index()
    )
    return rfm.fillna(0)


def run_customer_segmentation(df: pd.DataFrame) -> dict:
    rfm = calculate_rfm(df)
    if rfm.empty:
        return {"message": "Not enough customer data for segmentation."}

    if len(rfm) < 2:
        return {"message": "At least two customers are needed to run customer segmentation."}

    features = rfm[["recency", "frequency", "monetary"]].copy()
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    n_clusters = min(3, len(rfm))
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
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

    if len(cluster_summary) == 1:
        cluster_names = {0: "Current customers"}
    elif len(cluster_summary) == 2:
        cluster_names = {0: "High-value customers", 1: "Regular customers"}
    else:
        sorted_clusters = cluster_summary.sort_values(["avg_monetary", "avg_frequency"], ascending=False)
        cluster_names = {
            int(sorted_clusters.iloc[0]["cluster"]): "High-value customers",
            int(sorted_clusters.iloc[1]["cluster"]): "Regular customers",
            int(sorted_clusters.iloc[2]["cluster"]): "Less-active customers",
        }

    rfm["cluster_label"] = rfm["cluster"].map(cluster_names)
    cluster_summary["cluster_label"] = cluster_summary["cluster"].map(cluster_names)

    return {
        "total_customers": int(rfm["customer_id"].nunique()),
        "cluster_summary": cluster_summary.to_dict(orient="records"),
        "segments": rfm[["customer_id", "recency", "frequency", "monetary", "cluster", "cluster_label"]].to_dict(orient="records"),
        "message": "RFM segmentation completed successfully.",
    }
