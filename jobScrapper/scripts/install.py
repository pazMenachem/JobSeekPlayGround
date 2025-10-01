"""Installation script for the job scraper application."""

import subprocess
import sys
import os
import venv
from pathlib import Path


def create_virtual_environment():
    """Create a virtual environment for the project."""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists!")
        return True
    
    print("Creating virtual environment...")
    try:
        venv.create(venv_path, with_pip=True)
        print("✅ Virtual environment created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating virtual environment: {e}")
        return False


def get_venv_python():
    """Get the Python executable path in the virtual environment."""
    if os.name == 'nt':  # Windows
        return Path("venv/Scripts/python.exe")
    else:  # Unix/Linux/Mac
        return Path("venv/bin/python")


def install_requirements():
    """Install required packages from requirements.txt in virtual environment."""
    print("Installing required packages in virtual environment...")
    
    venv_python = get_venv_python()
    
    if not venv_python.exists():
        print("❌ Virtual environment Python not found!")
        return False
    
    try:
        # Upgrade pip first
        subprocess.check_call([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([str(venv_python), "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Successfully installed all requirements in virtual environment!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python version {sys.version.split()[0]} is compatible!")
    return True


def main():
    """Main installation function."""
    print("Job Scraper - Installation Script")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install requirements in virtual environment
    if not install_requirements():
        sys.exit(1)
    
    # Make shell scripts executable
    try:
        os.chmod("activate.sh", 0o755)
        os.chmod("run.sh", 0o755)
    except Exception as e:
        print(f"Warning: Could not make shell scripts executable: {e}")
    
    print("\n" + "=" * 40)
    print("✅ Installation completed successfully!")
    print("\nVirtual environment created at: ./venv")
    print("\nNext steps:")
    print("1. Activate the virtual environment:")
    print("   source scripts/activate.sh")
    print("   # IMPORTANT: Use 'source' not './scripts/activate.sh'")
    print("2. Edit 'src/config.py' to customize your settings and URLs")
    print("3. Run the application:")
    print("   scripts/run_app.sh")
    print("   # or manually: python main.py")
    print("\nFor examples, run: python example_usage.py")
    print("\nTo deactivate the virtual environment later, run: deactivate")


if __name__ == "__main__":
    main()
