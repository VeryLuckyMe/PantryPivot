# ── Pantry Management Logic ─────────────────────────────────────────────────
# Handles adding, removing, and querying pantry items in session state.

import streamlit as st
import time


def add_pantry_item(name, qty=1, unit="pieces", expiry=7):
    """Add an item to the pantry in session state."""
    st.session_state.pantry.append({
        "name": name, "qty": qty, "unit": unit, "expiry": expiry,
        "id": time.time()
    })
