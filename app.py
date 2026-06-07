import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

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
