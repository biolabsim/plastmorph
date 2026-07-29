# PlastMorph

PlastMorph is an educational Streamlit app that simulates how different plastics degrade in different environments over time.

## Features

- Plastic types: PE, PVC, PU, PP, PS, PET, PLA
- Environments: temperate forest, landfill, ocean, organic composting, desert
- Adjustable environmental variables (UV, moisture, oxygen, microbes, abrasion, temperature)
- Time-series plot of remaining plastic mass
- Iconographic shape-morph view that degrades over time

## Quick Start

```bash
make dev
make run
```

## Installation (from GitHub)

Replace `<your-org>/<your-repo>` with your GitHub repository path.

### 1. Clone the repository

```bash
git clone https://github.com/Biotaix/plastmorph.git
cd <your-repo>
```

### 2A. Install with virtual environment (.venv)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

For development tooling (lint, tests, docs):

```bash
python -m pip install -e ".[dev]"
```

Run the app:

```bash
streamlit run app/streamlit_app.py
```

Leave the environment:

```bash
deactivate
```

### 2B. Install with conda

```bash
conda create -n plastmorph python=3.13 -y
conda activate plastmorph
python -m pip install --upgrade pip
python -m pip install -e .
```

For development tooling (lint, tests, docs):

```bash
python -m pip install -e ".[dev]"
```

Run the app:

```bash
streamlit run app/streamlit_app.py
```

Deactivate conda env:

```bash
conda deactivate
```

## Developer Commands

```bash
make lint
make test
make docs
make i18n-check
```

## Documentation

Build docs with:

```bash
make docs
```

Then open the generated site in `site/`.

## Localization (English/German)

The app uses English as the canonical source language and supports runtime switching to German.

### Core Rules

- Add new user-facing text only through translation keys.
- Keep internal IDs and logic in English (for example material codes and environment keys).
- Update English first, then add German for the same keys.

### Translation Files

- English catalog: `src/plastmorph/locales/en.toml`
- German catalog: `src/plastmorph/locales/de.toml`
- Translation helper: `src/plastmorph/i18n.py`

### How To Add A New UI String

1. Add a key to `src/plastmorph/locales/en.toml`.
2. Add the same key to `src/plastmorph/locales/de.toml`.
3. Use `t("your.section.key", lang)` in app code.
4. Run `make i18n-check` to ensure key completeness.

Example:

```toml
# en.toml
[lesson]
new_metric = "Microplastic index"

# de.toml
[lesson]
new_metric = "Mikroplastik-Index"
```

```python
st.subheader(t("lesson.new_metric", lang))
```

### How To Add A New Simulation Function With en/de Support

When adding a new model function, keep the function language-neutral and localize only display text.

1. Add the function in `src/plastmorph/simulation.py` with a clear English docstring.
2. Add tests for the function in `tests/`.
3. If the function introduces new labels, metrics, or explanations in Streamlit:
	- Add keys in `en.toml` first.
	- Mirror keys in `de.toml`.
	- Render them through `t(...)`.
4. Validate quality:

```bash
make lint
make test
make i18n-check
```

### Fallback Behavior

- Missing key in selected language falls back to English.
- Missing key in all languages is shown as `[section.key]` so gaps are obvious during development.
