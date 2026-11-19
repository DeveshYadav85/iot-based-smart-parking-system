"""Streamlit real-time dashboard for BMU CSE3722 Smart Parking."""

from pathlib import Path
import os
import random
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

st.set_page_config(
    page_title="BMU Smart Parking | Real-Time Operations",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded"
)

PROJ_ROOT = Path("/Users/deveshyadav/Desktop/smartparking_project")
DIAGRAM_PATH = PROJ_ROOT / "wokwi" / "diagram.json"
SKETCH_PATH = PROJ_ROOT / "wokwi" / "sketch.ino"

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .main-header {
        background: linear-gradient(135deg, #0d3b66 0%, #001e3d 100%);
        padding: 22px 28px;
        border-radius: 14px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(0, 30, 61, 0.15);
    }
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }
    .kpi-title { font-size: 11.5px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-val { font-size: 26px; font-weight: 800; color: #0f172a; margin-top: 4px; }
    .zone-container {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")

def get_data(endpoint):
    try:
        r = requests.get(f"{API_URL}/{endpoint}", timeout=2)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

def post_data(endpoint, data=None):
    try:
        r = requests.post(f"{API_URL}/{endpoint}", json=data, timeout=2)
        return r.status_code == 200
    except Exception:
        return False

# Sidebar
st.sidebar.markdown("### 🎛️ Operations Control")

st.sidebar.markdown("#### 🚗 Vehicle Inbound / Outbound")
col_sim1, col_sim2 = st.sidebar.columns(2)
with col_sim1:
    if st.button("➕ Park Car", use_container_width=True):
        slots_data = get_data("slots") or []
        vacant = [s for s in slots_data if s["occupied"] == 0]
        if vacant:
            chosen = random.choice(vacant)
            post_data("simulate/slot", {"slot_id": chosen["slot_id"], "occupied": 1, "distance": round(random.uniform(4.0, 8.5), 1)})
            st.sidebar.success(f"Parked in {chosen['slot_id']}")
with col_sim2:
    if st.button("➖ Vacate Car", use_container_width=True):
        slots_data = get_data("slots") or []
        occupied = [s for s in slots_data if s["occupied"] == 1]
        if occupied:
            chosen = random.choice(occupied)
            post_data("simulate/slot", {"slot_id": chosen["slot_id"], "occupied": 0, "distance": round(random.uniform(22.0, 45.0), 1)})
            st.sidebar.info(f"Bay {chosen['slot_id']} vacated")

st.sidebar.markdown("#### 🌊 Preset Scenarios")
scen = st.sidebar.radio("Select Flow:", ["Live Stream", "Rush Hour (85%+ Saturation)", "Night Clearance", "Moderate Flow"])
if st.sidebar.button("Apply Preset", use_container_width=True):
    slots_data = get_data("slots") or []
    prob = 0.88 if "Rush Hour" in scen else (0.15 if "Night Clearance" in scen else 0.50)
    for s in slots_data:
        occ = 1 if random.random() < prob else 0
        post_data("simulate/slot", {"slot_id": s["slot_id"], "occupied": occ, "distance": 6.0 if occ else 35.0})
    st.sidebar.success("Preset applied")

st.sidebar.markdown("---")
st.sidebar.markdown("#### 🚪 Entrance Barrier Gate")
g_col1, g_col2 = st.sidebar.columns(2)
with g_col1:
    if st.button("🟢 OPEN", use_container_width=True):
        requests.post(f"{API_URL}/gate/open", timeout=2)
        st.sidebar.success("Gate Raised (90°)")
with g_col2:
    if st.button("🔴 CLOSE", use_container_width=True):
        requests.post(f"{API_URL}/gate/close", timeout=2)
        st.sidebar.error("Gate Lowered (0°)")

st.sidebar.markdown("---")
auto_refresh = st.sidebar.toggle("Auto-Refresh Stream", value=True)
refresh_rate = st.sidebar.slider("Refresh Interval (s)", 2, 10, 4)

summary = get_data("summary") or {
    "total_slots": 20, "total_occupied": 8, "total_available": 12,
    "occupancy_rate": 0.40, "occupancy_percentage": 40.0,
    "zone_occupied": {"A": 1, "B": 2, "C": 2, "D": 2, "E": 1}
}
slots = get_data("slots") or []
total_capacity = 20
total_occ = summary["total_occupied"]
total_avail = summary["total_available"]
occ_pct = summary["occupancy_percentage"]

prediction = get_data("predict") or {
    "current_occupied": total_occ,
    "prediction_15_min": round(total_occ * 1.15, 1),
    "prediction_30_min": round(total_occ * 1.35, 1),
    "prediction_60_min": round(total_occ * 0.95, 1),
    "near_full_alert_30": False
}

# Header
st.markdown(f"""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0; font-size: 24px; font-weight: 800;">🅿️ BMU Smart Campus Parking Facility</h1>
            <p style="margin: 4px 0 0 0; opacity: 0.9; font-size: 13.5px;">Real-Time IoT Ultrasonic Telemetry • Zone A (ESP32 Wokwi Node) • XGBoost Predictive Analytics</p>
        </div>
        <div style="text-align: right; background: rgba(255,255,255,0.12); padding: 8px 16px; border-radius: 10px;">
            <div style="font-size: 10px; text-transform: uppercase; font-weight: 700; letter-spacing: 1px;">Live Status</div>
            <div style="font-size: 16px; font-weight: 800; color: {'#4ade80' if total_avail > 3 else '#f87171'};">
                {'● ACCEPTING VEHICLES' if total_avail > 3 else '● LOT NEAR CAPACITY'}
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if occ_pct >= 85.0 or prediction.get("near_full_alert_30"):
    st.error("🚨 **CAPACITY WARNING (≥ 85% OCCUPANCY)** — Saturation imminent. VMS redirection active.")

# KPI Cards
k1, k2, k3, k4, k5 = st.columns(5)
k1.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Capacity</div><div class='kpi-val'>{total_capacity} <span style='font-size:14px;color:#888;'>Bays</span></div></div>", unsafe_allow_html=True)
k2.markdown(f"<div class='kpi-card'><div class='kpi-title'>Occupied</div><div class='kpi-val' style='color:#ef4444;'>{total_occ}</div></div>", unsafe_allow_html=True)
k3.markdown(f"<div class='kpi-card'><div class='kpi-title'>Available</div><div class='kpi-val' style='color:#22c55e;'>{total_avail}</div></div>", unsafe_allow_html=True)
k4.markdown(f"<div class='kpi-card'><div class='kpi-title'>Occupancy Rate</div><div class='kpi-val' style='color:#3b82f6;'>{occ_pct}%</div></div>", unsafe_allow_html=True)
p30 = prediction.get("prediction_30_min", total_occ)
k5.markdown(f"<div class='kpi-card'><div class='kpi-title'>+30m Forecast</div><div class='kpi-val' style='color:#6366f1;'>{p30} <span style='font-size:14px;color:#888;'>Bays</span></div></div>", unsafe_allow_html=True)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

tab_live, tab_wokwi = st.tabs(["🚘 Parking Lot Operations & AI Forecast", "⚡ Wokwi IoT Hardware Integration (Zone A)"])

with tab_live:
    col_left, col_right = st.columns([3, 2])
    with col_left:
        st.markdown("### 🚘 Visual Parking Lot Matrix")
        zones = ["A", "B", "C", "D", "E"]
        for z in zones:
            zone_slots = [s for s in slots if s.get("zone") == z]
            if not zone_slots:
                zone_slots = [{"slot_id": f"{z}{i}", "slot": i, "occupied": 0, "distance": 32.0} for i in range(1, 5)]
            occ_in_zone = sum(1 for s in zone_slots if s.get("occupied") == 1)
            badge_color = "#ef4444" if occ_in_zone == 4 else ("#22c55e" if occ_in_zone == 0 else "#3b82f6")
            st.markdown(f"""
            <div class="zone-container">
                <div style="font-size:14px;font-weight:700;color:#334155;margin-bottom:10px;display:flex;justify-content:space-between;">
                    <span>📍 Zone {z} {'<span style=\"font-size:11px;background:#e0f2fe;color:#0369a1;padding:2px 8px;border-radius:6px;\">ESP32 Hardware Node</span>' if z=='A' else '<span style=\"font-size:11px;background:#f1f5f9;color:#475569;padding:2px 8px;border-radius:6px;\">Simulated Zone</span>'}</span>
                    <span style="color:{badge_color};">{occ_in_zone}/4 Occupied</span>
                </div>
            """, unsafe_allow_html=True)
            scols = st.columns(4)
            for i, s in enumerate(zone_slots):
                is_occ = s.get("occupied", 0) == 1
                dist = s.get("distance", 30.0)
                car_icon = "🚘" if is_occ else "🅿️"
                status_color = "#ef4444" if is_occ else "#22c55e"
                bg_color = "#fef2f2" if is_occ else "#f0fdf4"
                border_color = "#fca5a5" if is_occ else "#86efac"
                with scols[i]:
                    st.markdown(f"""
                    <div style="background:{bg_color};border:1.5px solid {border_color};border-radius:10px;padding:10px 4px;text-align:center;margin-bottom:6px;">
                        <div style="font-size:12px;font-weight:800;color:#334155;">BAY {s.get('slot_id')}</div>
                        <div style="font-size:22px;margin:3px 0;">{car_icon}</div>
                        <div style="font-size:11px;font-weight:800;color:{status_color};">{'OCCUPIED' if is_occ else 'VACANT'}</div>
                        <div style="font-size:10px;color:#64748b;">{dist:.1f} cm</div>
                    </div>
                    """, unsafe_allow_html=True)
                    btn_label = "Vacate" if is_occ else "Park"
                    if st.button(btn_label, key=f"btn_{s.get('slot_id')}", use_container_width=True):
                        new_occ = 0 if is_occ else 1
                        new_dist = 6.0 if new_occ == 1 else 35.0
                        post_data("simulate/slot", {"slot_id": s.get("slot_id"), "occupied": new_occ, "distance": new_dist})
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("### 🤖 Predictive Forecasting Engine")
        p15 = prediction.get("prediction_15_min", round(total_occ * 1.15, 1))
        p30 = prediction.get("prediction_30_min", round(total_occ * 1.35, 1))
        p60 = prediction.get("prediction_60_min", round(total_occ * 0.95, 1))
        fig_pred = go.Figure()
        fig_pred.add_trace(go.Bar(
            x=["Current", "+15 Min", "+30 Min", "+60 Min"],
            y=[total_occ, p15, p30, p60],
            marker=dict(color=["#94a3b8", "#38bdf8", "#3b82f6" if p30 < 17 else "#ef4444", "#6366f1"]),
            text=[f"{total_occ}", f"{p15}", f"{p30}", f"{p60}"],
            textposition="auto",
        ))
        fig_pred.add_hline(y=17, line_dash="dot", line_color="#ef4444", annotation_text="Saturation Alert (17)")
        fig_pred.update_layout(title="Occupancy Horizon (Bays)", yaxis=dict(range=[0, 22]), height=230, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_pred, use_container_width=True)

        st.markdown("#### 📊 Zone Distribution")
        zone_counts = {z: sum(1 for s in slots if s.get("zone") == z and s.get("occupied") == 1) for z in zones}
        df_donut = pd.DataFrame({"Zone": [f"Zone {z}" for z in zone_counts.keys()], "Occupied": list(zone_counts.values())})
        fig_donut = px.pie(df_donut, values="Occupied", names="Zone", hole=0.55, color_discrete_sequence=px.colors.sequential.Blues_r)
        fig_donut.update_layout(height=200, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_donut, use_container_width=True)

with tab_wokwi:
    st.markdown("### 🔌 Wokwi ESP32 IoT Node Simulation (Zone A)")
    st.markdown("The physical hardware layer for **Zone A (Bays A1 to A4)** is simulated using an **ESP32 DevKit** in Wokwi.")
    col_w1, col_w2 = st.columns([3, 2])
    with col_w1:
        st.markdown("""
        #### 🚀 Quick Start Instructions:
        1. Open **[wokwi.com/projects/new/esp32](https://wokwi.com/projects/new/esp32)**.
        2. Paste `diagram.json` and `sketch.ino` below.
        3. Add libraries: `PubSubClient`, `Adafruit SSD1306`, `Adafruit GFX Library`, `ESP32Servo`, `ArduinoJson`.
        4. Click **Play (▶)**.
        """)
    with col_w2:
        st.code("""Broker: broker.hivemq.com:1883\nTopic: bmu/iotnaa/smartparking-g01/A/slot{1-4}\nGate: bmu/iotnaa/smartparking-g01/A/cmd/gate""", language="yaml")

    with st.expander("📄 View & Copy `diagram.json` (ESP32 Circuit)", expanded=False):
        if DIAGRAM_PATH.exists():
            with open(DIAGRAM_PATH, "r") as f:
                st.code(f.read(), language="json")

    with st.expander("📄 View & Copy `sketch.ino` (ESP32 Firmware)", expanded=False):
        if SKETCH_PATH.exists():
            with open(SKETCH_PATH, "r") as f:
                st.code(f.read(), language="cpp")

if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
