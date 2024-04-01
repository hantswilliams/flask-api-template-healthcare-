## look across all .html files that contain <script> tags,
## and make sure `<script nonce="{{ csp_nonce() }}">` exists in each <script> tag

from colorama import Fore, Style
from predeploy_checks.code.formatting_ruff import format_with_ruff
from predeploy_checks.code.security_nonce_html import check_html_files_for_nonce
from predeploy_checks.code.security_dependencies import check_dependencies_for_vulnerabilities
from predeploy_checks.code.security_bandit import check_code_for_security_flaws
from predeploy_checks.code.version_bumper import bump_version


###### PART 1 ########
###### PART 1 ########
###### PART 1 ########
###### PART 1 ########
###### PART 1 ########
### Check for nonces in script tags // this is related to, replace 'templates' with the path to your Flask templates directory
print("\n \n \n PART 1: Checking for nonces in script tags...\n \n \n")
good_files, bad_files, no_script_files = check_html_files_for_nonce("templates")

print("Checking for nonces in script tags...")
check_html_files_for_nonce("templates")
print("Nonce check complete.")
print(
    Fore.RED
    + "List of html files with script tags that do not contain `nonce=` that will break in production mode. THESE NEED TO BE FIXED: ",
    bad_files,
)
print(Style.RESET_ALL)
print(
    Fore.GREEN
    + "List of html files with script tags that contain `nonce=` which will SUCCEED in production mode: ",
    [good_files],
)
print(Style.RESET_ALL)
print(
    Fore.BLUE
    + "List of html files without any javascript tags that will SUCCEED in production mode: ",
    [good_files],
)
print(Style.RESET_ALL)




###### PART 2 ########
###### PART 2 ########
###### PART 2 ########
###### PART 2 ########
###### PART 2 ########
####### RUFF CHECKS FOR FORMATTING 
print("\n \n \n PART 2: Checking for Ruff formatting...\n \n \n")
print("Applying Ruff formatting...")
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



###### PART 3 ########
###### PART 3 ########
###### PART 3 ########
###### PART 3 ########
###### PART 3 ########
###### PART 3 ########
# run the safety check for dependencies with known vulnerabilities
print("\n \n \n PART 3: Checking for dependencies with known vulnerabilities...\n \n \n")
print("Checking for dependencies with known vulnerabilities with SAFETY...")
check_dependencies_for_vulnerabilities()




###### PART 4 ########
###### PART 4 ########
###### PART 4 ########
###### PART 4 ########
###### PART 4 ########
###Bandit security check
print("\n \n \n PART 4: Checking for security flaws in the code...\n \n \n")
print("Checking for security flaws in the code with BANDIT...")
check_code_for_security_flaws()



###### PART 5 ########
###### PART 5 ########
###### PART 5 ########
###### PART 5 ########
###### PART 5 ########
###### PART 5 ########
# # Verison bumper
# Bump the version
print("\n \n \n PART 5: Bumping the version...\n \n \n")
new_version = bump_version()
print(f"\n Bumped to new version: {new_version} \n")