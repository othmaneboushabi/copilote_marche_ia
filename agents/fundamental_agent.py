import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
# Import local
from rag.retriever import search_macro_context

# Initialisation du modèle Llama 3 via l'API gratuite Groq
llm = ChatGroq(model="llama3-8b-8192", temperature=0)
def fundamental_agent(state: dict):
    print("\n[Agent Fondamental] Analyse du contexte...")
    query = state.get("query", "")
    
    # Récupération du contexte (commenté en attendant d'avoir des PDF dans data/)
    # context = search_macro_context(query)
    context = "Aucun document PDF fourni. Analyse macro-économique générale."
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un analyste fondamental expert en macro-économie. Utilise le contexte fourni pour donner un bref biais de marché (Haussier, Baissier ou Neutre) en 2 ou 3 phrases maximum."),
        ("human", "Question de l'utilisateur : {query}\n\nContexte documentaire :\n{context}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"query": query, "context": context})
    
    return {"fundamental_context": response.content}