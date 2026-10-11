from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
# Import local
from tools.market_api import get_market_data

llm = ChatGroq(model="llama3-8b-8192", temperature=0)
def technical_agent(state: dict):
    print("\n[Agent Technique] Extraction et interprétation des données de marché...")
    ticker = state.get("ticker", "EURUSD=X")
    
    # 1. Extraction des données brutes via notre outil
    raw_data = get_market_data.invoke({"ticker": ticker, "interval": "1d", "period": "1mo"})
    
    # 2. Interprétation par l'IA
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un analyste technique financier. Résume la tendance actuelle (Haussière, Baissière, Neutre) de manière très concise, en te basant UNIQUEMENT sur ces données techniques : RSI et Moyennes Mobiles."),
        ("human", "Voici les données extraites pour {ticker} :\n{raw_data}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"ticker": ticker, "raw_data": raw_data})
    
    return {"technical_data": response.content}