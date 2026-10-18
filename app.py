import io
from contextlib import redirect_stdout

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from database.db import Machine, session
from digital_twin.machine import MachineTwin
from agents.machine_agent import MachineAgent
from agents.technician_agent import TechnicianAgent
from agents.scheduler_agent import SchedulerAgent
from agents.cost_agent import CostAgent


st.set_page_config(page_title="Digital Twin", page_icon="⚙️", layout="wide")

st.markdown("""
<style>
    .stApp { background: #07111f; color: #e6eefb; }
    [data-testid="stSidebar"] { background: #081526; border-right: 1px solid #1b2a3d; }
    .block-container { padding-top: 1.4rem; max-width: 1600px; }
    h1, h2, h3 { color: #eaf2ff; }
    .metric-card { background: linear-gradient(135deg, #10243a, #0b1728); border: 1px solid #20364e;
                   border-radius: 12px; padding: 16px; min-height: 126px; }
    .metric-label { color: #8db7e8; font-size: .78rem; font-weight: 700; }
    .metric-value { color: #f6f9ff; font-size: 2rem; font-weight: 800; margin: 6px 0; }
    .metric-note { color: #8fa5bc; font-size: .78rem; }
    .panel { background: #0b1728; border: 1px solid #20364e; border-radius: 12px; padding: 14px; }
    .status-healthy { color: #50d875; font-weight: 700; }
    .status-warning { color: #ffc229; font-weight: 700; }
    .status-critical { color: #ff5b5b; font-weight: 700; }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=5)
def load_data():
    rows = session.query(Machine).order_by(Machine.id.asc()).all()
    return pd.DataFrame([
        {
            "record_id": row.id,
            "Machine ID": row.machine_id,
            "Temperature (°C)": row.temperature,
            "Vibration (mm/s)": row.vibration,
            "Pressure (bar)": row.pressure,
            "RPM": row.rpm,
            "Recorded At": row.timestamp,
        }
        for row in rows
    ])


def build_twin(row):
    return MachineTwin(
        row["Machine ID"],
        row["Temperature (°C)"],
        row["Vibration (mm/s)"],
        row["Pressure (bar)"],
        row["RPM"],
    )


def latest_machine_data(data):
    return data.sort_values("record_id").groupby("Machine ID", as_index=False).tail(1)


def status_class(status):
    return f"status-{status.lower()}"


def card(label, value, note, color):
    st.markdown(
        f'<div class="metric-card" style="border-top: 3px solid {color};">'
        f'<div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div>'
        f'<div class="metric-note">{note}</div></div>',
        unsafe_allow_html=True,
    )


# Load data from database by default
data = load_data()


# Upload sensor file
with st.sidebar:

    st.subheader("📂 Upload Sensor File")

    uploaded_file = st.file_uploader(
        "Choose CSV File",
        type=["csv"]
    )


# If user uploads file, use that data
if uploaded_file:

    data = pd.read_csv(uploaded_file)

    # Rename CSV columns to match dashboard
    data.rename(columns={
        "machine_id": "Machine ID",
        "temperature": "Temperature (°C)",
        "vibration": "Vibration (mm/s)",
        "pressure": "Pressure (bar)",
        "rpm": "RPM"
    }, inplace=True)

    # Add required columns
    data["record_id"] = range(1, len(data) + 1)
    data["Recorded At"] = pd.Timestamp.now()

    st.sidebar.success("File uploaded successfully")

    
with st.sidebar:
    st.markdown("## <span style='color:#34b9ff'>DIGITAL TWIN</span>", unsafe_allow_html=True)
    st.caption("Predictive Maintenance")
    st.divider()
    page = st.radio(
        "DIGITAL TWIN CONTROL",
        ["Dashboard", "Machines", "Live Monitoring", "AI Predictions", "Maintenance"],
        label_visibility="visible",
    )
    st.divider()
    auto_refresh = st.toggle("Auto refresh", value=True)
    st.caption("Refresh data every 5 seconds")
    st.divider()
    st.markdown("**SYSTEM STATUS**  🟢 Online")
    st.caption(f"Database records: {len(data)}")

if auto_refresh:
    st.cache_data.clear()

st.markdown("# Digital Twin Dashboard")
st.caption("Real-time predictive maintenance and multi-agent decision support")

if data.empty:
    st.error("No sensor data is available in factory.db. Run the sensor simulator first.")
    st.stop()

latest = latest_machine_data(data)
twins = [build_twin(row) for _, row in latest.iterrows()]
dashboard_rows = []
for twin in twins:
    # The existing agents also print console reports.  Their return values are
    # what the dashboard needs, so keep the Streamlit terminal clean.
    with redirect_stdout(io.StringIO()):
        technician, action = TechnicianAgent.assign(twin)
        schedule = SchedulerAgent.schedule(twin)
        cost, cost_level = CostAgent.estimate(twin)
        decision = MachineAgent.monitor(twin)
    dashboard_rows.append({
        "Machine ID": twin.machine_id,
        "Temperature (°C)": twin.temperature,
        "Vibration (mm/s)": twin.vibration,
        "Pressure (bar)": twin.pressure,
        "RPM": twin.rpm,
        "Health Score": twin.health,
        "Status": twin.status,
        "Failure Risk": twin.failure_risk,
        "AI Prediction": twin.ai_prediction,
        "Recommendation": twin.recommendation,
        "Decision": decision,
        "Technician": technician,
        "Action": action,
        "Schedule": schedule,
        "Estimated Cost (₹)": cost,
        "Cost Level": cost_level,
    })

dashboard = pd.DataFrame(dashboard_rows)
healthy = (dashboard["Status"] == "Healthy").sum()
warning = (dashboard["Status"] == "Warning").sum()
critical = (dashboard["Status"] == "Critical").sum()
average_health = dashboard["Health Score"].mean()
scheduled = (dashboard["Schedule"] != "Next 30 Days").sum()

if page != "Dashboard":
    st.info(f"The **{page}** view is represented in the dashboard below. Use the sidebar later to add separate pages if needed.")

c1, c2, c3, c4 = st.columns(4)
with c1:
    card("AVERAGE HEALTH SCORE", f"{average_health:.1f}/100", "Across latest machine readings", "#45d66a")
with c2:
    card("MACHINES WARNING", warning, "Schedule inspection within 7 days", "#ffc229")
with c3:
    card("MACHINES CRITICAL", critical, "Immediate maintenance required", "#ff5757")
with c4:
    card("MAINTENANCE SCHEDULED", scheduled, "Machines needing an action", "#2f9bff")

left, right = st.columns([1.15, 1])
with left:
    st.markdown("### Live Machine Status")
    table = dashboard[["Machine ID", "Temperature (°C)", "Vibration (mm/s)", "Pressure (bar)", "RPM", "Health Score", "Status", "Failure Risk"]].copy()
    table["Failure Risk"] = table["Failure Risk"].map(lambda value: f"{value:.0f}%")
    st.dataframe(table, use_container_width=True, hide_index=True)

with right:
    st.markdown("### Live Sensor Data")
    selected_machine = st.selectbox("Machine", sorted(data["Machine ID"].unique()))
    history = data[data["Machine ID"] == selected_machine].sort_values("record_id")
    x_axis = history["Recorded At"].fillna(history["record_id"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_axis, y=history["Temperature (°C)"], name="Temperature (°C)", line=dict(color="#ff5d51")))
    fig.add_trace(go.Scatter(x=x_axis, y=history["Vibration (mm/s)"], name="Vibration (mm/s)", line=dict(color="#4bd66c"), yaxis="y2"))
    fig.add_trace(go.Scatter(x=x_axis, y=history["Pressure (bar)"], name="Pressure (bar)", line=dict(color="#2f9bff"), yaxis="y2"))
    fig.update_layout(
        template="plotly_dark", height=340, margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="#0b1728", plot_bgcolor="#0b1728",
        yaxis2=dict(overlaying="y", side="right", showgrid=False), legend=dict(orientation="h", y=1.14),
    )
    st.plotly_chart(fig, use_container_width=True)

prediction_col, agents_col, schedule_col = st.columns([0.9, 1.1, 1.05])
with prediction_col:
    st.markdown("### AI Prediction Overview")
    risk = dashboard["Failure Risk"].mean()
    gauge = go.Figure(go.Indicator(
        mode="gauge+number", value=risk, number={"suffix": "%"}, title={"text": "Overall Failure Risk"},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#ffc229"},
               "steps": [{"range": [0, 40], "color": "#153125"}, {"range": [40, 70], "color": "#423617"}, {"range": [70, 100], "color": "#421c22"}]},
    ))
    gauge.update_layout(template="plotly_dark", height=255, margin=dict(l=15, r=15, t=45, b=0), paper_bgcolor="#0b1728")
    st.plotly_chart(gauge, use_container_width=True)
    st.caption(f"Model predictions: {', '.join(sorted(dashboard['AI Prediction'].astype(str).unique()))}")

with agents_col:
    st.markdown("### Multi-Agent Decisions")
    agent_table = dashboard[["Machine ID", "Decision", "Technician", "Action"]]
    st.dataframe(agent_table, use_container_width=True, hide_index=True, height=305)

with schedule_col:
    st.markdown("### Maintenance Schedule")
    schedule_table = dashboard[["Machine ID", "Schedule", "Action", "Technician", "Estimated Cost (₹)"]]
    st.dataframe(schedule_table, use_container_width=True, hide_index=True, height=305)

chart_col, alerts_col = st.columns([1, 1])
with chart_col:
    st.markdown("### Health Score Distribution")
    colors = dashboard["Status"].map({"Healthy": "#45d66a", "Warning": "#ffc229", "Critical": "#ff5757"})
    health_fig = go.Figure(go.Bar(x=dashboard["Machine ID"], y=dashboard["Health Score"], marker_color=colors, text=dashboard["Health Score"], textposition="outside"))
    health_fig.update_layout(template="plotly_dark", height=300, paper_bgcolor="#0b1728", plot_bgcolor="#0b1728", yaxis=dict(range=[0, 110], title="Health Score"), margin=dict(l=10, r=10, t=15, b=10))
    st.plotly_chart(health_fig, use_container_width=True)

with alerts_col:
    st.markdown("### Alerts & Recommendations")
    alert_rows = dashboard[dashboard["Status"] != "Healthy"]
    if alert_rows.empty:
        st.success("No active alerts. All machines are healthy.")
    else:
        for _, row in alert_rows.iterrows():
            st.warning(f"**{row['Machine ID']} — {row['Status']}**: {row['Recommendation']} | {row['Schedule']}")
    st.download_button(
        "Download Dashboard Report (CSV)",
        dashboard.to_csv(index=False).encode("utf-8"),
        file_name="digital_twin_maintenance_report.csv",
        mime="text/csv",
        use_container_width=True,
    )