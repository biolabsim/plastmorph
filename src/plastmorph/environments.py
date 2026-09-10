"""Environment catalog and tunable environmental pressure variables."""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class EnvironmentProfile:
    """Defines a degradation environment.

    All intensity fields except temperature are normalized in [0, 1].

    Attributes:
        key: Internal key.
        name: Display name.
        uv: Relative UV exposure.
        moisture: Relative water availability.
        oxygen: Relative oxygen availability.
        microbes: Relative microbial activity.
        abrasion: Relative mechanical abrasion.
        temperature_c: Ambient temperature in Celsius.
    """

    key: str
    name: str
    uv: float
    moisture: float
    oxygen: float
    microbes: float
    abrasion: float
    temperature_c: float


ENVIRONMENTS: dict[str, EnvironmentProfile] = {
    "temperate_forest": EnvironmentProfile(
        "temperate_forest", "Temperate forest", 0.45, 0.70, 0.75, 0.80, 0.30, 14.0),
    "landfill": EnvironmentProfile("landfill", "Landfill", 0.05, 0.40, 0.20, 0.35, 0.10, 20.0),
    "ocean": EnvironmentProfile("ocean", "Ocean", 0.65, 1.00, 0.85, 0.45, 0.70, 16.0),
    "organic_composting": EnvironmentProfile("organic_composting", "Organic composting", 0.20, 0.85, 0.70, 1.00, 0.25, 55.0),
    "desert": EnvironmentProfile("desert", "Desert", 1.00, 0.08, 0.85, 0.05, 0.55, 34.0),
    "household": EnvironmentProfile("household", "Household", 0.05, 0.2, 0.21, 0.01, 0.1, 20.0),
}


def with_overrides(base: EnvironmentProfile, **overrides: float) -> EnvironmentProfile:
    """Return a new environment profile with user-provided overrides."""
    return replace(base, **overrides)
