from src.data.data_loader import load_data
from src.data.data_cleaning import clean_data
from src.features import rfm
from src.features.feature_engineering import add_features
from src.features.rfm import compute_rfm
from src.models.segmentation import run_kmeans, label_clusters
from src.models.forecasting import run_forecast
from src.insights.business_insights import generate_insights

def run_pipeline(path):
    # ========================
    # DATA PIPELINE
    # ========================
    df = load_data(path)
    print(df.head())
    df = clean_data(df)
    df = add_features(df)

    # ========================
    # RFM + SEGMENTATION
    # ========================
    rfm = compute_rfm(df)

    rfm, model = run_kmeans(rfm)
    rfm = label_clusters(rfm)

    # ========================
    # FORECAST
    # ========================
    forecast, mape = run_forecast(df)

    # ========================
    # INSIGHTS
    # ========================
    insights = generate_insights(rfm, mape)

    return {
        "data": df,
        "rfm": rfm,
        "forecast": forecast,
        "mape": mape,
        "insights": insights
    }


if __name__ == "__main__":
    print("STARTING PIPELINE")

    result = run_pipeline("data/online_retail_II.xlsx")

    print("\nDATA SHAPE:", result["data"].shape)

    print("\nSEGMENT DISTRIBUTION:")
    print(result["rfm"]["Segment"].value_counts())

    print("\nFORECAST SAMPLE:")
    print(result["forecast"].head())

    print("\nMAPE:", result["mape"])

    print("\nINSIGHTS:")
    for i in result["insights"]:
        print("-", i)

    print("\nDONE")

segment_stats = result["rfm"].groupby('Segment').agg({
    'Monetary': ['mean', 'sum'],
    'Frequency': 'mean',
    'Recency': 'mean'
})

print(segment_stats)