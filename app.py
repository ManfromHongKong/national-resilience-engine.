import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
water_tier = "Standard Municipal Feed (Grid Dependent)"
# 1. Page Configuration for Web App Layout
st.set_page_config(page_title="Drake Institute: National Resilience Engine", layout="wide")

st.title("🛡️ National Resilience Simulator: Maritime Chokepoint Engine")
st.caption("Interactive 'What-If' Tactical Dashboard built for Macro Allocators & Sovereign Risk Analysts")
st.markdown("---")

# 2. Sidebar: Interactive "What-If" Scenario Control Panel
st.sidebar.header("🕹️ Scenario Variables Configuration")

# Physical & Infrastructure Inputs
initial_inv_days = st.sidebar.slider("Initial Taiwan Onshore Inventory (Days of Autarky)", min_value=5, max_value=20, value=11)
daily_burn = 35000
max_capacity = 900000
starting_inventory = initial_inv_days * daily_burn

# Commercial Risk Inputs
pull_out_rate = st.sidebar.slider("Shipowner Flight / Pull-Out Probability (%)", min_value=0, max_value=100, value=60) / 100.0

# Geopolitical & Kinetic Inputs
ccg_intensity = st.sidebar.selectbox("China Coast Guard Interdiction Tempo", ["Low", "Medium", "High"])
navy_day = st.sidebar.number_input("ROC Navy 'Full Force' Authorization Day", min_value=1, max_value=15, value=4)

# 3. Core Engine Layer (Dynamic Re-calculation)
class DynamicInteractiveEngine:
    def __init__(self):
        self.max_capacity = max_capacity
        self.current_inventory = starting_inventory
        self.daily_consumption = daily_burn
        self.pull_out_prob = pull_out_rate
        
        # Fleet schedule
        self.fleet = [
            {"id": "Qat_1", "source": "Qatar", "arrival_day": 3, "capacity_ton": 70000},
            {"id": "Aus_1", "source": "Australia", "arrival_day": 5, "capacity_ton": 70000},
            {"id": "Qat_2", "source": "Qatar", "arrival_day": 9, "capacity_ton": 70000},
            {"id": "Aus_2", "source": "Australia", "arrival_day": 14, "capacity_ton": 70000},
            {"id": "Qat_3", "source": "Qatar", "arrival_day": 19, "capacity_ton": 70000},
        ]

    def run(self):
        sim_fleet = []
        cargoes_lost = 0
        for v in self.fleet:
            v_copy = v.copy()
            if np.random.random() < self.pull_out_prob:
                v_copy["active"] = False
                cargoes_lost += 1
            else:
                v_copy["active"] = True
                v_copy["arrival_day"] += 2 if v_copy["source"] == "Qatar" else 3
            sim_fleet.append(v_copy)

        history = []
        blockade_active = True
        day_broken = navy_day + (2 if ccg_intensity == "Low" else 3)
        collapse_day = None
        
        for day in range(1, 31):
            if day >= day_broken:
                blockade_active = False

            daily_inflow = 0.0
            for v in sim_fleet:
                if v["active"] and v["arrival_day"] == day:
                    if blockade_active:
                        v["arrival_day"] += 1
                    else:
                        success_rate = 0.90 if ccg_intensity == "Low" else (0.80 if ccg_intensity == "Medium" else 0.60)
                        if np.random.random() < success_rate:
                            daily_inflow += v["capacity_ton"]
                            v["active"] = False
                        else:
                            v["arrival_day"] += 1

            inventory_pct = self.current_inventory / self.max_capacity
            
            if inventory_pct <= 0.0:
                if collapse_day is None:
                    collapse_day = day
                demand = 0.0
                status = "Blackout"
            elif inventory_pct < 0.10:
                demand = self.daily_consumption * 0.40
                status = "TSMC Priority"
            elif inventory_pct < 0.25:
                demand = self.daily_consumption * 0.70
                status = "Industrial Cuts"
            else:
                demand = self.daily_consumption
                status = "Normal"

            if inventory_pct > 0.0:
                self.current_inventory = max(0.0, min(self.max_capacity, self.current_inventory + daily_inflow - demand))

            clarkson = min(450000, 75000 * (1.0 + (day * 0.12) + (self.pull_out_prob * 3.8)))
            
            history.append({
                "Day": day,
                "Inventory%": (self.current_inventory / self.max_capacity) * 100,
                "Clarkson_Spot": clarkson,
                "Grid_Status": status
            })
            
        return collapse_day, cargoes_lost, pd.DataFrame(history)

# Run simulation on input adjustments
sim = DynamicInteractiveEngine()
fail_day, ships_lost, df_results = sim.run()

# 4. Main Panel Response Board
col1, col2, col3 = st.columns(3)
with col1:
    if fail_day:
        st.metric(label="⚠️ System Infrastructure Status", value=f"COLLAPSE ON DAY {fail_day}", delta="CRITICAL FAILURE", delta_color="inverse")
    else:
        st.metric(label="✅ System Infrastructure Status", value="STABLE RUN", delta="SUSTAINED INTEGRITY")
with col2:
    st.metric(label="🚢 Peak Clarkson LNG Spot Rate", value=f"${int(df_results['Clarkson_Spot'].max()):,}/day", delta="MARKET CEILING REACHED" if df_results['Clarkson_Spot'].max() >= 450000 else None)
with col3:
    st.metric(label="📉 Commercial Cargo Integrity", value=f"{ships_lost} Aborted Journeys", delta=f"{len(sim.fleet)-ships_lost} Vessels Sailing")

st.markdown("### 📊 Simulated Operational Time Series")

# Step 2: Live Matplotlib Rendering
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 6), sharex=True)

ax1.plot(df_results["Day"], df_results["Inventory%"], color="#003366", linewidth=3, label="LNG Stockpile")
ax1.axhline(25, color="orange", linestyle="--", alpha=0.5, label="Industrial Limit (25%)")
ax1.axhline(10, color="red", linestyle="--", alpha=0.5, label="TSMC Collapse Limit (10%)")
ax1.set_ylabel("Gas Inventory (%)")
ax1.legend(loc="upper right")
ax1.grid(True, alpha=0.3)

ax2.plot(df_results["Day"], df_results["Clarkson_Spot"], color="#990000", linewidth=2.5, label="Clarkson Index")
ax2.set_ylabel("Spot Rate ($/Day)")
ax2.set_xlabel("Crisis Timeline (Days)")
ax2.yaxis.set_major_formatter("${x:,.0f}")
ax2.grid(True, alpha=0.3)

st.pyplot(fig)
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME
# ---------------------------------------------------------
st.set_page_config(
    page_title="Drake Semiconductor Supply Chain Resilience Engine (2026)",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛡️ Semiconductor Supply Chain Survival Engine")
st.caption("Based on data from the 'Drake Semiconductor Supply Chain Analysis (2026).docx' report.")
st.markdown("---")

# ---------------------------------------------------------
# 2. SIDEBAR - CONTROL PANEL (STRATEGIC LEVERS)
# ---------------------------------------------------------
st.sidebar.header("🕹️ Core Control Panel")
st.sidebar.markdown("Select a **Stacked Intervention Package** to evaluate its impact on Taiwan's survival window and the global chip supply:")
# --- CHIP-FAB WATER SECURITY LEVER ---
water_tier = st.sidebar.selectbox(
    "💧 Chip-Fabs Water Security Posture:",
    options=[
        "Standard Municipal Feed (Grid Dependent)",
        "On-Site Ultra-Pure Water (UPW) Reclamation",
        "Hardened Desalination + Local Power Micro-Grid"
    ],
    index=0
)
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
# Define the water tier variable for the app
water_tier = st.sidebar.selectbox(
    "💧 Chip-Fabs Water Security Posture:",
    options=[
        "Standard Municipal Feed (Grid Dependent)",
        "On-Site Ultra-Pure Water (UPW) Reclamation",
        "Hardened Desalination + Local Power Micro-Grid"
    ],
    index=0
)
# New Water Security Interdependency Impact Summary
    if water_tier == "Standard Municipal Feed (Grid Dependent)":
        st.error(
            "💧 **Water-Energy Cascade Disruption:** High-voltage grid instability forces a "
            "shutoff at municipal pumping stations. Without on-site Ultra-Pure Water (UPW) "
            "reclamation, wafer production hits an absolute halt due to filtration failure."
        )
    elif water_tier == "On-Site Ultra-Pure Water (UPW) Reclamation":
        st.warning(
            "🔄 **Recycling Buffer Active:** Closed-loop recycling nodes at the fab level mitigate "
            "the initial municipal drop. The system maintains internal water circulation, buying "
            "crucial operational days independent of the civilian grid."
        )
    else:
        st.success(
            "🌊 **Complete Infrastructure Decoupling:** Hardened coastal desalination units paired "
            "with dedicated energy micro-grids completely insulate chip manufacturing from external "
            "infrastructure attrition."
        )
# Insert this right under where you define package_tier = st.sidebar.radio(...)

# Dynamic White Paper Context Bridge
with st.sidebar.expander("🔍 View Tier Blueprint Details"):
    if package_tier == "Status Quo (No Intervention)":
        st.markdown("""
        **Operational Reality:**
        * **Helium:** Just-In-Time (JIT) reliance; no strategic buffers.
        * **Specialty Gases:** 0-day defensive runway.
        * **Energy:** High vulnerability to MOEA rationing and immediate grid fracture.
        * **Outcome:** Deterministic logistics failure within standard baseline window.
        """)
    elif package_tier == "Moderate Investment Package":
        st.markdown("""
        **Infrastructure Requirements:**
        * Establish a baseline **5-day Helium buffering** reserve.
        * Expand **Specialty Precursor Gas** strategic storage to cover an additional +10 to 14 days.
        * **Focus:** Designed to absorb minor localized maritime shocks, but vulnerable to a sustained blockade.
        """)
    elif package_tier == "Advanced Resilience Package":
        st.markdown("""
        **Strategic Infrastructure Blueprint:**
        * Implement **Helium Recycling Systems** alongside local buffers (+4 to 6 days).
        * Construct the **Subsea Strategic Molecule Pipeline (SSMP)** to bypass physical terrestrial logistics chokepoints (+15 to 20 days).
        * Physical hardening of the **Zhunan Air Separation Unit (ASU)** energy node (+7 days).
        """)
    elif package_tier == "Full Strategic Resilience Package":
        st.markdown("""
        **Deterrence Level Infrastructure:**
        * Construct hardened, decentralized **60-day strategic Helium reserve** facilities.
        * Scale domestic synthesis of **Neon and rare etching gases** to bypass import reliance (+20 days).
        * Full integration of **hardened energy micro-grids / SMR nodes** (+30+ days).
        * Massive **LNG storage expansion** to break the standard physical limits.
        """)
# Initialize variables based on report metrics
helium_boost = 0
gas_boost = 0
grid_boost = 0
lng_boost = 0
capex_tier = "None"
efficiency = "N/A"

if package_tier == "Status Quo (No Intervention)":
    helium_boost = 0    # No strategic buffer
    gas_boost = 0       # JIT delivery dependency
    grid_boost = 0      # Vulnerable to MOEA rationing[cite: 1]
    lng_boost = 0       # Bound to physical 11-day constraint[cite: 1]
    capex_tier = "Zero"
    efficiency = "Poor (Deterministic Failure)"

elif package_tier == "Moderate Investment Package":
    helium_boost = 5    # Helium buffering[cite: 1]
    gas_boost = 12      # Specialty gas strategic buffering (+10 to 14 days)[cite: 1]
    grid_boost = 0
    lng_boost = 0       # Missing critical energy multiplier[cite: 1]
    capex_tier = "Low - Medium"
    efficiency = "Excellent for local shocks, vulnerable to sustained blockade"

elif package_tier == "Advanced Resilience Package":
    helium_boost = 7    # Helium recycling + buffering (+4 to 6 days)[cite: 1]
    gas_boost = 14      # Expanded specialty gas storage[cite: 1]
    grid_boost = 7      # Zhunan ASU Hardening (+7 days)[cite: 1]
    lng_boost = 17      # Subsea Strategic Molecule Pipeline (SSMP) implementation (+15 to 20 days)[cite: 1]
    capex_tier = "High"
    efficiency = "Good Impact (Bypasses terrestrial logistical failure points)"

elif package_tier == "Full Strategic Resilience Package":
    helium_boost = 10   # Hardened 60-day helium reserve systems[cite: 1]
    gas_boost = 20      # Domestic neon and rare gas scaling[cite: 1]
    grid_boost = 25     # Hardened energy nodes / SMR integration (+30+ days)[cite: 1]
    lng_boost = 40      # LNG storage expansion multiplier (>30 days)[cite: 1]
    capex_tier = "Very High"
    efficiency = "Strategic Deterrence Threshold Achieved"

# Contextual Scenario Selector
st.sidebar.markdown("---")
st.sidebar.header("⚠️ Disruption Threat Vector")
scenario_type = st.sidebar.selectbox(
    "Select Red Team Threat Vector:",
    options=["Scenario A: Full Maritime Blockade", "Scenario B: Gray-Zone Harassment", "Scenario C: LNG Shock Event"]
)

# Anchor base timelines according to the technical report parameters
if scenario_type == "Scenario A: Full Maritime Blockade":
    base_mean = 12      # 10-14 day baseline failure window[cite: 1]
    base_std = 2
elif scenario_type == "Scenario B: Gray-Zone Harassment":
    base_mean = 31      # 28-35 day baseline failure window[cite: 1]
    base_std = 4
else:
    base_mean = 6.5     # 5-8 day baseline failure window due to immediate grid fracture[cite: 1]
    base_std = 1

# ---------------------------------------------------------
# 3. MATHEMATICAL CORE - MONTE CARLO SIMULATION LAYER
# ---------------------------------------------------------
runs = 10000
timeline_days = 90

# Calculate total resilience boost
total_resilience_boost = helium_boost + gas_boost + grid_boost + lng_boost

# Compute baseline vs simulated survival distributions using a normal distribution
np.random.seed(42)  # Maintain consistency across runs
simulated_baseline = np.random.normal(base_mean, base_std, runs)
simulated_protected = simulated_baseline + total_resilience_boost

# Generate survival probability vectors over a 90-day horizon
timeline = np.arange(0, timeline_days)
prob_baseline = np.array([(simulated_baseline > t).mean() for t in timeline])
prob_protected = np.array([(simulated_protected > t).mean() for t in timeline])

# Calculate metric deliverables
mean_survival_days = int(np.mean(simulated_protected))
if mean_survival_days < 20:
    status_color = "🔴 System Collapse Critical"
elif mean_survival_days <= 45:
    status_color = "🟠 Partial Resilience Elasticity"
elif mean_survival_days <= 60:
    status_color = "🟡 Strategic Stability Maintained"
else:
    status_color = "🟢 Strategic Deterrence Threshold Achieved"

# ---------------------------------------------------------
# 4. OUTPUT PANEL - EXECUTIVE REVENUE & RESULTS KEYS
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="Expected Semiconductor Survival Floor", 
        value=f"{mean_survival_days} Days", 
        delta=f"+{total_resilience_boost} Days Added" if total_resilience_boost > 0 else "0 Days"
    )
with col2:
    st.metric(label="System Operational Status", value=status_color)
with col3:
    st.metric(label="CAPEX Investment Tier Required", value=capex_tier)

st.markdown("---")

# ---------------------------------------------------------
# 5. VISUAL MODEL - THE SURVIVAL CURVE PLOT
# ---------------------------------------------------------
st.subheader("📊 Probability-Weighted Supply Chain Survival Curve")
st.markdown("This projection shows the probability of maintaining advanced semiconductor and AI chip output over time.")
# Insert this right above your plot configuration (around Section 5)
plt.style.use('dark_background') 

fig, ax = plt.subplots(figsize=(10, 4.5))
# ... your existing custom color overrides follow ...
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(timeline, prob_baseline * 100, label="Baseline Posture (Unprotected)", color="#d9534f", linestyle="--", linewidth=2)
ax.plot(timeline, prob_protected * 100, label=f"Simulated Posture ({package_tier})", color="#0275d8", linewidth=3)

# Aesthetic formatting
ax.set_facecolor("#121212")
fig.patch.set_facecolor("#121212")
ax.spines['bottom'].set_color('#cccccc')
ax.spines['top'].set_color('#333333')
ax.spines['right'].set_color('#333333')
ax.spines['left'].set_color('#cccccc')
ax.xaxis.label.set_color('#cccccc')
ax.yaxis.label.set_color('#cccccc')
ax.tick_params(axis='x', colors='#cccccc')
ax.tick_params(axis='y', colors='#cccccc')

ax.set_xlabel("Days Elapsed Under Disruption Scenario")
ax.set_ylabel("Probability of Sustained Global Supply (%)")
ax.set_xlim(0, timeline_days)
ax.set_ylim(0, 105)
ax.grid(True, linestyle=":", alpha=0.3, color="#555555")
ax.legend(facecolor="#222222", edgecolor="#444444", labelcolor="#cccccc")

st.pyplot(fig)

# ---------------------------------------------------------
# 6. GLOBAL SUPPLY ANALYSIS & STRATEGIC DECISION MATRIX
# ---------------------------------------------------------
st.markdown("---")
st.subheader("🗺️ Global Strategic Impact & Critical AI Supply Analysis")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🏬 Impact on Global Supply Chains")
    if mean_survival_days < 14:
        st.error(
            "⚠️ **Immediate Global AI & Tech Collapse:** Industrial paralysis begins within days. "
            "Advanced node manufacturing ($\le 3\\text{nm}$) faces an immediate Cold-Halt due to helium and power failure. "
            "The loss to the global economy exceeds **$250 Billion per week** as consumer tech, automotive, and AI server pipelines freeze."
        )
    elif mean_survival_days <= 30:
        st.warning(
            "⚡ **Severe Market Friction & Yield Erosion:** The system buys short-term stability but suffers chronic molecule arrhythmia. "
            "Global tech companies draw down downstream inventory. Global chip pricing experiences extreme volatility as "
            "advanced fabrication relies heavily on high-frequency land transport pipelines susceptible to localized disruptions."
        )
    elif mean_survival_days <= 60:
        st.info(
            "🛡️ **Allied Buffer Window:** The supply chain resists rapid transition into degraded states. "
            "By deploying the Subsea Strategic Molecule Pipeline (SSMP) and domestic scaling, Taiwan buys a buffer window of up to "
            "two months. This provides international frameworks time to execute maritime logistics escorts."
        )
    else:
        st.success(
            "💎 **Total Strategic Sovereignty:** Shifting from terrestrial, JIT reliance to independent subsea loops and hardened "
            "micro-grids pushes the industrial floor past the critical 60-day window. This changes the geopolitical risk-reward calculus, "
            "effectively neutralizing non-kinetic supply coercion."
        )

with col_right:
    st.markdown("### 📋 Stacked Investment Efficiency Breakdown")
    st.write(f"**Current Strategy Analysis:** {efficiency}")
    
    # Interactive Data Matrix Output
    st.markdown("**Intervention Factor Allocation Matrix**")
    st.json({
        "Strategic Helium Allocation Buffer": f"+{helium_boost} Days Output Validity",
        "Specialty Precursor Molecule Gas Buffering": f"+{gas_boost} Days Operational Runway",
        "Grid Hardening & Local ASU Prioritization": f"+{grid_boost} Power Isolation Window",
        "LNG Sovereign Storage Base Multiplier": f"+{lng_boost} Core System Buffer Extension"
    })

st.markdown("---")
st.caption("Strategic Decision Engine Layer • Integrated Systemic Attrition Model (2026) • Drake Institute of Geostrategic Intelligence.")
