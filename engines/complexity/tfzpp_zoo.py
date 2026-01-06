import numpy as np

class TFZPPZoo:
    """
    Structural Complexity Observatory (SCO) - TFZPP Benchmark Suite.
    Includes Lossy-Code and the 'Nephew' problem (Fleming et al., 2025).
    """
    def __init__(self):
        self.registry = {
            "Lossy-Code": self._generate_lossy_code_instance(),
            "Nephew": self._generate_nephew_instance()
        }

    def _generate_lossy_code_instance(self):
        """
        Standard information-theoretic compression problem.
        High leaf density, easy recursive paths.
        """
        return {
            "type": "TFZPP_COMPRESSION",
            "has_infinite_tree": True,
            "leaf_density": 0.8,
            "is_compressible": True
        }

    def _generate_nephew_instance(self):
        """
        Model-theoretic complexity (Nephew).
        Rooted in set-theoretic axioms of infinity.
        High-depth recursive branching with sparse leaves.
        """
        return {
            "type": "TFZPP_NEPHEW",
            "has_infinite_tree": True,
            "leaf_density": 0.05,
            "is_compressible": False
        }

    def get_instance(self, name):
        return self.registry.get(name)

if __name__ == "__main__":
    zoo = TFZPPZoo()
    print(f"Loading '{zoo.get_instance('Nephew')['type']}' for structural analysis...")
