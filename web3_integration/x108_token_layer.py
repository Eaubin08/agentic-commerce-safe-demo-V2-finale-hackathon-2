"""
X-108 Token Economics Layer
============================

Couche modulaire pour l'intégration Web3 avec le token $X108.
Ne modifie pas le core existant (demo/guard_lite.py).

"An agent should not pay because it can — it should pay only when the action survives time."

Fonctionnalités :
- Collecte de frais de transaction (0.1%)
- Distribution aux stakers $X108
- Récupération des paramètres de gouvernance depuis le smart contract
- Statistiques token economics
"""

from web3 import Web3
from typing import Dict, Optional
import os
import json

class X108TokenEconomics:
    """
    Gère l'économie du token $X108 et l'intégration avec le smart contract.
    """
    
    def __init__(self, contract_address: Optional[str] = None, provider_url: Optional[str] = None):
        """
        Initialize the token economics layer.
        
        Args:
            contract_address: Address of the deployed X108Token contract
            provider_url: RPC endpoint (Base, Ethereum, etc.)
        """
        # Configuration (peut être overridé par variables d'environnement)
        self.contract_address = contract_address or os.getenv('X108_CONTRACT_ADDRESS', '0x0000000000000000000000000000000000000000')
        self.provider_url = provider_url or os.getenv('WEB3_PROVIDER_URL', 'https://base-mainnet.g.alchemy.com/v2/YOUR_KEY')
        
        # Mode démo si pas de contrat déployé
        self.demo_mode = self.contract_address == '0x0000000000000000000000000000000000000000'
        
        if not self.demo_mode:
            try:
                self.w3 = Web3(Web3.HTTPProvider(self.provider_url))
                self.contract = self._load_contract()
            except Exception as e:
                print(f"Warning: Could not connect to Web3 provider. Running in demo mode. Error: {e}")
                self.demo_mode = True
        
        # Stats en mémoire pour le mode démo
        self.demo_stats = {
            'total_transactions': 0,
            'total_fees_collected': 0.0,
            'total_stakers': 89,  # Valeur fictive pour la démo
            'apy': 14.3,  # Valeur fictive pour la démo
            'token_price': 0.23,  # Valeur fictive pour la démo
            'market_cap': 2300000.0  # Valeur fictive pour la démo
        }
    
    def _load_contract(self):
        """
        Load the X108Token smart contract.
        """
        # ABI du contrat (simplifié pour les fonctions essentielles)
        contract_abi = [
            {
                "inputs": [],
                "name": "temporalWindow",
                "outputs": [{"type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "coherenceThreshold",
                "outputs": [{"type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"name": "_transactionAmount", "type": "uint256"}],
                "name": "collectFee",
                "outputs": [{"name": "fee", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "totalStaked",
                "outputs": [{"type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "estimateAPY",
                "outputs": [{"type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
        return self.w3.eth.contract(
            address=Web3.to_checksum_address(self.contract_address),
            abi=contract_abi
        )
    
    def charge_transaction_fee(self, payment_amount: float) -> Dict:
        """
        Applique 0.1% de frais sur chaque paiement validé.
        
        Args:
            payment_amount: Montant du paiement en USDC
            
        Returns:
            Dict avec net_amount, fee, et distribution info
        """
        # Frais de 0.1% (10 basis points)
        fee = payment_amount * 0.001
        net_amount = payment_amount - fee
        
        # Mise à jour des stats (mode démo ou on-chain)
        if self.demo_mode:
            self.demo_stats['total_transactions'] += 1
            self.demo_stats['total_fees_collected'] += fee
        else:
            try:
                # Appeler le smart contract pour collecter les frais
                # (nécessite une transaction signée en production)
                pass
            except Exception as e:
                print(f"Warning: Could not record fee on-chain: {e}")
        
        return {
            'net_amount': round(net_amount, 6),
            'fee': round(fee, 6),
            'fee_distribution': {
                'stakers': round(fee * 0.5, 6),  # 50% aux stakers
                'treasury': round(fee * 0.3, 6),  # 30% au treasury
                'buyback': round(fee * 0.2, 6)   # 20% buyback
            },
            'mode': 'demo' if self.demo_mode else 'on-chain'
        }
    
    def get_governance_params(self) -> Dict:
        """
        Récupère les paramètres de sécurité depuis le smart contract.
        
        Returns:
            Dict avec temporal_window et coherence_threshold
        """
        if self.demo_mode:
            return {
                'temporal_window': 10,  # secondes
                'coherence_threshold': 0.6,  # 0.0 à 1.0
                'source': 'demo'
            }
        
        try:
            temporal_window = self.contract.functions.temporalWindow().call()
            coherence_threshold = self.contract.functions.coherenceThreshold().call() / 100.0  # Convertir de 60 à 0.6
            
            return {
                'temporal_window': temporal_window,
                'coherence_threshold': coherence_threshold,
                'source': 'on-chain'
            }
        except Exception as e:
            print(f"Warning: Could not fetch governance params: {e}")
            return {
                'temporal_window': 10,
                'coherence_threshold': 0.6,
                'source': 'fallback'
            }
    
    def get_token_stats(self) -> Dict:
        """
        Récupère les statistiques du token $X108.
        
        Returns:
            Dict avec total_transactions, fees_collected, stakers, apy, price, market_cap
        """
        if self.demo_mode:
            return self.demo_stats
        
        try:
            total_staked = self.contract.functions.totalStaked().call()
            apy = self.contract.functions.estimateAPY().call()
            
            return {
                'total_transactions': self.demo_stats['total_transactions'],
                'total_fees_collected': self.demo_stats['total_fees_collected'],
                'total_stakers': 89,  # À récupérer depuis un indexer en production
                'apy': apy / 100.0,  # Convertir de 1430 à 14.3%
                'token_price': 0.23,  # À récupérer depuis un oracle de prix
                'market_cap': 2300000.0,  # Calculé depuis supply * price
                'total_staked': total_staked / 10**18  # Convertir de wei
            }
        except Exception as e:
            print(f"Warning: Could not fetch token stats: {e}")
            return self.demo_stats
    
    def format_transaction_for_display(self, transaction: Dict) -> str:
        """
        Formate une transaction pour l'affichage avec info token economics.
        
        Args:
            transaction: Dict avec les détails de la transaction
            
        Returns:
            String formaté pour affichage
        """
        fee_info = self.charge_transaction_fee(transaction.get('amount', 0))
        
        return f"""
💰 **Token Economics Applied**

**Original Amount:** {transaction.get('amount', 0)} USDC
**Transaction Fee (0.1%):** {fee_info['fee']} USDC
**Net Amount:** {fee_info['net_amount']} USDC

**Fee Distribution:**
- 🏆 Stakers (50%): {fee_info['fee_distribution']['stakers']} USDC
- 🏛️ Treasury (30%): {fee_info['fee_distribution']['treasury']} USDC
- 🔄 Buyback (20%): {fee_info['fee_distribution']['buyback']} USDC

**Mode:** {fee_info['mode']}
        """
    
    def is_contract_deployed(self) -> bool:
        """
        Vérifie si le contrat est déployé et accessible.
        
        Returns:
            True si le contrat est déployé, False sinon
        """
        return not self.demo_mode


# Fonction utilitaire pour créer une instance
def create_token_layer() -> X108TokenEconomics:
    """
    Factory function pour créer une instance de X108TokenEconomics.
    """
    return X108TokenEconomics()


# Exemple d'utilisation
if __name__ == "__main__":
    # Test en mode démo
    token_layer = create_token_layer()
    
    print("🔗 X-108 Token Economics Layer")
    print(f"Mode: {'Demo' if token_layer.demo_mode else 'On-Chain'}")
    print()
    
    # Test de frais de transaction
    print("📊 Transaction Fee Test:")
    fee_info = token_layer.charge_transaction_fee(100.0)
    print(f"Original: 100 USDC")
    print(f"Fee: {fee_info['fee']} USDC")
    print(f"Net: {fee_info['net_amount']} USDC")
    print()
    
    # Test des paramètres de gouvernance
    print("⚙️ Governance Parameters:")
    params = token_layer.get_governance_params()
    print(f"Temporal Window: {params['temporal_window']}s")
    print(f"Coherence Threshold: {params['coherence_threshold']}")
    print()
    
    # Test des statistiques
    print("📈 Token Statistics:")
    stats = token_layer.get_token_stats()
    print(f"Total Transactions: {stats['total_transactions']}")
    print(f"Total Fees: {stats['total_fees_collected']} USDC")
    print(f"Stakers: {stats['total_stakers']}")
    print(f"APY: {stats['apy']}%")
    print(f"Token Price: ${stats['token_price']}")
    print(f"Market Cap: ${stats['market_cap']:,.0f}")
