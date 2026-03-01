
import pandas as pd

def get_signals_with_stop(df: pd.DataFrame):

    df = df.copy()
    signals = []
    stop_prices = []

    for i in range(len(df)):

        if i == 0:
            signals.append(0)
            stop_prices.append(None)
            continue

        # Example strategy:
        # Break above previous high -> long
        if df["close"].iloc[i] > df["high"].iloc[i-1]:
            signals.append(1)
            stop_prices.append(df["low"].iloc[i-1])
        else:
            signals.append(0)
            stop_prices.append(None)

    return pd.DataFrame({
        "signal": signals,
        "stop_price": stop_prices
    })
