"""
ShakthiSAT Flight Suite - Core System Driver
Telemetry Generator (telemetry_generator.py)

Orchestrates data packet generation by aggregating real-time subsystem state matrices
across the ADCS and EPS architectural nodes into standardized CCSDS-like telemetry frames.
"""

import random
import time

# Import structural flight submodules built across the workspace repository
from ADCS.magnetorquer_controller import calculate_detumbling_field
from EPS.power_distribution_manager import PowerDistributionManager
from EPS.solar_panel_sun_tracker import SolarPanelSunTracker


class SpacecraftTelemetryOrchestrator:
    """Manages global satellite sensor telemetry generation and packet routing."""

    def __init__(self):
        # Instantiate active managers to parse physical telemetry conditions
        self.pdu_manager = PowerDistributionManager(critical_threshold_v=3.4)
        self.sun_tracker = SolarPanelSunTracker()
        self.packet_counter = 0

    def generate_flight_frame(self) -> dict:
        """
        Samples operational subsystem environments and aggregates them into an atomic frame.
        
        Returns:
            dict: High-fidelity telemetry structural packet frame.
        """
        self.packet_counter += 1

        # 1. Sample Core Spacecraft Dynamics
        altitude_km = round(random.uniform(350.0, 420.0), 2)  # Low Earth Orbit (LEO) tracking
        system_temp_c = round(random.uniform(-15.0, 35.0), 2)

        # 2. Extract EPS Subsystem telemetry metrics 
        simulated_bus_voltage = round(random.uniform(3.2, 4.1), 2)  # Fluctuating battery cell bus
        pdu_telemetry = self.pdu_manager.check_battery_voltage(simulated_bus_voltage)

        # 3. Simulate and resolve EPS Solar Tracking alignment
        mock_sun_vector = (random.choice([-1.0, 0.707, 1.0]), random.choice([0.0, 0.707, -1.0]))
        target_panel_angle = self.sun_tracker.calculate_optimal_angle(mock_sun_vector)

        # 4. Extract ADCS Detumbling vector command states
        mock_magnetometer_input = [1.2e-5, -0.4e-5, 2.1e-5]
        commanded_dipole = calculate_detumbling_field(mock_magnetometer_input)
        formatted_dipole = [float(f"{val:.2e}") for val in commanded_dipole]

        # Assemble unified CCSDS-structured dictionary payload
        return {
            "HEADER": {
                "packet_id": self.packet_counter,
                "timestamp_epoch": round(time.time(), 2),
                "system_mode": pdu_telemetry["mode"]
            },
            "SYS_HEALTH": {
                "altitude_km": altitude_km,
                "core_temp_c": system_temp_c
            },
            "EPS_METRICS": {
                "bus_voltage_v": simulated_bus_voltage,
                "rails_status": pdu_telemetry["rails"],
                "panel_actuator_target_deg": target_panel_angle
            },
            "ADCS_METRICS": {
                "mag_input_t": mock_magnetometer_input,
                "commandED_field_t": formatted_dipole
            }
        }


if __name__ == "__main__":
    print("====================================================")
    print("Starting ShakthiSAT Operational Telemetry Suite Simulator")
    print("====================================================\n")
    
    orchestrator = SpacecraftTelemetryOrchestrator()

    # Simulate 3 sequential housekeeping cycles
    for cycle in range(3):
        print(f"--- Housekeeping Cycle Frame {cycle + 1} ---")
        frame = orchestrator.generate_flight_frame()
        
        # Display aggregated structural telemetry data streams
        print(f"  [Header] Packet ID: {frame['HEADER']['packet_id']} | Mode: {frame['HEADER']['system_mode']}")
        print(f"  [Health] Altitude: {frame['SYS_HEALTH']['altitude_km']} km | Temp: {frame['SYS_HEALTH']['core_temp_c']}°C")
        print(f"  [EPS]    Bus Power: {frame['EPS_METRICS']['bus_voltage_v']}V | Rail Outages: {not all(frame['EPS_METRICS']['rails_status'].values())}")
        print(f"  [EPS]    Solar Panel Tracking Array Align Angle: {frame['EPS_METRICS']['panel_actuator_target_deg']}°")
        print(f"  [ADCS]   Commanded Detumbling Dipole Vector: {frame['ADCS_METRICS']['commandED_field_t']} T\n")
        
        time.sleep(1)

    print("Telemetry simulation period cycled down successfully.")
