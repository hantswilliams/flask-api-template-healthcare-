import os
import subprocess
from datetime import datetime


### in terminal run: safety scan --output html --save-html ./predeploy.checks/output.html
### to generate a report of all dependencies and their vulnerabilities

def check_dependencies_for_vulnerabilities():

    parent_dir = os.path.abspath(os.path.join("flask-api-template-healthcare", os.pardir))

    # Print the parent directory for debugging purposes
    print('Parent Directory: ', parent_dir)

    # Ensure the output directory exists (create if it doesn't)
    output_dir = os.path.join(parent_dir, "predeploy_checks/output")
    os.makedirs(output_dir, exist_ok=True)

    # Create a name for the output file that contains security_{timestamp}.html
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_name = f"security_dependencies_{timestamp}.html"

    # Specify the absolute path for the output HTML file
    output_file_path = os.path.join(output_dir, output_file_name)

    # Construct the safety check command with the absolute path
    command = ["safety", "check", "--output", "html", "--save-html", output_file_path]

    # Execute the command
    result = subprocess.run(command, cwd=parent_dir, capture_output=True, text=True)

    # bad_files = []

    # Check the result
    if result.returncode == 0:
        print("Safety check completed successfully.")
        print(result.stdout)
    else:
        print("Safety check encountered errors or vulnerabilities")
        print("\n Recommend to check the output file for more details: ", output_file_path)
        print(result.stderr)
        # bad_files.append(result.stderr)

    return "Completed safety check for dependencies."

    # return bad_files