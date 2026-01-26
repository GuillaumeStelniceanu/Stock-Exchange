import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from twelvedata import TDClient
import yfinance as yf
from datetime import datetime

# ==============================
# CONFIGURATION
# ==============================
API_KEY = "cc409ca76ef040c1b0904d2247707172"  # <-- Ta clé Twelve Data gratuite
td = TDClient(apikey=API_KEY)

# Créer le dossier outputs si n'existe pas
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Actions US via Twelve Data
US_TICKERS = {
"AMZN": "Amazon",
"AAPL": "Apple",
"NVDA": "NVIDIA",
"TTWO": "Take-Two Interactive"
}

#Actions EU (Yahoo Finance)

EU_TICKERS = {
    "TTE.PA": "TotalEnergies",
    "AI.PA": "Air Liquide",
    "ACA.PA": "Crédit Agricole",
    "VOW3.DE": "Volkswagen",
    "DN3.SG": "Metaplanet Inc.",
    "AM.PA": "Dassault Aviation",
    "BNP.PA": "BNP Paribas",
    "CAP.PA": "Capgemini",
    "RNO.PA": "Renault",
    "AIR.PA": "Airbus",
    "RACE.MI": "Ferrari",
    "BMW.DE": "BMW"
}

INTERVAL = "1day"
OUTPUTSIZE = 180
RSI_PERIOD = 14

# ==============================
# INDICATEURS
# ==============================
def compute_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

# ==============================
# Récupération données
# ==============================
def get_data_us(ticker):
    try:
        ts = td.time_series(symbol=ticker, interval=INTERVAL, outputsize=OUTPUTSIZE)
        df = ts.as_pandas().sort_index()
        df = df.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"})
        return df
    except Exception as e:
        print(f"⚠️ Erreur récupération US {ticker}: {e}")
        return None

def get_data_eu(ticker):
    try:
        # Téléchargement depuis Yahoo Finance
        df = yf.download(
            ticker,
            period="6mo",
            interval="1d",
            group_by="ticker",   # <— corrige le problème d’écrasement des noms de colonnes
            auto_adjust=False,
            progress=False
        )

        if df.empty:
            print(f"⚠️ Aucune donnée trouvée pour {ticker}.")
            return None

        # --- CAS 1 : colonnes normales (Open, Close, etc.)
        if "Close" in df.columns:
            pass

        # --- CAS 2 : multi-index (Price / Close)
        elif isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[1] if col[1] else col[0] for col in df.columns]

        # --- CAS 3 : colonnes nommées avec le ticker (ex. 'TTE.PA')
        elif ticker in df.columns:
            df = df.rename(columns={ticker: "Close"})
            # yfinance ne renvoie parfois que le prix de clôture, donc on simule le reste si besoin
            if "Open" not in df.columns:
                df["Open"] = df["Close"]
                df["High"] = df["Close"]
                df["Low"] = df["Close"]
                df["Volume"] = 0

        else:
            print(f"⚠️ Format de colonnes inattendu pour {ticker} : {list(df.columns)}")
            return None

        # Vérifie la présence des colonnes essentielles
        expected_cols = ["Open", "High", "Low", "Close", "Volume"]
        missing = [c for c in expected_cols if c not in df.columns]
        if missing:
            print(f"⚠️ Colonnes manquantes pour {ticker} : {missing}")
            return None

        # Nettoyage final
        df = df.dropna(subset=["Close"])
        return df

    except Exception as e:
        print(f"⚠️ Erreur récupération EU {ticker}: {e}")
        return None


# ==============================
# Graphique et sauvegarde
# ==============================
def plot_chart(df, name, ticker=""):
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["RSI"] = compute_rsi(df["Close"], RSI_PERIOD)

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[0.7, 0.3],
        vertical_spacing=0.05,
        subplot_titles=(f"{name} {ticker}", "RSI")
    )

    # Chandeliers
    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"], name="Chandeliers"
    ), row=1, col=1)

    # MA20 / MA50
    fig.add_trace(go.Scatter(x=df.index, y=df["MA20"], mode='lines', name="MA20"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["MA50"], mode='lines', name="MA50"), row=1, col=1)

    # Courbe prix de clôture
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode='lines', name="Prix Clôture", line=dict(color="purple", width=2)), row=1, col=1)

    # Volume
    fig.add_trace(go.Bar(x=df.index, y=df["Volume"], name="Volume", opacity=0.3), row=1, col=1)

    # RSI
    fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], mode='lines', name="RSI", line=dict(color="orange")), row=2, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

    fig.update_layout(height=800, xaxis_rangeslider_visible=False, template="plotly_dark")

    # Affichage interactif
    fig.show()

    # Sauvegarde automatique dans outputs/
    filename = f"{ticker or name}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.write_html(filepath)
    print(f"💾 Graphique sauvegardé : {filepath}")

# ==============================
# EXECUTION
# ==============================
# === Marché US ===
for ticker, name in US_TICKERS.items():
    print(f"Récupération US {name} ({ticker})...")
    df = get_data_us(ticker)
    if df is not None and not df.empty:
        print(f"→ Dernier cours : {df['Close'].iloc[-1]:.2f}")
        plot_chart(df, name, ticker)
    else:
        print(f"⚠️ Aucune donnée pour {name}.")

# === Marché EU ===
for ticker, name in EU_TICKERS.items():
    print(f"Récupération EU {name} ({ticker})...")
    df = get_data_eu(ticker)
    if df is not None and not df.empty:
        print(f"→ Dernier cours : {df['Close'].iloc[-1]:.2f}")
        print(df.tail())  # 👈 pour vérifier visuellement les données
        plot_chart(df, name, ticker)
    else:
        print(f"⚠️ Aucune donnée pour {name}.")
