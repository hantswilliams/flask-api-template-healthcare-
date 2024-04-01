
# Verison bumper
def bump_version():
    version_file = "version.txt"
    major, minor, patch = 0, 0, 0

    # Read the current version
    with open(version_file, "r") as file:
        major, minor, patch = map(int, file.read().strip().split("."))

    # Increment the patch version
    patch += 1

    # Write the new version back
    with open(version_file, "w") as file:
        new_version = f"{major}.{minor}.{patch}"
        file.write(new_version)

    return new_version

