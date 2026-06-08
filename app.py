import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. INITIAL SYSTEM SETUP & DESIGN PROTOCOLS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Drake Institute: National Resilience Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-title { font-size:2.4rem !important; font-weight:700; color:#ffffff; margin-bottom:0.5rem; }
    .subtitle { font-size:1.1rem !important; color:#cccccc; margin-bottom:1.5rem; }
    .card { background-color: #1e1e1e; padding: 20px; border-radius: 8px; border: 1px solid #333333; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🛡️ National Resilience Simulator: Compounded Stress Engine</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Sovereign Risk Architecture Framework & System Attrition Model (2026)</p>', unsafe_allow_html=True)
st.markdown("---")

# ---------------------------------------------------------
# 2. SIDEBAR - EXECUTIVE RADAR (STRATEGIC CONTROLS)
# ---------------------------------------------------------
st.sidebar.header("🕹️ Macro Stress & Intervention Radars")

st.sidebar.subheader("⚠️ Disruption Threat Vector")
scenario_type = st.sidebar.selectbox(
    "Select Red Team Threat Vector:",
    options=[
        "Scenario A: CCG Blockade (Kaohsiung Focus & Bashi Strait High-Risk Gridlock)", 
        "Scenario B: CCG Grey-Zone Interdiction (Qatar & Australia Shipments via Miyako Channel)", 
        "Scenario C: Critical Infrastructure LNG Node Physical Shock Event"
    ]
)

st.sidebar.subheader("⚡ Energy & Chemical Allocation")
package_tier = st.sidebar.radio(
    "Stacked Investment Packages:",
    options=["Status Quo (No Intervention)", "Moderate Investment Package", "Advanced Resilience Package", "Full Strategic Resilience Package"]
)

st.sidebar.subheader("💧 Module 4: Water Security Levers")
water_tier = st.sidebar.selectbox(
    "Chip-Fabs Water Security Posture:",
    options=["Standard Municipal Feed (Grid Dependent)", "On-Site Ultra-Pure Water (UPW) Reclamation", "Hardened Desalination + Local Power Micro-Grid"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Drake Institute of Geostrategic Intelligence • Enterprise Tier Model")

# ---------------------------------------------------------
# 3. INTERACTIVE CORRIDOR ESCORT ENGINE (WHITE PAPER LOGIC)
# ---------------------------------------------------------
st.markdown("### 🚢 CCG Lawfare Escort Response & Corridor Friction Engine")
st.markdown("###### White Paper Logic Matrix: Modeling 12,000-Ton White-Hull Cordon vs. ROC Escort Availability")

col_esc1, col_esc2 = st.columns(2)
with col_esc1:
    ccg_hull_count = st.slider("Deployable Mega-CCG Hulls (White-Hull Lawfare Loophole)", 2, 24, 16 if "Scenario A" in scenario_type else 8 if "Scenario B" in scenario_type else 2)
    roc_escort_ratio = st.slider("ROC Navy / CGA Escort Commitment Rate (%)", 0, 100, 35 if "Scenario A" in scenario_type else 65 if "Scenario B" in scenario_type else 100)
with col_esc2:
    escort_delay_days = st.number_input("Calculated ROC Fleet Operational Response Delay (Days)", 1.0, 14.0, 6.5 if "Scenario A" in scenario_type else 2.0 if "Scenario B" in scenario_type else 1.0, step=0.5)

# Calculate Escort Breakthrough Metrics and Owner Panic Flight
escort_success_rate = max(min(int(roc_escort_ratio - (ccg_hull_count * 2.5)), 100), 5)
commercial_flight_rate = max(min(int((escort_delay_days * 8) + (ccg_hull_count * 2) - (roc_escort_ratio * 0.3)), 95), 5)

# ---------------------------------------------------------
# 4. ADVANCED QUANT MARITIME ENGINE & BACKEND MATH
# ---------------------------------------------------------
base_charter_rate = 85000  
baltic_base_index = 1800

# Base parameters tie cleanly into the interactive escort math
if "Scenario A" in scenario_type:
    base_mean = 12
    base_std = 2
    lng_cutoff_day = 11
    risk_multiplier = 1.0 + (ccg_hull_count * 0.3)
    active_transit = max(100 - commercial_flight_rate, 5)
    holding_safe = int(commercial_flight_rate * 0.7)
    defection = int(commercial_flight_rate * 0.3)
    flight_penalty = int(commercial_flight_rate / 15)
    hull_status = "Mass Retreat: Vessels holding in Subic Bay / Diversion to Tokyo Bay & Yokohama (Negishi/Sodegaura)"
elif "Scenario B" in scenario_type:
    base_mean = 31
    base_std = 4
    lng_cutoff_day = 25
    risk_multiplier = 1.0 + (ccg_hull_count * 0.15)
    active_transit = max(100 - commercial_flight_rate, 10)
    holding_safe = int(commercial_flight_rate * 0.6)
    defection = int(commercial_flight_rate * 0.4)
    flight_penalty = int(commercial_flight_rate / 25)
    hull_status = "Tactical Hedging: Safe-harbor positioning inside Southern Japan anchorage nodes"
else:
    base_mean = 6.5
    base_std = 1
    lng_cutoff_day = 5
    risk_multiplier = 1.1
    active_transit, holding_safe, defection = 90, 8, 2
    flight_penalty = 0
    hull_status = "Standard Operations: Normal corridor lanes active via Taiwan Strait"

current_charter_rate = int(base_charter_rate * risk_multiplier)
current_baltic_index = int(baltic_base_index * risk_multiplier)

# Process Defense Investment Interventions
helium_boost, gas_boost, grid_boost, lng_boost, water_boost = 0, 0, 0, 0, 0
capex_tier = "Zero Base"
efficiency = "Poor (Deterministic Cascade Failure)"

if package_tier == "Moderate Investment Package":
    helium_boost, gas_boost, capex_tier = 5, 12, "Low - Medium Allocations"
    efficiency = "Excellent for isolated local shocks; vulnerable to sustained attrition"
elif package_tier == "Advanced Resilience Package":
    helium_boost, gas_boost, grid_boost, lng_boost, capex_tier = 7, 14, 7, 17, "High Institutional Tier"
    efficiency = "Strong Impact (Decouples terrestrial logistics failure points)"
elif package_tier == "Full Strategic Resilience Package":
    helium_boost, gas_boost, grid_boost, lng_boost, capex_tier = 10, 20, 25, 40, "Sovereign/Macro Enterprise"
    efficiency = "Strategic Deterrence Threshold Achieved"

if water_tier == "On-Site Ultra-Pure Water (UPW) Reclamation":
    water_boost = 6
elif water_tier == "Hardened Desalination + Local Power Micro-Grid":
    water_boost = 12

# Run Core Monte Carlo Engine with integrated Escort Failure Penalty
runs = 10000
timeline_days = 90
total_resilience_boost = (helium_boost + gas_boost + grid_boost + lng_boost + water_boost) - flight_penalty

np.random.seed(42)
simulated_baseline = np.random.normal(base_mean, base_std, runs)
simulated_protected = simulated_baseline + total_resilience_boost

timeline = np.arange(0, timeline_days)
prob_baseline = np.array([(simulated_baseline > t).mean() for t in timeline])
prob_protected = np.array([(simulated_protected > t).mean() for t in timeline])
mean_survival_days = max(int(np.mean(simulated_protected)), 1)

status_color = "🔴 Critical Convergence" if mean_survival_days < 20 else "🟠 Degraded System" if mean_survival_days <= 45 else "🟡 Stressed" if mean_survival_days <= 60 else "🟢 Normal"

st.markdown("---")

# ---------------------------------------------------------
# 5. USER INTERFACE ARCHITECTURE (FOUR-TAB CHASSIS)
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📊 Live Quant Simulator", "⚓ Phase 2: Port Chokepoints", "📋 System Scorecards & Cascades", "🚨 Executive Policy Framework"])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Systemic Survival Floor (Autarky)", value=f"{mean_survival_days} Days", delta=f"+{total_resilience_boost} Net Days" if total_resilience_boost > 0 else "Baseline Friction")
    with col2:
        st.metric(label="National Sovereignty Status", value=status_color)
    with col3:
        st.metric(label="Model CAPEX Requirements", value=capex_tier)

    # Re-engineered Quant Maritime Display Panel
    st.markdown("### 🗠 Real-Time Maritime Freight & Insurance Premium Panel")
    st.info(f"**Current Hull Dispersal Directives:** {hull_status}")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"<div class='card'>📋 <b>Clarksons Assessment</b><br><span style='font-size:1.5rem;color:#f0ad4e;'>${current_charter_rate:,}/day</span><br><small>Spot Charter Rate Inflation</small></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='card'>📈 <b>Baltic Freight Index</b><br><span style='font-size:1.5rem;color:#d9534f;'>{current_baltic_index:,}</span><br><small>War-Risk Premium Multiplier</small></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='card'>⚓ <b>Tokyo/Subic Escape Profile</b><br><span style='font-size:1.3rem;color:#5bc85c;'>{holding_safe}% Retreated</span><br><small>Idling in Safe Anchorages</small></div>", unsafe_allow_html=True)
    with m4:
        st.markdown(f"<div class='card'>🔄 <b>Commercial Flight Scale</b><br><span style='font-size:1.3rem;color:#0275d8;'>{commercial_flight_rate}% Diverted</span><br><small>Vessels Avoiding Taiwan Corridor</small></div>", unsafe_allow_html=True)

    st.markdown("---")
    
    # Visualization Columns
    viz_col1, viz_col2 = st.columns(2)
    with viz_col1:
        st.markdown("### Probability-Weighted Infrastructure Survival Curve")
        plt.style.use('dark_background') 
        fig1, ax1 = plt.subplots(figsize=(6, 3.5))
        ax1.plot(timeline, prob_baseline * 100, color="#d9534f", linestyle="--", linewidth=2, label="Status Quo Profile")
        ax1.plot(timeline, prob_protected * 100, color="#0275d8", linewidth=3, label="Simulated Defense Curve")
        ax1.set_facecolor("#121212")
        fig1.patch.set_facecolor("#121212")
        ax1.set_xlabel("Days Elapsed Under Stress Conditions")
        ax1.set_ylabel("Probability of Uninterrupted Output (%)")
        ax1.set_xlim(0, timeline_days)
        ax1.set_ylim(0, 105)
        ax1.grid(True, linestyle=":", alpha=0.3, color="#555555")
        ax1.legend(facecolor="#222222", edgecolor="#444444", labelcolor="#cccccc", fontsize='small')
        st.pyplot(fig1)

    with viz_col2:
        st.markdown("### LNG Shipping Cut-Off & Inventory Decay Tracker")
        extended_lng_buffer = max(lng_cutoff_day + lng_boost - flight_penalty, 1)
        lng_inventory = []
        for t in timeline:
            if t < extended_lng_buffer:
                lng_inventory.append(max(100 * (1.0 - (t / extended_lng_buffer)), 0))
            else:
                lng_inventory.append(0)
                
        fig2, ax2 = plt.subplots(figsize=(6, 3.5))
        ax2.fill_between(timeline, lng_inventory, color="#f0ad4e", alpha=0.2, label="Sovereign Inventory Volume")
        ax2.plot(timeline, lng_inventory, color="#f0ad4e", linewidth=2.5)
        ax2.axvline(x=lng_cutoff_day, color="#d9534f", linestyle=":", label=f"Baseline Exhaustion (Day {lng_cutoff_day})", linewidth=2)
        if lng_boost > 0:
            ax2.axvline(x=extended_lng_buffer, color="#5cb85c", linestyle="-.", label=f"Adjusted Run (Day {int(extended_lng_buffer)})", linewidth=2)
        ax2.set_facecolor("#121212")
        fig2.patch.set_facecolor("#121212")
        ax2.set_xlabel("Days Elapsed Post Shipping Cut-Off")
        ax2.set_ylabel("Available Grid Generation Capacity (%)")
        ax2.set_xlim(0, 45)
        ax2.set_ylim(0, 105)
        ax2.grid(True, linestyle=":", alpha=0.3, color="#555555")
        ax2.legend(facecolor="#222222", edgecolor="#444444", labelcolor="#cccccc", fontsize='small')
        st.pyplot(fig2)

    st.markdown("---")
    st.markdown("### 🏬 Cross-Sector Cascade Matrix & Global Impact")
    col_l, col_r = st.columns(2)
    with col_l:
        if water_tier == "Standard Municipal Feed (Grid Dependent)":
            st.error("💧 **Water-Energy Cascade Active:** Electrical grid instability forces instant shutoffs at municipal pumping stations. Without localized UPW reclamation, semiconductor lines hit an immediate hard halt due to filtration failure.")
        elif water_tier == "On-Site Ultra-Pure Water (UPW) Reclamation":
            st.warning("🔄 **Recycling Buffer Engaged:** Closed-loop recycling nodes mitigate immediate municipal drop-offs. Internal circulation slows the volumetric attrition decay curve, buying operational days independent of the civilian grid.")
        else:
            st.success("🌊 **Infrastructure Decoupling:** Hardened coastal desalination infrastructure powered by local energy micro-grids fully insulates core manufacturing loops from public infrastructure attrition.")
            
        if mean_survival_days < 14:
            st.error("⚠️ **Immediate Tech Pipeline Freeze:** Advanced node manufacturing (3nm and below) hits a Cold-Halt. Global economic losses exceed **$250 Billion/week**.")
        elif mean_survival_days <= 45:
            st.warning("⚡ **Downstream Depletion & Friction:** High market volatility. Severe molecule arrhythmia limits assembly throughput.")
        else:
            st.success("💎 **Strategic Attrition Defended:** The system extends past the critical 60-day target, shifting the geopolitical risk-reward equation.")

    with col_r:
        st.markdown("**Intervention Efficiency Breakdown**")
        st.write(f"**Strategic Assessment:** {efficiency}")
        st.json({
            "Module 2: Escort Success Breakthrough Probability": f"{escort_success_rate}% Success Probability",
            "Module 3: Precursor Molecule Gas Buffering": f"+{gas_boost} Days Operational Runway",
            "Module 3: Grid Hardening & ASU Prioritization": f"+{grid_boost} Power Isolation Window",
            "Module 3: LNG Sovereign Storage Multiplier": f"+{lng_boost} Core System Buffer Extension",
            "Module 4: Ultra-Pure Water (UPW) Continuity Vector": f"+{water_boost} Closed-Loop Buffering Days",
            "Maritime Hull Flight Flight Penalty": f"-{flight_penalty} Days (Owner Flight Accounted)"
        })

# --- TAB 2: PHASE 2 PORT CHOKEPOINTS ENGINE ---
with tab2:
    st.markdown("### ⚓ Module 2: Physical Logistics Chokepoints & Port Capacity")
    st.markdown("###### Real-Time Attrition Modeling: Port of Kaohsiung vs. Port of Keelung")
    
    st.markdown("##### 🛠️ Port Operational Adjustments")
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        kao_efficiency = st.slider("Port of Kaohsiung Crane Operating Efficiency (%)", 0, 100, 100 if "Scenario B" in scenario_type else 30 if "Scenario A" in scenario_type else 100)
        kao_backlog = st.number_input("Kaohsiung Container Yard Congestion Factor (Multiplier)", 1.0, 5.0, 3.8 if "Scenario A" in scenario_type else 1.2, step=0.1)
    with p_col2:
        kee_efficiency = st.slider("Port of Keelung Offloading Bottleneck Threshold (%)", 0, 100, 85 if "Scenario B" in scenario_type else 50 if "Scenario A" in scenario_type else 100)
        kee_diversion_load = st.checkbox("Automatically Reroute Diverted Southern Hulls to Keelung?", value=True if "Scenario A" in scenario_type else False)

    base_processing_days = 2.5
    if kee_diversion_load and kao_efficiency < 50:
        port_stress_multiplier = (kao_backlog * 1.6) + (100 - kee_efficiency) / 50
        port_status_msg = "⚠️ SEVERE PORT CONGESTION: Keelung structural capacity exceeded by diverted southern freight hulls."
        port_color = "error"
    else:
        port_stress_multiplier = kao_backlog + (100 - kao_efficiency) / 100
        port_status_msg = "🟢 Port processing lines managing normal queuing profiles."
        port_color = "success"
        
    calculated_clearance_lag = round(base_processing_days * port_stress_multiplier, 1)
    
    st.markdown("---")
    if port_color == "error":
        st.error(port_status_msg)
    else:
        st.success(port_status_msg)
        
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        st.markdown(f"<div class='card'>🏗️ <b>Kaohsiung Clearance Delay</b><br><span style='font-size:1.5rem;color:#f0ad4e;'>{calculated_clearance_lag} Days</span><br><small>Baseline: 2.5 Days</small></div>", unsafe_allow_html=True)
    with pc2:
        re_routed_pct = 0 if not kee_diversion_load else 45 if "Scenario B" in scenario_type else 85
        st.markdown(f"<div class='card'>🔄 <b>Northern Diversion Load</b><br><span style='font-size:1.5rem;color:#0275d8;'>{re_routed_pct}% Freight</span><br><small>Keelung Yard Strain</small></div>", unsafe_allow_html=True)
    with pc3:
        demurrage_surge = int(25000 * port_stress_multiplier)
        st.markdown(f"<div class='card'>💸 <b>Daily Demurrage Attrition</b><br><span style='font-size:1.5rem;color:#d9534f;'>${demurrage_surge:,}/ship</span><br><small>Sovereign Financial Leakage</small></div>", unsafe_allow_html=True)

    st.markdown("""
    💡 **Sovereign Risk Context:** Physical bottlenecks at the pier act as a *Physical-to-Economic conversion mechanism*. 
    When Kaohsiung crane efficiency falls below 40%, ships are stranded in open waters longer. This increases their 
    exposure to maritime interdiction vectors and spikes daily spot-freight charter costs exponentially, 
    forcing institutional charter walk-aways.
    """)

# --- TAB 3: SYSTEM SCORECARDS & CHRONOLOGICAL CASCADES ---
with tab3:
    st.subheader("📋 Core Module Performance & Resilience Scorecard")
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.markdown("### 🚢 Module 2: Port Resilience\n* **Score: 3.1 / 5.0**\n* Physical bottlenecks over storage metrics dictate initial backlogs. Insurance cancellation triggers rapid charter walk-aways.")
    with sc2:
        st.markdown("### ⚡ Module 3: Energy Continuity\n* **Score: 3.0 / 5.0**\n* Total reliance on continuous LNG imports creates an immediate high-exposure horizon when storage buffers dry out.")
    with sc3:
        st.markdown("### 💧 Module 4: Water Continuity\n* **Score: 2.8 / 5.0**\n* Deep operational coupling to the primary high-voltage grid. Drops quickly into public-health stress thresholds if power fails.")

    st.markdown("---")
    st.subheader("🕒 Chronological Port Disruption Propagation (T+ Sequence)")
    st.info("**[T+0]** Throughput reduction begins at port berths, cranes, and offloading systems.")
    st.info("**[T+6–24 Hours]** LNG shipment backlogs accumulate; specialized chemical unloading delays cascade.")
    st.info("**[T+2–5 Days]** Industrial gas shortages hit manufacturing fabs; grid operating flexibility tightens critically.")
    st.info("**[T+5–11 Days]** High-voltage energy buffer depletion; mandatory rolling industrial power cuts begin.")
    st.warning("**[T+11+ Days]** Full national transition to an energy-rationing triage regime; industrial export capacity drops severely.")

# --- TAB 4: EXECUTIVE POLICY MANDATES ---
with tab4:
    st.subheader("🚨 Executive Design Requirements & Infrastructure Mandates")
    st.markdown("1. **Establish a National Resilience Integration Layer (NRIL)**\n2. **Deploy the National System Stress Index (NSSI)**\n3. **Target Response Latency Reduction**\n4. **Enforce Manual Override Readiness**\n5. **Decentralize Strategic Buffering**")
    st.markdown("---")
    st.success("💰 **Commercial Monetization Blueprint (Drake SaaS Licensing Strategy)**")
    st.markdown("This prototype represents **Step 1** of a highly scalable, subscription-driven enterprise SaaS offering designed for Sovereign Wealth Funds, Macro Asset Allocators, Global Technology Enterprises, and Reinsurance Consortiums.")

st.markdown("---")
st.caption("Strategic Decision Engine Layer • Integrated Systemic Attrition Model (2026) • Drake Institute of Geostrategic Intelligence.")
