import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

# --- Functions ---
def calculate_multipliers(temporal_stage, active_switches):
    switch_efficiency = 0.15
    emp_boost = switch_efficiency if "emp" in active_switches else 0.0
    ubo_delay = True if "ubo" in active_switches else False
    academic_shield = True if "academic" in active_switches else False
    defense_boost = 0.15 if "defense" in active_switches else 0.0
    temporal_decay_multiplier = 1.0 if temporal_stage == 0 else 1.5
    return emp_boost, ubo_delay, academic_shield, defense_boost, temporal_decay_multiplier

# --- Master Layout ---
app.layout = dbc.Container([
    html.H1("National Resilience Engine", className="text-white my-4"),
    
    dcc.Tabs(id="core-module-tabs", value='tab-1', children=[
        dcc.Tab(label='Simulation Engine', value='tab-1'),
        dcc.Tab(label='Policy Settings', value='tab-2'),
    ]),
    
    html.Div(id='tabs-content-example', className="mt-4"),

    # Hidden components to satisfy the callback requirements
    html.Div(id="infra-metric-kaohsiung", className="d-none"),
    html.Div(id="infra-metric-lng", className="d-none"),
    html.Div(id="infra-metric-water", className="d-none"),
    dcc.Graph(id="infra-simulation-graph", className="d-none"),
    html.Div(id="c2-matrix-table-container", className="d-none"),
    dcc.Graph(id="c2-simulation-graph", className="d-none"),
    html.Div(id="semi-metric-value", className="d-none"),
    html.Div(id="semi-metric-mirror", className="d-none"),
    dcc.Graph(id="semi-simulation-graph", className="d-none"),
    html.Div(id="asymmetric-threat-alert-box", className="d-none"),
    dcc.Graph(id="spark-simulation-graph", className="d-none"),

    # Input Controls
    dcc.Slider(id="escalation-slider", min=0, max=10, value=5),
    dcc.Slider(id="temporal-slider", min=0, max=1, value=0),
    dcc.Checklist(id="switch-emp", options=[{'label': 'EMP', 'value': 'emp'}], value=[]),
    dcc.Checklist(id="switch-ubo", options=[{'label': 'UBO', 'value': 'ubo'}], value=[]),
    dcc.Checklist(id="switch-academic", options=[{'label': 'Academic', 'value': 'academic'}], value=[]),
    dcc.Checklist(id="switch-defense", options=[{'label': 'Defense', 'value': 'defense'}], value=[]),
], fluid=True)

# --- Central Callback ---
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
    [Input("core-module-tabs", "value"),
     Input("escalation-slider", "value"),
     Input("temporal-slider", "value"),
     Input("switch-emp", "value"),
     Input("switch-ubo", "value"),
     Input("switch-academic", "value"),
     Input("switch-defense", "value")]
)
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
    [Input("core-module-tabs", "value"),
     Input("escalation-slider", "value"),
     Input("temporal-slider", "value"),
     Input("switch-emp", "value"),
     Input("switch-ubo", "value"),
     Input("switch-academic", "value"),
     Input("switch-defense", "value")]
)
def update_all_metrics(tab, esc, temp, emp, ubo, acad, defn):
    # 1. Combine the switches into a list
    active_switches = []
    if emp: active_switches.append("emp")
    if ubo: active_switches.append("ubo")
    if acad: active_switches.append("academic")
    if defn: active_switches.append("defense")
    
    # 2. Get the multipliers
    emp_b, ubo_d, acad_s, def_b, temp_m = calculate_multipliers(temp, active_switches)
    
    # 3. Create the graph figure using these variables
    fig = go.Figure()
    # Using the multipliers to make the graph react to the switches!
    y_values = [10 * (1 + emp_b), (10 - esc) * temp_m, 5, 5 - (esc * 0.5)]
    
    fig.add_trace(go.Scatter(
        x=[0, 1, 2, 3], 
        y=y_values, 
        mode='lines+markers',
        line=dict(color='cyan')
    ))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    # 4. Return the 11 items required by the callback
   # 4. Return the 11 items required by the callback
    # Using a dictionary for empty figures is much more stable for Render
    empty_fig = {"data": [], "layout": {"paper_bgcolor": "rgba(0,0,0,0)", "plot_bgcolor": "rgba(0,0,0,0)"}}
    
    return ["0", "0", "0", fig, "None", empty_fig, "0", "0", empty_fig, "System Nominal", empty_fig]
