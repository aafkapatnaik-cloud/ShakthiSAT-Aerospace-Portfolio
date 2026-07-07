"""
ShakthiSAT Flight Suite - Electrical Power System (EPS)
Depth of Discharge Tracker (depth_of_discharge_tracker.py)

Simulates multi-epoch battery health degradation vectors as a linear decay 
function bound to orbital Depth of Discharge (DoD) profiling metrics.
"""

import random


class DepthOfDischargeTracker:
    """Tracks state-of-health degradation across prolonged orbital cycling epochs."""

    def __init__(self, initial_capacity_pct: float = 100.0):
        self.initial_capacity = initial_capacity_pct
        self.current_capacity = initial_capacity_pct
        self.capacity_history = [initial_capacity_pct]

    def _simulate_orbit_dod(self) -> float:
        """
        Simulates individual orbital Depth of Discharge variance markers.
        Assumes nominal operating conditions fluctuate between 10% and 30%.
        """
        return random.uniform(0.10, 0.30)

    def track_degradation(self, num_orbits: int = 1000, report_interval: int = 100):
        """
        Executes a long-horizon flight lifetime cycle degradation evaluation loop.

        Args:
            num_orbits (int): Total operational orbits to calculate. Default 1000.
            report_interval (int): Console log printing stride step interval to prevent stdout flood.
        """
        print(f"--- EPS Battery Degradation Tracker Initialized ---")
        print(f"Starting Pack Capacity Base: {self.initial_capacity:.2f}%\n")

        for orbit_idx in range(1, num_orbits + 1):
            dod = self._simulate_orbit_dod()
            
            # Algorithmic degradation factor: capacity reduces based on cycle depth
            degradation_factor = dod * 0.001
            self.current_capacity -= (self.initial_capacity * degradation_factor)

            # Atomic boundary clamp to protect mathematical limits
            if self.current_capacity <= 0:
                self.current_capacity = 0.0
                self.capacity_history.append(self.current_capacity)
                print(f"[ALERT] Battery fully degraded after {orbit_idx} orbits.")
                break

            self.capacity_history.append(self.current_capacity)

            # Periodic status telemetry logging to avoid terminal flooding
            if orbit_idx % report_interval == 0 or orbit_idx == 1:
                print(f"Orbit {orbit_idx:04d} -> Sampled DoD: {dod:.2f} | Estimated Remaining State-of-Health: {self.current_capacity:.2f}%")

        print(f"\nSimulation Complete across {num_orbits} Orbital Epochs.")
        print(f"Final Residual Capacity: {self.current_capacity:.2f}%")
        print(f"Status: Battery health decay modeling NOMINAL")
        return self.capacity_history


if __name__ == "__main__":
    # Instantiate tracker and map life assessment across 1,000 continuous loops
    tracker = DepthOfDischargeTracker(initial_capacity_pct=100.0)
    tracker.track_degradation(num_orbits=1000, report_interval=200)
