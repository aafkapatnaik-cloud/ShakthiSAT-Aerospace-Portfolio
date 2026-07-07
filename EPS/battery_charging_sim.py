"""
ShakthiSAT Flight Suite - Electrical Power System (EPS)
Battery Charging Simulator (battery_charging_sim.py)

Simulates continuous orbital battery state modifications, computing buck-converter 
efficiency behaviors across sunlight propagation horizons and eclipse intervals.
"""

# --- Orbital Engineering Constants ---
ORBIT_DURATION_MIN = 90       # Full orbital epoch period in minutes
SUNLIGHT_DURATION_MIN = 60    # Sunlight exposure period in minutes
ECLIPSE_DURATION_MIN = ORBIT_DURATION_MIN - SUNLIGHT_DURATION_MIN

SOLAR_ARRAY_VOLTAGE_V = 30.0  # Unregulated solar array bus voltage
SOLAR_ARRAY_CURRENT_A = 2.0   # Current generation profile under sunlight

BATTERY_NOMINAL_VOLTAGE_V = 12.0  # Main regulated battery pack bus
BATTERY_CAPACITY_AH = 10.0        # Pack capacity limit
CHARGING_EFFICIENCY = 0.90        # Buck converter power conversion efficiency
TIME_STEP_MIN = 1                 # Operational evaluation step interval


class BatteryChargingSimulation:
    """Manages energy accumulation vectors throughout an operational orbit."""

    def __init__(self, initial_soc_pct: float = 50.0):
        # Establish initial capacity based on input state-of-charge percentage
        self.battery_charge_ah = BATTERY_CAPACITY_AH * (initial_soc_pct / 100.0)
        self.time_elapsed_min = 0

    def run_orbit_simulation(self):
        """Simulates battery state across a complete orbital period loop."""
        print(f"--- EPS Battery Charging Sim Initialized ---")
        print(f"Orbital Epoch Duration : {ORBIT_DURATION_MIN} minutes")
        print(f"Initial State of Charge: {self.battery_charge_ah:.2f} Ah\n")

        while self.time_elapsed_min < ORBIT_DURATION_MIN:
            is_in_sunlight = self.time_elapsed_min < SUNLIGHT_DURATION_MIN
            charge_rate_ah_per_min = 0.0

            if is_in_sunlight:
                # Solar generation power evaluation (P = V * I)
                solar_power_w = SOLAR_ARRAY_VOLTAGE_V * SOLAR_ARRAY_CURRENT_A

                # Calculate current translation through an efficient buck profile
                # I_battery = (P_solar * efficiency) / V_battery
                current_into_battery_a = (solar_power_w * CHARGING_EFFICIENCY) / BATTERY_NOMINAL_VOLTAGE_V
                charge_rate_ah_per_min = current_into_battery_a / 60.0
            else:
                # System transitions to zero solar power during eclipse tracking
                charge_rate_ah_per_min = 0.0

            # Update battery storage value 
            self.battery_charge_ah += charge_rate_ah_per_min * TIME_STEP_MIN
            
            # CRITICAL ATOMIC CLAMP: Prevent battery overcharging past maximum hardware boundaries
            if self.battery_charge_ah > BATTERY_CAPACITY_AH:
                self.battery_charge_ah = BATTERY_CAPACITY_AH

            # Increment operational simulation step
            self.time_elapsed_min += TIME_STEP_MIN

        # Evaluate final state profiles
        final_soc_pct = (self.battery_charge_ah / BATTERY_CAPACITY_AH) * 100
        print(f"Simulation Epoch Completed Successfully.")
        print(f"Final Battery Capacity : {self.battery_charge_ah:.2f} Ah ({final_soc_pct:.2f}%)")
        print(f"Status: Charging model iteration NOMINAL")


if __name__ == "__main__":
    # Instantiate simulation starting at 50% capacity
    sim = BatteryChargingSimulation(initial_soc_pct=50.0)
    sim.run_orbit_simulation()
