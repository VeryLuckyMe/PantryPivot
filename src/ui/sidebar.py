# ── Sidebar Navigation ──────────────────────────────────────────────────────
# Renders the sidebar with branding, navigation buttons, and footer.

import streamlit as st


def render_sidebar(fresh_percent):
    """Render the application sidebar with navigation and branding."""
    with st.sidebar:
        st.markdown(f"""
          <div class="sidebar-logo">
            <div class="icon-box">🥫</div>
            <span>PantryPivot</span>
          </div>
          <div class="sidebar-subtitle">
            <div class="title">Kitchen Intel</div>
            <div class="status-pill">
              <div class="pulse"></div>
              {fresh_percent}% FRESHNESS
            </div>
          </div>
        """, unsafe_allow_html=True)

        pages = [
            ("home", "grid_view", "Dashboard"),
            ("recipes", "auto_awesome", "Recipe Assistant"),
            ("pantry", "inventory_2", "Pantry"),
            ("mealplan", "calendar_month", "Meal Planner"),
        ]

        for code, icon, label in pages:
            is_active = st.session_state.page == code
            if is_active:
                st.markdown('<div class="active-nav">', unsafe_allow_html=True)
            if st.button(f"{label}", icon=f":material/{icon}:", key=f"nav_{code}", use_container_width=True):
                st.session_state.page = code
                st.rerun()
            if is_active:
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="btn-log-waste">', unsafe_allow_html=True)
        st.button("🗑️ Log Waste", key="log_waste", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
          <div class="sidebar-footer">
            <div class="badge">PRO</div>
            <h5>Chef's Edition</h5>
            <p>Advanced AI Features & <br>Unlimited Pantry Sync</p>
          </div>
        """, unsafe_allow_html=True)
