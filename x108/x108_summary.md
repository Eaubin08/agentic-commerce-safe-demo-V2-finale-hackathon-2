# X-108 — Temporal Coherence (Hackathon Summary)

**Claim (operational):**
For irreversible actions (like payments), **speed is a structural risk**.
A system must satisfy **coherence over time** before it is allowed to act.

**What we enforce in this demo:**
- **Safety threshold** (1–10 scale): if below threshold → HOLD
- **Coherence threshold** (0–1): if below threshold → HOLD
- **Temporal HOLD window**: if the last signal is too recent → HOLD

**Why it matters for agentic commerce:**
Agentic payments are not mainly a payment execution problem.
They are a **decision under irreversibility** problem.
The gate makes unsafe/ambiguous money movement non-executable.

**Result:**
- Fast/optimizing behavior can be blocked *by structure*
- Stable, coherent behavior is allowed

This is presented as a **research + hackathon safety pattern**.
