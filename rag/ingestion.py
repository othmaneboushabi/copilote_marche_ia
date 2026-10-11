import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Configuration des chemins
DATA_DIR = "data"
CHROMA_PATH = "chroma_db"

def load_and_process_documents():
    # S'assurer que le dossier data existe
    os.makedirs(DATA_DIR, exist_ok=True)
    
    print("1. Recherche et chargement des documents PDF...")
    # On charge tous les PDF présents dans le dossier data/
    loader = PyPDFDirectoryLoader(DATA_DIR)
    documents = loader.load()

    if not documents:
        print("⚠️ Aucun document trouvé. Veuillez placer des fichiers PDF dans le dossier 'data/'.")
        return None

    print(f"-> {len(documents)} pages chargées. Découpage en cours...")

    # 2. Découpage (Chunking) : on coupe en morceaux de 1000 caractères avec un chevauchement de 200
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"-> {len(chunks)} morceaux (chunks) générés.")

    # 3. Indexation Vectorielle (Embeddings) et Stockage dans ChromaDB
    print("2. Génération des embeddings et stockage dans ChromaDB...")
    # On utilise un modèle léger et performant via sentence-transformers
    embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Création de la base vectorielle persistante
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        persist_directory=CHROMA_PATH
    )

    print("✅ Base de données vectorielle générée avec succès dans le dossier 'chroma_db' !")
    return db

if __name__ == "__main__":
    load_and_process_documents()