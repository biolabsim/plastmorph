"""Material catalog and material-specific degradation modifiers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PlasticMaterial:
    """Describes a plastic type and its degradation behavior profile.

    Attributes:
        code: Short polymer code.
        name: Human-readable name.
        icon_shape: Shape family used for iconographic rendering.
        base_half_life_years: Reference half-life in a neutral environment.
        microbe_affinity: Boost to microbial degradation susceptibility.
        uv_sensitivity: Boost to UV-driven degradation susceptibility.
    """

    code: str
    name: str
    icon_shape: str
    base_half_life_years: float
    microbe_affinity: float
    uv_sensitivity: float


MATERIALS: dict[str, PlasticMaterial] = {
    "PE": PlasticMaterial("PE", "Polyethylene", "bag", 180.0, 0.10, 0.50),
    "PVC": PlasticMaterial("PVC", "Polyvinyl Chloride", "pipe", 250.0, 0.05, 0.30),
    "PU": PlasticMaterial("PU", "Polyurethane", "foam", 90.0, 0.30, 0.40),
    "PP": PlasticMaterial("PP", "Polypropylene", "cap", 160.0, 0.10, 0.45),
    "PS": PlasticMaterial("PS", "Polystyrene", "cup", 140.0, 0.10, 0.35),
    "PET": PlasticMaterial("PET", "Polyethylene Terephthalate", "bottle", 120.0, 0.12, 0.55),
    "PLA": PlasticMaterial("PLA", "Polylactic Acid", "fork", 6.0, 0.95, 0.40),
}
