import pandas as pd

def compute_rfm(df):
    df = df.copy()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("Customer_ID").agg({
        "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
        "Invoice": "nunique",
        "TotalPrice": "sum"
    })

    rfm.columns = ["Recency", "Frequency", "Monetary"]

    # Robust binning
    rfm["R"] = pd.qcut(rfm["Recency"], q=4, labels=[4, 3, 2, 1], duplicates="drop")
    rfm["F"] = pd.qcut(rfm["Frequency"].rank(method="first"), q=4, labels=[1, 2, 3, 4], duplicates="drop")
    rfm["M"] = pd.qcut(rfm["Monetary"], q=4, labels=[1, 2, 3, 4], duplicates="drop")

    # Segment logic MUST be inside the function
    def segment(row):
        if row["R"] == 4 and row["F"] >= 3:
            return "VIP Customers"
        elif row["F"] >= 3:
            return "Loyal Customers"
        elif row["R"] <= 2:
            return "At Risk Customers"
        else:
            return "Regular Customers"

    rfm["Segment"] = rfm.apply(segment, axis=1)

    return rfm.reset_index()
