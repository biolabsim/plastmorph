"""PlastMorph simulation package."""

from plastmorph.environments import ENVIRONMENTS, EnvironmentProfile
from plastmorph.i18n import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES, translate
from plastmorph.materials import MATERIALS, PlasticMaterial
from plastmorph.simulation import SimulationConfig, simulate_mass_curve

__all__ = [
    "MATERIALS",
    "ENVIRONMENTS",
    "DEFAULT_LANGUAGE",
    "SUPPORTED_LANGUAGES",
    "PlasticMaterial",
    "EnvironmentProfile",
    "SimulationConfig",
    "simulate_mass_curve",
    "t",
]
