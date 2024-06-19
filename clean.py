import subprocess

# Read packages from requirements.txt
with open('requirements.txt', 'r') as f:
    required_packages = {line.strip().split('==')[0] for line in f.readlines()}

# Read currently installed packages
with open('installed_packages.txt', 'r') as f:
    installed_packages = {line.strip().split('==')[0] for line in f.readlines()}

# Find packages to uninstall
packages_to_uninstall = installed_packages - required_packages

# Uninstall packages not in requirements.txt
for package in packages_to_uninstall:
    subprocess.call(['pip', 'uninstall', '-y', package])

print("Unnecessary packages removed.")
