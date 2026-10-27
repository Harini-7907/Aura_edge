# ==========================================
# AURA-EDGE DASHBOARD
# ==========================================

import sys
from pathlib import Path

# Ensure the project root is available before importing project modules.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import streamlit as st

from monitoring.live_telemetry import get_live_telemetry
from orchestration.enact_adapter import (
    load_enact_resources,
    get_enact_prediction,
)
from orchestration.mecperf_adapter import get_network_profile
from orchestration.task_profiler import create_task
from orchestration.resource_profile import create_execution_resources
from orchestration.decision_engine import select_resource, explain_decision


# ==========================================
# PAGE CONFIGURATION (must be before UI calls)
# ==========================================

st.set_page_config(
    page_title="AURA-Edge",
    page_icon="⚡",
    layout="wide",
)


# ==========================================
# STYLING
# ==========================================

st.markdown(
    """
    <style>
    .stApp { background-color: #f5f7ff; }
    .block-container { padding-top: 2rem; padding-bottom: 3rem; }
    .aura-title {
        font-size: 44px; font-weight: 800; color: #312e81; margin-bottom: 0;
    }
    .aura-subtitle {
        font-size: 18px; color: #64748b; margin-bottom: 15px;
    }
    .section-title {
        font-size: 25px; font-weight: 750; color: #1e1b4b;
        margin-top: 28px; margin-bottom: 15px;
    }
    .live-box {
        background-color: #dcfce7; border: 1px solid #86efac;
        border-radius: 14px; padding: 12px 18px; color: #166534;
        font-weight: 700; margin-bottom: 15px;
    }
    .footer-card {
        background-color: #e0e7ff; padding: 20px; border-radius: 18px;
        text-align: center; color: #3730a3; font-weight: 650; margin-top: 30px;
    }
        /* Paste the new CSS here */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #475569;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #312e81;
        font-weight: 750;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px;
    }

    .stAlert {
        border-radius: 12px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        overflow: hidden;
    }
    </style>
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# CACHED DATA LOADERS
# ==========================================

@st.cache_data(ttl=30)
def load_current_edge():
    nodes = load_enact_resources()
    for node in nodes:
        if node.get("node_name") == "rpi4":
            return node
    return None


@st.cache_data(ttl=30)
def load_edge_prediction():
    return get_enact_prediction("rpi4")


@st.cache_data(ttl=30)
def load_network_profile():
    return get_network_profile(0)


@st.cache_resource
def load_candidate_resources():
    # These are the project's configured Local/Edge/Cloud candidate profiles.
    # They are not remote servers being queried live.
    return create_execution_resources()


# ==========================================
# HEADER
# ==========================================

st.markdown('<div class="aura-title">⚡ AURA-EDGE</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="aura-subtitle">AI Resource Orchestration for Edge-Cloud Environments</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="live-box">LIVE TELEMETRY — Reading this computer</div>',
    unsafe_allow_html=True,
)
st.divider()


# ==========================================
# LIVE RESOURCE PANEL
# Only this fragment reruns every 3 seconds.
# ==========================================

@st.fragment(run_every="3s")
def live_resource_panel():
    try:
        live_data = get_live_telemetry()
        st.write("DEBUG: Telemetry loaded:", live_data)
        
        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("🧠 Live CPU Usage", f"{live_data['cpu_percent']:.1f}%")
        with c2:
            st.metric("💾 Live Memory Usage", f"{live_data['memory_percent']:.1f}%")
        with c3:
            battery = live_data.get("battery_percent")
            st.metric(
                "🔋 Live Battery",
                f"{float(battery):.1f}%" if battery is not None else "N/A",
            )

        st.caption(f"Last updated: {live_data['timestamp']}")
    except Exception as error:
        st.error(f"Live telemetry unavailable: {type(error).__name__}: {error}")


st.markdown(
    '<div class="section-title">🖥️ Live Resource Status — Your Computer</div>',
    unsafe_allow_html=True,
)
live_resource_panel()


# ==========================================
# REFERENCE DATA LOADS
# ==========================================

st.markdown(
    '<div class="section-title">📡 Live Telemetry Source</div>',
    unsafe_allow_html=True,
)
source1, source2, source3 = st.columns(3)
with source1:
    st.info("**Live source**\n\nYour computer via psutil")
with source2:
    st.info("**Reference edge source**\n\nENACT recorded telemetry")
with source3:
    st.info("**Network source**\n\nMECPerf recorded measurements")

try:
    edge = load_current_edge()
    if edge is None:
        st.warning("ENACT rpi4 reference telemetry was not found.")
except Exception as error:
    edge = None
    st.warning(f"ENACT telemetry unavailable: {type(error).__name__}: {error}")

try:
    prediction = load_edge_prediction()
except Exception as error:
    prediction = None
    st.warning(f"ENACT prediction unavailable: {type(error).__name__}: {error}")

try:
    network = load_network_profile()
except Exception as error:
    network = None
    st.warning(f"MECPerf network profile unavailable: {type(error).__name__}: {error}")


# ==========================================
# PREDICTION & NETWORK INTELLIGENCE
# ==========================================

st.markdown(
    '<div class="section-title">🔮 Prediction & Network Intelligence</div>',
    unsafe_allow_html=True,
)
prediction_col, network_col = st.columns(2)

with prediction_col:
    st.subheader("🔮 Predicted Resource Demand")
    if prediction is not None:
        p1, p2 = st.columns(2)
        with p1:
            st.metric("Predicted CPU", f"{float(prediction['predicted_cpu']):.2f}%")
            st.caption(f"Uncertainty: ±{float(prediction['cpu_uncertainty']):.2f}%")
        with p2:
            st.metric("Predicted Memory", f"{float(prediction['predicted_memory']):.2f}%")
            st.caption(f"Uncertainty: ±{float(prediction['memory_uncertainty']):.2f}%")
        st.success("Prediction model loaded. Forecast uses recorded ENACT telemetry.")
    else:
        st.info("Prediction values are unavailable; see the warning above.")

with network_col:
    st.subheader("📡 Network Conditions")
    if network is not None:
        n1, n2 = st.columns(2)
        with n1:
            st.metric("Latency", f"{float(network['latency_ms']):.2f} ms")
        with n2:
            st.metric("Bandwidth", f"{float(network['bandwidth_mbps']):.2f} Mbps")
        st.info("These are recorded MECPerf measurements, not a live speed test.")
    else:
        st.info("Network values are unavailable; see the warning above.")


# ==========================================
# CURRENT VS PREDICTED CHARTS
# ==========================================

st.markdown(
    '<div class="section-title">📈 Current vs Predicted Resources</div>',
    unsafe_allow_html=True,
)

try:
    live_snapshot = get_live_telemetry()
    current_cpu = float(live_snapshot["cpu_percent"])
    current_memory = float(live_snapshot["memory_percent"])

    chart1, chart2 = st.columns(2)
    with chart1:
        st.bar_chart(
            pd.DataFrame(
                {"CPU (%)": [current_cpu, float(prediction["predicted_cpu"])]},
                index=["Current laptop", "ENACT prediction"],
            )
            if prediction is not None
            else pd.DataFrame({"CPU (%)": [current_cpu]}, index=["Current laptop"])
        )
    with chart2:
        st.bar_chart(
            pd.DataFrame(
                {"Memory (%)": [current_memory, float(prediction["predicted_memory"])]},
                index=["Current laptop", "ENACT prediction"],
            )
            if prediction is not None
            else pd.DataFrame({"Memory (%)": [current_memory]}, index=["Current laptop"])
        )
except Exception as error:
    st.warning(f"Could not draw current/predicted charts: {type(error).__name__}: {error}")


# ==========================================
# REAL DECISION ENGINE INTEGRATION
# ==========================================

st.markdown('<div class="section-title">🧠 AURA Decision</div>', unsafe_allow_html=True)
st.caption(
    "The engine below evaluates the configured Local/Edge/Cloud candidate profiles. "
    "The sample task is currently fixed for demonstration."
)

with st.container(border=True):
    try:
        task = create_task(
            task_id="dashboard_task",
            cpu_requirement=10,
            memory_requirement=10,
            deadline=2,
            priority=2,
            estimated_execution_time=1,
            task_size=5,
        )

        resources = load_candidate_resources()
        best_resource, results, rejected = select_resource(task, resources)

        if best_resource is None:
            st.warning("No feasible resource was found for this task.")
        else:
            st.success(f"Selected resource: {best_resource.name}")

            if results:
                score_rows = []
                for resource, score in results:
                    score_rows.append(
                        {
                            "Resource": resource.name,
                            "Score": round(float(score), 2),
                            "Status": (
                                "SELECTED"
                                if resource.name == best_resource.name
                                else "Candidate"
                            ),
                        }
                    )
                st.markdown("#### Candidate Resource Scores")
                st.dataframe(
                    pd.DataFrame(score_rows),
                    use_container_width=True,
                    hide_index=True,
                )

            explanation = explain_decision(task, best_resource)
            st.markdown("#### Why this resource?")
            components = explanation.get("components") if isinstance(explanation, dict) else None
            if components:
                positive_labels = {
                    "latency_score": "Latency contribution",
                    "bandwidth_score": "Bandwidth contribution",
                    "energy_score": "Energy contribution",
                    "reliability_score": "Reliability contribution",
                }
                penalty_labels = {
                    "risk_penalty": "Risk penalty",
                    "uncertainty_penalty": "Prediction uncertainty penalty",
                    "future_cpu_penalty": "Future CPU penalty",
                    "future_memory_penalty": "Future memory penalty",
                    "priority_penalty": "Priority penalty",
                    "battery_penalty": "Battery penalty",
                    "temperature_penalty": "Temperature penalty",
                }
                explanation_rows = []
                for key, label in positive_labels.items():
                    explanation_rows.append(
                        {"Factor": label, "Value": f"+{float(components.get(key, 0)):.2f}"}
                    )
                for key, label in penalty_labels.items():
                    explanation_rows.append(
                        {"Factor": label, "Value": f"-{float(components.get(key, 0)):.2f}"}
                    )
                st.dataframe(
                    pd.DataFrame(explanation_rows),
                    use_container_width=True,
                    hide_index=True,
                )

        if rejected:
            with st.expander("Rejected resources and reasons"):
                for resource, reasons in rejected:
                    st.markdown(f"**{resource.name}**")
                    for reason in reasons:
                        st.write(f"- {reason}")

    except Exception as error:
        st.error(f"Decision Engine failed: {type(error).__name__}")
        st.code(str(error))


# ==========================================
# ENACT REFERENCE TELEMETRY
# ==========================================

st.markdown(
    '<div class="section-title">🧪 ENACT Reference Telemetry</div>',
    unsafe_allow_html=True,
)
if edge is not None:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("ENACT CPU", f"{float(edge['cpu_utilization']):.2f}%")
    with c2:
        st.metric("ENACT Memory", f"{float(edge['memory_utilization']):.2f}%")
    with c3:
        st.metric("ENACT Energy", f"{float(edge['energy_watts']):.2f} W")
    st.caption("ENACT values are from recorded edge-device telemetry, not your laptop.")
else:
    st.info("ENACT reference values are currently unavailable.")


# ==========================================
# NETWORK ADAPTATION RESULTS
# ==========================================

st.markdown(
    '<div class="section-title">📊 Network Adaptation Decisions</div>',
    unsafe_allow_html=True,
)
network_file = PROJECT_ROOT / "results" / "network_adaptation_results.csv"
if network_file.exists():
    try:
        network_df = pd.read_csv(network_file)
        display_columns = [
            column
            for column in ["condition", "latency_ms", "bandwidth_mbps", "selected_resource"]
            if column in network_df.columns
        ]
        st.dataframe(
            network_df[display_columns],
            use_container_width=True,
            hide_index=True,
        )
    except Exception as error:
        st.warning(f"Could not read network adaptation results: {error}")
else:
    st.info("Network adaptation results are not available yet.")


# ==========================================
# MIGRATION LOG
# ==========================================

st.markdown(
    '<div class="section-title">🔄 Recent Migration Decisions</div>',
    unsafe_allow_html=True,
)
migration_file = PROJECT_ROOT / "results" / "migration_log.csv"
if migration_file.exists():
    try:
        migration_df = pd.read_csv(migration_file)
        st.dataframe(
            migration_df.tail(5),
            use_container_width=True,
            hide_index=True,
        )
    except Exception as error:
        st.warning(f"Could not read migration log: {error}")
else:
    st.info("Migration log is not available yet.")


# ==========================================
# PROJECT GOALS & FOOTER
# ==========================================

st.markdown('<div class="section-title">🎯 AURA-Edge Project Goals</div>', unsafe_allow_html=True)
g1, g2, g3 = st.columns(3)
with g1:
    st.success("✓ Predict future resource demand")
with g2:
    st.success("✓ Adapt to network conditions")
with g3:
    st.success("✓ Make deadline-aware placement decisions")

st.markdown(
    """
    <div class="footer-card">
        🌱 Efficient AI. Sustainable Edge-Cloud.
        <br>
        <i>Right Task. Right Resource.</i>
    </div>
    """,
    unsafe_allow_html=True,
)
