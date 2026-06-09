# Triggering redeploy
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, ALL
import plotly.graph_objects as go
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
# --- INITIALIZATION ---
# This 'app' variable is what your callbacks need


# ... now your existing helper functions and code follow below ...


# --- STEP 3: MASTER MATH ENGINES, REPOSITORY POPULATION, & CALLBACKS ---

# Helper function to compute the resilience scaling multiplier based on the temporal engine and switches
def calculate_multipliers(temporal_stage, active_switches):
    # 2025-2035 Runway allows a high mitigation impact (+25%), 2035-2050 Closure limits it (+5%)
    switch_efficiency = 0.25 if temporal_stage == 0 else 0.05
    
    # Calculate dampener modifiers based on active policy switches
    emp_boost = switch_efficiency if "emp" in active_switches else 0.0
    ubo_delay = True if "ubo" in active_switches else False
    academic_shield = True if "academic" in active_switches else False
    defense_boost = 0.15 if "defense" in active_switches else 0.0
    
    # Base acceleration factor (shifter for decay curves depending on the timeline era)
    temporal_decay_multiplier = 1.0 if temporal_stage == 0 else 1.5
    
    return emp_boost, ubo_delay, academic_shield, defense_boost, temporal_decay_multiplier
# ... (Imports and Initialization) ...
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# ADD THIS: The Master Layout
app.layout = dbc.Container([
    html.H1("National Resilience Engine", className="text-white my-4"),
    
    # 1. The Tabs
    dcc.Tabs(id="core-module-tabs", value='tab-1', children=[
        dcc.Tab(label='Simulation Engine', value='tab-1'),
        dcc.Tab(label='Policy Settings', value='tab-2'),
    ]),
    
    # 2. The area where your callbacks will put the content
    html.Div(id='tabs-content-example', className="mt-4"),
    
    # 3. Add your grid container here so it exists on the page
    html.Div(id="restricted-grid-container"),
    
    # 4. Hidden store for state (if you use it)
    dcc.Store(id="global-dummy-state")
], fluid=True, style={"backgroundColor": "#0f1219", "minHeight": "100vh"})

# ... (Now all your functions and callbacks follow) ...

# Central Unified Callback to run the simulation engines for all 4 tabs simultaneously
@app.callback(
    [Output("infra-metric-kaohsiung", "children"),
     Output("infra-metric-lng", "children"),
     Output("infra-metric-water", "children"),
     Output("infra-simulation-graph", "figure"),
     Output("c2-matrix-table-container", "children"),
     Output("c2-simulation-graph", "figure"),
     Output("semi-metric-value", "children"),
     Output("semi-metric-mirror", "children"),
     Output("semi-simulation-graph", "figure"),
     Output("asymmetric-threat-alert-box", "children"),
     Output("spark-simulation-graph", "figure")],
    [Input("core-module-tabs", "active_tab"),
     Input("escalation-slider", "value"),
     Input("temporal-slider", "value"),
     Input("switch-emp", "value"),
     Input("switch-ubo", "value"),
     Input("switch-academic", "value"),
     Input("switch-defense", "value")]
)
def run_national_resilience_simulation(active_tab, escalation, temporal, emp_sw, ubo_sw, acad_sw, def_sw):
    # Collect collective switch values
    active_switches = []
    if emp_sw: active_switches.append("emp")
    if ubo_sw: active_switches.append("ubo")
    if acad_sw: active_switches.append("academic")
    if def_sw: active_switches.append("defense")
    
    # Extract calculated mathematical multipliers
    emp_boost, ubo_delay, academic_shield, defense_boost, decay_mult = calculate_multipliers(temporal, active_switches)
    
    # Prevent callback calculation breaks if components aren't mounted yet
    blank_fig = go.Figure(layout=dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=10, b=10), height=50))
    
    # Initialize all returns with defaults to ensure stable packing layout
    k_html, l_html, w_html = "", "", ""
    infra_fig = blank_fig
    c2_table_html = ""
    c2_fig = blank_fig
    semi_val_html, semi_mir_html = "", ""
    semi_fig = blank_fig
    spark_alert_html = ""
    spark_fig = blank_fig

    # =========================================================================
    # MODULE 1 ENGINE: PHYSICAL INFRASTRUCTURE LIFELINES
    # =========================================================================
    # 1. Kaohsiung Logistics Timeline
    if escalation <= 2:
        k_cap = 100 if not ubo_delay else 100
        k_status, k_color = "BASELINE STABLE", ACCENT_SUCCESS
    elif escalation in [3, 4]:
        k_cap = 60 if ubo_delay else 40
        k_status, k_color = "QUARANTINE DELAY (T+0 to T+3)", ACCENT_WARN
    else: # Stages 5-6
        k_cap = 35 if ubo_delay else 15
        k_status, k_color = "CRITICAL ASPHYXIATION (T+11+ Days)", ACCENT_FAIL
        
    k_html = html.Div([
        html.Div("KAOHSIUNG PORT CAPACITY", style={"fontSize": "0.75rem", "color": TEXT_MUTED}),
        html.H4(f"{k_cap}%", style={"color": k_color, "margin": "0"}),
        html.Div(k_status, style={"fontSize": "0.65rem", "color": "#fff", "fontWeight": "bold"})
    ])
    
    # 2. LNG Grid Compression State
    lng_phase = min(max(1, escalation - 2), 4) if escalation > 2 else 1
    if lng_phase == 1: lng_lbl, lng_color = "PHASE 1: NORMAL", ACCENT_SUCCESS
    elif lng_phase == 2: lng_lbl, lng_color = "PHASE 2: THROTTLED", ACCENT_INFO
    elif lng_phase == 3: lng_lbl, lng_color = "PHASE 3: CURTAILMENT", ACCENT_WARN
    else: lng_lbl, lng_color = "PHASE 4: ISOLATION", ACCENT_FAIL
    
    l_html = html.Div([
        html.Div("LNG RESERVES SYSTEM STATE", style={"fontSize": "0.75rem", "color": TEXT_MUTED}),
        html.H5(lng_lbl, style={"color": lng_color, "margin": "4px 0"}),
        html.Div(f"System Redundancy -{(escalation-1)*12}%", style={"fontSize": "0.65rem", "color": "#fff"})
    ])
    
    # 3. Water Utilities Degradation Buffer
    if escalation >= 4:
        w_lbl, w_color, w_sub = "7-DAY BUFFER COUNTDOWN", ACCENT_FAIL, "Pressure failure cascade risk"
    else:
        w_lbl, w_color, w_sub = "BUFFERS FUNCTIONAL", ACCENT_SUCCESS, "Grid utility pressure normal"
        
    w_html = html.Div([
        html.Div("WATER / SANITATION INTEGRITY", style={"fontSize": "0.75rem", "color": TEXT_MUTED}),
        html.H5(w_lbl, style={"color": w_color, "margin": "4px 0"}),
        html.Div(w_sub, style={"fontSize": "0.65rem", "color": "#fff"})
    ])
    
    # Generate Infrastructure Chart Waveform
    x_timeline = [f"T+{d} Days" for d in range(0, 15)]
    # Mathematical decay model matching calculated compound stress parameters
    y_infra = [max(min(100 - (i * (escalation * 1.3) * decay_mult) + (emp_boost * 100), 100), 10) for i in range(0, 15)]
    
    infra_fig = {
        'data': [go.Scatter(x=x_timeline, y=y_infra, mode='lines+markers', name='Functional Integrity Index', line=dict(color=ACCENT_INFO, width=3))],
        'layout': go.Layout(
            title=dict(text=f"Predictive Infrastructure Decay Curve (Stage {escalation} Parameters)", font=dict(color='#fff', size=12)),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#1e222b', tickfont=dict(color='#888')),
            yaxis=dict(gridcolor='#1e222b', tickfont=dict(color='#888'), title="System Performance %", range=[0, 105]),
            margin=dict(l=50, r=20, t=40, b=30), height=260
        )
    }

    # =========================================================================
    # MODULE 2 ENGINE: 5-LAYERED COMMUNICATION DEFENCE STRATEGY
    # =========================================================================
    # Build dynamic status attributes for the communication array
    leo_h = max(95 - (escalation * 12 * decay_mult) + (defense_boost * 100), 20)
    leo_stat = "ACTIVE" if leo_h > 50 else ("THROTTLED" if leo_h > 30 else "JAMMED / OVERLOAD")
    
    hars_stat = "STANDBY" if escalation < 3 else "ACTIVE FAILOVER"
    hars_h = 90 if escalation < 3 else max(85 - (escalation * 4), 45)
    
    tropo_stat = "OFFLINE (SECURE)" if escalation < 4 else "ENCRYPTED LINK ACTIVE"
    tropo_h = 100 if escalation < 4 else max(90 - (escalation * 2), 70)
    
    fiber_h = max(95 - (escalation * 15 * decay_mult), 10)
    fiber_stat = "ROUTING NORMAL" if fiber_h > 60 else "COMPROMISED / RE-ROUTED"
    
    uhf_h = 75 + int(defense_boost * 15)
    uhf_stat = "EMERGENCY READY"
    
    # Render premium status matrix diagnostic table rows
    c2_table_html = dbc.Table([
        html.Thead(html.Tr([html.Th("Communication Defense Layer"), html.Th("Operational Status"), html.Th("Signal Health Index")])),
        html.Tbody([
            html.Tr([html.Td("Layer 1: LEO Satellite Array", className="fw-bold"), html.Td(leo_stat), html.Td(f"{int(leo_h)}%", className="text-info")]),
            html.Tr([html.Td("Layer 2: High-Altitude Radio Systems (HARS)", className="fw-bold"), html.Td(hars_stat), html.Td(f"{int(hars_h)}%", className="text-info")]),
            html.Tr([html.Td("Layer 3: Troposcatter Array Backbone", className="fw-bold"), html.Td(tropo_stat), html.Td(f"{int(tropo_h)}%", className="text-info")]),
            html.Tr([html.Td("Layer 4: Hardened Terrestrial Fiber Network", className="fw-bold"), html.Td(fiber_stat), html.Td(f"{int(fiber_h)}%", className="text-info")]),
            html.Tr([html.Td("Layer 5: HF/VHF/UHF Resilient Tactical Radio", className="fw-bold"), html.Td(uhf_stat), html.Td(f"{int(uhf_h)}%", className="text-info")]),
        ])
    ], bordered=True, dark=True, hover=True, responsive=True, size="sm", className="bg-black small border-secondary text-light")
    
    # Render C2 Health bar matrix representation
    c2_fig = {
        'data': [go.Bar(x=["LEO", "HARS", "Tropo", "Fiber", "HF/UHF"], y=[leo_h, hars_h, tropo_h, fiber_h, uhf_h], marker_color=ACCENT_SUCCESS, width=0.4)],
        'layout': go.Layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#888')), yaxis=dict(gridcolor='#1e222b', tickfont=dict(color='#888'), range=[0, 105]),
            margin=dict(l=40, r=20, t=10, b=30), height=140
        )
    }

    # =========================================================================
    # MODULE 3 ENGINE: SILICON SHIELD ANALYSIS
    # =========================================================================
    base_val = 155.8 # Billions USD
    current_val = max(base_val - (escalation * 22.5 * decay_mult), 12.0)
    
    semi_val_html = html.Div([
        html.Div("ADVANCED FAB NODE EXPORT RUNRATE (<7nm)", style={"fontSize": "0.75rem", "color": TEXT_MUTED}),
        html.H4(f"${current_val:.1f}B USD", style={"color": ACCENT_WARN if current_val > 50 else ACCENT_FAIL, "margin": "0"}),
        html.Div("Estimated quarterly baseline throughput", style={"fontSize": "0.65rem", "color": "#fff"})
    ])
    
    mirror_rate = 98 if academic_shield else max(98 - (escalation * 14 * decay_mult), 30)
    semi_mir_html = html.Div([
        html.Div("OFFSHORE PROCESS SCHEMA MIRRORING", style={"fontSize": "0.75rem", "color": TEXT_MUTED}),
        html.H4(f"{int(mirror_rate)}%", style={"color": ACCENT_SUCCESS if mirror_rate > 80 else ACCENT_WARN, "margin": "0"}),
        html.Div("Fab recipe redundancy & code lockouts", style={"fontSize": "0.65rem", "color": "#fff"})
    ])
    
    # Advanced node manufacturing buffer runway countdown math
    x_nodes = ["Industrial Gases", "Raw Ingestion", "Lithography", "Testing Array", "Global Outbound"]
    y_semi = [max(100 - (escalation * i * 3 * decay_mult), 15) for i in range(1, 6)]
    if emp_sw: y_semi = [min(v + 15, 100) for v in y_semi]
    
    semi_fig = {
        'data': [go.Scatter(x=x_nodes, y=y_semi, fill='tozeroy', mode='none', fillcolor='rgba(243, 156, 18, 0.15)', name='Node Security Buffer')],
        'layout': go.Layout(
            title=dict(text="Supply Dependency Pipeline Continuity Buffer", font=dict(color='#fff', size=11)),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(color='#888')), yaxis=dict(gridcolor='#1e222b', tickfont=dict(color='#888'), range=[0, 105]),
            margin=dict(l=40, r=20, t=30, b=30), height=200
        )
    }

    # =========================================================================
    # MODULE 4 ENGINE: ASYMMETRIC FLASHPOINTS
    # =========================================================================
    shock_index = escalation * 16
    if academic_shield: shock_index -= 20
    shock_index = max(min(shock_index, 100), 5)
    
    if escalation >= 4 and not academic_shield:
        alert_text = "CRITICAL: Dual-use technology transfer risk flagged. Malware telemetry scraping active."
        alert_col = "danger"
    elif escalation >= 3:
        alert_text = "WARNING: Asymmetric coordinate drift detected around strategic infrastructure hubs."
        alert_col = "warning"
    else:
        alert_text = "System Nominal. Asymmetric monitoring scripts scanning gray-zone vectors."
        alert_col = "success"
        
    spark_alert_html = dbc.Alert(alert_text, color=alert_col, className="py-2 small small font-weight-bold text-center")
    
    # 7 Mapped Sleeper Scenarios Coordinate Vectors
    scenarios = ["Qixingtan Spark", "Hualien Link", "Network Spoof", "Financial Decouple", "Port Subversion", "Transit Stasis", "Media Infiltration"]
    probability_y = [max(min((escalation * 14) + (i*4) - (25 if academic_shield else 0), 95), 10) for i in range(7)]
    impact_x = [20, 35, 45, 60, 75, 80, 90]
    
    spark_fig = {
        'data': [go.Scatter(
            x=impact_x, y=probability_y, mode='markers+text',
            text=scenarios, textposition="top center",
            marker=dict(size=12, color=ACCENT_FAIL, symbol="diamond"),
            textfont=dict(color="#fff", size=9)
        )],
        'layout': go.Layout(
            title=dict(text="Asymmetric Scenarios: Probability vs Strategic Impact Matrix", font=dict(color='#fff', size=11)),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Strategic Shock Level", gridcolor='#1e222b', tickfont=dict(color='#888'), range=[0, 110]),
            yaxis=dict(title="Active Threat Probability %", gridcolor='#1e222b', tickfont=dict(color='#888'), range=[0, 110]),
            margin=dict(l=50, r=30, t=40, b=40), height=220
        )
    }

    return (k_html, l_html, w_html, infra_fig, 
            c2_table_html, c2_fig, 
            semi_val_html, semi_mir_html, semi_fig, 
            spark_alert_html, spark_fig)


# --- STEP 3: INJECT COMPONENT GRID GENERATOR FOR TIER 2 REPOSITORY ---
@app.callback(
    Output("restricted-grid-container", "children"),
    Input("global-dummy-state", "data")
)
def populate_restricted_ui(_):
    premium_papers = [
        {"title": "WP - Ghost Strike", "desc": "Covert EMP & Grid Compression Dynamics", "mod": "Module 1: Physical Disruption"},
        {"title": "WP - Silent Horizon", "desc": "Radar Blackout & Tactical Network Spoofing", "mod": "Module 1: Physical Disruption"},
        {"title": "WP - Operation Big Bertha", "desc": "Maritime Lawfare & Blockade Quarantine Stasis", "mod": "Module 2: Maritime Strategy"},
        {"title": "WP - Defeating the Shadow War", "desc": "Hybrid Assault & Institutional Trust Erosion", "mod": "Module 3: Cognitive & Subversion"},
        {"title": "WP - The Dove vs. The Hawk", "desc": "U.S. Leadership Posture Variance Engines", "mod": "Module 4: Geopolitical Variance"},
        {"title": "WP - The Bomb Taiwan Never Had", "desc": "Historical Sovereign Restriction Baselines", "mod": "Module 4: Geopolitical Variance"},
        {"title": "WP - South China Sea IQ Test", "desc": "Gray-Zone Force Adjustments & Signaling", "mod": "Module 6: Regional Context"},
        {"title": "WP - The Sino Neo-Tanaka Plan", "desc": "Indo-Pacific Deterrence Collapse Framework", "mod": "Module 6: Regional Context"}
    ]
    
    return dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Div(wp["mod"], style={"fontSize": "0.7rem", "color": ACCENT_WARN, "letterSpacing": "1px"}, className="fw-bold mb-1"),
                    html.H6(wp["title"], className="text-white mb-1", style={"fontSize": "0.85rem"}),
                    html.P(wp["desc"], className="text-muted small mb-3", style={"fontSize": "0.75rem", "lineHeight": "1.2"}),
                    dbc.Button(
                        [html.I(className="bi bi-lock-fill me-1"), "Inspect Pipeline"],
                        id={'type': 'restricted-node', 'index': i},
                        color="outline-warning", size="sm", className="w-100 text-start btn-sm p-1 ps-2",
                        style={"fontSize": "0.75rem", "borderColor": "#22252e"}
                    )
                ]),
                style={"backgroundColor": INNER_BG, "borderColor": BORDER_COLOR},
                className="h-100"
            ),
            width=6, className="mb-3"
        ) for i, wp in enumerate(premium_papers)
    ])


# --- STEP 3: CONTROL INTERACTION OVERLAYS FOR MODALS ---
@app.callback(
    [Output("premium-licensing-modal", "is_open"), Output("premium-modal-content", "children")],
    [Input({'type': 'restricted-node', 'index': ALL}, 'n_clicks'), Input("close-premium-modal-btn", "n_clicks")],
    [State("premium-licensing-modal", "is_open")]
)
def handle_restricted_modals(lock_clicks, close_click, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open, dash.no_update
        
    triggered_id = ctx.triggered[0]['prop_id']
    if "close-premium-modal-btn" in triggered_id:
        return False, dash.no_update
        
    if "restricted-node" in triggered_id and any(lock_clicks):
        premium_papers = [
            {"title": "WP - Ghost Strike", "desc": "Covert EMP & Grid Compression Dynamics", "details": "Models covert high-altitude electromagnetic pulse impacts across domestic defensive infrastructure coordinates, evaluating real-time localized energy isolation times and black-start backup capabilities."},
            {"title": "WP - Silent Horizon", "desc": "Radar Blackout & Tactical Network Spoofing", "details": "Simulates multi-domain optical and electromagnetic blindness across primary early-warning defense installations, mapping systemic latencies during active spoofing windows."},
            {"title": "WP - Operation Big Bertha", "desc": "Maritime Lawfare & Blockade Quarantine Stasis", "details": "Maps out a scenario where an adversary uses legal and commercial quarantines rather than open kinetic engagement to restrict maritime trade routes without triggering international tripwires."},
            {"title": "WP - Defeating the Shadow War", "desc": "Hybrid Assault & Institutional Trust Erosion", "details": "Tracks gray-zone economic coercion and structural cognitive attacks designed to target critical media infrastructure, financial protocols, and community trust networks."},
            {"title": "WP - The Dove vs. The Hawk", "desc": "U.S. Leadership Posture Variance Engines", "details": "Calculates defense dependency timelines by cross-referencing shifting geopolitical postures and security agreement parameters under divergent Western political leadership scenarios."},
            {"title": "WP - The Bomb Taiwan Never Had", "desc": "Historical Sovereign Restriction Baselines", "details": "A detailed doctrinal lookup tool examining legacy structural limitations placed on sovereign defensive programs, establishing an analytical baseline for current vulnerability matrices."},
            {"title": "WP - South China Sea IQ Test", "desc": "Gray-Zone Force Adjustments & Signaling", "details": "Triggers multi-vector tactical naval deployments to model gray-zone deterrence thresholds, commercial shipping re-routing protocols, and maritime signaling dynamics."},
            {"title": "WP - The Sino Neo-Tanaka Plan", "desc": "Indo-Pacific Deterrence Collapse Framework", "details": "Tracks regional industrial decoupling pathways, raw material access channels, and institutional vulnerability mapping to model structural deterrence decay."}
        ]
        
        try:
            clicked_index = eval(triggered_id.split(".")[0])["index"]
            wp = premium_papers[clicked_index]
        except:
            wp = {"title": "Restricted Framework Module", "desc": "", "details": "Strategic analytical data node."}
            
        modal_body = html.Div([
            html.H4(wp["title"], className="text-warning mb-1"),
            html.P(wp["desc"], className="text-muted small mb-4", style={"fontStyle": "italic"}),
            html.H6("ANALYTICAL MODULE OVERVIEW:", className="text-white small fw-bold"),
            html.P(wp["details"], className="text-light small mb-4", style={"lineHeight": "1.5"}),
            html.Hr(style={"borderColor": BORDER_COLOR}),
            html.H6("COMMERCIAL PIPELINE REQUIREMENT:", className="text-danger small fw-bold"),
            html.P("This dataset is integrated exclusively via the Tier 2 Institutional Multi-Year Licensing Framework. Active annual subscriptions grant enterprise environments quarterly threat parameter updates, custom scenario stress-testing variables, and direct analytical access to the Drake Institute team.", className="text-muted small", style={"lineHeight": "1.4"})
        ])
        return True, modal_body
        
    return is_open, dash.no_update


# --- EXECUTION GATEWAYS ---
if __name__ == '__main__':
    # Set to debug=False for live investor presentation delivery environments
    app.run_server(debug=True)
