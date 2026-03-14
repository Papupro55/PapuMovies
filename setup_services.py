#!/usr/bin/env python3
"""
PapuMovies Microservices - Setup Script
This script installs dependencies for all services
"""

import os
import sys
import subprocess
from pathlib import Path

# Define services and their directories
SERVICES = {
    'frontend': 'frontend',
    'movie-service': 'movie-service',
    'rating-service': 'rating-service',
    'trailer-service': 'trailer-service'
}

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50 + "\n")

def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"❌ {text}")

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print_error(f"Python 3.8+ required. You have {sys.version}")
        sys.exit(1)
    print_success(f"Python version: {sys.version.split()[0]}")

def check_pip():
    """Check if pip is available"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
        print_success("pip is available")
        return True
    except subprocess.CalledProcessError:
        print_error("pip is not available")
        return False

def install_service_dependencies(service_name, service_dir):
    """Install dependencies for a specific service"""
    print_info(f"Installing dependencies for {service_name}...")
    
    requirements_file = Path(service_dir) / "requirements.txt"
    
    if not requirements_file.exists():
        print_error(f"requirements.txt not found in {service_dir}")
        return False
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            check=True
        )
        print_success(f"{service_name} dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install {service_name} dependencies: {e}")
        return False

def main():
    """Main setup function"""
    print_header("PapuMovies - Microservices Setup")
    
    print("This script will install dependencies for all services:\n")
    for service_name, service_dir in SERVICES.items():
        print(f"  • {service_name} ({'Python': service_dir})")
    
    print("\n" + "-" * 50 + "\n")
    
    # Check prerequisites
    print_header("Checking Prerequisites")
    check_python_version()
    
    if not check_pip():
        print_error("pip is required for installation")
        sys.exit(1)
    
    # Get current directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    # Install dependencies for each service
    print_header("Installing Dependencies")
    
    failed_services = []
    installed_services = []
    
    for service_name, service_dir in SERVICES.items():
        full_path = script_dir / service_dir
        
        if not full_path.exists():
            print_error(f"Directory not found: {full_path}")
            failed_services.append(service_name)
            continue
        
        if install_service_dependencies(service_name, full_path):
            installed_services.append(service_name)
        else:
            failed_services.append(service_name)
    
    # Summary
    print_header("Installation Summary")
    
    print(f"Successfully installed ({len(installed_services)}):")
    for service in installed_services:
        print(f"  ✅ {service}")
    
    if failed_services:
        print(f"\nFailed to install ({len(failed_services)}):")
        for service in failed_services:
            print(f"  ❌ {service}")
        print("\nPlease try installing manually:")
        for service_name, service_dir in SERVICES.items():
            if service_name in failed_services:
                print(f"  cd {service_dir}")
                print(f"  pip install -r requirements.txt")
    else:
        print_success("\nAll dependencies installed successfully!")
        print("\nNext steps:")
        print("  1. Run: python start_services.py")
        print("  2. Or use: start_services.bat (Windows)")
        print("  3. Or use: start_services.ps1 (PowerShell)")
        print("  4. Or manually start each service in separate terminals")
        print("\nThen open http://localhost:5000 in your browser")
    
    return 0 if not failed_services else 1

if __name__ == "__main__":
    sys.exit(main())
