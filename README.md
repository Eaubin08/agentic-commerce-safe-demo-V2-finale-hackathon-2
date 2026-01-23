Agentic Commerce — Safe USDC Payments (Arc)

🇬🇧 English

What is this project?

This project is a research and hackathon demo exploring a critical question in agentic commerce:

How can AI agents pay in USDC without making unsafe, premature, or incoherent decisions?

Instead of optimizing how fast an agent can pay, this demo focuses on when an agent should NOT pay.

Core idea

In agentic commerce, AI agents may soon autonomously pay for APIs, compute, data, and digital services.
The primary risk is not technical execution, but irreversible money movement without sufficient judgment.

This demo introduces an opaque safety gate placed between:

Agent intent → Safety Gate → USDC payment


If the action is deemed safe, payment is allowed

If the action is unsafe, premature, or ambiguous, payment is blocked (HOLD)

What this demo demonstrates

This demo demonstrates that safe agentic payments do not require intelligence or optimization, but structural constraints.

Specifically, it shows that:

Payment decisions can be blocked by design, not by learning

Safety can emerge from temporal and coherence constraints, even with simple agents

A system can reliably say “NO” without exposing internal decision logic

The decision logic is intentionally opaque and non-explainable, focusing on observable behavior, not reasoning disclosure.

Architecture overview
Agent → Safety Gate → Arc USDC Settlement (mocked)


The USDC settlement layer is mocked

No real funds are moved

The focus is strictly on decision gating, not execution

What this demo is (and is not)

✅ A conceptual safety pattern for agentic commerce
✅ A behavioral proof of safe refusal (HOLD)
❌ Not a production payment system
❌ Not an AI optimization model
❌ Not a disclosed safety algorithm

How to run
python demo/run_demo.py
streamlit run ui/app.py

Demo behavior note

See SAFETY_SCALE.md for a short explanation of the 1–10 safety scale and why:

A payment may be allowed in CLI

But blocked in the UI

This is intentional and demonstrates context-sensitive safety gating.

Hackathon context

Designed for the Arc + Circle Agentic Commerce Hackathon.

This project intentionally limits disclosure to demonstrate safety outcomes, not internal mechanisms.

Intellectual Property & Usage Notice

This repository contains a demonstration and conceptual prototype.

Underlying decision logic, structural constraints, and extended safety mechanisms remain proprietary and undisclosed.

Reuse or production deployment requires explicit authorization.

🇫🇷 Français

De quoi s’agit-il ?

Ce projet est une démo de recherche / hackathon explorant une question centrale de l’agentic commerce :

Comment permettre à des agents IA de payer en USDC sans prendre de décisions dangereuses, prématurées ou incohérentes ?

La démo ne cherche pas à montrer comment payer vite, mais quand il ne faut pas payer.

Idée centrale

Dans l’agentic commerce, les agents IA pourraient bientôt payer de manière autonome des APIs, du calcul, des données ou des services numériques.
Le risque principal n’est pas technique, mais décisionnel : déplacer de l’argent sans jugement suffisant.

Cette démo introduit une barrière de sécurité opaque entre :

Intention de l’agent → Barrière de sécurité → Paiement USDC


Action sûre → paiement autorisé

Action dangereuse, prématurée ou ambiguë → blocage (HOLD)

Ce que la démo démontre réellement

Cette démo montre que la sécurité des paiements agentiques ne dépend pas de l’intelligence, mais de la structure.

Elle démontre que :

Un paiement peut être bloqué par conception, sans apprentissage

La sécurité peut émerger de contraintes temporelles et de cohérence

Un système peut dire « NON » de manière fiable, sans expliquer sa logique

La logique décisionnelle est volontairement opaque, afin de se concentrer sur le comportement observable, pas sur l’explication interne.

Architecture
Agent → Barrière de sécurité → Paiement USDC Arc (simulé)


La couche de paiement est simulée

Aucun fonds réel n’est déplacé

L’objectif est uniquement la barrière décisionnelle

Ce que cette démo est (et n’est pas)

✅ Un prototype conceptuel de sécurité
✅ Une preuve comportementale du HOLD
❌ Pas un système de paiement réel
❌ Pas un modèle d’IA optimisé
❌ Pas une divulgation de mécanismes internes

Lancer la démo
python demo/run_demo.py
streamlit run ui/app.py

Note sur le comportement

Voir SAFETY_SCALE.md pour une explication courte (EN/FR) de l’échelle de sécurité (1–10) et pourquoi :

Un paiement peut passer en CLI

Mais être bloqué dans l’UI

Ce comportement est intentionnel.

Contexte hackathon

Projet conçu pour le Arc + Circle Agentic Commerce Hackathon.

Le niveau de divulgation est volontairement limité afin de montrer les effets, pas les mécanismes internes.

Propriété intellectuelle & conditions d’usage

Ce dépôt contient une démo conceptuelle.

Les mécanismes avancés, contraintes structurelles et extensions restent propriétaires et non divulgués.

Toute réutilisation ou déploiement en production nécessite une autorisation explicite.