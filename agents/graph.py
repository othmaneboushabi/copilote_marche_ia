import os
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, END

# Chargement de la clé API
load_dotenv()

# Import des vrais agents
from agents.fundamental_agent import fundamental_agent
from agents.technical_agent import technical_agent
from agents.strategist_agent import strategy_agent
from agents.risk_manager import evaluate_risk

class GraphState(TypedDict):
    ticker: str
    query: str
    fundamental_context: str
    technical_data: str
    proposed_trade: dict
    risk_status: str
    iteration_count: int

def risk_management_node(state: GraphState):
    print("\n[Risk Manager] Vérification des règles...")
    trade = state.get("proposed_trade", {})
    
    evaluation = evaluate_risk(
        entry_price=trade.get("entry", 0), 
        stop_loss=trade.get("sl", 0), 
        take_profit=trade.get("tp", 0), 
        position_type=trade.get("type", "LONG")
    )
    
    print(f"-> Résultat : {evaluation['status']} (R:R = {evaluation.get('rr_ratio', 'N/A')})")
    return {"risk_status": evaluation["status"]}

def route_risk(state: GraphState):
    return "approved" if state.get("risk_status") == "APPROUVÉ" else "rejected"

def build_graph():
    workflow = StateGraph(GraphState)
    
    # Ajout des nœuds IA
    workflow.add_node("fundamental", fundamental_agent)
    workflow.add_node("technical", technical_agent)
    workflow.add_node("strategist", strategy_agent)
    workflow.add_node("risk_manager", risk_management_node)
    
    # Routage
    workflow.set_entry_point("fundamental")
    workflow.add_edge("fundamental", "technical")
    workflow.add_edge("technical", "strategist")
    workflow.add_edge("strategist", "risk_manager")
    
    workflow.add_conditional_edges(
        "risk_manager",
        route_risk,
        {"approved": END, "rejected": "strategist"}
    )
    
    return workflow.compile()