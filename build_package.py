#!/usr/bin/env python
"""Build script for creating and publishing the package to PyPI."""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command):
    """Run a shell command and print output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        sys.exit(1)

def clean_build():
    """Clean build directories."""
    print("\nCleaning build directories...")
    directories = ['build', 'dist', 'distributedapps_mas.egg-info']
    for directory in directories:
        if os.path.exists(directory):
            run_command(f'rm -rf {directory}')

def build_package():
    """Build the package."""
    print("\nBuilding package...")
    run_command('python -m pip install --upgrade pip')
    run_command('python -m pip install --upgrade build')
    run_command('python -m build')

def check_package():
    """Check the package for errors."""
    print("\nChecking package...")
    run_command('python -m pip install --upgrade twine')
    run_command('twine check dist/*')

def publish_test():
    """Publish to TestPyPI."""
    print("\nPublishing to TestPyPI...")
    run_command('twine upload --repository testpypi dist/*')

def publish_prod():
    """Publish to PyPI."""
    print("\nPublishing to PyPI...")
    run_command('twine upload dist/*')

def main():
    """Main build process."""
    # Ensure we're in the correct directory
    os.chdir(Path(__file__).parent)
    
    print("=== Building distributedapps-mas Package ===")
    
    # Clean previous builds
    clean_build()
    
    # Build package
    build_package()
    
    # Check package
    check_package()
    
    # Ask for publishing
    while True:
        choice = input("""
Choose an action:
1. Publish to TestPyPI
2. Publish to PyPI
3. Exit
Choice (1-3): """)
        
        if choice == '1':
            publish_test()
            print("\nTest installation command:")
            print("pip install --index-url https://test.pypi.org/simple/ distributedapps-mas")
            break
        elif choice == '2':
            publish_prod()
            print("\nInstallation command:")
            print("pip install distributedapps-mas")
            break
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
