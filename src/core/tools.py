import streamlit as st
import time
from src.core.pantry import save_pantry

def deduct_pantry_items(items_to_remove: list[dict]) -> str:
    """
    Deducts the specified items from the user's pantry.
    Expected items_to_remove format: [{'name': 'Eggs', 'qty': 2}]
    """
    if "pantry" not in st.session_state:
        return "Error: Pantry not found."

    removed_log = []
    not_found_log = []

    # Process each requested deduction
    for target in items_to_remove:
        target_name = target.get("name", "").lower().strip()
        target_qty = target.get("qty", 1)
        
        found = False
        for item in st.session_state.pantry:
            if item["name"].lower().strip() == target_name:
                found = True
                if item["qty"] > target_qty:
                    item["qty"] -= target_qty
                    removed_log.append(f"Reduced {target['name']} by {target_qty}")
                else:
                    removed_log.append(f"Removed all {target['name']} from pantry")
                    st.session_state.pantry.remove(item)
                break
        
        if not found:
            not_found_log.append(f"Could not find {target['name']} in pantry")

    save_pantry(st.session_state.pantry)
    
    response = "Pantry Update Complete.\n"
    if removed_log:
        response += "- " + "\n- ".join(removed_log) + "\n"
    if not_found_log:
        response += "Note: " + ", ".join(not_found_log)
        
    return response

# Gemini Tool Definition
pantry_update_tool = {
    "function_declarations": [
        {
            "name": "deduct_pantry_items",
            "description": "Subtracts or removes ingredients from the user's pantry. Use this ONLY when the user explicitly confirms they have cooked a recipe or consumed items.",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "items_to_remove": {
                        "type_": "ARRAY",
                        "description": "A list of items to deduct from the pantry.",
                        "items": {
                            "type_": "OBJECT",
                            "properties": {
                                "name": {"type_": "STRING", "description": "The name of the ingredient"},
                                "qty": {"type_": "NUMBER", "description": "The quantity to subtract"}
                            },
                            "required": ["name", "qty"]
                        }
                    }
                },
                "required": ["items_to_remove"]
            }
        }
    ]
}
