# Structural Complexity Observatory (SCO)

> ⚠️ **Status: Experimental Research Framework**
> 
> This repository implements the Structural Complexity Observatory (SCO), a neuro-symbolic reasoning laboratory for exploring computational complexity through formal verification.

## Critical Notices

### Retracted Theories (Phase 14)

Several foundational theories have been **RETRACTED** or marked as **SPECULATIVE**:

| Pillar | Status | Confidence | Issue |
|--------|--------|------------|-------|
| Holographic Optimization | **RETRACTED** | 10% | Nye (2025): "proof of main theorem is incorrect" |
| Topological Homology | **SPECULATIVE** | 15% | Tang (2025): placeholder/future-dated work |
| AMC Ising Physics | **NON-STANDARD** | 25% | Zhang's claims not mainstream consensus |
| Nephew TFZPP | **PARADOX** | 20% | White-box SCO contradicts black-box hardness |

### What This System IS

✅ A **research exploration tool** for neuro-symbolic reasoning  
✅ A **formal verification laboratory** using HERMES/Lemmanaid architecture  
✅ A **benchmark platform** for testing AI-assisted theorem proving  

### What This System IS NOT

❌ A proof of P ≠ NP  
❌ A deployable complexity classifier  
❌ Evidence for separation results  

## Architecture

### Neuro-Symbolic Core (Phase 15)

```
┌─────────────────────────────────────────────────────┐
│                    SCO Laboratory                    │
├─────────────────────────────────────────────────────┤
│  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │  HERMES   │  │ Lemmanaid │  │  RMaxTS   │       │
│  │  Core     │  │ Templates │  │  Search   │       │
│  │           │  │           │  │           │       │
│  │ Translate │  │ Generate  │  │ MCTS with │       │
│  │ Verify    │  │ Fill Holes│  │ Lean      │       │
│  │ Store     │  │ Filter    │  │ Feedback  │       │
│  └───────────┘  └───────────┘  └───────────┘       │
│         │              │              │             │
│         └──────────────┼──────────────┘             │
│                        ▼                            │
│              ┌─────────────────┐                    │
│              │   Lean 4 REPL   │                    │
│              │   (Verifier)    │                    │
│              └─────────────────┘                    │
└─────────────────────────────────────────────────────┘
```

### Modules

- `engines/agent/hermes_core.py` - Translation-Verification-Memory loop
- `engines/agent/lemmanaid.py` - Template-based lemma synthesis
- `engines/search/rmax_ts.py` - Monte-Carlo tree search with UCB
- `experiments/putnam_bench.py` - University-level problem benchmark

### Legacy Modules (Heuristic Only)

- `engines/meta/epistemic_ledger.py` - Tracks confidence in theoretical pillars
- `engines/meta/bridge.py` - Physical-homological consistency (EXPERIMENTAL)
- `engines/physics/thermodynamic.py` - Entropic cost analysis (HEURISTIC)

## Quick Start

```bash
# Run the HERMES agent
python engines/agent/hermes_core.py

# Run Lemmanaid synthesis
python engines/agent/lemmanaid.py

# Run benchmark
python experiments/putnam_bench.py

# Check epistemic status
python engines/meta/epistemic_ledger.py
```

## References

### Verified Sources
- Edwards (Nov 2025): SPDP Rank for algebraic complexity
- Ghentiyala & Li (Jul 2025): Self-lowness in TFNP
- Li et al. (2024): Metamathematical scaling to TFNP

### Retracted/Speculative Sources
- ~~Nye (Nov 2025)~~: Holographic simulation (RETRACTED)
- ~~Tang (2025)~~: Topological homology (PLACEHOLDER)
- ~~Zhang (2022-2025)~~: AMC Ising bounds (NON-STANDARD)

## License

Research use only. Not for production deployment.

---

*"The limits of my language mean the limits of my world."* - Wittgenstein
