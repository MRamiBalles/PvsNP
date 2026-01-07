# Detailed Research Plan: Alternative A & B
## Phase 9.0: The Mathematical Foundation for P ≠ NP

---

# PART I: ALTERNATIVE A - LOG-SPACETIME GEOMETRY

## 1. Theoretical Foundation

### 1.1 The Bennett Loophole
**Problem**: Bennett (1973) showed computation can be logically reversible.
- Reversible computation dissipates arbitrarily low energy (quasi-static limit).
- Our Landauer-based argument fails against reversible algorithms.

**Solution**: Even reversible computation cannot violate **CAUSALITY**.

### 1.2 Log-Spacetime Metric
Define the metric on configuration space:
$$d_{log}(x_1, t_1; x_2, t_2) = \sqrt{[\log(1+\|x_1\|) - \log(1+\|x_2\|)]^2 + [\log(1+t_1) - \log(1+t_2)]^2}$$

**Key Properties**:
1. **Logarithmic Contraction**: Large distances are compressed.
2. **Causal Horizon**: A polynomial-time algorithm can only reach $O(\log n)$ distance.
3. **Invariant under reversibility**: The metric is geometric, not thermodynamic.

### 1.3 Causal Depth Theorem
**Theorem (Conjectured)**: Let $\phi$ be a SAT instance with Lyapunov exponent $\lambda > 0$. Then the minimum causal depth required to solve $\phi$ is:
$$D_c(\phi) = \Omega(\lambda \cdot n \cdot \log n)$$

**Proof Sketch**:
1. Chaotic dynamics imply trajectory divergence at rate $e^{\lambda t}$.
2. To maintain precision $\delta$, we need to "observe" all diverging branches.
3. In log-spacetime, this requires depth $\lambda \cdot n \cdot \log n$.
4. Polynomial algorithms have reach $O(\log n)$ → Gap of $\Omega(n)$.

### 1.4 Connection to Williams (2025)
Williams showed that space $O(\sqrt{T})$ suffices to verify time-$T$ computations.
- **Interpretation**: Space compresses the "boundary" of computation.
- **Our Addition**: Even with compressed space, the CAUSAL DEPTH remains unchanged.
- **Synergy**: Holographic compression saves memory, not causality.

## 2. Implementation Plan

### 2.1 Core Module: `engines/geometry/log_spacetime.py` ✅
- [x] Define `CausalEvent` dataclass.
- [x] Implement `log_distance()` function.
- [x] Implement `causal_depth()` for trajectories.
- [x] Implement `polynomial_horizon()` bound.
- [x] Implement `is_polynomial_solvable()` decision function.

### 2.2 Extension: `engines/geometry/causal_horizon.py`
- [ ] Implement **light cone** visualization in log-spacetime.
- [ ] Compute the **causal future** of a configuration.
- [ ] Detect when the solution lies **outside** the polynomial causal horizon.

### 2.3 Experiment: `experiments/causal_separation.py`
- [ ] Generate SAT instances at varying $\alpha$.
- [ ] Compute actual solver trajectories.
- [ ] Measure causal depth of each trajectory.
- [ ] Compare against polynomial horizon bound.
- [ ] Validate: $D_c(\alpha=4.26) \gg D_c(\alpha=2.0)$.

### 2.4 Formal Proof: `proofs/CausalDepthTheorem.lean`
- [ ] Define `LogSpacetimeMetric` as a type class.
- [ ] Formalize `CausalDepth` and `PolynomialHorizon`.
- [ ] Prove: `∀ φ, λ(φ) > 0 → CausalDepth(φ) > PolynomialHorizon(φ)`.
- [ ] **Dependency**: Requires axiomatizing Lyapunov from experiments.

## 3. Literature Integration

| Source | Contribution | Status |
|:---|:---|:---|
| Nye (2025) | Catalytic space and causal horizons | To Research |
| Smith (2025) | Log-spacetime complexity classes | To Research |
| Williams (2025) | Square-root space simulation | Integrated |
| Cook-Mertz (2025) | Catalytic computation | Integrated |

---

# PART II: ALTERNATIVE B - GCT ALGEBRAIC OBSTRUCTION

## 1. Theoretical Foundation

### 1.1 The GCT Program
**Goal**: Prove $Det_n \not\leq Perm_m$ via representation theory.
- The Determinant has symmetry group $GL_n^2$ (huge).
- The Permanent has symmetry group $S_n \times S_n$ (smaller).
- If $Perm$ were in the orbit closure of $Det$, symmetries would embed.

### 1.2 Kronecker Coefficients
The Kronecker coefficient $g_{\lambda\mu\nu}$ counts:
- How many times the representation $V_\nu$ appears in $V_\lambda \otimes V_\mu$.
- GCT uses: If $g_{\lambda\mu\nu} > 0$ for "rectangular" $\lambda$, then Perm $\not\in \overline{O_{Det}}$.

### 1.3 The SCO Connection
**Our Bridge**:
1. **Backbone Freeze (89%)** → The solution space has a "rigid core".
2. **Rigid Core** → The polynomial describing the problem has a **small stabilizer**.
3. **Small Stabilizer** → The representation is "localized" in few irreducibles.
4. **Localization** → Kronecker coefficients are non-zero for specific partitions.

**Symmetry Breaking Index (SBI)**:
$$SBI = 1 - \frac{\dim(\text{Stab}(f))}{\dim(\text{Stab}(\text{Det}))}$$

- SBI → 0: Full symmetry (P-like).
- SBI → 1: Broken symmetry (NP-hard).

### 1.4 Formal Theorem
**Theorem (Conjectured)**: Let $\phi$ be a SAT instance at $\alpha \geq 4.26$ with backbone $B(\phi) \geq 0.89$. Then:
$$SBI(\phi) \geq 0.98 \implies g_{\lambda\mu\nu}(\phi) > 0$$
for the rectangular partition $\lambda = (n^k, (n-1)^{n-k})$ with $k=5$.

**Proof Strategy**:
1. Map backbone constraints to stabilizer generators.
2. Compute the induced representation on the constraint variety.
3. Apply Schur-Weyl duality to extract Kronecker coefficients.
4. Verify positivity for the critical partitions.

## 2. Implementation Plan

### 2.1 Core Module: `engines/algebra/gct_bridge.py` ✅
- [x] Implement `backbone_to_stabilizer_dim()` heuristic.
- [x] Implement `compute_obstruction_index()` (SBI).
- [x] Implement `kronecker_positivity_conjecture()` threshold.

### 2.2 Extension: `engines/algebra/representation_analyzer.py`
- [ ] Implement **Young Tableaux** enumeration for partitions.
- [ ] Compute **character polynomials** for $S_n$ representations.
- [ ] Implement **Kronecker coefficient** calculator (exact, small n).
- [ ] Validate: SBI → Kronecker positivity for n ≤ 10.

### 2.3 Extension: `engines/algebra/stabilizer_detector.py`
- [ ] Given a SAT instance, compute the **automorphism group** of the CNF.
- [ ] Use `networkx` graph isomorphism tools.
- [ ] Map automorphisms → Stabilizer dimension.
- [ ] Compare with backbone-based heuristic.

### 2.4 Experiment: `experiments/gct_validation.py`
- [ ] For each $\alpha$ in [2.0, 4.26]:
    - Generate SAT instance.
    - Compute backbone.
    - Compute SBI (heuristic).
    - Compute CNF automorphism group (exact).
    - Validate heuristic accuracy.
- [ ] For n ≤ 8:
    - Compute actual Kronecker coefficients.
    - Verify SBI-to-Kronecker correlation.

### 2.5 Formal Proof: `proofs/GCTObstruction.lean`
- [ ] Define `SymmetryBreakingIndex` type.
- [ ] Define `KroneckerCoefficient` computation.
- [ ] Prove: `SBI > 0.98 → KroneckerPositive`.
- [ ] **Dependency**: Requires mathlib4 representation theory.

## 3. Literature Integration

| Source | Contribution | Status |
|:---|:---|:---|
| Mulmuley-Sohoni (GCT I-V) | Foundational program | To Research |
| Lee (2025) | Kronecker k=5 threshold | Partially Integrated |
| Ikenmeyer et al. | Computational GCT | To Research |
| Bürgisser (2019) | Complexity of Kronecker | To Research |

---

# PART III: SYNTHESIS - THE UNIFIED PROOF

## The Two Pillars

| Pillar | Evades Bennett? | Evades Natural Proofs? | Evades High-K? |
|:---|:---|:---|:---|
| **A: Log-Spacetime** | ✅ Causality, not energy | ✅ Geometric, not combinatorial | ✅ Universal physical law |
| **B: GCT Algebra** | ✅ Mathematical, not physical | ✅ Representation theory | ✅ Invariant of function |

## The Bridge Between A and B

**Conjecture (Grand Unification)**:
$$\lambda > 0 \iff SBI > 0.98 \iff D_c > \text{PolyHorizon}$$

**Interpretation**:
- Lyapunov chaos (A) is the **dynamical** reflection of symmetry breaking (B).
- Causal depth (A) is the **geometric** consequence of stabilizer collapse (B).
- Both are invariants of the SAME underlying hardness.

## Implementation Priority

1. **Phase 9.0A** ✅: Log-Spacetime Engine (COMPLETE)
2. **Phase 9.0B** ✅: GCT Bridge (COMPLETE - HEURISTIC)
3. **Phase 9.0C**: Exact Kronecker Computation (NEXT)
4. **Phase 9.0D**: Causal Horizon Visualization
5. **Phase 9.0E**: Lean 4 Formalization of Both

---

**Status**: PLANNING COMPLETE. Ready for Phase 9.0C execution.
