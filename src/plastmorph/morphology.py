"""Iconographic morphology generation for degraded plastic shapes."""

import numpy as np


def _grid(size: int) -> tuple[np.ndarray, np.ndarray]:
    x = np.linspace(-1.0, 1.0, size)
    y = np.linspace(-1.0, 1.0, size)
    return np.meshgrid(x, y)


def base_shape(shape: str, size: int = 96) -> np.ndarray:
    """Create a binary mask for a symbolic plastic object shape."""
    xx, yy = _grid(size)

    if shape == "bottle":
        body = (np.abs(xx) < 0.25) & (yy > -0.75) & (yy < 0.6)
        neck = (np.abs(xx) < 0.12) & (yy >= 0.6) & (yy < 0.9)
        cap = (np.abs(xx) < 0.16) & (yy >= 0.9)
        return body | neck | cap
    if shape == "bag":
        return (np.abs(xx) < 0.55) & (yy > -0.7) & (yy < 0.7)
    if shape == "pipe":
        outer = (xx * xx + yy * yy) < 0.78
        inner = (xx * xx + yy * yy) < 0.40
        return outer & ~inner
    if shape == "foam":
        return (np.abs(xx) < 0.6) & (np.abs(yy) < 0.45)
    if shape == "cap":
        return (xx * xx + yy * yy) < 0.55
    if shape == "cup":
        outer = (np.abs(xx) < (0.15 + 0.55 * (yy + 1) / 2)) & (yy > -0.75) & (yy < 0.8)
        inner = (np.abs(xx) < (0.08 + 0.40 * (yy + 1) / 2)) & (yy > -0.62) & (yy < 0.72)
        return outer & ~inner
    if shape == "fork":
        handle = (np.abs(xx) < 0.10) & (yy > -0.8) & (yy < 0.25)
        prongs = np.zeros_like(handle)
        for center in (-0.22, -0.07, 0.07, 0.22):
            prongs |= (np.abs(xx - center) < 0.04) & (yy >= 0.25) & (yy < 0.85)
        return handle | prongs

    return (xx * xx + yy * yy) < 0.6


def degrade_shape(mask: np.ndarray, remaining_fraction: float, seed: int = 42) -> np.ndarray:
    """Stochastically remove boundary pixels to mimic progressive fragmentation."""
    rng = np.random.default_rng(seed)
    degraded = mask.copy()
    target_pixels = int(mask.sum() * float(np.clip(remaining_fraction, 0.0, 1.0)))

    if target_pixels <= 0:
        return np.zeros_like(mask)

    # Iteratively peel border pixels until the requested mass proxy is reached.
    while int(degraded.sum()) > target_pixels:
        neighbors = (
            np.roll(degraded, 1, axis=0)
            & np.roll(degraded, -1, axis=0)
            & np.roll(degraded, 1, axis=1)
            & np.roll(degraded, -1, axis=1)
        )
        border = degraded & ~neighbors
        border_idx = np.argwhere(border)
        if len(border_idx) == 0:
            break

        current = int(degraded.sum())
        removable = max(1, min(current - target_pixels, len(border_idx)))
        chosen = border_idx[rng.choice(len(border_idx), size=removable, replace=False)]
        degraded[chosen[:, 0], chosen[:, 1]] = False

    return degraded
