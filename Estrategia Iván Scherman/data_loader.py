import yfinance as yf
import pandas as pd

def load_sp500_data(start="1990-01-01"):

    df = yf.download(
        "^GSPC",
        start=start,
        interval="1d",
        progress=False
    )

    if df.empty:
        raise ValueError("No se pudieron descargar los datos")

    # FIX CRÍTICO: eliminar MultiIndex si existe
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    df = df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })

    df = df[['open', 'high', 'low', 'close', 'volume']]
    df.dropna(inplace=True)

    return df
