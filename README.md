# Portfolio

# ShakthiSAT Aerospace Flight Software & Autonomy Suite
> **Live Interactive Core Dashboard:** [View Live Mission Dashboard](https://aafkapatnaik-cloud.github.io/ShakthiSAT-Aerospace-Portfolio/)

An interactive, high-fidelity aerospace flight software architecture designed to demonstrate modular, real-time deterministic spacecraft operations and autonomous fault-management loops. Built using pure, dependency-free Python modules for strict execution isolation, paired with a reactive, client-side simulation engine for immediate architectural verification.

---

## 🛰️ System Architecture Overview

The flight software is built following a decoupled, domain-oriented structural pattern corresponding to standard SmallSat / CubeSat subsystem layouts. By avoiding heavy external runtime frameworks (like NumPy or SciPy), the modules achieve highly predictable, microsecond-level execution times perfect for low-overhead embedded microcontrollers.

   ┌────────────────────────────────────────────────────────┐
   │             AI AUTONOMY COGNITIVE CORE                 │
   │   (Telemetry Scrapers · Automated Anomaly Diagnostics)   │
   └─────────────────────────┬──────────────────────────────┘
                             │ Intercepts & Re-stabilizes
                             ▼
┌───────────────────────────────────────────────────────────────────────┐
│                       CORE FLIGHT LOGIC PIPELINE                      │
├───────────────────┬───────────────────┬───────────────────┬───────────┤
│    1. EPS Core    │   2. ADCS Core    │    3. CDH Core    │  4. GS    │
│  (Power & BMU)    │ (Pointing & Detumble)│  (FS & Watchdog)  │(RF Demod) │
└───────────────────┴───────────────────┴───────────────────┴───────────┘


### 1. Electrical Power System (EPS)
* **`eps_battery_manager.py`**: Manages primary Li-ion pack telemetry, state-of-charge (SoC) estimation via Coulomb counting, and passive cell balancing.
* **`eps_solar_regulator.py`**: Implements a perturb-and-observe Maximum Power Point Tracking (MPPT) algorithm to maximize solar panel array draw.
* **`eps_power_distribution.py`**: A software-switched Power Distribution Unit (PDU) featuring automated individual rail trips on over-current detection.
* **`eps_telemetry.py`**: Packs raw housekeeping metrics into standard fixed-width binary structures via python `struct` packing.

### 2. Attitude Determination & Control System (ADCS)
* **`adcs_sensor_fusion.py`**: A complementary multi-axis sensor fusion filter blending high-frequency gyroscope rates with magnetometer vectors into a quaternion estimate.
* **`adcs_controller.py`**: Dual-mode attitude laws featuring a B-Dot rate damping algorithm for initial detumbling alongside classic PID loops for pointing accuracy.
* **`adcs_actuator_interface.py`**: Clamps commanded torque vectors safely inside physical saturation limits for reaction wheels and magnetorquers.
* **`adcs_orbit_propagator.py`**: Evaluates two-body analytical Keplerian equations to predict pointing horizons and eclipse windows.

### 3. Command & Data Handling (CDH)
* **`cdh_telemetry_aggregator.py`**: Intercepts sub-system frames and aggregates them into unified downlinks.
* **`cdh_command_dispatcher.py`**: Min-heap priority scheduling queue managing sub-millisecond command dispatch loops.
* **`cdh_flash_fs.py`**: Implements basic wear-leveling cursors across a virtualized flash block array to eliminate sector burn-out during high-rate storage.
* **`cdh_watchdog.py`**: An independent software-tick supervisor that triggers fallback safe-modes if the standard operating runtime misses its heartbeat refresh windows.

### 4. Ground Station Suite (GS)
* **`gs_receiver.py` & `gs_transmitter.py`**: Complete uplink/downlink frame compilers verifying CCSDS sync words (`0x1ACFFC1D`) and appending CCITT CRC-16 integrity layers.
* **`gs_pass_predictor.py`**: Computes station look-angles (elevation limits and Doppler shift boundaries) relative to local ground track masks.

---

## 🧠 Core Highlight: Autonomous Fault Management (FDIR)

The cornerstone of this flight suite is its integrated **Agentic Fault Detection, Isolation, and Recovery (FDIR)** engine. 

When an operator triggers the simulation anomaly injector, the architecture demonstrates real-time cognitive resilience:
1. **Detection:** The runtime framework flags out-of-bounds metrics (e.g., thermal spikes in EPS or runaway spinning rates in ADCS).
2. **Isolation:** The core cognitive agent dynamically isolates the specific thread, printing step-by-step diagnostic reasoning inside the monitoring console feed.
3. **Recovery:** The engine automatically builds and passes an architectural hotpatch string to hot-swap the misbehaving block, instantly dropping metrics back down into optimal boundaries without breaking system continuity.

---

## 🛠️ Local Verification & Development

Since the entire workspace compiles inside an efficient web engine for instantaneous structural review, running it locally requires zero toolchain setups.

1. Clone the repository:
   ```bash
   git clone [https://github.com/aafkapatnaik-cloud/ShakthiSAT-Aerospace-Portfolio.git](https://github.com/aafkapatnaik-cloud/ShakthiSAT-Aerospace-Portfolio.git)
Launch the dashboard:
Simply double-click the index.html file or run a local lightweight listener to view the interface:

Bash
# If you have Python installed locally:
python -m http.server 8000
Navigate to http://localhost:8000 to interact with the runtime execution modules.

📄 License and Verification
Developed as an interactive, safe portfolio demonstration mapping actual flight-software layout standards down to an isolated, client-side sandbox environment. No actual spacecraft hardware was harmed during testing sequences.
