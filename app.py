import streamlit as st
import plotly.graph_objects as go

# --- Setup ---
st.set_page_config(layout="wide")
st.title("National Resilience Engine")

# --- Functions ---
def calculate_multipliers(temporal_stage, active_switches):
    switch_efficiency = 0.15
    emp_boost = switch_efficiency if "emp" in active_switches else 0.0
    ubo_delay = True if "ubo" in active_switches else False
    academic_shield = True if "academic" in active_switches else False
    defense_boost = 0.15 if "defense" in active_switches else 0.0
    temporal_decay_multiplier = 1.0 if temporal_stage == 0 else 1.5
    return emp_boost, ubo_delay, academic_shield, defense_boost, temporal_decay_multiplier

# --- Sidebar Controls ---
st.sidebar.header("Policy Settings")
escalation = st.sidebar.slider("Escalation Level", 0, 10, 5)
temporal = st.sidebar.slider("Temporal Stage", 0, 1, 0)
emp = st.sidebar.checkbox("EMP Switch")
ubo = st.sidebar.checkbox("UBO Switch")
academic = st.sidebar.checkbox("Academic Switch")
defense = st.sidebar.checkbox("Defense Switch")

# --- Logic ---
active_switches = []
if emp: active_switches.append("emp")
if ubo: active_switches.append("ubo")
if academic: active_switches.append("academic")
if defense: active_switches.append("defense")

emp_b, _, _, _, temp_m = calculate_multipliers(temporal, active_switches)

# --- Visualization ---
tab1, tab2 = st.tabs(["Simulation Engine", "Policy Settings"])

with tab1:
    y_values = [10 * (1 + emp_b), (10 - escalation) * temp_m, 5, 5 - (escalation * 0.5)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 1, 2, 3], y=y_values, mode='lines+markers', line=dict(color='cyan')))
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
    st.plotly_chart(fig)
