from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

CHROMA_PATH = "chroma_db"

def get_retriever():
    """Initialise et retourne l'objet retriever connecté à ChromaDB."""
    # On recharge le même modèle d'embedding utilisé lors de l'ingestion
    embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Connexion à la base existante
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings_model)
    
    # Création du retriever (k=3 signifie qu'on récupère les 3 passages les plus pertinents)
    retriever = db.as_retriever(search_kwargs={"k": 3})
    return retriever

def search_macro_context(query: str):
    """
    Recherche dans la base documentaire et formate la sortie 
    pour imposer la citation des sources.
    """
    retriever = get_retriever()
    docs = retriever.invoke(query)
    
    if not docs:
        return "Aucun contexte macro-économique trouvé dans les documents."
    
    formatted_context = "Voici les informations extraites de la base documentaire :\n\n"
    
    for i, doc in enumerate(docs):
        # Extraction de la source exacte pour le contrôle d'ancrage
        source = doc.metadata.get('source', 'Source inconnue')
        page = doc.metadata.get('page', 'N/A')
        
        formatted_context += f"--- Extrait {i+1} ---\n"
        formatted_context += f"Source : {source} (Page: {page})\n"
        formatted_context += f"Texte : {doc.page_content}\n\n"
        
    return formatted_context

# Petit test intégré (qui retournera vide pour l'instant vu qu'il n'y a pas de PDF)
if __name__ == "__main__":
    print("Test du Retriever...")
    try:
        resultat = search_macro_context("Quel est le dernier taux directeur ?")
        print(resultat)
    except Exception as e:
        print(f"Erreur (probablement car la base n'existe pas encore) : {e}")