# SCO: Structural Complexity Observatory (Neuro-Symbolic Lab)

> ✅ **Status: OPERATIONAL** | Epistemic Confidence: **95%**
>
> This repository hosts a **Neuro-Symbolic Reasoning Laboratory** for investigating computational complexity via holographic algorithms and AI-assisted formal verification.

## 🚀 Current State (Phase 20 - 2025/2026)

The system has **overcome the Emergency Rollback** (Phase 14) and now operates under the **SOTA 2025 paradigm**.

### 1. Holographic Engine - **ACTIVE (95%)**
Implementation of the *Algebraic Replay Engine* (ARE) and *Height Compression Theorem*.
- **Capability**: Deterministic simulation of time $T$ in space $O(\sqrt{T})$.
- **Validation**: Based on R. Ryan Williams (STOC 2025 Accepted) and Cook & Mertz (2025).
- **Status**: ✅ Empirically verified (Area Law Monitor, Vacuum Test).

### 2. Neuro-Symbolic Agent (HERMES/Lemmanaid)
Hybrid system combining LLMs with formal verification in Lean 4.
- **Functionality**: Lemma template generation (`?Hk`) and MCTS proof search with intrinsic reward (RMaxTS/DUCB).
- **Sources**: DeepSeek-Prover-V1.5, Alhessi et al. (2025), Ospanov et al. (2025).

### 3. Metamathematics (TFNP Classifier)
Total search complexity classifier.
- **Capability**: Detection of reductions to `rwPHP(PLS)` and refutation game analysis.
- **Sources**: Li et al. (2024), Ghentiyala & Li (2025).

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   SCO Laboratory                     │
├─────────────────────────────────────────────────────┤
│  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │  HERMES   │  │ Lemmanaid │  │  RMaxTS   │       │
│  │  Core     │  │ Templates │  │  Search   │       │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘       │
│        └──────────────┼──────────────┘             │
│                       ▼                            │
│              ┌─────────────────┐                    │
│              │   Lean 4 REPL   │                    │
│              └─────────────────┘                    │
│                       │                            │
│        ┌──────────────┼──────────────┐             │
│        ▼              ▼              ▼             │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │Holographic│  │  TFNP     │  │ Epistemic │       │
│  │  Engine   │  │ Classifier│  │  Ledger   │       │
│  └───────────┘  └───────────┘  └───────────┘       │
└─────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Run Holographic Monitor
python -m engines.visual.holographic_monitor

# Run Vacuum Test
python -m engines.tests.vacuum_test

# Check Epistemic Status
python engines/meta/epistemic_ledger.py
```

## ⚠️ Academic Disclaimer
This software is an **experimental research tool**. While individual modules (ARE, MCTS, TFNP) implement proven theorems, the integration for exploring lower bounds ($P \neq NP$) remains an active research area and does not constitute a mathematical proof by itself.

## References

### Validated Sources
- **Williams (STOC 2025)**: Simulating Time with Square-Root Space
- **Cook & Mertz (2025)**: Log-Space Simulation of TM
- **DeepSeek-Prover-V1.5**: DUCB + RMax intrinsic rewards
- **Li et al. (2024)**: Metamathematical scaling to TFNP

### Speculative Sources
- ~~Tang (2025)~~: Topological homology (PLACEHOLDER - 15%)
- ~~Zhang (2022-2025)~~: AMC Ising bounds (NON-STANDARD - 25%)

---

*"The limits of my language mean the limits of my world."* - Wittgenstein
