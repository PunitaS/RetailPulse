import pandas as pd
def clean_data(df):
    df = df.copy()

    # Normalize column names
    df.columns = df.columns.str.strip().str.replace(' ', '_')

    print("CLEANING FUNCTION IS RUNNING")

    # ----------------------------
    # FIX DATA TYPES (CRITICAL)
    # ----------------------------
    
    # StockCode should ALWAYS be string (fixes your error)
    if 'StockCode' in df.columns:
        df['StockCode'] = df['StockCode'].astype(str).str.strip()

    # Customer_ID should be string (not float)
    if 'Customer_ID' in df.columns:
        df['Customer_ID'] = df['Customer_ID'].astype(str).str.strip()

    # Convert InvoiceDate to datetime
    if 'InvoiceDate' in df.columns:
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')

    # Ensure numeric columns are correct
    if 'Quantity' in df.columns:
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

    if 'Price' in df.columns:
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # ----------------------------
    # DATA CLEANING
    # ----------------------------
    
    df = df.dropna(subset=['Customer_ID'])
    df = df.dropna(subset=['InvoiceDate'])
    
    df = df[df['Quantity'] > 0]
    df = df[df['Price'] > 0]

    df = df.drop_duplicates()

    # ----------------------------
    # FINAL SAFETY (STREAMLIT FIX)
    # ----------------------------
    
    # Force object columns to string (prevents Arrow errors)
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str)

    return df