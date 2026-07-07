"""
ShakthiSAT Flight Suite - Electrical Power System (EPS)
Power Distribution Manager (power_distribution_manager.py)

Implements an autonomous Fault Detection, Isolation, and Recovery (FDIR) loop
monitoring main battery bus voltage and executing load-shedding commands.
"""


class PowerDistributionManager:
    """Manages satellite power rails and executes safety load-shedding sequences."""

    def __init__(self, critical_threshold_v: float = 3.4):
        self.critical_threshold_v = critical_threshold_v
        # Track active operational mode: "NOMINAL" or "SAFE_MODE"
        self.system_mode = "NOMINAL"
        # Track mock hardware power rail configurations
        self.rails_online = {
            "CDH": True,        # Command & Data Handling (Essential)
            "Radio_RX": True,   # Communications Receiver (Essential)
            "Radio_TX": True,   # Communications Transmitter (Non-Essential under fault)
            "Payload": True     # Scientific Instruments (Non-Essential)
        }

    def check_battery_voltage(self, voltage: float) -> dict:
        """
        Evaluates battery telemetry, updates system mode, and sheds power loads if necessary.

        Args:
            voltage (float): Current main battery bus voltage measurement in Volts.

        Returns:
            dict: Current state summary of the distribution bus.
        """
        if voltage < self.critical_threshold_v:
            self.system_mode = "SAFE_MODE"
            # Execute load shedding: Isolation of non-essential components
            self.rails_online["Radio_TX"] = False
            self.rails_online["Payload"] = False
            
            print(f"[CRITICAL FAULT] Main battery bus voltage dropped to {voltage:.2f}V (Threshold: {self.critical_threshold_v}V).")
            print("Action: Engaging Emergency SAFE_MODE. Load-shedding non-essential payloads and high-power radio transmissions.")
        else:
            self.system_mode = "NOMINAL"
            # Restore full operational infrastructure
            self.rails_online["Radio_TX"] = True
            self.rails_online["Payload"] = True
            print(f"[INFO] Main battery bus voltage is {voltage:.2f}V. Distribution rails nominal.")

        return {
            "mode": self.system_mode,
            "rails": self.rails_online.copy()
        }


if __name__ == "__main__":
    print("--- EPS Power Distribution Manager Self-Test ---")
    pdu = PowerDistributionManager(critical_threshold_v=3.4)

    print("\nScenario 1: Voltage is good (3.7V)")
    telemetry_1 = pdu.check_battery_voltage(3.7)
    print(f"Active Rails Status: {telemetry_1['rails']}")

    print("\nScenario 2: Voltage falls below threshold (3.3V)")
    telemetry_2 = pdu.check_battery_voltage(3.3)
    print(f"Active Rails Status: {telemetry_2['rails']}")

    print("\nScenario 3: Voltage recovers to borderline threshold (3.4V)")
    telemetry_3 = pdu.check_battery_voltage(3.4)
    print(f"Active Rails Status: {telemetry_3['rails']}")
    print("\nStatus: Power distribution FDIR routine execution NOMINAL")
