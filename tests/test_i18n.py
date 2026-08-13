"""Tests for translation catalog completeness and fallback behavior."""

from plastmorph.i18n import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES, missing_translation_keys, translate


def test_default_language_is_english() -> None:
    """English should remain the canonical development baseline language."""
    assert DEFAULT_LANGUAGE == "en"


def test_all_supported_languages_cover_english_keys() -> None:
    """Every non-English catalog should contain all keys defined in English."""
    missing_by_language = {
        lang: missing_translation_keys(lang)
        for lang in SUPPORTED_LANGUAGES
        if lang != DEFAULT_LANGUAGE
    }
    assert all(not missing for missing in missing_by_language.values())


def test_unknown_keys_are_marked_explicitly() -> None:
    """Unknown translation keys should be visible during development."""
    assert translate("missing.section.key", "de") == "[missing.section.key]"
