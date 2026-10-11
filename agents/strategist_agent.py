from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = ChatGroq(model="llama3-8b-8192", temperature=0)
def strategy_agent(state: dict):
    iteration = state.get("iteration_count", 0)
    print(f"\n[Agent Stratégiste] Génération du scénario (Tentative {iteration + 1})...")
    
    # Construction du prompt de correction si l'agent a été rejeté précédemment
    correction_prompt = ""
    if state.get("risk_status") == "REJETÉ":
        correction_prompt = "ATTENTION : Ta proposition précédente a été REJETÉE car le ratio Risque/Rendement (R:R) était inférieur à 1.5. Tu DOIS élargir le Take Profit ou resserrer le Stop Loss pour respecter ce ratio strict."

    prompt = ChatPromptTemplate.from_messages([
        ("system", """Tu es un trader quantitatif expert. Basé sur l'analyse fondamentale et technique fournie, propose un scénario de trading pertinent.
        {correction_prompt}
        Tu dois renvoyer UNIQUEMENT un objet JSON valide (sans aucun autre texte) avec exactement ces clés :
        - "entry": prix d'entrée (float)
        - "sl": Stop Loss (float)
        - "tp": Take Profit (float)
        - "type": "LONG" ou "SHORT"
        """),
        ("human", "Actif: {ticker}\n\nContexte Fondamental:\n{fundamental}\n\nDonnées Techniques:\n{technical}")
    ])
    
    chain = prompt | llm | JsonOutputParser()
    
    try:
        trade = chain.invoke({
            "ticker": state.get("ticker"),
            "fundamental": state.get("fundamental_context"),
            "technical": state.get("technical_data"),
            "correction_prompt": correction_prompt
        })
    except Exception as e:
        # Sécurité si le LLM hallucine le format JSON
        print(f"Erreur de parsing : {e}")
        trade = {"entry": 1.1000, "sl": 1.0900, "tp": 1.1200, "type": "LONG"}
        
    return {"proposed_trade": trade, "iteration_count": iteration + 1}