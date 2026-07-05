import pandas as pd

def get_monthly_sales(df):
    monthly_sales = df.groupby('YearMonth')['TotalPrice'].sum()
    return monthly_sales.iloc[1:-1]

def get_top_countries(df, n=5):
    return df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(n)

def get_top_products(df, n=5):
    return df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(n)

def country_metrics(df):
    country_avg = df.groupby('Country').agg({
        'Customer_ID': 'nunique',
        'TotalPrice': 'sum'
    })

    country_avg['AvgRevenuePerCustomer'] = (
        country_avg['TotalPrice'] / country_avg['Customer_ID']
    )

    return country_avg.sort_values('AvgRevenuePerCustomer', ascending=False)

def orders_vs_revenue(df):
    orders = df.groupby('Country')['Invoice'].nunique()
    revenue = df.groupby('Country')['TotalPrice'].sum()

    comparison = pd.DataFrame({
        'Orders': orders,
        'Revenue': revenue
    })

    comparison['Revenue_per_Order'] = comparison['Revenue'] / comparison['Orders']

    return comparison.sort_values('Revenue', ascending=False)

def avg_order_value_by_country(df):
    orders = df.groupby('Country')['Invoice'].nunique()
    revenue = df.groupby('Country')['TotalPrice'].sum()

    aov = revenue / orders
    return aov.sort_values(ascending=False).rename("AvgOrderValue")

def segment_revenue(rfm):
    return rfm.groupby('Segment')['Monetary'].sum()