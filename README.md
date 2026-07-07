# ShakthiSAT Operational Flight Software Suite & Architecture Simulation

An embedded-style, zero-dependency Python flight software (FSW) architecture and interactive telemetry suite for the **ShakthiSAT CubeSat mission**. This repository demonstrates production-grade modularity, attitude determination control operations, autonomous electrical fault protection, and telemetry stream orchestration.

🌐 **[Live Interactive Mission Control Dashboard](YOUR_GITHUB_PAGES_LINK_HERE)**

---

## 🛰️ System Architecture

The software is engineered with strict modular isolation principles to mimic real-time embedded flight environments, removing heavy library dependencies to ensure deterministic runtime safety on microcontrollers.

```text
├── ADCS/                       # Attitude Determination & Control System
│   └── magnetorquer_controller.py   # Algorithmic B-dot rate damping logic
├── EPS/                        # Electrical Power System
│   ├── battery_charging_sim.py      # Orbital solar flux energy accumulator
│   ├── depth_of_discharge_tracker.py# Multi-epoch electrochemical decay model
│   ├── power_distribution_manager.py# Autonomous FDIR safety load-shedder
│   ├── shunt_regulator.py           # Bus over-voltage thermal dump control
│   └── solar_panel_sun_tracker.py   # Trigonometric sun vector tracking math
└── telemetry_generator.py      # Core System Driver & Frame Aggregator
🚀 Subsystem Flight Profiles
🔹 Command & Data Handling (C&DH) / Telemetry Orchestration
File: telemetry_generator.py

Aggregates modular data vectors across all active processing nodes into standardized packet streams, executing structural housekeeping cycles.

🔹 Fault Detection, Isolation, & Recovery (FDIR)
File: EPS/power_distribution_manager.py

Monitors main battery bus voltage. If telemetry drops below the critical hardware voltage threshold (3.4V), the system triggers an autonomous event to shed non-essential loads (Radio_TX, Payload) to safeguard core computing modules (CDH, Radio_RX).

🔹 Detumbling Actuation
File: ADCS/magnetorquer_controller.py

Implements a streamlined scalar version of standard B-dot control law damping matrices to counteract post-deployment high-rate spin using magnetic coils.

🛠️ Testing the Local Flight Simulation
To execute the core flight software orchestration loop and view aggregated operational frames locally, execute the main driver script:

Bash
python telemetry_generator.py
📈 Portfolio Interface
The project includes a client-side JavaScript mission controller board built to visually demonstrate FDIR triggers and dynamic telemetry streaming matching these precise back-end algorithms.
