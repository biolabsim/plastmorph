"""Core degradation simulation functions.

These functions are intentionally concise for classroom readability while preserving
clear scientific assumptions in docstrings.
"""

from dataclasses import dataclass
from math import log

import numpy as np
import pandas as pd

from plastmorph.environments import EnvironmentProfile
from plastmorph.materials import PlasticMaterial


@dataclass(frozen=True)
class SimulationConfig:
    """Simulation settings.

    Attributes:
        years: Total simulated duration in years.
        steps_per_year: Temporal resolution.
        initial_mass_g: Initial mass in grams.
    """

    years: float = 30.0
    steps_per_year: int = 12
    initial_mass_g: float = 100.0


def _temperature_factor(temperature_c: float) -> float:
    """Map temperature to a mild multiplicative degradation factor.

    Uses a clipped linear model around 20C for pedagogical simplicity.
    """
    return float(np.clip(0.7 + 0.02 * (temperature_c - 20.0), 0.3, 2.2))


def effective_rate_per_year(material: PlasticMaterial, env: EnvironmentProfile) -> float:
    """Compute effective first-order degradation rate (1/year)."""
    base_k = log(2.0) / material.base_half_life_years
    pressure = (
        (0.25 + material.uv_sensitivity) * env.uv
        + 0.25 * env.moisture
        + 0.15 * env.oxygen
        + (0.25 + material.microbe_affinity) * env.microbes
        + 0.20 * env.abrasion
    )
    return base_k * pressure * _temperature_factor(env.temperature_c)


def simulate_mass_curve(
    material: PlasticMaterial,
    env: EnvironmentProfile,
    config: SimulationConfig,
) -> pd.DataFrame:
    """Simulate plastic mass over time.

    Args:
        material: Polymer profile.
        env: Environmental condition profile.
        config: Numerical simulation setup.

    Returns:
        DataFrame with time in years and remaining mass in grams.
    """
    n = int(config.years * config.steps_per_year) + 1
    t = np.linspace(0.0, config.years, n)
    k = effective_rate_per_year(material, env)
    mass = config.initial_mass_g * np.exp(-k * t)
    return pd.DataFrame({"time_years": t, "mass_g": mass})


def remaining_fraction(df: pd.DataFrame, time_years: float) -> float:
    """Interpolate remaining mass fraction at a selected time."""
    mass = np.interp(time_years, df["time_years"].to_numpy(), df["mass_g"].to_numpy())
    return float(mass / df["mass_g"].iloc[0])
