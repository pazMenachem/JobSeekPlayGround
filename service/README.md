# Windows Service Learning Project

This project demonstrates how to create a Windows service using Python that runs a CLI application in the background.

## Project Structure
- `hello_app.py` - Simple CLI application that the service will execute
- `my_service.py` - Main Windows service implementation
- `logs/` - Directory for service logs
- `requirements.txt` - Python dependencies

## Setup Instructions

### 1. Create Virtual Environment
```cmd
python -m venv venv
```

### 2. Activate Virtual Environment
```cmd
venv\Scripts\activate.bat
```

### 3. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 4. Install Service
```cmd
python my_service.py install
```

### 5. Start Service
```cmd
python my_service.py start
```

## Service Management Commands
- Install: `python my_service.py install`
- Start: `python my_service.py start`
- Stop: `python my_service.py stop`
- Remove: `python my_service.py remove`
- Debug: `python my_service.py debug`

## Requirements
- Python 3.7+
- Windows OS
- Administrator privileges (for installing/starting services)

