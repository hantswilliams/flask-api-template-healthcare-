import os
import re
import fnmatch
from datetime import datetime


def check_html_files_for_nonce(directory):
    # Regular expressions
    script_tag_regex = re.compile(r"<script.*?>", re.DOTALL)
    nonce_regex = re.compile(r"nonce=")

    # Dictionaries to store good and bad files
    good_files = []
    bad_files = []
    no_script_files = []

    # Walk through the directory
    for root, _, files in os.walk(directory):
        for filename in fnmatch.filter(files, "*.html"):  # Filter for HTML files
            file_path = os.path.join(root, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

                # Find script tags
                script_tags = script_tag_regex.findall(content)

                if script_tags:
                    # Check each script tag for nonce
                    script_with_nonce = any(
                        nonce_regex.search(tag) for tag in script_tags
                    )
                    if script_with_nonce:
                        # Good file: contains at least one script tag with nonce
                        good_files.append(file_path)
                    else:
                        # Bad file: contains script tags but none with nonce
                        bad_files.append(file_path)
                else:
                    # File does not contain any script tags
                    no_script_files.append(file_path)

    # Printing the results
    print("Files with script tags and nonce present:")
    for path in good_files:
        print(f"Good: {path}")

    print("\nFiles with script tags but nonce missing:")
    for path in bad_files:
        print(f"Bad: {path}")

    print("\nFiles without any script tags:")
    for path in no_script_files:
        print(f"No Script: {path}")

    if good_files:
        print("Good files: ", good_files)
        ### save good_files as a text file with datetime stamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file_name = f"security_nonce_html_good_{timestamp}.txt"
        with open(f"predeploy_checks/output/{output_file_name}", "w") as file:
            file.write("Files with script tags and nonce present:\n")
            for path in good_files:
                file.write(f"{path}\n")

    if bad_files:
        ### save bad_files as a text file with datetime stamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file_name = f"security_nonce_html_bad_{timestamp}.txt"
        with open(f"predeploy_checks/output/{output_file_name}", "w") as file:
            file.write("Files with script tags but nonce missing:\n")
            for path in bad_files:
                file.write(f"{path}\n")

    return good_files, bad_files, no_script_files