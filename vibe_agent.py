import os
import subprocess
from google import genai
from google.genai import types

# 1. Initialize Client & Create Portfolio Directory
client = genai.Client()
TARGET_DIR = "./ShakthiSAT-Aerospace-Portfolio/04-CubeSat-Telemetry-Simulator"
os.makedirs(TARGET_DIR, exist_ok=True)

# 2. Define the Agent's File Write Tool
def write_code_file(filename: str, code_content: str) -> str:
    """Writes or overwrites a file in the portfolio directory."""
    filepath = os.path.join(TARGET_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code_content)
    return f"Successfully wrote file to {filepath}"

def execute_and_test_file(filename: str) -> str:
    """Runs the script to check for syntax or runtime errors."""
    filepath = os.path.join(TARGET_DIR, filename)
    try:
        # Runs script for up to 3 seconds to catch quick startup bugs
        result = subprocess.run(["python", filepath], capture_output=True, text=True, timeout=3)
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "Script ran successfully without immediate runtime crashes (Timeout reached)."
    except Exception as e:
        return f"Execution failed: {str(e)}"

# 3. Execution Orchestrator
def run_autonomous_builder(user_goal: str):
    print(f"🚀 Mission Control: Starting autonomous build for: '{user_goal}'")
    
    # Give the agent tool-use permissions and a strict systems-engineering prompt
    system_instruction = (
        "You are an autonomous aerospace software engineering agent. Your objective is to build functional scripts "
        "and iteratively fix them if they throw syntax/runtime errors. Always use write_code_file to save scripts "
        "and execute_and_test_file to verify they run perfectly."
    )
    
    # Maintain conversation state for the autonomous back-and-forth loop
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[write_code_file, execute_and_test_file],
            temperature=0.2
        )
    )
    
    response = chat.send_message(user_goal)
    
    # The Loop: The agent reviews execution results and adjusts code on its own
    for iteration in range(5):  # Limit to 5 reflective turns to prevent runaway infinite API usage
        if not response.function_calls:
            print("🎯 Agent completed task successfully!")
            break
            
        for function_call in response.function_calls:
            name = function_call.name
            args = function_call.args
            print(f"⚙️ Agent invoking tool: {name} with args {args}")
            
            # Dynamically execute the function specified by the LLM
            if name == "write_code_file":
                tool_output = write_code_file(**args)
            elif name == "execute_and_test_file":
                tool_output = execute_and_test_file(**args)
                print(f"📊 Execution Feedback to AI:\n{tool_output}")
                
            # Feed the execution results right back into the chat history
            response = chat.send_message(tool_output)

if __name__ == "__main__":
    mission_prompt = (
        "Create a file named telemetry_generator.py that outputs simulated orbital battery voltages. "
        "Test it to ensure there are no indentation or syntax errors."
    )
    run_autonomous_builder(mission_prompt)
