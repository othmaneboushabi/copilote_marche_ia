import yfinance as yf
import pandas as pd
import pandas_ta as ta
from langchain_core.tools import tool

@tool
def get_market_data(ticker: str, interval: str = "1d", period: str = "1mo") -> str:
    """
    Outil pour récupérer les données de marché en direct et calculer les indicateurs techniques (RSI, SMA).
    Arguments:
    - ticker: Le symbole financier (ex: 'EURUSD=X' pour le Forex, '^GSPC' pour le S&P 500, 'GC=F' pour l'or).
    - interval: L'unité de temps (ex: '1h' pour H1, '1d' pour D1).
    - period: La profondeur d'historique (ex: '1mo', '5d').
    """
    try:
        # 1. Téléchargement des données de marché via yfinance
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        
        if df.empty:
            return f"Aucune donnée trouvée pour le ticker {ticker}."

        # Aplatir le MultiIndex si nécessaire (selon la version de yfinance)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)

        # 2. Calcul des indicateurs techniques avec pandas-ta
        # Moyenne Mobile Simple (SMA) sur 10 et 20 périodes
        df.ta.sma(length=10, append=True)
        df.ta.sma(length=20, append=True)
        # Relative Strength Index (RSI) sur 14 périodes
        df.ta.rsi(length=14, append=True)

        # 3. Extraction des données de la bougie la plus récente (dernière ligne)
        last_row = df.iloc[-1]
        
        # Sécurisation de la lecture des valeurs
        close_price = last_row['Close']
        rsi = last_row['RSI_14'] if 'RSI_14' in df.columns else 'Non disponible'
        sma_10 = last_row['SMA_10'] if 'SMA_10' in df.columns else 'Non disponible'
        sma_20 = last_row['SMA_20'] if 'SMA_20' in df.columns else 'Non disponible'
        
        # 4. Formatage du résultat textuel pour l'agent LLM
        result = (
            f"--- Analyse Technique Spontanée pour {ticker} (Unité de temps: {interval}) ---\n"
            f"Prix de clôture actuel : {close_price:.4f}\n"
            f"RSI (14) : {rsi:.2f}\n"
            f"SMA (10) : {sma_10:.4f}\n"
            f"SMA (20) : {sma_20:.4f}\n"
        )
        return result
        
    except Exception as e:
        return f"Erreur lors de la récupération des données pour {ticker} : {str(e)}"

# Test direct de l'outil
if __name__ == "__main__":
    print("Test de l'outil API de Marché sur la paire EUR/USD (Forex) :")
    # On utilise .invoke() car c'est un outil LangChain
    resultat = get_market_data.invoke({"ticker": "EURUSD=X", "interval": "1d", "period": "1mo"})
    print(resultat)