import pandas as pd

def add_features(df):
    df = df.copy()

    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # Core metric (USE THIS EVERYWHERE)
    df['TotalPrice'] = df['Quantity'] * df['Price']

    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')
    df['Date'] = df['InvoiceDate'].dt.date

    return df