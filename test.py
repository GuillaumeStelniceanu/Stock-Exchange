import yfinance as yf

df = yf.download("TTE.PA", period="6mo", interval="1d", group_by="column")
print(df.head())
