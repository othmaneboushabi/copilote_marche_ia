# 📈 Copilote IA Multi-Agents & Risk Management (Agentic RAG)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-orange)](https://python.langchain.com/docs/langgraph)
[![Streamlit](https://img.shields.io/badge/Streamlit-Interface-FF4B4B)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📌 Présentation du Projet
Ce projet est un système multi-agents autonome conçu pour l'analyse des marchés financiers (Forex, indices, matières premières) et la gestion stricte du risque. Il résout le problème des hallucinations des LLMs standards en combinant un pipeline **RAG (Retrieval-Augmented Generation)** pour l'analyse fondamentale et le **Tool Calling** pour l'extraction de données techniques en temps réel[cite: 1]. 

L'orchestration est gérée par un graphe d'états (State Graph) garantissant une boucle d'auto-correction prudente avant toute émission de recommandation[cite: 1].

## 🏗️ Architecture Multi-Agents

Le système repose sur la collaboration de 4 entités distinctes orchestrées par **LangGraph**[cite: 1] :

1. **Agent Fondamental (RAG)** : Ingère et vectorise des rapports macro-économiques (PDF) via ChromaDB pour extraire le contexte sémantique exact[cite: 1].
2. **Agent Technique (Tool Calling)** : Interroge dynamiquement l'API Yahoo Finance pour extraire les cotations en direct et calcule les indicateurs techniques (RSI, SMA) via `pandas-ta`[cite: 1].
3. **Agent Stratégiste** : Croise les biais fondamentaux et techniques pour formuler un scénario de trading structuré (Entrée, Stop Loss, Take Profit)[cite: 1].
4. **Agent Risk Manager** : Applique un contrôle déterministe strict. Si le ratio Risque/Rendement (R:R) est inférieur à 1:1.5, il rejette la proposition et force le Stratégiste à s'auto-corriger[cite: 1].

## 🛠️ Stack Technologique

| Composant | Technologie |
| :--- | :--- |
| **Langage** | Python 3.11+[cite: 1] |
| **Orchestration IA** | LangGraph, LangChain[cite: 1] |
| **Modèle LLM** | Llama 3 / Mistral (via Groq API)[cite: 1] |
| **Base Vectorielle** | ChromaDB, HuggingFace Embeddings[cite: 1] |
| **Données de Marché** | `yfinance`, `pandas-ta`[cite: 1] |
| **Interface Utilisateur** | Streamlit[cite: 1] |

## 📂 Structure du Répertoire

```text
copilote_marche_ia/
├── agents/                  # Cerveau de l'application
│   ├── fundamental_agent.py # Analyse macro-économique
│   ├── technical_agent.py   # Extraction des données de marché
│   ├── strategist_agent.py  # Génération du trade
│   ├── risk_manager.py      # Contrôle prudentiel et R:R
│   └── graph.py             # Orchestration LangGraph
├── app/                     # Interface Utilisateur
│   └── interface.py         # Application web Streamlit
├── data/                    # Corpus documentaire (Rapports PDF)
├── rag/                     # Pipeline RAG
│   ├── ingestion.py         # Découpage et vectorisation
│   └── retriever.py         # Recherche sémantique
├── tools/                   # Outils externes (Tool Calling)
│   └── market_api.py        # Connexion yfinance & calculs TA
├── .env                     # Variables d'environnement (Clé API)
├── requirements.txt         # Dépendances Python
└── README.md                # Documentation du projet

🚀 Installation & Démarrage
1. Prérequis
Python 3.11 ou supérieur

Une clé API Groq (gratuite) pour l'accès aux modèles Llama/Mistral

2. Configuration de l'environnement
Clonez ce dépôt et installez les dépendances requises :

Bash
git clone [https://github.com/votre-nom-utilisateur/copilote_marche_ia.git](https://github.com/votre-nom-utilisateur/copilote_marche_ia.git)
cd copilote_marche_ia
python -m venv venv
# Activation sous Windows : venv\Scripts\activate
# Activation sous Linux/Mac : source venv/bin/activate
pip install -r requirements.txt
3. Variables d'environnement
Créez un fichier .env à la racine du projet et ajoutez votre clé API Groq :

Code snippet
GROQ_API_KEY=votre_cle_api_ici
4. Lancement
Placez quelques rapports macro-économiques au format PDF dans le dossier data/, initialisez la base vectorielle, puis lancez l'interface web :

Bash
# 1. Ingestion des documents (optionnel si pas de PDF)
python .\rag\ingestion.py

# 2. Lancement de l'interface Streamlit
python -m streamlit run app/interface.py


🧠 Démonstration du Flux d'Auto-Correction
L'un des atouts majeurs de cette architecture est sa résilience. Si l'IA propose un Stop Loss trop large, le Risk Manager intercepte le flux, annule la transaction, et renvoie un feedback explicite au Stratégiste pour qu'il affine sa précision de ciblage