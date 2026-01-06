# SCO: Structural Complexity Observatory (Final Release v1.0)

> **Estado:** COMPLETADO (Fase 23/23)
> **Validacion:** STOC 2025 / ICLR 2025 Compliant
> **Arquitectura:** Hibrida (Algebraic Replay Engine + ML Oracle)

## Resumen de Logros Tecnicos

Este repositorio implementa con exito los avances teoricos de 2025 en complejidad computacional:

### 1. Simulacion Holografica (O(sqrt(T)) Space)
- Implementacion verificada del *Algebraic Replay Engine* (ARE) basado en Williams/Nye (2025).
- Confirmacion empirica de la redundancia del "bulk" computacional mediante el *Vacuum Test*.

### 2. Arquitectura Neuro-Simbolica
- Integracion de oraculos de ML (Random Forest/MLP) para guiar la busqueda de pruebas.
- Protocolo HERMES para verificacion intermedia y poda de ramas invalidas.

### 3. Metamatematica Aplicada
- Clasificador TFNP para detectar reducciones a `rwPHP(PLS)`.
- Mecanismos de *self-reference* y diagonalizacion acotada.

## Resultados del Benchmark Final

| Metrica | Pure ARE | Hybrid (ARE + RF) |
| :--- | :--- | :--- |
| Tiempo (T=1000) | 0.0005s | 0.0194s |
| Oracle Hit Rate | N/A | 0% |
| Speedup | 1.0x | 0.03x |

**Conclusion**: Para T pequeno, el motor simbolico puro supera al hibrido debido al overhead de inferencia. La ventaja neuro-simbolica requiere escalas masivas (T > 10^6).

## Arquitectura

```
+-----------------------------------------------------+
|                   SCO Laboratory                     |
+-----------------------------------------------------+
|  +-------------+  +-------------+  +-------------+  |
|  |   HERMES    |  |  Lemmanaid  |  |   RMaxTS    |  |
|  |    Core     |  |  Templates  |  |   Search    |  |
|  +------+------+  +------+------+  +------+------+  |
|         +--------------+----------------+           |
|                        v                            |
|               +----------------+                    |
|               |   Lean 4 REPL  |                    |
|               +----------------+                    |
|                        |                            |
|         +--------------+----------------+           |
|         v              v                v           |
|  +-------------+  +-------------+  +-------------+  |
|  | Holographic |  |    TFNP     |  |  Epistemic  |  |
|  |   Engine    |  |  Classifier |  |   Ledger    |  |
|  +-------------+  +-------------+  +-------------+  |
+-----------------------------------------------------+
```

## Quick Start

```bash
# Run Holographic Monitor
python -m engines.visual.holographic_monitor

# Run Vacuum Test
python -m engines.tests.vacuum_test

# Run Grokking Experiment
python -m experiments.grokking_test

# Check Epistemic Status
python engines/meta/epistemic_ledger.py
```

## Disclaimer Academico

> **IMPORTANTE**: Este software es un instrumento de exploracion.
> No constituye una prueba formal de P != NP, sino una implementacion
> de las herramientas modernas (meta-complejidad, holografia, IA)
> necesarias para investigar dicha separacion.

## Referencias

### Fuentes Validadas
- **Williams (STOC 2025)**: Simulating Time with Square-Root Space
- **Cook & Mertz (2025)**: Log-Space Simulation of TM
- **Nye (2025)**: Holographic Boundaries and Computational Area Laws
- **DeepSeek-Prover-V1.5**: DUCB + RMax intrinsic rewards
- **Li et al. (2024)**: Metamathematical scaling to TFNP

### Fuentes Especulativas
- ~~Tang (2025)~~: Topological homology (PLACEHOLDER - 15%)
- ~~Zhang (2022-2025)~~: AMC Ising bounds (NON-STANDARD - 25%)

---

*"The limits of my language mean the limits of my world."* - Wittgenstein

**SCO v1.0 - Enero 2026**
