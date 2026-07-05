import pandas as pd
import gdown
import os


def load_data(path=None):
    file_id = "1-zdT_OTbdY3QqzdMJ_sEdQNu4x8zJ3Rw"
    drive_path = "data/online_retail_II.xlsx"

    # ---------------- LOAD FILE ----------------
    if path and os.path.exists(path):
        print("Loading data from LOCAL file...")
        df = read_all_sheets(path)

    else:
        if not os.path.exists(drive_path):
            print("Downloading from Google Drive...")
            gdown.download(
                f"https://drive.google.com/uc?id={file_id}",
                drive_path,
                quiet=False
            )

        print("Loading data from DOWNLOADED file...")
        df = read_all_sheets(drive_path)

    # ---------------- CLEANING ----------------
    df = clean_data(df)

    return df


def read_all_sheets(file_path):
    print("Reading ALL sheets...")

    all_sheets = pd.read_excel(file_path, sheet_name=None)
    df = pd.concat(all_sheets.values(), ignore_index=True)

    print(f"Loaded shape: {df.shape}")

    return df


def clean_data(df):
    print("CLEANING DATA...")

    df = df.copy()

    # ✅ Normalize column names
    df.columns = df.columns.str.strip().str.replace(" ", "_")

    # 🔥 CRITICAL CHECK
    required_cols = ["Customer_ID", "Quantity", "Price", "InvoiceDate"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    # ✅ Remove invalid rows
    df = df.dropna(subset=["Customer_ID"])
    df = df[df["Quantity"] > 0]
    df = df[df["Price"] > 0]

    # ✅ Convert data types
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # ✅ Feature engineering
    df["TotalPrice"] = df["Quantity"] * df["Price"]

    # ✅ Remove duplicates
    df = df.drop_duplicates()

    print(f"Cleaned shape: {df.shape}")

    return df