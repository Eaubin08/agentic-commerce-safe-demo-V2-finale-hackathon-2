"""X-108 Hackathon Gate (minimal).

Goal: show *when NOT to pay* by enforcing:
- a temporal HOLD before irreversible actions
- a minimal coherence check

This is intentionally simple for hackathon/demo use.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
import time

@dataclass
class GateDecision:
    allow: bool
    action: str              # "ACT" or "HOLD"
    reason: str
    details: Dict[str, Any]

def evaluate_payment_gate(
    safety_score: float,
    coherence_score: float,
    *,
    now_ts: Optional[float] = None,
    last_signal_ts: Optional[float] = None,
    min_hold_seconds: int = 15,
    safety_threshold: float = 7.0,
    coherence_threshold: float = 0.70,
) -> GateDecision:
    """Return a decision for an irreversible action (e.g., USDC payment).

    Inputs:
      - safety_score: 1..10 (higher is safer)
      - coherence_score: 0..1 (higher is more coherent)
      - last_signal_ts: timestamp of the last *new* signal/event/intent update
        (used to require a temporal HOLD window before acting)
    """
    now_ts = time.time() if now_ts is None else float(now_ts)

    # 1) Hard safety threshold (cheap, explicit)
    if safety_score < safety_threshold:
        return GateDecision(
            allow=False,
            action="HOLD",
            reason="Safety score below threshold",
            details={
                "safety_score": safety_score,
                "safety_threshold": safety_threshold,
            },
        )

    # 2) Coherence check (still lightweight)
    if coherence_score < coherence_threshold:
        return GateDecision(
            allow=False,
            action="HOLD",
            reason="Coherence below threshold",
            details={
                "coherence_score": coherence_score,
                "coherence_threshold": coherence_threshold,
            },
        )

    # 3) Temporal HOLD before irreversible action (time as safety primitive)
    if last_signal_ts is not None:
        elapsed = now_ts - float(last_signal_ts)
        if elapsed < min_hold_seconds:
            return GateDecision(
                allow=False,
                action="HOLD",
                reason="Temporal HOLD window not satisfied",
                details={
                    "elapsed_seconds": round(elapsed, 3),
                    "min_hold_seconds": min_hold_seconds,
                },
            )

    # Passed
    return GateDecision(
        allow=True,
        action="ACT",
        reason="Gate passed (safe + coherent + temporal)",
        details={
            "safety_score": safety_score,
            "coherence_score": coherence_score,
            "min_hold_seconds": min_hold_seconds,
        },
    )
