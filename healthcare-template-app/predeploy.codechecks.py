## look across all .html files that contain <script> tags,
## and make sure `<script nonce="{{ csp_nonce() }}">` exists in each <script> tag

import os
import re
import fnmatch
import subprocess
from colorama import Fore, Style
from datetime import datetime











# ### Part 1: Check for nonces in script tags // this is related to 
# ### the Talisman configuration in the Flask app in production mode
# def check_html_files_for_nonce(directory):
#     # Regular expressions
#     script_tag_regex = re.compile(r"<script.*?>", re.DOTALL)
#     nonce_regex = re.compile(r"nonce=")

#     # Dictionaries to store good and bad files
#     good_files = []
#     bad_files = []
#     no_script_files = []

#     # Walk through the directory
#     for root, _, files in os.walk(directory):
#         for filename in fnmatch.filter(files, "*.html"):  # Filter for HTML files
#             file_path = os.path.join(root, filename)
#             with open(file_path, "r", encoding="utf-8") as file:
#                 content = file.read()

#                 # Find script tags
#                 script_tags = script_tag_regex.findall(content)

#                 if script_tags:
#                     # Check each script tag for nonce
#                     script_with_nonce = any(
#                         nonce_regex.search(tag) for tag in script_tags
#                     )
#                     if script_with_nonce:
#                         # Good file: contains at least one script tag with nonce
#                         good_files.append(file_path)
#                     else:
#                         # Bad file: contains script tags but none with nonce
#                         bad_files.append(file_path)
#                 else:
#                     # File does not contain any script tags
#                     no_script_files.append(file_path)

#     # Printing the results
#     print("Files with script tags and nonce present:")
#     for path in good_files:
#         print(f"Good: {path}")

#     print("\nFiles with script tags but nonce missing:")
#     for path in bad_files:
#         print(f"Bad: {path}")

#     print("\nFiles without any script tags:")
#     for path in no_script_files:
#         print(f"No Script: {path}")

#     return good_files, bad_files, no_script_files

# # Replace 'templates' with the path to your Flask templates directory
# good_files, bad_files, no_script_files = check_html_files_for_nonce("templates")

# print("Checking for nonces in script tags...")

# check_html_files_for_nonce("templates")

# print("Nonce check complete.")
# print(
#     Fore.RED
#     + "List of html files with script tags that do not contain `nonce=` that will break in production mode. THESE NEED TO BE FIXED: ",
#     bad_files,
# )
# print(Style.RESET_ALL)

# print(
#     Fore.GREEN
#     + "List of html files with script tags that contain `nonce=` which will SUCCEED in production mode: ",
#     [good_files],
# )
# print(Style.RESET_ALL)

# print(
#     Fore.BLUE
#     + "List of html files without any javascript tags that will SUCCEED in production mode: ",
#     [good_files],
# )
# print(Style.RESET_ALL)












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
    with open(f"predeploy-checks/{output_file_name}", "w") as file:
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


print("Applying Ruff formatting...")

# Replace 'your_project_directory' with the path to your project or subdirectory you want to format
ruff_errors = format_with_ruff(".")

if ruff_errors:
    print(
        Fore.RED
        + "Errors found in the Ruff formatting. Please review the error messages above and make the necessary changes to the files."
    )
    print(Style.RESET_ALL)
else:
    print(Fore.GREEN + "Ruff formatting complete.")
    print(Style.RESET_ALL)

















# ### in terminal run: safety scan --output html --save-html ./predeploy.checks/output.html
# ### to generate a report of all dependencies and their vulnerabilities

# def check_dependencies_for_vulnerabilities():

#     parent_dir = os.path.abspath(os.path.join("flask-api-template-healthcare", os.pardir))

#     # Print the parent directory for debugging purposes
#     print('Parent Directory: ', parent_dir)

#     # Ensure the output directory exists (create if it doesn't)
#     output_dir = os.path.join(parent_dir, "predeploy-checks")
#     os.makedirs(output_dir, exist_ok=True)

#     # Create a name for the output file that contains security_{timestamp}.html
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     output_file_name = f"security_dependencies_{timestamp}.html"

#     # Specify the absolute path for the output HTML file
#     output_file_path = os.path.join(output_dir, output_file_name)

#     # Construct the safety check command with the absolute path
#     command = ["safety", "check", "--output", "html", "--save-html", output_file_path]

#     # Execute the command
#     result = subprocess.run(command, cwd=parent_dir, capture_output=True, text=True)

#     # bad_files = []

#     # Check the result
#     if result.returncode == 0:
#         print("Safety check completed successfully.")
#         print(result.stdout)
#     else:
#         print("Safety check encountered errors or vulnerabilities")
#         print("\n Recommend to check the output file for more details: ", output_file_path)
#         print(result.stderr)
#         # bad_files.append(result.stderr)

#     return "Completed safety check for dependencies."

#     # return bad_files

# # run the safety check
# check_dependencies_for_vulnerabilities()























# # ## Bandit security check

# def check_code_for_security_flaws():
#     # Determine the parent directory of the target application
#     parent_dir = os.path.abspath(os.path.join("flask-api-template-healthcare", os.pardir))

#     # Ensure the output directory exists (create if it doesn't)
#     output_dir = os.path.join(parent_dir, "predeploy-checks")
#     os.makedirs(output_dir, exist_ok=True)

#     # Create a name for the output file that contains security_bandit_{timestamp}.txt
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     output_file_name = f"security_bandit_{timestamp}.txt"

#     # Specify the absolute path for the Bandit output file
#     output_file_path = os.path.join(output_dir, output_file_name)

#     # Construct the Bandit command with the output file path
#     # Using the '-r' option to recursively check all python files from the parent directory
#     command = ["bandit", "-r", ".", "-f", "txt", "-o", output_file_path]

#     # Execute the command in the parent directory
#     result = subprocess.run(command, cwd=parent_dir, capture_output=True, text=True)

#     # Optionally, print any stderr output or handle it in some way
#     if result.stderr:
#         print("Error:", result.stderr)

#     return "Completed Bandit security check for code."

# # Remember to call the function to perform the check
# check_code_for_security_flaws()













# # Verison bumper
# def bump_version():
#     version_file = "version.txt"
#     major, minor, patch = 0, 0, 0

#     # Read the current version
#     with open(version_file, "r") as file:
#         major, minor, patch = map(int, file.read().strip().split("."))

#     # Increment the patch version
#     patch += 1

#     # Write the new version back
#     with open(version_file, "w") as file:
#         new_version = f"{major}.{minor}.{patch}"
#         file.write(new_version)

#     return new_version


# #### if ruff_errors is empty and bad_files is empty, then the code checks pass
# #### and we should print a success message in all bold green text

# ruff_errors = []
# bad_files = []

# if not ruff_errors and not bad_files:
#     # Bump the version
#     new_version = bump_version()
#     print(f"\n Bumped to new version: {new_version} \n")

#     print(
#         Fore.GREEN
#         + Style.BRIGHT
#         + """
#           ALL CODE CHECKS PASSED...YOU'RE GOOD TO GO! \n
#           No errors found in the code checks for embedded scripts and ruff formatting. \n
#           Please proceed with the deployment process. \n"""
#     )
#     print(Style.RESET_ALL)

# #### if ruff_errors is not empty or bad_files is not empty, then the code checks fail

# else:
#     print(
#         Fore.RED
#         + Style.BRIGHT
#         + """
#           CODE CHECKS FAILED...PLEASE REVIEW AND RESOLVE ISSUES! \n
#           Errors found in the code checks for embedded scripts and ruff formatting. \n
#           Please review the error messages above and make the necessary changes to the files. \n"""
#     )
#     print(Style.RESET_ALL)
#     exit(1)
