def evaluate_risk(entry_price: float, stop_loss: float, take_profit: float, position_type: str = "LONG") -> dict:
    """
    Module de contrôle prudentiel.
    Vérifie si le scénario respecte le ratio risque/rendement minimum de 1:1.5.
    """
    if position_type.upper() == "LONG":
        risk = entry_price - stop_loss
        reward = take_profit - entry_price
    else: # SHORT
        risk = stop_loss - entry_price
        reward = entry_price - take_profit

    # Prévention des divisions par zéro ou des stop loss incohérents
    if risk <= 0:
        return {"status": "REJETÉ", "reason": "Le Stop Loss est mal placé (risque négatif ou nul)."}

    rr_ratio = reward / risk

    # Règle stricte : R:R doit être >= 1.5
    if rr_ratio < 1.5:
        return {
            "status": "REJETÉ", 
            "reason": f"Ratio R:R insuffisant ({rr_ratio:.2f}). Le minimum requis est de 1.5.",
            "rr_ratio": round(rr_ratio, 2)
        }
    
    return {
        "status": "APPROUVÉ", 
        "reason": f"Scénario validé. Ratio R:R de {rr_ratio:.2f}.",
        "rr_ratio": round(rr_ratio, 2)
    }

# Test direct des règles de gestion du risque
if __name__ == "__main__":
    print("--- Test du Risk Manager ---")
    
    # Scénario 1 : R:R de 2.0 (Doit être approuvé)
    print("\nScénario LONG (Entrée: 1.1200, SL: 1.1150, TP: 1.1300) :")
    print(evaluate_risk(1.1200, 1.1150, 1.1300, "LONG"))
    
    # Scénario 2 : R:R de 1.0 (Doit être rejeté)
    print("\nScénario SHORT (Entrée: 1.1200, SL: 1.1250, TP: 1.1150) :")
    print(evaluate_risk(1.1200, 1.1250, 1.1150, "SHORT"))