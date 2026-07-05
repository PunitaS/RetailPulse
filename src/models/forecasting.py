from prophet import Prophet
import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error


def run_forecast(df):
    df = df.copy()

    # =========================
    # WEEKLY AGGREGATION (BIG FIX)
    # =========================
    ts = (
        df.set_index('InvoiceDate')
        .resample('W')['TotalPrice']
        .sum()
        .reset_index()
    )

    ts.columns = ['ds', 'y']

    # =========================
    # REMOVE EXTREME OUTLIERS
    # =========================
    upper_limit = ts['y'].quantile(0.99)
    ts['y'] = ts['y'].clip(upper=upper_limit)

    # =========================
    # TRAIN-TEST SPLIT
    # =========================
    train = ts[:-8]
    test = ts[-8:]

    # =========================
    # MODEL
    # =========================
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,  # already aggregated weekly
        daily_seasonality=False
    )

    # Add holidays (important for retail)
    model.add_country_holidays(country_name='UK')

    model.fit(train)

    # =========================
    # FUTURE
    # =========================
    future = model.make_future_dataframe(periods=8, freq='W')
    forecast = model.predict(future)

    # =========================
    # EVALUATION
    # =========================
    preds = forecast.tail(8)['yhat'].values
    actual = test['y'].values

    mape = mean_absolute_percentage_error(actual, preds)

    print(f"Forecast MAPE: {mape:.2%}")

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], mape