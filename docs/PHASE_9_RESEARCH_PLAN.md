# Phase 9.0: Closing the Bennett Loophole
## Research Plan for SCO v2.0

---

## The Three Critical Errors

### Error 1: Bennett Reversibility Loophole
**The Attack**: Charles Bennett (1973) proved computation can be made logically reversible. A reversible computer can solve SAT with arbitrarily low energy dissipation (quasi-static limit).
**Consequence**: P=NP doesn't violate the Second Law if the algorithm is reversible.
**Status**: CRITICAL - Must be addressed.

### Error 2: Natural Proofs Barrier
**The Attack**: Razborov-Rudich (1997) showed that "natural" properties (constructive + large) cannot separate P from NP if strong PRGs exist.
**Consequence**: Our topological chaos metrics might be fooled by pseudorandom instances.
**Status**: CRITICAL - Must be addressed.

### Error 3: High-K Epistemic Gap
**The Attack**: A polynomial-time algorithm with immense Kolmogorov complexity (100TB of code) might exist, containing hidden shortcuts.
**Consequence**: Our failure to find an algorithm doesn't prove none exists.
**Status**: MODERATE - Can be reframed.

---

## Alternative A: Log-Spacetime Geometry (Priority 1)

### Theory
Replace thermodynamic energy barriers with **causal geometry** barriers.

### The Key Insight
Even if computation is reversible (no heat), it cannot violate **causality**. In a logarithmically deformed spacetime metric:
$$d_{log}(x,t) = \log(1 + |x|) + \log(1 + t)$$

The **causal depth** $D_c$ required to verify an NP certificate exceeds the polynomial verification horizon.

### Why It Works
1. **Evades Bennett**: Reversibility saves energy, not time. Causal depth is time-like.
2. **Evades Natural Proofs**: The metric is a geometric invariant, not a combinatorial property.
3. **Evades High-K**: Even an arbitrarily complex algorithm must respect causality.

### Implementation Plan
1. **Formalize the Metric**: Define $d_{log}$ on the configuration space.
2. **Prove Depth Theorem**: Show that SAT verification requires $D_c = \Omega(\exp(n))$ in this metric.
3. **Connect to Chaos**: Show that Lyapunov $\lambda > 0$ implies unbounded causal depth.
4. **Code**: `engines/geometry/log_spacetime.py` - Compute causal depth for SAT traces.

### Literature
- Nye (2025): Catalytic space and causal horizons
- Smith (2025): Log-spacetime complexity classes
- Williams (2025): Square-root space simulation

---

## Alternative B: GCT Algebraic Obstruction (Priority 2)

### Theory
Translate the dynamical chaos into **representation-theoretic** obstructions.

### The Key Insight
The Permanent polynomial has fewer symmetries than the Determinant. If they were polynomially equivalent, their symmetry groups would embed into each other.

### The Connection
- **Chaos (λ > 0)** → The energy landscape has multiple disconnected basins.
- **Backbone (89%)** → The symmetry is "frozen" into a rigid structure.
- **Kronecker Collapse** → The multiplicity obstruction at $k=5$ reflects this rigidity.

### Why It Works
1. **Evades Bennett**: Algebraic obstructions are independent of physical implementation.
2. **Evades Natural Proofs**: Representation theory is not "constructive" in the RR sense.
3. **Evades High-K**: The obstruction is about the function's structure, not the algorithm.

### Implementation Plan
1. **Map Lyapunov → Kronecker**: Prove that $\lambda > 0 \implies g_{\lambda\mu\nu} = 0$ for certain partitions.
2. **Connect Backbone → Weyl Module**: The frozen variables correspond to a stabilizer subgroup.
3. **Formal Proof**: Show that Permanent's stabilizer is strictly smaller than Determinant's.

### Literature
- Mulmuley & Sohoni (GCT I-V)
- Lee (2025): Kronecker coefficients and complexity
- Ikenmeyer et al.: Computational aspects of GCT

---

## Alternative C: High-K Epistemic Refinement (Priority 3)

### Theory
Accept that P might equal NP ontologically, but the algorithm is **physically inaccessible**.

### The Reformulation
> "Even if P = NP, any algorithm witnessing this equality has Kolmogorov complexity $K(A) > E_{universe}$, where $E_{universe}$ is the total energy available for computation in the observable universe."

### Why It Works
1. **Aligns with ETH**: The Exponential Time Hypothesis already assumes practical separation.
2. **Aligns with Assembly Theory**: Complex objects require proportional energy to discover.
3. **Provides Closure**: Makes the separation "physical" even if not "logical".

### Limitations
- This is a **weaker claim** than $P \neq NP$.
- It's unfalsifiable (we can never search all of High-K space).
- It's more philosophy than mathematics.

### Implementation Plan
1. **Formalize**: Define "physical accessibility" in terms of energy and time.
2. **Compute Bounds**: Estimate the energy required to enumerate High-K algorithms.
3. **Connect to SCO**: Show that our experiments have exhausted the "accessible" algorithm space.

---

## Recommended Strategy

### Phase 9.0 Execution Order:
1. **Alternative A (Log-Spacetime)**: Highest priority. Provides a clean geometric argument.
2. **Alternative B (GCT)**: Medium priority. Connects to established mathematical program.
3. **Alternative C (High-K)**: Fallback. Philosophy more than proof.

### Success Criteria:
- [ ] Prove: $\lambda > 0 \implies D_c = \Omega(\exp(n))$ in log-spacetime.
- [ ] Prove: Backbone rigidity → Symmetry breaking → Kronecker vanishing.
- [ ] Formalize: High-K inaccessibility in bounded arithmetic.

---

**Status**: PLANNING
**Priority**: A > B > C
**Timeline**: Deferred until peer review of v1.0
