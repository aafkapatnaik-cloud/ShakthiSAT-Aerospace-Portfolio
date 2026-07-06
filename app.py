import sys
import threading
import time

try:
    from flask import Flask, jsonify, render_template
    import serial
except ImportError as e:
    print(f"❌ ERROR: Missing required library! {e}")
    sys.exit(1)

app = Flask(__name__)

SERIAL_PORT = "COM3"  
BAUD_RATE = 9600

grid_data = {
    "solar": 0.00, "wind": 0.00, "total": 0.00,
    "status": "⏳ Initializing System Connection...",
    "hospital": "active", "residential": "on_hold", "industrial": "on_hold", "commercial": "on_hold"
}

def read_arduino():
    global grid_data
    while True:
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            time.sleep(2)
            while True:
                if ser.in_waiting > 0:
                    try:
                        line = ser.readline().decode('utf-8').strip()
                        if "SOLAR:" in line and ",WIND:" in line:
                            parts = line.split(",")
                            solar_val = float(parts[0].split(":")[1])
                            wind_val = float(parts[1].split(":")[1])
                            total_val = float(parts[2].split(":")[1])
                            
                            # ☀️ NEW LOW INDOOR THRESHOLDS ☀️
                            if total_val >= 0.8:     # Tier 4: All 4 Active
                                status_text = "🟢 Grid Power Surplus"
                                states = {"h": "active", "r": "active", "i": "active", "c": "active"}
                            elif total_val >= 0.5:   # Tier 3: Hospital, Residential, Industrial
                                status_text = "🟡 High Load Capacity"
                                states = {"h": "active", "r": "active", "i": "active", "c": "on_hold"}
                            elif total_val >= 0.2:   # Tier 2: Hospital, Residential (Your 0.34V hits this!)
                                status_text = "🟡 Stable Load Demand"
                                states = {"h": "active", "r": "active", "i": "on_hold", "c": "on_hold"}
                            else:                    # Tier 1: Emergency backup only
                                status_text = "🔴 Critical Grid Deficit"
                                states = {"h": "active", "r": "on_hold", "i": "on_hold", "c": "on_hold"}
                            
                            grid_data = {
                                "solar": round(solar_val, 2), "wind": round(wind_val, 2), "total": round(total_val, 2),
                                "status": status_text, "hospital": states["h"], "residential": states["r"], "industrial": states["i"], "commercial": states["c"]
                            }
                    except Exception:
                        pass
                time.sleep(0.05)
        except serial.SerialException:
            time.sleep(2)

@app.route('/')
def home(): return render_template('index.html')

@app.route('/api/data')
def get_data(): return jsonify(grid_data)

if __name__ == '__main__':
    threading.Thread(target=read_arduino, daemon=True).start()
    app.run(debug=False, host='0.0.0.0', port=5000)