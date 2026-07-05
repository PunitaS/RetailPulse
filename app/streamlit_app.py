import streamlit as st
import pandas as pd
import plotly.express as px

from src.data.data_loader import load_data
from src.features.rfm import compute_rfm
from src.insights.business_insights import generate_insights

st.set_page_config(page_title="Retail Pulse Dashboard", layout="wide")

st.title("📊 Retail Pulse Business Dashboard")

# ---------------- LOAD DATA ----------------
@st.cache_data
def get_data():
    df = load_data()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df

df = get_data()

# ---------------- RFM ----------------
rfm = compute_rfm(df)

# ---------------- SIDEBAR ----------------
st.sidebar.header("Filters")

selected_segment = st.sidebar.multiselect(
    "Select Customer Segment",
    options=rfm["Segment"].unique(),
    default=rfm["Segment"].unique()
)

filtered_rfm = rfm[rfm["Segment"].isin(selected_segment)]
filtered_df = df[df["Customer_ID"].isin(filtered_rfm["Customer_ID"])]

# ---------------- KPIs ----------------
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

total_revenue = filtered_df["TotalPrice"].sum()
total_customers = filtered_rfm.shape[0]
avg_revenue = total_revenue / total_customers if total_customers else 0

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Customers", total_customers)
col3.metric("Avg Revenue / Customer", f"${avg_revenue:,.2f}")

# ---------------- RFM DISTRIBUTION ----------------
st.subheader("📊 RFM Score Distribution")

col1, col2, col3 = st.columns(3)

with col1:
    st.bar_chart(rfm["R"].value_counts().sort_index())

with col2:
    st.bar_chart(rfm["F"].value_counts().sort_index())

with col3:
    st.bar_chart(rfm["M"].value_counts().sort_index())

# ---------------- SEGMENT DISTRIBUTION ----------------
st.subheader("📊 Segment Distribution")

seg_counts = filtered_rfm["Segment"].value_counts().reset_index()
seg_counts.columns = ["Segment", "Count"]

fig_seg = px.bar(
    seg_counts,
    x="Segment",
    y="Count",
    title="Customer Segments"
)

st.plotly_chart(fig_seg, width="stretch")  # FIXED

# ---------------- MONTHLY REVENUE ----------------
st.subheader("📅 Monthly Revenue Trend")

monthly_sales = (
    filtered_df
    .resample("ME", on="InvoiceDate")["TotalPrice"]
    .sum()
)

st.line_chart(monthly_sales)

# ---------------- REVENUE BY COUNTRY ----------------
st.subheader("🌍 Revenue by Country")

country_sales = (
    filtered_df
    .groupby("Country")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(country_sales)

# ---------------- ORDER SIZE DISTRIBUTION ----------------
st.subheader("📦 Order Size Distribution")

order_size = filtered_df.groupby("Invoice")["TotalPrice"].sum()

# Better histogram instead of dumb counts
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.hist(order_size, bins=30)
ax.set_title("Order Size Distribution")

st.pyplot(fig)

# ---------------- SEGMENT REVENUE SHARE ----------------
st.subheader("📊 Segment Revenue Share (%)")

segment_share = (
    filtered_rfm
    .groupby("Segment")["Monetary"]
    .sum()
)

segment_share = (segment_share / segment_share.sum()) * 100

st.bar_chart(segment_share)

# ---------------- DAILY SALES TREND ----------------
st.subheader("📈 Daily Sales Trend")

daily_sales = (
    filtered_df
    .groupby("InvoiceDate")["TotalPrice"]
    .sum()
    .reset_index()
)

fig_time = px.line(
    daily_sales,
    x="InvoiceDate",
    y="TotalPrice",
    title="Daily Revenue Trend"
)

st.plotly_chart(fig_time, width="stretch")  # FIXED

# ---------------- TOP PRODUCTS ----------------
st.subheader("🏆 Top Selling Products")

top_products = (
    filtered_df
    .groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_products)

# ---------------- INSIGHTS ----------------
st.subheader("📊 Business Insights")

mape = 0.075  # TODO: connect real model output

insights = generate_insights(filtered_rfm, mape)

for insight in insights:
    st.info(insight)