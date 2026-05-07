# ── Custom CSS & Resource Injection ─────────────────────────────────────────
# Loads style.css, Google Fonts, Material Icons, and Tailwind CSS.

import streamlit as st


@st.cache_data
def get_custom_resources():
    """Load and cache custom CSS and font/icon resources."""
    try:
        with open("style.css", "r", encoding="utf-8") as f:
            css_content = f.read()
    except FileNotFoundError:
        css_content = ""

    return (
        f'<style>{css_content}</style>'
        '<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>'
        '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>'
        '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>'
    )


def inject_custom_css():
    """Inject custom CSS and resources into the Streamlit app."""
    st.markdown(get_custom_resources(), unsafe_allow_html=True)
