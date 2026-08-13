"""Streamlit front-end for the PlastMorph educational simulator."""

import matplotlib.pyplot as plt
import streamlit as st

from plastmorph.environments import ENVIRONMENTS, with_overrides
from plastmorph.i18n import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES, labels_for, translate
from plastmorph.materials import MATERIALS
from plastmorph.morphology import base_shape, degrade_shape
from plastmorph.simulation import SimulationConfig, remaining_fraction, simulate_mass_curve

if "lang" not in st.session_state:
    st.session_state.lang = DEFAULT_LANGUAGE

active_lang = st.session_state.lang

st.set_page_config(page_title=translate("app.title", active_lang), layout="wide")

selected_lang = st.selectbox(
    translate("language.label", active_lang),
    list(SUPPORTED_LANGUAGES),
    index=list(SUPPORTED_LANGUAGES).index(active_lang),
    format_func=lambda code: translate(f"language.{code}", active_lang),
    key="lang_selector",  # stable widget identity
)
if selected_lang != st.session_state.lang:
    st.session_state.lang = selected_lang
    st.rerun()

lang = st.session_state.lang

st.title(translate("app.title", lang))
st.caption(translate("app.caption", lang))

left, right = st.columns([1, 2])

with left:
    material_labels = labels_for("materials", lang)
    environment_labels = labels_for("environments", lang)

    material_code = st.selectbox(
        translate("sidebar.material_component", lang),
        list(MATERIALS.keys()),
        index=5,
        format_func=lambda code: f"{code} - {material_labels.get(code, code)}",
    )
    env_key = st.selectbox(
        translate("sidebar.environment", lang),
        list(ENVIRONMENTS.keys()),
        index=0,
        format_func=lambda key: environment_labels.get(key, key),
    )

    st.subheader(translate("sidebar.simulation_timeline", lang))
    years = st.slider(translate("controls.years", lang), min_value=1, max_value=200, value=40)
    # steps_per_year = st.slider(
    #     translate("controls.steps_per_year", lang), min_value=2, max_value=52, value=12
    # )
    initial_mass_g = st.slider(
        translate("controls.initial_mass_g", lang), min_value=10, max_value=2000, value=500
    )

    st.subheader(translate("sidebar.environment_tinkering", lang))
    base_env = ENVIRONMENTS[env_key]
    uv = st.slider(translate("controls.uv_exposure", lang), 0.0, 1.0, float(base_env.uv), 0.01)
    moisture = st.slider(translate("controls.moisture", lang), 0.0, 1.0, float(base_env.moisture), 0.01)
    oxygen = st.slider(translate("controls.oxygen", lang), 0.0, 1.0, float(base_env.oxygen), 0.01)
    microbes = st.slider(
        translate("controls.microbial_activity", lang), 0.0, 1.0, float(base_env.microbes), 0.01
    )
    abrasion = st.slider(
        translate("controls.mechanical_abrasion", lang), 0.0, 1.0, float(base_env.abrasion), 0.01
    )
    temperature_c = st.slider(
        translate("controls.temperature_c", lang), -10.0, 80.0, float(base_env.temperature_c), 0.5
    )

material = MATERIALS[material_code]
custom_env = with_overrides(
    base_env,
    uv=uv,
    moisture=moisture,
    oxygen=oxygen,
    microbes=microbes,
    abrasion=abrasion,
    temperature_c=temperature_c,
)
config = SimulationConfig(years=years, steps_per_year=12, initial_mass_g=initial_mass_g)
curve = simulate_mass_curve(material, custom_env, config)

with right:
    st.subheader(translate("plots.mass_over_time", lang))
    st.line_chart(curve, x="time_years", y="mass_g", width='stretch')

    checkpoints = [0.0, years * 0.25, years * 0.5, years]
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.5))
    base = base_shape(material.icon_shape)

    for ax, time_point in zip(axes, checkpoints, strict=True):
        frac = remaining_fraction(curve, time_point)
        mask = degrade_shape(base, frac, seed=int(time_point * 13) + 7)
        ax.imshow(mask, cmap="viridis", vmin=0, vmax=1)
        ax.set_title(
            translate(
                "plots.snapshot_title",
                lang,
                years=time_point,
                year_unit=translate("units.year_short", lang),
                percent=frac * 100,
                mass_label=translate("units.mass_label", lang),
            )
        )
        ax.axis("off")

    st.subheader(translate("plots.morphology_over_time", lang))
    st.pyplot(fig, width='stretch')
