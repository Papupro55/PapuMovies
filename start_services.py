#!/usr/bin/env python3
"""
PapuMovies Microservices - Start Services Script
This script starts all microservices in separate processes
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

# Define services with their ports
SERVICES = {
    'Movie Service': {
        'dir': 'movie-service',
        'port': 5001,
        'description': 'TMDB API wrapper'
    },
    'Rating Service': {
        'dir': 'rating-service',
        'port': 5002,
        'description': 'OMDb API wrapper'
    },
    'Trailer Service': {
        'dir': 'trailer-service',
        'port': 5003,
        'description': 'YouTube API wrapper'
    },
    'Frontend Service': {
        'dir': 'frontend',
        'port': 5000,
        'description': 'Web UI'
    }
}

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_warning(text):
    """Print warning message"""
    print(f"⚠️  {text}")

def start_service(service_name, service_config):
    """Start a single service"""
    service_dir = service_config['dir']
    port = service_config['port']
    description = service_config['description']
    
    print_info(f"Starting {service_name} on port {port}...")
    print(f"    Directory: {service_dir}")
    print(f"    Description: {description}\n")
    
    try:
        # Change to service directory
        service_path = Path(__file__).parent / service_dir
        
        if not service_path.exists():
            print_warning(f"Directory not found: {service_path}")
            return None
        
        # Start the service
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            cwd=str(service_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        return process
    
    except Exception as e:
        print(f"❌ Failed to start {service_name}: {e}\n")
        return None

def main():
    """Main function to start all services"""
    print_header("PapuMovies - Microservices Startup")
    
    print("This will start 4 services:\n")
    
    # Display service information
    for service_name, config in SERVICES.items():
        print(f"  • {service_name} (Port {config['port']})")
        print(f"    {config['description']}\n")
    
    print("-" * 60 + "\n")
    
    # Verify all requirements are met
    if not Path('frontend/app.py').exists():
        print_warning("This script must be run from the movie-microservices root directory")
        sys.exit(1)
    
    # Start all services
    processes = {}
    print_header("Starting Services")
    
    for service_name, service_config in SERVICES.items():
        process = start_service(service_name, service_config)
        if process:
            processes[service_name] = process
            time.sleep(1)  # Give each service time to start
    
    if not processes:
        print("\n❌ Failed to start any services. Check the errors above.")
        sys.exit(1)
    
    print_header("Services Started Successfully")
    
    print("✅ All services are running!\n")
    print("Service URLs:")
    print("  • Movie Service: http://localhost:5001")
    print("  • Rating Service: http://localhost:5002")
    print("  • Trailer Service: http://localhost:5003")
    print("  • Frontend: http://localhost:5000\n")
    
    print("📺 Open http://localhost:5000 in your browser to access the application\n")
    
    print("To stop all services, press CTRL+C\n")
    print("-" * 60 + "\n")
    
    try:
        # Keep the script running and monitor processes
        while True:
            for service_name, process in list(processes.items()):
                if process.poll() is not None:  # Process has terminated
                    print_warning(f"{service_name} has stopped. PID: {process.pid}")
                    del processes[service_name]
            
            if not processes:
                print("\n❌ All services have stopped")
                sys.exit(1)
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("  Shutting Down Services...")
        print("=" * 60 + "\n")
        
        # Terminate all processes
        for service_name, process in processes.items():
            try:
                process.terminate()
                print_info(f"Terminating {service_name}...")
                process.wait(timeout=5)
                print_success(f"{service_name} stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                print_warning(f"{service_name} forced to stop")
            except Exception as e:
                print_warning(f"Error stopping {service_name}: {e}")
        
        print_success("All services stopped")
        sys.exit(0)

if __name__ == "__main__":
    main()
