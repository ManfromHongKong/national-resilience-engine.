import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. PAGE SETUP & CORPORATE IDENTITY
# ---------------------------------------------------------
st.set_page_config(
    page_title="Drake Institute: National Resilience Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Enterprise Pitch Appeal
st.markdown("""
    <style>
    .main-title { font-size:2.4rem !important; font-weight:700; color:#ffffff; margin-bottom:0.5rem; }
    .subtitle { font-size:1.1rem !important; color:#cccccc; margin-bottom:1.5rem; }
    .metric-card { background-color: #1e1e1e; padding: 15px; border-radius: 8px; border: 1px solid #333333; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🛡️ National Resilience Simulator: Compounded Stress Engine</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Sovereign Risk Architecture Framework & System Attrition Model (2026)</p>', unsafe_allow_html=True)
st.markdown("---")

# ---------------------------------------------------------
# 2. SIDEBAR - EXECUTIVE RADAR (STRATEGIC CONTROLS)
# ---------------------------------------------------------
st.sidebar.header("🕹️ Macro Stress & Intervention Radars")
st.sidebar.markdown("Adjust risk baselines and layered defensive investments to run the live cascade models.")

# Vector A: Threat Profiles (Explicit Maritime Logistics Choke Points)
st.sidebar.subheader("⚠️ Disruption Threat Vector")
scenario_type = st.sidebar.selectbox(
    "Select Red Team Threat Vector:",
    options=[
        "Scenario A: CCG Blockade (Kaohsiung Interdiction & Bashi Strait Escalation)", 
        "Scenario B: CCG Grey-Zone Interdiction (Qatar & Australia Transit Disruptions via Miyako Channel)", 
        "Scenario C: Critical Infrastructure LNG Node Physical Shock Event"
    ]
)

# Vector B: Energy, Logistics, & Molecule Interventions
st.sidebar.subheader("⚡ Energy & Chemical Allocation")
package_tier = st.sidebar.radio(
    "Stacked Investment Packages:",
    options=[
        "Status Quo (No Intervention)",
        "Moderate Investment Package",
        "Advanced Resilience Package",
        "Full Strategic Resilience Package"
    ],
    index=0
)

# Vector C: Elevated Water Infrastructure Modifiers
st.sidebar.subheader("💧 Module 4: Water Security Levers")
water_tier = st.sidebar.selectbox(
    "Chip-Fabs Water Security Posture:",
    options=[
        "Standard Municipal Feed (Grid Dependent)",
        "On-Site Ultra-Pure Water (UPW) Reclamation",
        "Hardened Desalination + Local Power Micro-Grid"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.caption("Drake Institute of Geostrategic Intelligence • Enterprise Tier Model")

# ---------------------------------------------------------
# 3. MATHEMATICAL CORE - QUANT COUPLING ENGINE
# ---------------------------------------------------------
# Define core metric boosts from Chemical & Energy Packages
helium_boost = 0
gas_boost = 0
grid_boost = 0
lng_boost = 0
capex_tier = "None"
efficiency = "N/A"

if package_tier == "Status Quo (No Intervention)":
    capex_tier = "Zero Base"
    efficiency = "Poor (Deterministic Cascade Failure)"
elif package_tier == "Moderate Investment Package":
    helium_boost = 5
    gas_boost = 12
    capex_tier = "Low - Medium Allocations"
    efficiency = "Excellent for isolated local shocks; vulnerable to sustained attrition"
elif package_tier == "Advanced Resilience Package":
    helium_boost = 7
    gas_boost = 14
    grid_boost = 7
    lng_boost = 17
    capex_tier = "High Institutional Tier"
    efficiency = "Strong Impact (Decouples terrestrial logistics failure points)"
elif package_tier == "Full Strategic Resilience Package":
    helium_boost = 10
    gas_boost = 20
    grid_boost = 25
    lng_boost = 40
    capex_tier = "Sovereign/Macro Enterprise"
    efficiency = "Strategic Deterrence Threshold Achieved"

# Define quantitative scope for the elevated Water Security Spoke
water_boost = 0
if water_tier == "On-Site Ultra-Pure Water (UPW) Reclamation":
    water_boost = 6
elif water_tier == "Hardened Desalination + Local Power Micro-Grid":
    water_boost = 12

# Shipping Economics Multipliers based on selected threat vectors
clarksons_surge = "+0%"
baltic_premium = "Baseline"
fleet_flight_status = "Normal Operations"
shipping_friction_deduction = 0

if "Scenario A" in scenario_type:
    base_mean = 12      
    base_std = 2
    lng_cutoff_day = 11  
    clarksons_surge = "+450% Spike"
    baltic_premium = "War-Risk Surcharge Active (Bashi Strait Gridlock)"
    fleet_flight_status = "Mass Retreat: Vessels holding in Subic Bay / Offloading in Japan"
    shipping_friction_deduction = 3  # Strategic shipping flight drops runway days
elif "Scenario B" in scenario_type:
    base_mean = 31      
    base_std = 4
    lng_cutoff_day = 25  
    clarksons_surge = "+180% Increase"
    baltic_premium = "Elevated Risk Index (Miyako Channel Diverting)"
    fleet_flight_status = "Active Re-Chartering: Hulls fleeing cross-strait lanes for safer routes"
    shipping_friction_deduction = 5
else:
    base_mean = 6.5     
    base_std = 1
    lng_cutoff_day = 5   
    clarksons_surge = "+40% Friction"
    baltic_premium = "Localized Shock Adjustments"
    fleet_flight_status = "Insurance Warnings Issued for Taiwan Territorial Waters"

# Execute Monte Carlo Modeling with dynamic Shipping Friction Adjustment
runs = 10000
timeline_days = 90
total_resilience_boost = (helium_boost + gas_boost + grid_boost + lng_boost + water_boost) - shipping_friction_deduction

np.random.seed(42)
simulated_baseline = np.random.normal(base_mean, base_std, runs)
simulated_protected = simulated_baseline + total_resilience_boost

timeline = np.arange(0, timeline_days)
prob_baseline = np.array([(simulated_baseline > t).mean() for t in timeline])
prob_protected = np.array([(simulated_protected > t).mean() for t in timeline])

mean_survival_days = max(int(np.mean(simulated_protected)), 1)

# Establish State Transition Flags based on quantified survival
if mean_survival_days < 20:
    status_color = "🔴 Critical Convergence"
elif mean_survival_days <= 45:
    status_color = "🟠 Degraded System Function"
elif mean_survival_days <= 60:
    status_color = "🟡 Stressed Operation"
else:
    status_color = "🟢 Normal Operation Threshold"

# ---------------------------------------------------------
# 4. INTERFACE ARCHITECTURE - THE THREE-TAB PLATFORM
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📊 Live Quant Simulator", "⚓ Phase 2: Port Chokepoints", "📋 System Scorecards & Cascades", "🚨 Executive Policy Framework"])

# --- TAB 1: THE INVESTOR QUANT ENGINE VISUALIZER ---
with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Systemic Survival Floor (Days of Autarky)", 
            value=f"{mean_survival_days} Days", 
            delta=f"+{total_resilience_boost} Days Net Variance" if total_resilience_boost > 0 else "Baseline Attrition Friction"
        )
    with col2:
        st.metric(label="National Sovereignty Stability Status", value=status_color)
    with col3:
        st.metric(label="Model CAPEX Requirements", value=capex_tier)

    # RE-INTEGRATED MARITIME CHARTER MARKET TICKER PANEL
    st.markdown("### 🚢 Shipbroker & Maritime Freight Risk Ticker")
    tick1, tick2, tick3 = st.columns(3)
    with tick1:
        st.info(f"**Clarksons Spot Assessment:** {clarksons_surge}")
    with tick2:
        st.info(f"**Baltic Exchange Status:** {baltic_premium}")
    with tick3:
        st.warning(f"**Shipowner Disposition:** {fleet_flight_status}")

    st.markdown("---")
    
    # Dual Visualization Layout
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        st.markdown("### Probability-Weighted Infrastructure Survival Curve")
        st.caption("Investor Note: This curve tracks the decay curve of advanced production viability under compounding cross-sector friction.")
        
        plt.style.use('dark_background') 
        fig1, ax1 = plt.subplots(figsize=(6, 3.5))
        ax1.plot(timeline, prob_baseline * 100, label="Status Quo Profile (Unprotected)", color="#d9534f", linestyle="--", linewidth=2)
        ax1.plot(timeline, prob_protected * 100, label="Simulated Defense Curve", color="#0275d8", linewidth=3)

        ax1.set_facecolor("#121212")
        fig1.patch.set_facecolor("#121212")
        ax1.spines['bottom'].set_color('#cccccc')
        ax1.spines['top'].set_color('#333333')
        ax1.spines['right'].set_color('#333333')
        ax1.spines['left'].set_color('#cccccc')
        ax1.xaxis.label.set_color('#cccccc')
        ax1.yaxis.label.set_color('#cccccc')
        
        ax1.set_xlabel("Days Elapsed Under Stress Conditions")
        ax1.set_ylabel("Probability of Uninterrupted Output (%)")
        ax1.set_xlim(0, timeline_days)
        ax1.set_ylim(0, 105)
        ax1.grid(True, linestyle=":", alpha=0.3, color="#555555")
        ax1.legend(facecolor="#222222", edgecolor="#444444", labelcolor="#cccccc", fontsize='small')
        st.pyplot(fig1)

    with viz_col2:
        st.markdown("### LNG Shipping Cut-Off & Inventory Decay Tracker")
        st.caption("Investor Note: This model illustrates the physical depletion rate of domestic LNG strategic storage stocks vs. port backlogs.")
        
        # Calculate dynamic inventory decay based on interventions and shipping risk factors
        extended_lng_buffer = max(lng_cutoff_day + lng_boost - shipping_friction_deduction, 1)
        lng_inventory = []
        for t in timeline:
            if t < extended_lng_buffer:
                remaining = 100 * (1.0 - (t / extended_lng_buffer))
                lng_inventory.append(max(remaining, 0))
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
        ax2.spines['bottom'].set_color('#cccccc')
        ax2.spines['top'].set_color('#333333')
        ax2.spines['right'].set_color('#333333')
        ax2.spines['left'].set_color('#cccccc')
        ax2.xaxis.label.set_color('#cccccc')
        ax2.yaxis.label.set_color('#cccccc')
        
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
        # Dynamic Water Cascade Module
        if water_tier == "Standard Municipal Feed (Grid Dependent)":
            st.error(
                "💧 **Water-Energy Cascade Active:** Electrical grid instability forces instant shutoffs at municipal "
                "pumping stations. Without localized UPW reclamation, semiconductor lines hit an immediate hard halt due to filtration failure."
            )
        elif water_tier == "On-Site Ultra-Pure Water (UPW) Reclamation":
            st.warning(
                "🔄 **Recycling Buffer Engaged:** Closed-loop recycling nodes mitigate immediate municipal drop-offs. "
                "Internal circulation slows the volumetric attrition decay curve, buying operational days independent of the civilian grid."
            )
        else:
            st.success(
                "🌊 **Infrastructure Decoupling:** Hardened coastal desalination infrastructure powered by local energy micro-grids "
                "fully insulates core manufacturing loops from public infrastructure attrition."
            )
            
        # Core Global Supply Chain Warnings
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
            "Module 3: Strategic Helium Allocation Buffer": f"+{helium_boost} Days Output Validity",
            "Module 3: Precursor Molecule Gas Buffering": f"+{gas_boost} Days Operational Runway",
            "Module 3: Grid Hardening & ASU Prioritization": f"+{grid_boost} Power Isolation Window",
            "Module 3: LNG Sovereign Storage Multiplier": f"+{lng_boost} Core System Buffer Extension",
            "Module 4: Ultra-Pure Water (UPW) Continuity Vector": f"+{water_boost} Closed-Loop Buffering Days",
            "Maritime Hull Attrition Friction Penalty": f"-{shipping_friction_deduction} Days (Owner Flight Accounted)"
        })

# --- TAB 2: SYSTEM SCORECARDS & CHRONOLOGICAL CASCADES ---
with tab2:
    st.subheader("📋 Core Module Performance & Resilience Scorecard")
    st.markdown("Evaluation of foundational critical domains based on the Drake Institute Strategic Report.")
    
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.markdown("### 🚢 Module 2: Port Resilience")
        st.error("🌟 **Score: 3.1 / 5.0**")
        st.markdown("""
        * **Constraints:** Concentration at physical bottlenecks (crane/berth availability) over sheer storage capacity.
        * **SPoFs:** LNG unloading continuity and instant maritime insurance flight.
        """)
    with sc2:
        st.markdown("### ⚡ Module 3: Energy Continuity")
        st.error("🌟 **Score: 3.0 / 5.0**")
        st.markdown("""
        * **Constraints:** Deep dependency on continuous LNG imports; zero domestic short-term fuel substitution alternatives at scale.
        * **Trajectory:** Shifts abruptly to a supply-constrained allocation model when reserve margins fracture.
        """)
    with sc3:
        st.markdown("### 💧 Module 4: Water Continuity")
        st.error("🌟 **Score: 2.8 / 5.0**")
        st.markdown("""
        * **Constraints:** Tight coupling to the electrical grid (pumping station power) and digital SCADA control loops.
        * **Societal State:** Enters 'Public Health Stress Regime' within 3–7 days of flow disruption, forcing contamination issues.
        """)

    st.markdown("---")
    st.subheader("🕒 Chronological Port Disruption Propagation (T+ Sequence)")
    st.markdown("Calculated timeline when primary stress hits the Kaohsiung industrial convergence node:")
    
    st.info("**[T+0]** Throughput reduction begins at port berths, cranes, and offloading systems.")
    st.info("**[T+6–24 Hours]** LNG shipment backlogs accumulate; specialized chemical unloading delays cascade.")
    st.info("**[T+2–5 Days]** Industrial gas shortages hit manufacturing fabs; grid operating flexibility tightens critically.")
    st.info("**[T+5–11 Days]** High-voltage energy buffer depletion; mandatory rolling industrial power cuts begin.")
    st.warning("**[T+11+ Days]** Full national transition to an energy-rationing triage regime; industrial export capacity drops severely.")

# --- TAB 3: EXECUTIVE POLICY MANDATES & COMMERCIAL VALUATION ---
with tab3:
    st.subheader("🚨 Executive Design Requirements & Infrastructure Mandates")
    st.markdown("To build systemic immunity, enterprise macro allocators must move away from siloed management toward five explicit shifts:")

    st.markdown("""
    1. **Establish a National Resilience Integration Layer (NRIL):** Create a centralized technical node bridging independent agency monitors into a unified, actionable viewer.
    2. **Deploy the National System Stress Index (NSSI):** Implement cross-sector anomaly correlation to flag overlapping minor stresses before they morph into a macro-cascade.
    3. **Target Response Latency Reduction:** Shift core KPIs from isolated repair speeds to cross-domain coordination response times, stretching executive decision windows.
    4. **Enforce Manual Override Readiness:** Mandate continuous, field-level drills for operating critical valves, grid sub-stations, and port infrastructure without central SCADA visibility.
    5. **Decentralize Strategic Buffering:** Expand and physically isolate critical chemical stocks (for semiconductor and water treatment) and push LNG reserves beyond the current baseline 11-day framework.
    """)
    
    st.markdown("---")
    # THE REVENUE DRIVER SECTION FOR INVESTORS
    st.success("💰 **Commercial Monetization Blueprint (Drake SaaS Licensing Strategy)**")
    st.markdown("""
    This prototype represents **Step 1** of a highly scalable, subscription-driven enterprise SaaS offering designed for:
    * **Sovereign Wealth Funds & Macro Asset Allocators:** For pricing cross-border geopolitical risk and hedging infrastructure portfolios.
    * **Global Technology Enterprises:** For continuous stress-testing of JIT supply-chain choke points.
    * **Insurance & Reinsurance Consortiums:** For underwriting multi-sector casualty and business interruption models under compound threat scenarios.
    
    **Next-Phase Expansion Targets (Post-Seed Investment):**
    * Deep APIs pulling live maritime AIS shipping data and regional SCADA telemetry.
    * Predictive machine learning layers modeling non-linear climate and kinetic stress interdependencies.
    """)

st.markdown("---")
st.caption("Strategic Decision Engine Layer • Integrated Systemic Attrition Model (2026) • Drake Institute of Geostrategic Intelligence.")
