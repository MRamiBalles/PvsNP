# engines/physics/__init__.py
"""Physics engines for computational phase transitions."""

from engines.physics.phase_detector import SpinGlassPhaseDetector, PhaseType, SATInstance
from engines.physics.cavity_solver import SurveyPropagationEngine

__all__ = ['SpinGlassPhaseDetector', 'PhaseType', 'SATInstance', 'SurveyPropagationEngine']
