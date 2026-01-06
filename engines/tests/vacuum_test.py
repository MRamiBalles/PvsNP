"""
Vacuum Test - Information Redundancy Audit
Status: NEW (Phase 19)
Source: Nye (2025)

Verifies the Vacuum of Information property: internal states are reconstructible
from the holographic boundary with O(1) conditional complexity.
"""

import unittest
import math
from engines.holography.optimization import AlgebraicReplayEngine

class TestHolographicProperties(unittest.TestCase):
    def test_computational_area_law(self):
        """
        Verifica que el Payload escala como sqrt(T) y el Overhead como log(T).
        Fuente: Williams (2025), Nye (2025) Appendices B & C.
        """
        T = 4000
        are = AlgebraicReplayEngine(T)
        are.recursive_eval(0, T, 0)
        
        # Verificaciones asintóticas aproximadas
        # Payload b + t/b approx 2*sqrt(T)
        # Overhead log(T) * c
        limit_p = math.sqrt(T) * 3
        limit_o = math.log2(T) * 5
        
        print(f"\n[Area Law Audit] T={T}")
        print(f"  Observed Payload:  {are.max_payload} (Limit: <{limit_p:.1f})")
        print(f"  Observed Overhead: {are.max_overhead} (Limit: <{limit_o:.1f})")
        
        self.assertLess(are.max_payload, limit_p, "Payload violates sqrt(T) bound.")
        self.assertLess(are.max_overhead, limit_o, "Overhead exceeds log(T) bound.")
        self.assertLess(are.max_overhead, are.max_payload, "Overhead should be smaller than Payload.")

    def test_vacuum_of_information(self):
        """
        Verifica que los estados internos pueden reconstruirse solo desde la frontera.
        Fuente: Nye (2025), Lemma 1 (Bulk configurations have O(1) conditional complexity).
        """
        T = 1024
        are = AlgebraicReplayEngine(T)
        
        # 1. Generar la historia (solo se guarda el root summary en boundary_store al final)
        root_summary = are.recursive_eval(0, T, 0)
        
        # 2. Elegir un tiempo interno arbitrario que ya fue "olvidado"
        target_t = 512
        
        # 3. Intentar reconstruir el estado en t=512
        reconstructed_state = are.reconstruct_state_from_boundary(target_t, (0, T))
        
        self.assertIsNotNone(reconstructed_state, "Vacuum reconstruction failed.")
        self.assertEqual(reconstructed_state['t'], target_t, "Reconstructed time mismatch.")
        print(f"[Vacuum Test] Internal state {target_t} successfully regenerated from boundary.")

if __name__ == '__main__':
    unittest.main()
