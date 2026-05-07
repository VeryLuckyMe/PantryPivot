# ── Pantry Management Logic ─────────────────────────────────────────────────
# Handles adding, removing, and querying pantry items in session state.

import streamlit as st
import time
import json
import os
import uuid

PANTRY_FILE = "pantry.json"

def load_pantry():
    """Load pantry from JSON file or return empty list."""
    if os.path.exists(PANTRY_FILE):
        try:
            with open(PANTRY_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_pantry(pantry_data):
    """Save pantry state to JSON file."""
    with open(PANTRY_FILE, "w") as f:
        json.dump(pantry_data, f, indent=2)

def add_pantry_item(name, qty=1, unit="pieces", expiry=7):
    """Add an item to the pantry in session state and save."""
    st.session_state.pantry.append({
        "name": name, "qty": qty, "unit": unit, "expiry": expiry,
        "id": uuid.uuid4().hex
    })
    save_pantry(st.session_state.pantry)
