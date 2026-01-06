import numpy as np

class TFZPPZoo:
    """
    Structural Complexity Observatory (SCO) - TFZPP Benchmark Suite (v2).
    Includes Lossy-Code and the 'Nephew' problem (Fleming et al., 2025).
    
    Phase 12 Update:
    Fleming et al. show that TFZPP collapses to FP under white-box access
    (assuming E requires exponential circuits). The hardness of Nephew is
    only robust under BLACK_BOX oracle access.
    """
    def __init__(self):
        self.registry = {
            "Lossy-Code": self._generate_lossy_code_instance(),
            "Nephew": self._generate_nephew_instance()
        }

    def _generate_lossy_code_instance(self):
        return {
            "type": "TFZPP_COMPRESSION",
            "has_infinite_tree": True,
            "leaf_density": 0.8,
            "is_compressible": True,
            "access_mode": "ANY"
        }

    def _generate_nephew_instance(self):
        """
        Nephew: Model-theoretic complexity from set-theoretic axioms.
        CRITICAL: Hardness is BLACK_BOX_ONLY per Fleming et al.
        """
        return {
            "type": "TFZPP_NEPHEW",
            "has_infinite_tree": True,
            "leaf_density": 0.05,
            "is_compressible": False,
            "access_mode": "BLACK_BOX_ONLY",
            "derandomization_note": "Collapses to FP under white-box + E-hardness hypothesis."
        }

    def get_instance(self, name, access_mode="BLACK_BOX"):
        instance = self.registry.get(name)
        if instance and instance.get("access_mode") == "BLACK_BOX_ONLY" and access_mode != "BLACK_BOX":
            print(f"[WARNING] {name} hardness is BLACK_BOX_ONLY. Under WHITE_BOX, problem is DERANDOMIZABLE_TO_P.")
            return {**instance, "effective_hardness": "DERANDOMIZABLE_TO_P"}
        return instance

if __name__ == "__main__":
    zoo = TFZPPZoo()
    print(zoo.get_instance('Nephew', access_mode='BLACK_BOX'))
    print(zoo.get_instance('Nephew', access_mode='WHITE_BOX'))
