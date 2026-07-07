"""
ShakthiSAT Flight Suite - Electrical Power System (EPS)
Shunt Regulator Simulation (shunt_regulator.py)

Models active power regulation loops, evaluating power dump limits when 
solar arrays generate power exceeding maximum battery capacity.
"""


class FlightBattery:
    """Represents the main satellite battery system storage architecture."""

    def __init__(self, capacity_wh: float, initial_soc_pct: float):
        self.capacity_wh = capacity_wh
        self.soc_percent = initial_soc_pct
        self.current_charge_wh = (capacity_wh * initial_soc_pct) / 100.0

    def charge(self, power_watts: float, duration_hours: float) -> float:
        """
        Calculates and applies energy absorption profile limits.

        Returns:
            float: Precise amount of energy absorbed in Watt-hours (Wh).
        """
        potential_energy_wh = power_watts * duration_hours
        available_headroom_wh = self.capacity_wh - self.current_charge_wh

        if potential_energy_wh >= available_headroom_wh:
            # Battery only absorbs what it can hold up to absolute capacity limits
            actual_absorbed_wh = available_headroom_wh
            self.current_charge_wh = self.capacity_wh
            self.soc_percent = 100.0
        else:
            actual_absorbed_wh = potential_energy_wh
            self.current_charge_wh += actual_absorbed_wh
            self.soc_percent = (self.current_charge_wh / self.capacity_wh) * 100.0

        return actual_absorbed_wh


class ShuntRegulator:
    """Manages excessive electrical energy conversion into safe thermal dissipation."""

    def __init__(self, max_dissipation_watts: float):
        self.max_dissipation_watts = max_dissipation_watts
        self.dissipated_power_watts = 0.0

    def dissipate_excess_power(self, excess_power_watts: float) -> float:
        """Dumps excess power loads safely up to the hardware resistor capacity threshold."""
        if excess_power_watts > 0:
            self.dissipated_power_watts = min(excess_power_watts, self.max_dissipation_watts)
            return self.dissipated_power_watts
        
        self.dissipated_power_watts = 0.0
        return 0.0


def run_bus_simulation():
    """Simulates active EPS bus regulation across a generation window."""
    # Simulation Hyperparameters
    BATTERY_CAPACITY_WH = 1000
    INITIAL_SOC_PERCENT = 80.0
    SOLAR_PANEL_POWER_WATTS = 100.0
    SIMULATION_DURATION_HOURS = 5.0
    TIME_STEP_HOURS = 0.5  # Stride interval block duration

    # Component Instantiations
    battery = FlightBattery(BATTERY_CAPACITY_WH, INITIAL_SOC_PERCENT)
    shunt = ShuntRegulator(max_dissipation_watts=150.0)

    print("--- EPS Shunt Regulator & Bus Manager Initialization ---")
    print(f"Initial Battery SoC: {battery.soc_percent:.2f}%\n")

    time_elapsed = 0.0
    while time_elapsed < SIMULATION_DURATION_HOURS:
        time_elapsed += TIME_STEP_HOURS
        
        # Potential input energy calculated over the current time step
        generated_power = SOLAR_PANEL_POWER_WATTS
        total_energy_input_wh = generated_power * TIME_STEP_HOURS

        # Process charge absorption paths
        actual_energy_absorbed_wh = battery.charge(generated_power, TIME_STEP_HOURS)
        
        # Unabsorbed energy translates back to excess power on the bus
        excess_energy_wh = total_energy_input_wh - actual_energy_absorbed_wh
        excess_power_watts = excess_energy_wh / TIME_STEP_HOURS

        # Regulate bus using the shunt architecture
        shunt.dissipate_excess_power(excess_power_watts)

        # Periodic telemetry monitoring output printout
        print(f"T + {time_elapsed:.1f} Hours | Bus State: SoC={battery.soc_percent:.1f}% | "
              f"Absorbed={actual_energy_absorbed_wh / TIME_STEP_HOURS:.1f}W | "
              f"Shunt Dissipation={shunt.dissipated_power_watts:.1f}W")

    print("\n--- Simulation Period Terminated ---")
    print(f"Final Battery Capacity Profile State: {battery.soc_percent:.2f}%")
    print("Status: EPS Bus Shunt Regulation Model NOMINAL")


if __name__ == "__main__":
    run_bus_simulation()
