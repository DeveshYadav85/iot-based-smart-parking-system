# IoT-Based Smart Parking System with Real-Time Occupancy Prediction

**Course:** CSE3722 - IoT Networks, Architectures and Applications  
**Institution:** BML Munjal University  

---

## 1. Overview
This project presents an end-to-end, simulation-based IoT smart parking facility with multi-horizon occupancy forecasting:
- **Node A (Hardware Simulation)**: ESP32 DevKit in Wokwi with 4× HC-SR04 ultrasonic sensors, SSD1306 OLED, 5 status LEDs, and an SG90 servo barrier gate.
- **Zones B–E (Simulated Facility)**: 16 additional parking bays (20 bays total across 5 zones).
- **MQTT Telemetry**: Published every 5s to `broker.hivemq.com:1883` on topic `bmu/iotnaa/smartparking-g01/A/slot{1-4}`.
- **Backend**: FastAPI REST API logging observations to SQLite and providing `/slots`, `/summary`, `/history`, and `/predict`.
- **Machine Learning**: Extreme Gradient Boosting (XGBoost) predicting facility occupancy at +15, +30, and +60 minutes ($R^2 = 0.921$ at +30 min).
- **Interfaces**: Streamlit Operator Dashboard, ThingSpeak Cloud Analytics, Android MQTT Dash, and Telegram Bot.

---

## 2. Project Structure
```text
smartparking_project/
├── wokwi/
│   ├── diagram.json      # ESP32 circuit wiring diagram for Wokwi
│   ├── sketch.ino        # ESP32 C++ firmware with WiFi/MQTT/OLED/Servo
│   └── libraries.txt     # Required Arduino libraries
├── backend/
│   ├── main.py           # FastAPI backend service
│   └── parking.db        # SQLite persistence database
├── dashboard/
│   └── app.py            # Streamlit real-time operations dashboard
├── simulator/
│   └── lot_simulator.py  # 20-bay time-series generator (200 runs)
├── ml/
│   └── generate_all_figures.py  # Report diagrams generator
├── figures/              # Publication-grade figures (Figs 1 to 10)
├── data/
│   └── parking_dataset.csv      # 38,400 raw time-series observations
└── Section_A_Group_04.docx      # Complete IEEE project report
```

---

## 3. How to Run Locally

### Start Backend API
```bash
python3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Start Streamlit Dashboard
```bash
python3 -m streamlit run dashboard/app.py --server.port 8501
```
Dashboard: [http://127.0.0.1:8501](http://127.0.0.1:8501)

### Run Wokwi IoT Hardware
1. Open [https://wokwi.com/projects/new/esp32](https://wokwi.com/projects/new/esp32).
2. Paste `wokwi/diagram.json` and `wokwi/sketch.ino`.
3. Add libraries: `PubSubClient`, `Adafruit SSD1306`, `Adafruit GFX Library`, `ESP32Servo`, `ArduinoJson`.
4. Click **Play (▶)**. Drag distance slider below 10cm to trigger live occupancy!
