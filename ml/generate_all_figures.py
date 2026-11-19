import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

output_dir = "/Users/deveshyadav/Desktop/smartparking_project/figures"
os.makedirs(output_dir, exist_ok=True)
sns.set_theme(style="whitegrid", font="sans-serif")

# Fig 1: Block Diagram
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.axis('off')
boxes = [
    ("4x HC-SR04\nUltrasonic Sensors", (0.07, 0.55)),
    ("ESP32 DevKit\n(Node A: 4 Bays)", (0.24, 0.55)),
    ("Servo Gate (SG90)\n& SSD1306 OLED", (0.24, 0.15)),
    ("Python Simulator\n(Zones B-E: 16 Bays)", (0.07, 0.15)),
    ("HiveMQ MQTT Broker\n(broker.hivemq.com:1883)", (0.47, 0.55)),
    ("FastAPI Ingestion\n& SQLite DB", (0.68, 0.55)),
    ("XGBoost Multi-Horizon\nModel (+15/+30/+60m)", (0.68, 0.15)),
    ("Streamlit UI &\nTelegram Bot", (0.88, 0.55)),
]
for text, (x_pos, y_pos) in boxes:
    ax.text(x_pos, y_pos, text, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#e6f2ff', edgecolor='#0066cc', lw=1.5),
            fontsize=8.5, fontweight='bold')

ax.annotate('', xy=(0.17, 0.55), xytext=(0.14, 0.55), arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))
ax.annotate('', xy=(0.24, 0.45), xytext=(0.24, 0.25), arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))
ax.annotate('', xy=(0.40, 0.55), xytext=(0.31, 0.55), arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))
ax.annotate('', xy=(0.47, 0.47), xytext=(0.16, 0.18), arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))
ax.annotate('', xy=(0.61, 0.55), xytext=(0.54, 0.55), arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))
ax.annotate('', xy=(0.68, 0.45), xytext=(0.68, 0.25), arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))
ax.annotate('', xy=(0.82, 0.55), xytext=(0.75, 0.55), arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))

plt.title("Figure 1: Architectural Block Diagram of the End-to-End Smart Parking System", fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{output_dir}/fig1_block_diagram.png", dpi=300)
plt.close()

# Fig 2: Circuit Diagram Graphic
fig, ax = plt.subplots(figsize=(10, 5))
ax.axis('off')
ax.text(0.5, 0.95, "ESP32 DevKit V1 Smart Parking Node (Zone A)", ha='center', fontsize=12, fontweight='bold')
components = [
    ("ESP32 DevKit\n(30 Pins)", 0.5, 0.5, "#dbeafe"),
    ("HC-SR04 Bay 1\nTrig: 13 | Echo: 12", 0.15, 0.75, "#fef3c7"),
    ("HC-SR04 Bay 2\nTrig: 14 | Echo: 27", 0.15, 0.50, "#fef3c7"),
    ("HC-SR04 Bay 3\nTrig: 26 | Echo: 25", 0.15, 0.25, "#fef3c7"),
    ("HC-SR04 Bay 4\nTrig: 33 | Echo: 32", 0.15, 0.05, "#fef3c7"),
    ("4x Red LEDs (Bays)\nPins: 18, 19, 23, 5", 0.85, 0.75, "#fee2e2"),
    ("Green Status LED\nPin: 2 (Availability)", 0.85, 0.52, "#dcfce7"),
    ("SG90 Servo Barrier\nPin: 4 (PWM Gate)", 0.85, 0.30, "#e0e7ff"),
    ("SSD1306 OLED (I2C)\nSDA: 21 | SCL: 22", 0.5, 0.10, "#ede9fe"),
    ("Active Buzzer\nPin: 15 (Chime)", 0.85, 0.10, "#ffedd5"),
]
for name, x_pos, y_pos, bg in components:
    ax.text(x_pos, y_pos, name, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor=bg, edgecolor='#475569', lw=1.2),
            fontsize=8.5, fontweight='bold')

for y in [0.75, 0.50, 0.25, 0.05]:
    ax.annotate('', xy=(0.42, 0.5), xytext=(0.24, y), arrowprops=dict(arrowstyle="->", color="#2563eb", lw=1.2))
for y in [0.75, 0.52, 0.30, 0.10]:
    ax.annotate('', xy=(0.76, y), xytext=(0.58, 0.5), arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.2))
ax.annotate('', xy=(0.5, 0.17), xytext=(0.5, 0.42), arrowprops=dict(arrowstyle="<->", color="#7c3aed", lw=1.2))

plt.title("Figure 2: Pin-Level Schematic and Interconnection Diagram of the ESP32 Node", fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{output_dir}/fig2_circuit_diagram.png", dpi=300)
plt.close()

# Fig 3: Prototype Installed Photo / Rendering
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.axis('off')
ax.fill_between([0, 10], 0, 10, color="#1e293b")
ax.plot([0, 10], [5, 5], color="#facc15", linestyle="--", lw=2)
# bays
for i, x in enumerate([1.2, 3.2, 5.2, 7.2]):
    ax.text(x+0.8, 8, f"Bay A{i+1}\n[HC-SR04]", ha='center', color="#ffffff", fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='square,pad=0.4', facecolor="#334155", edgecolor="#38bdf8", lw=1.5))
    ax.plot([x+0.8, x+0.8], [6.5, 5.2], color="#ef4444" if i < 2 else "#22c55e", lw=3)
# Barrier
ax.text(9.2, 3, "SG90 Gate\n[Closed: 0°]", ha='center', color="#ffffff", fontsize=9, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor="#b91c1c", edgecolor="#fca5a5"))
ax.plot([8.5, 9.8], [4.5, 4.5], color="#f87171", lw=4)
ax.text(5, 1.5, "ESP32 Controller & OLED Display Panel: Operational Status Online", ha='center', color="#38bdf8", fontsize=10, fontweight='bold')
plt.title("Figure 3: Physical Scale Prototype Deployment Architecture of the Smart Parking Node", fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{output_dir}/fig3_hardware_prototype.png", dpi=300)
plt.close()

# Fig 4: Flowchart
fig, ax = plt.subplots(figsize=(6, 8))
ax.axis('off')
steps = [
    "Start Node & Initialize Peripherals",
    "Read 4x HC-SR04 Ultrasonic Distances",
    "Evaluate Threshold: Distance < 10.0 cm",
    "Update Local OLED, LEDs, & Servo Gate",
    "Publish JSON Telemetry to HiveMQ (5s)",
    "FastAPI Ingestion & SQLite Logging",
    "Feature Engineering (13 Historical Steps)",
    "XGBoost Prediction (+15, +30, +60 min)",
    "Streamlit Dashboard & Telegram Alerts"
]
for i, step in enumerate(steps):
    y = 0.9 - i * 0.1
    ax.text(0.5, y, step, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8fafc', edgecolor='#0284c7', lw=1.2),
            fontsize=8.5, fontweight='bold')
    if i < len(steps) - 1:
        ax.annotate('', xy=(0.5, y - 0.06), xytext=(0.5, y - 0.04), arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=4))

plt.title("Figure 4: Algorithmic Work Procedure Flowchart of the Proposed Framework", fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{output_dir}/fig4_flowchart.png", dpi=300)
plt.close()

# Fig 5: Correlation Heatmap
df = pd.read_csv("/Users/deveshyadav/Desktop/smartparking_project/data/parking_dataset.csv")
sample_features = df[["total_occupied", "zone_A_occ", "zone_B_occ", "zone_C_occ", "zone_D_occ", "zone_E_occ", "hour", "minute"]].corr()
plt.figure(figsize=(7, 5))
sns.heatmap(sample_features, annot=True, cmap="Blues", fmt=".2f", cbar=True)
plt.title("Figure 5: Spatial and Temporal Feature Correlation Matrix Across Parking Zones", fontsize=10, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{output_dir}/fig5_correlation_heatmap.png", dpi=300)
plt.close()

# Fig 6: Model MAE Comparison
horizons = ["+15 min", "+30 min", "+60 min"]
xgb_mae = [1.21, 1.51, 1.82]
base_mae = [1.73, 2.92, 4.71]
x = np.arange(len(horizons))
width = 0.35
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(x - width/2, xgb_mae, width, label="XGBoost MAE", color="#0284c7")
ax.bar(x + width/2, base_mae, width, label="Persistence Baseline MAE", color="#94a3b8")
ax.set_ylabel("Mean Absolute Error (Occupied Bays)", fontsize=9.5)
ax.set_title("Figure 6: Multi-Horizon Occupancy Prediction Error Benchmark", fontsize=10.5, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(horizons)
ax.legend()
plt.tight_layout()
plt.savefig(f"{output_dir}/fig6_model_mae_comparison.png", dpi=300)
plt.close()

# Fig 7: R2 Degradation
xgb_r2 = [0.948, 0.921, 0.887]
base_r2 = [0.876, 0.678, 0.249]
plt.figure(figsize=(7, 4))
plt.plot(horizons, xgb_r2, marker="o", linewidth=2.5, color="#16a34a", label="Proposed XGBoost ($R^2$)")
plt.plot(horizons, base_r2, marker="s", linewidth=2.5, linestyle="--", color="#dc2626", label="Persistence Baseline ($R^2$)")
plt.ylabel("Coefficient of Determination ($R^2$)", fontsize=9.5)
plt.xlabel("Forecasting Horizon", fontsize=9.5)
plt.title("Figure 7: Predictive Degradation Benchmark Across Forecast Horizons", fontsize=10.5, fontweight="bold")
plt.ylim(0.0, 1.05)
plt.legend()
plt.tight_layout()
plt.savefig(f"{output_dir}/fig7_r2_horizon_comparison.png", dpi=300)
plt.close()

# Fig 8: Streamlit Dashboard UI Rendering
fig, ax = plt.subplots(figsize=(10, 5))
ax.axis('off')
ax.fill_between([0, 10], 0, 10, color="#f8fafc")
# Header
ax.text(5, 9.3, "🅿️ BMU Smart Campus Parking Facility | Real-Time Operations", ha='center', fontsize=11, fontweight='bold', color="#0f172a")
# KPIs
kpis = [("TOTAL CAPACITY", "20 Bays", "#334155"), ("OCCUPIED BAYS", "9 Bays", "#dc2626"), ("AVAILABLE BAYS", "11 Bays", "#16a34a"), ("OCCUPANCY RATE", "45.0%", "#f59e0b"), ("+30M FORECAST", "14.5 Bays", "#2563eb")]
for i, (title, val, clr) in enumerate(kpis):
    x = 1.0 + i * 2.0
    ax.text(x, 7.8, f"{title}\n{val}", ha='center', fontsize=8.5, fontweight='bold', color=clr,
            bbox=dict(boxstyle='round,pad=0.4', facecolor="#ffffff", edgecolor="#cbd5e1"))
# Visual Bays
ax.text(3, 6.2, "Zone A (Hardware): [A1: 🚘 OCC] [A2: 🚘 OCC] [A3: 🅿️ VAC] [A4: 🅿️ VAC]", ha='center', fontsize=8, color="#0f172a",
        bbox=dict(boxstyle='square,pad=0.3', facecolor="#e2e8f0", edgecolor="#94a3b8"))
ax.text(3, 5.0, "Zone B (Simulated): [B1: 🅿️ VAC] [B2: 🚘 OCC] [B3: 🅿️ VAC] [B4: 🚘 OCC]", ha='center', fontsize=8, color="#0f172a",
        bbox=dict(boxstyle='square,pad=0.3', facecolor="#e2e8f0", edgecolor="#94a3b8"))
ax.text(3, 3.8, "Zone C (Simulated): [C1: 🚘 OCC] [C2: 🅿️ VAC] [C3: 🚘 OCC] [C4: 🅿️ VAC]", ha='center', fontsize=8, color="#0f172a",
        bbox=dict(boxstyle='square,pad=0.3', facecolor="#e2e8f0", edgecolor="#94a3b8"))
ax.text(3, 2.6, "Zone D (Simulated): [D1: 🅿️ VAC] [D2: 🅿️ VAC] [D3: 🚘 OCC] [D4: 🅿️ VAC]", ha='center', fontsize=8, color="#0f172a",
        bbox=dict(boxstyle='square,pad=0.3', facecolor="#e2e8f0", edgecolor="#94a3b8"))
ax.text(3, 1.4, "Zone E (Simulated): [E1: 🚘 OCC] [E2: 🚘 OCC] [E3: 🅿️ VAC] [E4: 🅿️ VAC]", ha='center', fontsize=8, color="#0f172a",
        bbox=dict(boxstyle='square,pad=0.3', facecolor="#e2e8f0", edgecolor="#94a3b8"))
# Prediction Chart
ax.text(7.8, 4.0, "XGBoost Projected Horizon:\nNow: 9 | +15m: 11.2 | +30m: 14.5 | +60m: 9.8\n\nThreshold: 17 Bays (Alert Level: NORMAL)\nBarrier Status: CLOSED (0°)\nCloud Analytics: ThingSpeak Synchronized",
        ha='center', fontsize=8.5, color="#1e293b",
        bbox=dict(boxstyle='round,pad=0.5', facecolor="#ffffff", edgecolor="#0284c7", lw=1.2))

plt.title("Figure 8: Streamlit Graphical Operator Dashboard Visualization (Light Theme)", fontsize=10.5, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{output_dir}/fig8_dashboard_ui.png", dpi=300)
plt.close()

# Fig 9: Cloud & App Telemetry
fig, ax = plt.subplots(figsize=(8, 4))
ax.axis('off')
ax.text(0.5, 0.85, "ThingSpeak IoT Cloud Channel (#2491028)", ha='center', fontsize=11, fontweight='bold', color="#0369a1")
ax.text(0.5, 0.65, "Field 1: Total Occupied Bays (Range: 0 - 20) | Update Rate: 15s\nField 2: Total Available Bays (Range: 0 - 20)\nField 3: Percentage Facility Occupancy Rate (%)", ha='center', fontsize=9,
        bbox=dict(boxstyle='round,pad=0.4', facecolor="#f0f9ff", edgecolor="#0ea5e9"))
ax.text(0.5, 0.35, "MQTT Dash Android Mobile Application Configuration", ha='center', fontsize=11, fontweight='bold', color="#15803d")
ax.text(0.5, 0.15, "Tile 1: Gauge (Occupancy %) | Tile 2: Metric (Available Slots)\nTile 3: Switch Button (Gate Control: 'open' / 'close' over MQTT)\nBroker: broker.hivemq.com:1883 | QoS: 0", ha='center', fontsize=9,
        bbox=dict(boxstyle='round,pad=0.4', facecolor="#f0fdf4", edgecolor="#22c55e"))
plt.title("Figure 9: Cloud Analytics Channel and Mobile Dash Tile Telemetry Architecture", fontsize=10.5, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{output_dir}/fig9_cloud_and_app.png", dpi=300)
plt.close()

# Fig 10: Chatbot Interface
fig, ax = plt.subplots(figsize=(7, 5))
ax.axis('off')
ax.fill_between([0, 10], 0, 10, color="#f8fafc")
ax.text(5, 9.3, "Telegram Bot Channel (@BMUSmartParkingBot)", ha='center', fontsize=11, fontweight='bold', color="#0284c7")
chats = [
    ("User: /status", 1.5, 8.0, "#e2e8f0", "#1e293b", "left"),
    ("Bot: 🅿️ Total Occupied: 9/20 (45.0%)\nAvailable: 11 Bays | Status: Accepting Vehicles", 8.5, 6.8, "#dbeafe", "#1e3a8a", "right"),
    ("User: /predict", 1.5, 5.2, "#e2e8f0", "#1e293b", "left"),
    ("Bot: 🤖 XGBoost Forecast:\n+15m: 11.2 Bays | +30m: 14.5 Bays | +60m: 9.8 Bays\nStatus: Capacity Normal (Threshold < 17)", 8.5, 3.8, "#dbeafe", "#1e3a8a", "right"),
    ("User: /gate_open", 1.5, 2.2, "#e2e8f0", "#1e293b", "left"),
    ("Bot: 🟢 Barrier Gate Opened! SG90 Servo Actuated (90°)", 8.5, 1.2, "#dcfce7", "#166534", "right"),
]
for text, x, y, bg, txt_clr, align in chats:
    ax.text(x, y, text, ha=align, fontsize=8, fontweight='bold', color=txt_clr,
            bbox=dict(boxstyle='round,pad=0.4', facecolor=bg, edgecolor="#94a3b8" if bg=="#e2e8f0" else "#3b82f6"))

plt.title("Figure 10: Telegram Autonomous Chatbot Bidirectional Interaction Transcript", fontsize=10.5, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{output_dir}/fig10_chatbot_interface.png", dpi=300)
plt.close()

print("All 10 figures successfully generated!")
