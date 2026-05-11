# ── Page Renderers ──────────────────────────────────────────────────────────
# Each function renders one full page of the PantryPivot application.

import streamlit as st
import uuid
import os

from src.core.pantry import add_pantry_item, save_pantry
from src.core.recipe import generate_recipe, generate_meal_plan
from src.core.rag import setup_rag


# ── HOME / DASHBOARD ────────────────────────────────────────────────────────
def page_home(pantry_count, meals_rescued, expiring_count, waste_count, fresh_percent):
    """Render the main dashboard page."""
    # Top Nav & Header
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 48px;">
        <div class="top-nav" style="margin-bottom:0; border:none; padding:0;">
            <span class="active">OVERVIEW</span>
            <span>ANALYTICS</span>
            <span>COMMUNITY</span>
        </div>
        <div>
           <input type="text" placeholder="🔍 Search pantry..." style="background:rgba(255,255,255,0.05); border:none; padding:8px 16px; border-radius:99px; color:white; width:220px; font-size:0.8rem;"/>
        </div>
    </div>

    <div class="hero-header">
      <h1>Good Morning,<br>Chef.</h1>
      <p>Your kitchen is currently <span>{fresh_percent}% Fresh</span>. You have {expiring_count} items that need<br>immediate attention to maintain peak sustainability.</p>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    st.markdown(f"""
    <div class="scorecard-grid">
      <div class="score-card">
        <span class="material-symbols-outlined icon">inventory_2</span>
        <div class="title">PANTRY ITEMS</div>
        <div class="value">{pantry_count}</div>
        <div class="sub"><span class="material-symbols-outlined" style="font-size:14px;color:var(--accent-blue)">trending_up</span> <span style="color:var(--accent-blue)">Updated now</span></div>
      </div>
      <div class="score-card">
        <span class="material-symbols-outlined icon">restaurant</span>
        <div class="title">MEALS RESCUED</div>
        <div class="value">{meals_rescued}</div>
        <div class="sub"><span class="material-symbols-outlined" style="font-size:14px">eco</span> CO2 rescue mode</div>
      </div>
      <div class="score-card {'alert' if expiring_count > 0 else ''}">
        <span class="material-symbols-outlined icon">timer</span>
        <div class="title">EXPIRING SOON</div>
        <div class="value {'red' if expiring_count > 0 else ''}">{expiring_count}</div>
        <div class="sub {'red' if expiring_count > 0 else ''}"><span class="material-symbols-outlined" style="font-size:14px">warning</span> {'Action required' if expiring_count > 0 else 'All stable'}</div>
      </div>
      <div class="score-card">
        <span class="material-symbols-outlined icon">delete</span>
        <div class="title">WASTE LOGGED</div>
        <div class="value">{waste_count}</div>
        <div class="sub">Log daily for accuracy</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Lower Section
    left, right = st.columns([1.1, 1])

    with left:
        st.markdown('<div class="section-title">Navigation Hub</div>', unsafe_allow_html=True)
        
        # We use a container to stack the HTML card and a transparent button hitbox
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown(f"""
            <div class="card-hitbox-container">
                <div class="hub-card-large">
                    <div>
                        <h3>Recipe<br>Assistant</h3>
                        <p>AI-crafted dishes based on<br>your inventory.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(" ", key="hitbox_recipes", use_container_width=True):
                st.session_state.page = "recipes"
                st.rerun()
                
        with c2:
            # Your Pantry Card
            st.markdown(f"""
            <div class="card-hitbox-container">
                <div class="hub-card-small">
                    <span class="material-symbols-outlined icon">inventory_2</span>
                    <h4>Your Pantry</h4>
                    <p>{pantry_count} ACTIVE INGREDIENTS</p>
                    <span class="material-symbols-outlined arrow">arrow_forward</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(" ", key="hitbox_pantry", use_container_width=True):
                st.session_state.page = "pantry"
                st.rerun()
            
            st.markdown('<div style="margin-top:16px;"></div>', unsafe_allow_html=True)
            
            # Meal Plan Card
            st.markdown(f"""
            <div class="card-hitbox-container">
                <div class="hub-card-small">
                    <span class="material-symbols-outlined icon">calendar_month</span>
                    <h4>Meal Plan</h4>
                    <p>NEXT: VIEW PLAN</p>
                    <span class="material-symbols-outlined arrow">arrow_forward</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(" ", key="hitbox_mealplan", use_container_width=True):
                st.session_state.page = "mealplan"
                st.rerun()

    with right:
        st.markdown("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
          <div class="section-title" style="margin-bottom:0;">Use These First</div>
          <a href="#" style="color:white; font-size:0.75rem; font-weight:700; text-decoration:none; letter-spacing:0.05em;">VIEW ALL</a>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="utf-list">
        """, unsafe_allow_html=True)

        expiring = sorted([i for i in st.session_state.pantry if i["expiry"] <= 7], key=lambda x: x["expiry"])
        if expiring:
            for item in expiring[:3]:
                icon = "nutrition" if "Veg" in item["name"] or "Spinach" in item["name"] else "water_drop" if "Milk" in item["name"] else "egg_alt"
                bg = "#166534" if icon == "nutrition" else "#e0f2fe" if icon == "water_drop" else "#fef3c7"
                color = "#4ade80" if icon == "nutrition" else "#38bdf8" if icon == "water_drop" else "#f59e0b"
                badge = "critical" if item["expiry"] <= 3 else "warning"

                st.markdown(f"""
                <div class="utf-item">
                    <div class="utf-left">
                    <div class="utf-icon" style="background:{bg};"><span class="material-symbols-outlined" style="color:{color}">{icon}</span></div>
                    <div class="utf-info">
                        <h4>{item["name"]}</h4>
                        <p><span class="{'red' if badge == 'critical' else ''}">{item['expiry']} DAYS LEFT</span> • {item['qty']} {item['unit']}</p>
                    </div>
                    </div>
                    <div class="badge {badge}">{badge.upper()}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:var(--text-muted); font-size:0.85rem; padding:20px;">No items expiring soon! 🥗</p>', unsafe_allow_html=True)

        st.markdown("""
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="btn-rescue">', unsafe_allow_html=True)
        if st.button("GENERATE RESCUE RECIPE", use_container_width=True):
            if expiring:
                name = expiring[0]["name"]
                st.session_state.messages.append({"role": "user", "content": f"Generate a recipe using my expiring {name}."})
            else:
                st.session_state.messages.append({"role": "user", "content": "Generate a surprise recipe from my pantry."})
            st.session_state.page = "recipes"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ── PANTRY / INVENTORY ──────────────────────────────────────────────────────
def page_pantry():
    """Render the pantry inventory management page."""
    st.markdown("""
    <div class="pp-topbar">
      <div><h1 style="font-size:3rem; margin:0; letter-spacing:-0.03em;">Inventory</h1><p style="color:#94a3b8; font-size:1.1rem;">Manage your ingredients</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚡ Quick Add", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:0.9rem; margin-top:-10px; margin-bottom:20px;'>Click any ingredient to instantly add it to your pantry.</p>", unsafe_allow_html=True)

    quick_items = [
        ("Eggs", "🥚", 14), ("Rice", "🍚", 90), ("Pasta", "🍝", 365), ("Bread", "🍞", 5), ("Onion", "🧅", 14),
        ("Garlic", "🧄", 30), ("Tomatoes", "🍅", 7), ("Carrots", "🥕", 14), ("Spinach", "🥬", 4), ("Cheese", "🧀", 14),
        ("Milk", "🥛", 7), ("Chicken", "🍗", 3), ("Beef", "🥩", 3), ("Beans", "🫘", 365), ("Broccoli", "🥦", 5),
        ("Potatoes", "🥔", 30), ("Butter", "🧈", 30), ("Yogurt", "🥛", 14), ("Corn", "🌽", 5), ("Lemon", "🍋", 14)
    ]

    # Render in a responsive grid container
    st.markdown('<div class="quick-add-grid">', unsafe_allow_html=True)
    for i in range(0, len(quick_items), 5):
        cols = st.columns(5)
        for j in range(5):
            idx = i + j
            if idx < len(quick_items):
                n, e, exp = quick_items[idx]
                with cols[j]:
                    if st.button(f"{e} {n}", key=f"q_{n}", use_container_width=True):
                        add_pantry_item(n, 1, "pack", exp)
                        save_pantry(st.session_state.pantry)
                        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><hr style='border-color:rgba(255,255,255,0.05)'><br>", unsafe_allow_html=True)
    left, right = st.columns([2, 1])
    with left:
        st.markdown("### 📦 Current Stock")
        if not st.session_state.pantry:
            st.info("Pantry empty.")
        for item in sorted(st.session_state.pantry, key=lambda x: x["expiry"]):
            badge_cls = "critical" if item["expiry"] <= 3 else "warning" if item["expiry"] <= 7 else "stable"
            with st.container():
                st.markdown(f'<div class="pp-card" style="margin-bottom:12px; display:flex; justify-content:space-between; align-items:center;"><span><strong>{item["name"]}</strong><br><span style="font-size:0.8rem;color:#94a3b8;">{item["qty"]} {item["unit"]}</span></span><span class="pp-badge {badge_cls}">{item["expiry"]} days</span></div>', unsafe_allow_html=True)
                if st.button(f"🗑️ Delete", key=f"del_{item['id']}"):
                    st.session_state.pantry = [i for i in st.session_state.pantry if i["id"] != item["id"]]
                    save_pantry(st.session_state.pantry)
                    st.rerun()

    with right:
        st.markdown('<div class="pp-glass">', unsafe_allow_html=True)
        st.markdown("### ✍️ Manual Entry")
        with st.form("add_form", clear_on_submit=True):
            name = st.text_input("Name")
            cols2 = st.columns(2)
            qty = cols2[0].number_input("Qty", min_value=1)
            unit = cols2[1].selectbox("Unit", ["pieces", "grams", "ml", "pack"])
            expiry = st.number_input("Expiry (days)", value=7)
            if st.form_submit_button("Add to Pantry"):
                if name:
                    add_pantry_item(name, qty, unit, expiry=expiry)
                    save_pantry(st.session_state.pantry)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ── RECIPE ASSISTANT ────────────────────────────────────────────────────────
def page_recipes():
    """Render the AI recipe assistant page."""
    st.markdown("""
    <div class="pp-topbar">
      <div><h1 style="font-size:3rem; margin:0; letter-spacing:-0.03em;">Recipe Assistant</h1><p style="color:#94a3b8; font-size:1.1rem;">AI-powered culinary inspiration</p></div>
    </div>
    """, unsafe_allow_html=True)

    # ✅ RAG STATUS
    rag_result = setup_rag()
    retriever = rag_result.get("retriever")
    error = rag_result.get("error")

    if retriever:
        st.success("📚 Knowledge Base Loaded & Active")
    else:
        st.error(f"⚙️ RAG Error: {error if error else 'Unknown initialization error'}")

    # ── Recipe Settings ──
    with st.expander("⚙️ Recipe Settings", expanded=True):
        st.markdown('<div class="pp-glass" style="padding:20px;">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.session_state.recipe_settings["mode"] = st.radio("Mode", ["Strict Mode", "Flexible Mode"],
                                                                index=0 if st.session_state.recipe_settings["mode"] == "Strict Mode" else 1,
                                                                horizontal=True, help="Strict uses ONLY your pantry.")
            st.session_state.recipe_settings["cuisine"] = st.text_input("Cuisine Pivot (optional)",
                                                                        value=st.session_state.recipe_settings["cuisine"],
                                                                        placeholder="e.g. Mexican, Italian, Thai...")
        with col2:
            st.session_state.recipe_settings["meal_type"] = st.selectbox("Meal Type", ["None", "Breakfast", "Lunch", "Dinner", "Snack"],
                                                                         index=["None", "Breakfast", "Lunch", "Dinner", "Snack"].index(st.session_state.recipe_settings["meal_type"]))
            st.session_state.recipe_settings["difficulty"] = st.selectbox("Difficulty", ["Fast (< 15 min)", "Balanced (30-45 min)", "Project (> 1h)"],
                                                                          index=["Fast (< 15 min)", "Balanced (30-45 min)", "Project (> 1h)"].index(st.session_state.recipe_settings["difficulty"]))
            model_options = {
                "Gemini 2.5 Flash (Recommended)": "gemini-2.5-flash",
                "Gemini 2.5 Pro (Smartest)": "gemini-2.5-pro",
                "Gemini 2.0 Flash": "gemini-2.0-flash",
                "Gemini 2.0 Flash-Lite (Fastest)": "gemini-2.0-flash-lite",
                "Gemini 2.5 Flash-Lite": "gemini-2.5-flash-lite",
            }
            labels = list(model_options.keys())
            values = list(model_options.values())
            current_model = st.session_state.recipe_settings["model"]
            default_idx = values.index(current_model) if current_model in values else 0
            
            selected_label = st.selectbox("AI Model (Free Tier)", labels, index=default_idx, help="Switch to 'Pro' for high-quality logic.")
            st.session_state.recipe_settings["model"] = model_options[selected_label]
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Quick Actions ──
    st.markdown("### ⚡ Quick Actions", unsafe_allow_html=True)
    q_cols = st.columns(6)
    actions = [
        ("Breakfast idea", "🌅"), ("Healthy lunch", "🥗"), ("Dinner tonight", "🍽️"),
        ("15-minute meal", "⏱️"), ("Use expiring items", "🌿"), ("Comfort food", "🍜")
    ]

    for i, (label, emoji) in enumerate(actions):
        with q_cols[i]:
            if st.button(f"{emoji} {label}", key=f"qa_{label}", use_container_width=True):
                generate_recipe(f"Give me a {label.lower()}")
                st.rerun()

    st.markdown('<div class="pp-recipe-chat" style="margin-top:30px;">', unsafe_allow_html=True)
    if not st.session_state.messages:
        ingredients = ", ".join([i["name"] for i in st.session_state.pantry])
        st.info(f"Available ingredients: **{ingredients if ingredients else 'None'}**")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    if getattr(st.session_state, "pending_tool_call", None):
        st.warning("🤖 **AI Kitchen Manager:** I have prepared a pantry update for you.")
        args = st.session_state.pending_tool_call
        items = args.get("items_to_remove", [])
        for item in items:
            st.write(f"- Deduct **{item['qty']}** x **{item['name']}**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm Deduction", use_container_width=True):
                from src.core.tools import deduct_pantry_items
                result = deduct_pantry_items(items)
                st.session_state.messages.append({"role": "assistant", "content": result})
                st.session_state.pending_tool_call = None
                st.rerun()
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.messages.append({"role": "assistant", "content": "Pantry update cancelled."})
                st.session_state.pending_tool_call = None
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    prompt = st.chat_input("Ask for a recipe e.g. 'Make a fast dinner out of my expiring items'")
    if prompt:
        generate_recipe(prompt)
        st.rerun()


# ── MEAL PLANNER ────────────────────────────────────────────────────────────
def page_mealplan():
    """Render the weekly meal planner page."""
    st.markdown("""
    <div class="pp-topbar">
      <div><h1 style="font-size:3rem; margin:0; letter-spacing:-0.03em;">Meal Planner</h1><p style="color:#94a3b8; font-size:1.1rem;">Zero-waste weekly planning</p></div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([3, 1])
    with left:
        st.markdown('<div class="pp-card">', unsafe_allow_html=True)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        cols = st.columns(7)
        for i, (day, col) in enumerate(zip(days, cols)):
            with col:
                st.markdown(f'<div class="pp-day-col"><h4>{day}</h4>', unsafe_allow_html=True)
                for meal in ["Breakfast", "Lunch", "Dinner"]:
                    meal_text = "AI Target"
                    if st.session_state.meal_plan and day in st.session_state.meal_plan.get("plan", {}):
                        meal_text = st.session_state.meal_plan["plan"][day].get(meal, "AI Target")
                    st.markdown(f'<div class="pp-meal-slot"><strong>{meal}</strong><br><span style="font-size:0.65rem;font-style:italic">{meal_text}</span></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✨ Generate AI Weekly Plan"):
            with st.spinner("AI Cooking up a plan..."):
                generate_meal_plan()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="pp-glass">', unsafe_allow_html=True)
        st.markdown("### 🛒 Smart Shopping")
        if st.session_state.meal_plan and "shopping_list" in st.session_state.meal_plan:
            for item in st.session_state.meal_plan["shopping_list"]:
                st.markdown(f"- {item}")
        else:
            st.info("Generate a meal plan first to see your missing ingredients.")

        expiring = [i for i in st.session_state.pantry if i["expiry"] <= 3]
        if expiring:
            st.markdown("<br>", unsafe_allow_html=True)
            names = ", ".join(i["name"] for i in expiring)
            st.error(f"**Waste Alert:** Use {names} soon!")
        st.markdown('</div>', unsafe_allow_html=True)
