# ShakthiSAT Operational Flight Software Suite & Architecture Simulation

An embedded-style, zero-dependency Python flight software (FSW) architecture and interactive telemetry suite for the **ShakthiSAT CubeSat mission**. This repository demonstrates production-grade modularity, attitude determination control operations, autonomous electrical fault protection, and telemetry stream orchestration.

🌐 **[Live Interactive Mission Control Dashboard](https://aafkapatnaik-cloud.github.io/ShakthiSAT-Aerospace-Portfolio/)**

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
