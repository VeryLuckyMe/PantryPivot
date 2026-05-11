# ── PantryPivot — Main Entry Point ──────────────────────────────────────────
# A production-ready AI chatbot for zero-waste kitchen management.
# Architecture: RAG + Enhanced Prompt Defenses
#
# Project Structure:
#   src/core/rag.py          → Retrieval-Augmented Generation pipeline
#   src/core/recipe.py       → AI recipe generation & meal planning
#   src/core/pantry.py       → Pantry inventory management
#   src/security/defenses.py → Prompt injection detection & output filtering
#   src/ui/styles.py         → CSS & font injection
#   src/ui/sidebar.py        → Sidebar navigation
#   src/ui/pages.py          → Dashboard, Pantry, Recipes, Meal Planner pages

import streamlit as st

from src.ui.styles import inject_custom_css
from src.ui.sidebar import render_sidebar
from src.ui.pages import page_home, page_pantry, page_recipes, page_mealplan
from src.core.pantry import load_pantry

# ── Page Config (MUST be first Streamlit command) ────────────────────────────
st.set_page_config(
    page_title="PantryPivot",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject Custom CSS ────────────────────────────────────────────────────────
inject_custom_css()

# ── Session State Defaults ──────────────────────────────────────────────────
_defaults = {
    "page": "home",
    "pantry": load_pantry(),
    "messages": [],
    "recipes": [],
    "waste_log": [],
    "meal_plan": {},
    "stats": {"money": 0.0, "meals": 0},
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if "recipe_settings" not in st.session_state:
    st.session_state.recipe_settings = {
        "mode": "Flexible",
        "meal_type": "None",
        "cuisine": "",
        "difficulty": "Balanced (30-45 min)",
        "model": "gemini-2.5-flash",
    }
if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = None


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    """Application entry point — calculates metrics and routes to the active page."""
    # ── URL Navigation Sync ──
    if "nav" in st.query_params:
        requested_page = st.query_params["nav"]
        if requested_page in ["home", "pantry", "recipes", "mealplan"]:
            if st.session_state.page != requested_page:
                st.session_state.page = requested_page
                # Clear query param to avoid sticky state
                st.query_params.clear()
                st.rerun()

    # Pre-calculate common metrics
    pantry_count = len(st.session_state.pantry)
    meals_rescued = st.session_state.stats["meals"]
    expiring_count = len([i for i in st.session_state.pantry if i["expiry"] <= 3])
    waste_count = len(st.session_state.waste_log)

    # Kitchen freshness score
    if pantry_count == 0:
        fresh_percent = 100
    else:
        fresh_percent = int(100 - (expiring_count / pantry_count * 100))

    render_sidebar(fresh_percent)

    # Page routing
    pg = st.session_state.page
    if pg == "home":
        page_home(pantry_count, meals_rescued, expiring_count, waste_count, fresh_percent)
    elif pg == "pantry":
        page_pantry()
    elif pg == "recipes":
        page_recipes()
    elif pg == "mealplan":
        page_mealplan()


if __name__ == "__main__":
    main()