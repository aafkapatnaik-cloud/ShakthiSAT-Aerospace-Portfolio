"""
ShakthiSAT Flight Suite - Electrical Power System (EPS)
Solar Panel Sun Tracker (solar_panel_sun_tracker.py)

Resolves external sun position tracking vectors into structural actuator target 
angles using clear quadrant-safe trigonometric mappings.
"""

import math


class SolarPanelSunTracker:
    """Calculates optimal articulation alignment angles for active solar tracking."""

    def __init__(self):
        pass

    def calculate_optimal_angle(self, sun_vector: tuple) -> float:
        """
        Calculates the optimal alignment angle in degrees for a single axis panel array.

        Args:
            sun_vector (tuple): A 2D positional coordinate reference array (X, Y).

        Returns:
            float: An absolute target angular correction localized between 0 and 360 degrees.
        """
        # Extract vector components
        x, y = sun_vector

        # Handle zero vector edge cases to protect trigonometric system stability
        if x == 0.0 and y == 0.0:
            return 0.0

        # Resolve vector to radians and convert to absolute degrees
        angle_rad = math.atan2(y, x)
        angle_deg = math.degrees(angle_rad)

        # CRITICAL ATOMIC WRAP: Map negative quadrant bounds (-180 to 0) to a positive 360 loop
        if angle_deg < 0:
            angle_deg += 360.0

        return round(angle_deg, 2)


def execute_tracking_sweep():
    """Simulates active tracking corrections against transient orbital sun profiles."""
    tracker = SolarPanelSunTracker()

    # Simulated sun position arrays targeting distinct array alignment points
    sun_position_vectors = [
        (1.0, 0.0),       # Scenario 1: Sun directly in alignment sector (0 degrees)
        (0.707, 0.707),   # Scenario 2: Sun offset in positive quadrant (45 degrees)
        (-1.0, 0.0),      # Scenario 3: Sun directly in reverse western sector (180 degrees)
        (0.0, -1.0)       # Scenario 4: Sun position in southern sector (270 degrees)
    ]

    print("--- EPS Solar Panel Tracking Matrix Run ---")
    
    for idx, sun_vector in enumerate(sun_position_vectors):
        optimal_angle = tracker.calculate_optimal_angle(sun_vector)
        print(f"Array Interface Segment {idx + 1}:")
        print(f"  Transient Input Sun Vector : {sun_vector}")
        print(f"  Target Actuation Command   : {optimal_angle}°")

    print("\nStatus: Solar articulation calculation sweep NOMINAL")


if __name__ == "__main__":
    execute_tracking_sweep()
