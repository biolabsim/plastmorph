"""Tests for degradation mass simulation behavior."""

import numpy as np

from plastmorph.environments import ENVIRONMENTS
from plastmorph.materials import MATERIALS
from plastmorph.simulation import SimulationConfig, simulate_mass_curve


def test_mass_curve_is_non_increasing() -> None:
    """Mass should only decrease or stay constant over time."""
    cfg = SimulationConfig(years=20, steps_per_year=12, initial_mass_g=100)
    df = simulate_mass_curve(MATERIALS["PET"], ENVIRONMENTS["ocean"], cfg)
    diffs = np.diff(df["mass_g"].to_numpy())
    assert np.all(diffs <= 1e-12)


def test_pla_degrades_faster_in_compost_than_landfill() -> None:
    """PLA should degrade faster in composting than in landfill conditions."""
    cfg = SimulationConfig(years=2, steps_per_year=12, initial_mass_g=100)
    compost = simulate_mass_curve(MATERIALS["PLA"], ENVIRONMENTS["organic_composting"], cfg)
    landfill = simulate_mass_curve(MATERIALS["PLA"], ENVIRONMENTS["landfill"], cfg)
    assert compost["mass_g"].iloc[-1] < landfill["mass_g"].iloc[-1]


def test_mass_never_exceeds_initial_mass() -> None:
    """Computed mass should never rise above the initialized mass."""
    cfg = SimulationConfig(years=60, steps_per_year=24, initial_mass_g=300)
    df = simulate_mass_curve(MATERIALS["PP"], ENVIRONMENTS["desert"], cfg)
    assert float(df["mass_g"].max()) <= cfg.initial_mass_g
