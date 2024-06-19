import subprocess

def read_packages(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        # Use list comprehension to strip whitespace and filter out empty lines
        return {line.strip().split('==')[0] for line in f if line.strip()}

# Read packages from requirements.txt
required_packages = read_packages('requirements.txt')

# Read currently installed packages
installed_packages = read_packages('installed_packages.txt')

# Find packages to uninstall
packages_to_uninstall = installed_packages - required_packages

# Uninstall packages not in requirements.txt
for package in packages_to_uninstall:
    subprocess.call(['pip', 'uninstall', '-y', package])

print("Unnecessary packages removed.")
