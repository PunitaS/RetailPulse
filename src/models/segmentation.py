from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np


def run_kmeans(rfm, k_range=(2, 10)):
    rfm = rfm.copy()

    # =========================
    # FEATURE SELECTION
    # =========================
    features = rfm[['Recency', 'Frequency', 'Monetary']].copy()

    # =========================
    # LOG TRANSFORMATION (CRITICAL FIX)
    # =========================
    features['Recency'] = np.log1p(features['Recency'])
    features['Frequency'] = np.log1p(features['Frequency'])
    features['Monetary'] = np.log1p(features['Monetary'])

    # =========================
    # SCALE DATA
    # =========================
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    # =========================
    # FIND BEST K
    # =========================
    best_k = None
    best_score = -1
    best_labels = None

    for k in range(k_range[0], k_range[1]):
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(scaled)

        # Avoid useless clustering
        if len(set(labels)) < 3:
            continue

        score = silhouette_score(scaled, labels)

        if score > best_score:
            best_score = score
            best_k = k
            best_labels = labels

    print(f"Best K found: {best_k} (Silhouette Score: {best_score:.3f})")

    # =========================
    # FINAL MODEL
    # =========================
    model = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    rfm['Cluster'] = model.fit_predict(scaled)

    print("\nCluster Distribution:")
    print(rfm['Cluster'].value_counts())

    return rfm, model


def label_clusters(rfm):
    rfm = rfm.copy()

    summary = rfm.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean()

    # Better scoring logic
    summary['Score'] = (
        summary['Monetary'].rank(ascending=False) * 2 +
        summary['Frequency'].rank(ascending=False) -
        summary['Recency'].rank(ascending=True)
    )

    summary = summary.sort_values('Score', ascending=False)

    labels = {}
    for i, cluster in enumerate(summary.index):
        if i == 0:
            labels[cluster] = "VIP Customers"
        elif i == 1:
            labels[cluster] = "Loyal Customers"
        elif i == len(summary) - 1:
            labels[cluster] = "At Risk Customers"
        else:
            labels[cluster] = "Regular Customers"

    rfm['Segment'] = rfm['Cluster'].map(labels)

    print("\nSegment Distribution:")
    print(rfm['Segment'].value_counts())

    return rfm