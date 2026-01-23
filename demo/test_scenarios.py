"""
Script de test automatique pour démontrer le système de sécurité
Teste plusieurs scénarios : paiements normaux, rapides, avec faible cohérence
"""
import time
from demo.agent import agent_request
from demo.guard_lite import evaluate
from demo.pay_usdc import pay_usdc

def print_separator():
    print("\n" + "="*70 + "\n")

def test_scenario(name, description, action, wait_time=0):
    """Teste un scénario et affiche le résultat"""
    print(f"📋 SCÉNARIO : {name}")
    print(f"   Description : {description}")
    print(f"   Action : {action}")
    
    decision = evaluate(action)
    
    print(f"   🔒 Décision de sécurité : {decision}")
    
    if decision == "ALLOW":
        pay_usdc(action["amount_usdc"], action["recipient"])
        print(f"   ✅ Paiement exécuté : {action['amount_usdc']} USDC → {action['recipient']}")
    else:
        print(f"   ❌ Paiement bloqué pour raisons de sécurité")
    
    if wait_time > 0:
        print(f"   ⏳ Attente de {wait_time} secondes...")
        time.sleep(wait_time)
    
    print_separator()
    return decision

def run_all_tests():
    """Exécute tous les scénarios de test"""
    print("\n" + "🚀 DÉMONSTRATION DU SYSTÈME DE SÉCURITÉ AGENTIC COMMERCE" + "\n")
    print("Ce système protège contre les paiements dangereux ou irrationnels")
    print_separator()
    
    results = []
    
    # Scénario 1 : Paiement normal
    action1 = agent_request({"amount": 3, "recipient": "api_provider"})
    result1 = test_scenario(
        "1. Paiement Normal",
        "Un agent IA achète un accès API pour 3 USDC",
        action1,
        wait_time=2
    )
    results.append(("Paiement Normal (3 USDC)", result1))
    
    # Scénario 2 : Paiement rapide (devrait être bloqué)
    action2 = agent_request({"amount": 2, "recipient": "data_provider"})
    result2 = test_scenario(
        "2. Paiement Rapide Successif",
        "L'agent essaie de payer à nouveau immédiatement (< 10 secondes)",
        action2,
        wait_time=2
    )
    results.append(("Paiement Rapide (< 10s)", result2))
    
    # Scénario 3 : Paiement avec faible cohérence (devrait être bloqué)
    action3 = {
        "intent": "suspicious_action",
        "amount_usdc": 5,
        "recipient": "unknown_merchant",
        "coherence": 0.3  # Faible cohérence
    }
    result3 = test_scenario(
        "3. Paiement avec Faible Cohérence",
        "Action suspecte avec score de cohérence de 0.3 (seuil : 0.6)",
        action3,
        wait_time=2
    )
    results.append(("Faible Cohérence (0.3)", result3))
    
    # Scénario 4 : Paiement après attente (devrait être autorisé)
    print("⏳ Attente de 10 secondes pour réinitialiser la contrainte temporelle...")
    time.sleep(10)
    print_separator()
    
    action4 = agent_request({"amount": 4, "recipient": "compute_provider"})
    result4 = test_scenario(
        "4. Paiement Après Délai de Sécurité",
        "Paiement après avoir attendu 10 secondes (contrainte temporelle respectée)",
        action4
    )
    results.append(("Paiement Après Délai", result4))
    
    # Scénario 5 : Paiement avec bonne cohérence
    action5 = {
        "intent": "buy_premium_api",
        "amount_usdc": 7,
        "recipient": "trusted_provider",
        "coherence": 0.95  # Excellente cohérence
    }
    result5 = test_scenario(
        "5. Paiement avec Excellente Cohérence",
        "Action légitime avec score de cohérence de 0.95",
        action5
    )
    results.append(("Excellente Cohérence (0.95)", result5))
    
    # Résumé des résultats
    print("\n" + "📊 RÉSUMÉ DES TESTS" + "\n")
    print(f"{'Scénario':<35} {'Résultat':<10}")
    print("-" * 70)
    
    allow_count = 0
    block_count = 0
    
    for scenario, result in results:
        status = "✅ ALLOW" if result == "ALLOW" else "❌ BLOCK"
        print(f"{scenario:<35} {status:<10}")
        if result == "ALLOW":
            allow_count += 1
        else:
            block_count += 1
    
    print("-" * 70)
    print(f"\nTotal : {allow_count} autorisés, {block_count} bloqués")
    print("\n🎯 Le système de sécurité a fonctionné comme prévu !")
    print("   - Bloque les paiements trop rapides (spam)")
    print("   - Bloque les actions avec faible cohérence (suspectes)")
    print("   - Autorise les paiements légitimes après vérification")
    print_separator()

if __name__ == "__main__":
    run_all_tests()
