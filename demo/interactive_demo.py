"""
Démo interactive en ligne de commande
Permet à l'utilisateur de tester différents montants et destinataires
"""
from demo.agent import agent_request
from demo.guard_lite import evaluate
from demo.pay_usdc import pay_usdc

def print_header():
    print("\n" + "="*70)
    print("🚀 AGENTIC COMMERCE - DÉMONSTRATION INTERACTIVE")
    print("="*70)
    print("\nCe système protège contre les paiements dangereux ou irrationnels")
    print("Testez différents scénarios pour voir comment la sécurité fonctionne\n")

def print_separator():
    print("-" * 70)

def get_user_input():
    """Récupère les paramètres du paiement depuis l'utilisateur"""
    print_separator()
    print("📝 Entrez les détails du paiement :\n")
    
    # Montant
    while True:
        try:
            amount = float(input("💰 Montant en USDC (ex: 3.5) : "))
            if amount <= 0:
                print("❌ Le montant doit être positif. Réessayez.")
                continue
            break
        except ValueError:
            print("❌ Veuillez entrer un nombre valide.")
    
    # Destinataire
    recipient = input("👤 Destinataire (ex: api_provider) : ").strip()
    if not recipient:
        recipient = "merchant_demo"
        print(f"   → Destinataire par défaut : {recipient}")
    
    # Cohérence (optionnel)
    print("\n🎯 Score de cohérence (optionnel, 0.0 à 1.0)")
    print("   - 1.0 = action très cohérente et légitime")
    print("   - 0.0 = action suspecte ou incohérente")
    print("   - Seuil de sécurité : 0.6")
    
    coherence_input = input("   Score (appuyez sur Entrée pour 1.0 par défaut) : ").strip()
    
    if coherence_input:
        try:
            coherence = float(coherence_input)
            coherence = max(0.0, min(1.0, coherence))  # Limiter entre 0 et 1
        except ValueError:
            coherence = 1.0
            print("   → Valeur invalide, utilisation de 1.0")
    else:
        coherence = 1.0
    
    return amount, recipient, coherence

def process_payment(amount, recipient, coherence):
    """Traite le paiement et affiche le résultat"""
    print_separator()
    print("🔄 TRAITEMENT DU PAIEMENT...\n")
    
    # Créer l'action
    action = {
        "intent": "user_initiated_payment",
        "amount_usdc": amount,
        "recipient": recipient,
        "coherence": coherence
    }
    
    print(f"📋 Action : {action}")
    print()
    
    # Évaluer la sécurité
    decision = evaluate(action)
    
    print(f"🔒 Décision de sécurité : {decision}")
    print()
    
    if decision == "ALLOW":
        pay_usdc(action["amount_usdc"], action["recipient"])
        print(f"✅ PAIEMENT AUTORISÉ ET EXÉCUTÉ")
        print(f"   {amount} USDC → {recipient}")
    else:
        print(f"❌ PAIEMENT BLOQUÉ")
        print(f"   Raisons possibles :")
        print(f"   - Paiement trop rapide (< 10 secondes depuis le dernier)")
        print(f"   - Score de cohérence trop faible (< 0.6)")
    
    print_separator()

def show_tips():
    """Affiche des conseils pour tester différents scénarios"""
    print("\n💡 CONSEILS POUR TESTER :\n")
    print("1. Essayez un paiement normal (ex: 3 USDC, cohérence 1.0)")
    print("2. Essayez immédiatement un second paiement → BLOQUÉ (contrainte temporelle)")
    print("3. Attendez 10 secondes et réessayez → AUTORISÉ")
    print("4. Essayez avec une faible cohérence (ex: 0.3) → BLOQUÉ")
    print("5. Essayez avec une bonne cohérence (ex: 0.8) → AUTORISÉ\n")

def main():
    """Boucle principale de la démo interactive"""
    print_header()
    show_tips()
    
    while True:
        try:
            # Récupérer les paramètres
            amount, recipient, coherence = get_user_input()
            
            # Traiter le paiement
            process_payment(amount, recipient, coherence)
            
            # Demander si l'utilisateur veut continuer
            print("\n❓ Voulez-vous tester un autre paiement ?")
            choice = input("   (o)ui / (n)on : ").strip().lower()
            
            if choice not in ['o', 'oui', 'y', 'yes']:
                print("\n👋 Merci d'avoir testé la démo !")
                print("="*70 + "\n")
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Démo interrompue. Au revoir !")
            print("="*70 + "\n")
            break
        except Exception as e:
            print(f"\n❌ Erreur : {e}")
            print("Veuillez réessayer.\n")

if __name__ == "__main__":
    main()
