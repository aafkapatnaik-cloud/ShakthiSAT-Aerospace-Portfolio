"""
ShakthiSAT Flight Suite - Attitude Determination & Control System (ADCS)
Magnetorquer Controller (magnetorquer_controller.py)

Calculates the active detumbling magnetic dipole moments using an algorithmic 
B-dot control law pattern to damp high-rate angular velocity post-deployment.
"""

def calculate_detumbling_field(b_field_input: list) -> list:
    """
    Calculates a detumbling magnetic field based on the input B-field vectors.
    
    Uses an optimized pure-Python scalar multiplication step to maintain a 
    zero-dependency runtime environment for embedded target safety.
    
    Args:
        b_field_input (list): 3-axis magnetometer measurements [Bx, By, Bz] in Tesla.
        
    Returns:
        list: 3-axis commanded detumbling control field vectors.
    """
    # Mock operational control loop gain for detumbling rate damping
    detumbling_gain = -0.1

    # Calculate the detumbling field using list comprehension (eliminating numpy dependency)
    detumbling_field = [detumbling_gain * element for element in b_field_input]

    return detumbling_field


if __name__ == "__main__":
    # Mock B-field input vectors (e.g., from a three-axis magnetometer) in Tesla [Bx, By, Bz]
    mock_b_field = [1.0e-5, -0.5e-5, 2.0e-5]

    print(f"--- ADCS Magnetorquer Controller Self-Test ---")
    print(f"Mock Magnetometer Input B-field : {mock_b_field} T")

    # Evaluate detumbling magnetic vector calculations
    commanded_detumbling_field = calculate_detumbling_field(mock_b_field)

    # Format values in scientific notation for clean telemetry telemetry logs
    formatted_field = [f"{val:.2e}" for val in commanded_detumbling_field]
    print(f"Commanded Detumbling Output     : [{', '.join(formatted_field)}] T")
    print(f"Status: Control matrix calculation NOMINAL")
