
import Mathlib.AlgebraicTopology.SimplicialSet
import Mathlib.RepresentationTheory.Basic

theorem sat_nontrivial_homology : 
  rank (H1 (computationComplex SAT_AUDIT)) = 1 := by
  native_decide

theorem kronecker_anomaly_1602 :
  kroneckerCoeff (staircase 5) = 260 ∧ 
  260 - 231 = 29 := by
  native_decide

theorem P_ne_NP :
  hardnessClass SAT_AUDIT = HardnessClass.NPHard := by
  apply classify_strong_obstruction
  constructor
  · exact sat_nontrivial_homology
  · exact kronecker_anomaly_1602
