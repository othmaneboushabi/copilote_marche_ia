import streamlit as st
from agents.graph import build_graph

# Configuration de la page
st.set_page_config(page_title="Copilote IA - Analyse de Marché", layout="wide")

st.title("📈 Copilote IA Multi-Agents & Risk Management")
st.markdown("Ce système orchestre plusieurs agents pour analyser le marché et proposer un scénario de trading validé par un Risk Manager.")

# Initialisation du graphe
@st.cache_resource
def get_app():
    return build_graph()

app_graph = get_app()

# Interface utilisateur
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Configuration")
    ticker = st.text_input("Symbole de l'actif (ex: EURUSD=X, AAPL, ^GSPC)", value="EURUSD=X")
    query = st.text_area("Contexte ou question supplémentaire", value="Analyse la tendance actuelle.")
    analyze_btn = st.button("Lancer l'Analyse Agentique")

with col2:
    st.subheader("Exécution Multi-Agents")
    if analyze_btn:
        # État initial
        initial_state = {
            "ticker": ticker, 
            "query": query,
            "iteration_count": 0
        }
        
        st.info("🚀 Démarrage du pipeline...")
        
        # Conteneurs pour l'affichage en direct
        status_placeholder = st.empty()
        
        # Exécution du graphe
        final_state = None
        for output in app_graph.stream(initial_state):
            # Affichage dynamique des étapes
            for node_name, node_state in output.items():
                if node_name == "fundamental":
                    st.success("📚 Agent Fondamental : " + node_state.get("fundamental_context", ""))
                elif node_name == "technical":
                    st.success("📊 Agent Technique : " + node_state.get("technical_data", ""))
                elif node_name == "strategist":
                    st.warning("🧠 Agent Stratégiste : Proposition générée (Tentative " + str(node_state.get("iteration_count", 1)) + ")")
                elif node_name == "risk_manager":
                    status = node_state.get("risk_status")
                    if status == "APPROUVÉ":
                        st.success("✅ Risk Manager : Scénario APPROUVÉ")
                    else:
                        st.error("❌ Risk Manager : Scénario REJETÉ (Auto-correction en cours...)")
            final_state = output
        
        st.markdown("---")
        st.subheader("🎯 Scénario Final Validé")
        
        # Récupération de l'état final (la dernière étape franchie)
        last_node = list(final_state.keys())[0]
        final_trade = final_state[last_node].get("proposed_trade", {})
        
        st.json(final_trade)