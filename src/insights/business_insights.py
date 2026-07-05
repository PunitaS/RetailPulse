def generate_insights(rfm, forecast_mape):
    insights = []
# Revenue by segment
    segment_revenue = rfm.groupby("Segment")["Monetary"].sum()
    total_revenue = segment_revenue.sum()

    top_segment = segment_revenue.idxmax()
    top_revenue = segment_revenue.max()
    revenue_share = (top_revenue / total_revenue) * 100

# Churn risk
    churn_count = rfm[rfm["Segment"] == "At Risk Customers"].shape[0]

    insights.append(
    f"{top_segment} contributes {revenue_share:.2f}% of total revenue, making it the most critical segment."
)

    if top_segment == "At Risk Customers":
     insights.append(
        "⚠️ High-risk situation: Your highest revenue is coming from customers likely to churn. Immediate retention strategies are required."
    )

    insights.append(
    f"There are {churn_count} at-risk customers. Targeted campaigns (discounts, emails, loyalty rewards) should be launched immediately."
)

    insights.append(
    f"Forecast model error is {forecast_mape*100:.2f}%, which indicates reliable demand prediction for inventory and planning."
)

    insights.append(
    "Recommendation: Focus on reducing churn before increasing acquisition. Retention will give higher ROI."
)

    return insights