import subprocess
from colorama import Fore, Style
from datetime import datetime

## Part 2: Run Ruff to format the code
## now run ruff format . to format all files in the healthcare-template-app directory
def format_with_ruff(directory):
    # Construct the Ruff formatting command
    command = ["ruff", "check", directory]

    # Execute the command
    result = subprocess.run(command, capture_output=True, text=True)

    print('What we got from ruff result command: ', result)

    ## save result as ruff_check_{timestamp}.txt inside predeploy-checks directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_name = f"formatting_ruff_{timestamp}.txt"
    with open(f"predeploy_checks/output/{output_file_name}", "w") as file:
        file.write(result.stdout)

    ruff_errors = []
    
    # Check the result
    if result.returncode == 0:
        print("Ruff formatting applied successfully.")
        print(result.stdout)
    else:
        print("Ruff formatting encountered errors:")
        print(result.stderr)
        ruff_errors.append(result.stderr)

    return ruff_errors


