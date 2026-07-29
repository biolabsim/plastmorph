"""Localization helpers for English-first, key-based translation catalogs."""

import tomllib
from functools import cache
from importlib.resources import files

DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ("en", "de")


@cache
def _load_catalog(language: str) -> dict:
    """Load and cache a translation catalog from TOML resources."""
    normalized = language if language in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
    catalog_text = files("plastmorph.locales").joinpath(f"{normalized}.toml").read_text(
        encoding="utf-8"
    )
    return tomllib.loads(catalog_text)


def _lookup(data: dict, key: str) -> str | None:
    """Resolve dot-separated keys in nested dictionaries."""
    current: dict | str = data
    for part in key.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current if isinstance(current, str) else None


def _flatten(data: dict, prefix: str = "") -> set[str]:
    """Flatten nested dictionaries into dot-separated key names."""
    flat: set[str] = set()
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat |= _flatten(value, full_key)
        else:
            flat.add(full_key)
    return flat


def t(key: str, language: str = DEFAULT_LANGUAGE, **kwargs: str | float) -> str:
    """Translate a key with English fallback and optional formatting."""
    value = _lookup(_load_catalog(language), key)
    if value is None:
        value = _lookup(_load_catalog(DEFAULT_LANGUAGE), key)
    if value is None:
        return f"[{key}]"
    return value.format(**kwargs) if kwargs else value


def labels_for(section: str, language: str = DEFAULT_LANGUAGE) -> dict[str, str]:
    """Return merged section labels with localized values overriding English defaults."""
    en_section = _load_catalog(DEFAULT_LANGUAGE).get(section, {})
    target_section = _load_catalog(language).get(section, {})
    if not isinstance(en_section, dict):
        en_section = {}
    if not isinstance(target_section, dict):
        target_section = {}
    merged = {**en_section, **target_section}
    return {str(k): str(v) for k, v in merged.items()}


def missing_translation_keys(language: str) -> list[str]:
    """List keys that are present in English but missing in the target language."""
    if language == DEFAULT_LANGUAGE:
        return []
    baseline = _flatten(_load_catalog(DEFAULT_LANGUAGE))
    target = _flatten(_load_catalog(language))
    return sorted(baseline - target)
