import streamlit as st
from src.core.pantry import save_pantry
from typing import List
from pydantic import BaseModel, Field

class PantryItemToRemove(BaseModel):
    name: str = Field(description="The name of the ingredient to remove, e.g., 'Eggs'")
    qty: float = Field(description="The quantity of the ingredient to subtract")

def deduct_pantry_items(items_to_remove: list[PantryItemToRemove]) -> str:
    """
    Subtracts ingredients from the user's pantry.
    """
    if "pantry" not in st.session_state:
        return "Error: Pantry not found."

    removed_log = []
    not_found_log = []

    # Process each requested deduction
    for target in items_to_remove:
        target_name = target.name.lower().strip()
        target_qty = target.qty
        
        found = False
        # Create a copy to iterate safely
        pantry_copy = list(st.session_state.pantry)
        for item in pantry_copy:
            if item["name"].lower().strip() == target_name:
                found = True
                if item["qty"] > target_qty:
                    item["qty"] -= target_qty
                    removed_log.append(f"Reduced {item['name']} by {target_qty}")
                    target_qty = 0
                    break # Fully deducted
                else:
                    # Deduct what we can from this entry and keep looking
                    deducted = item["qty"]
                    removed_log.append(f"Removed {deducted} of {item['name']} from pantry")
                    st.session_state.pantry.remove(item)
                    target_qty -= deducted
                    
                    if target_qty <= 0:
                        break # Fully deducted
        
        if not found:
            not_found_log.append(f"Could not find {target.name}")

    save_pantry(st.session_state.pantry)
    
    response = "Pantry Update Processed.\n"
    if removed_log:
        response += "- " + "\n- ".join(removed_log) + "\n"
    if not_found_log:
        response += "Note: " + ", ".join(not_found_log)
        
    return response
