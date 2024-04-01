import os
import subprocess
from datetime import datetime

def check_code_for_security_flaws():
    # Determine the parent directory of the target application
    parent_dir = os.path.abspath(os.path.join("flask-api-template-healthcare", os.pardir))

    # Ensure the output directory exists (create if it doesn't)
    output_dir = os.path.join(parent_dir, "predeploy_checks/output")
    os.makedirs(output_dir, exist_ok=True)

    # Create a name for the output file that contains security_bandit_{timestamp}.txt
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_name = f"security_bandit_{timestamp}.txt"

    # Specify the absolute path for the Bandit output file
    output_file_path = os.path.join(output_dir, output_file_name)

    # Construct the Bandit command with the output file path
    # Using the '-r' option to recursively check all python files from the parent directory
    command = ["bandit", "-r", ".", "-f", "txt", "-o", output_file_path]

    # Execute the command in the parent directory
    result = subprocess.run(command, cwd=parent_dir, capture_output=True, text=True)

    # Optionally, print any stderr output or handle it in some way
    if result.stderr:
        print("Error:", result.stderr)

    return "Completed Bandit security check for code."

# Remember to call the function to perform the check