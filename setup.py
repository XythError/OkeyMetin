"""
Setup and configuration script for Metin2 Okey Bot
"""
import os
import sys
import json
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        'templates',
        'images', 
        'logs',
        'config'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_config_file():
    """Create default configuration file"""
    config = {
        "game_window": {
            "name": "Metin2",
            "window_size": [800, 600],
            "window_position": [200, 100]
        },
        "player_rack": {
            "position": [220, 480],
            "size": [560, 80]
        },
        "game_board": {
            "position": [220, 200], 
            "size": [560, 280]
        },
        "timing": {
            "click_delay": 0.3,
            "action_delay": 1.0,
            "game_start_delay": 2.0
        },
        "recognition": {
            "tile_min_area": 800,
            "tile_max_area": 3000,
            "template_threshold": 0.7,
            "ocr_config": "--psm 8 -c tessedit_char_whitelist=0123456789"
        },
        "strategy": {
            "prefer_sets": True,
            "joker_conservation": True,
            "aggressive_mode": False,
            "meld_scores": {
                "SET_3": 10,
                "SET_4": 15,
                "RUN_3": 12,
                "RUN_4": 18,
                "RUN_5": 25,
                "RUN_6": 32,
                "RUN_7": 40
            }
        },
        "debug": {
            "save_debug_images": False,
            "verbose_logging": False,
            "performance_monitoring": True
        }
    }
    
    with open('config/bot_config.json', 'w') as f:
        json.dump(config, f, indent=4)
    
    print("✓ Created default configuration file: config/bot_config.json")

def check_dependencies():
    """Check if required dependencies are available"""
    required_packages = [
        'cv2',
        'numpy', 
        'pytesseract',
        'win32gui',
        'pydirectinput',
        'PySimpleGUI'
    ]
    
    missing = []
    available = []
    
    for package in required_packages:
        try:
            __import__(package)
            available.append(package)
        except ImportError:
            missing.append(package)
    
    print(f"✓ Available packages: {', '.join(available)}")
    
    if missing:
        print(f"⚠ Missing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    else:
        print("✓ All required packages are available!")
        return True

def setup_logging():
    """Setup logging configuration"""
    log_config = """
import logging
import logging.handlers
import os

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure main logger
logger = logging.getLogger('okey_bot')
logger.setLevel(logging.INFO)

# File handler with rotation
file_handler = logging.handlers.RotatingFileHandler(
    'logs/okey_bot.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Performance logger
perf_logger = logging.getLogger('performance')
perf_handler = logging.FileHandler('logs/performance.log')
perf_handler.setFormatter(formatter)
perf_logger.addHandler(perf_handler)
perf_logger.setLevel(logging.DEBUG)
"""
    
    with open('config/logging_config.py', 'w') as f:
        f.write(log_config.strip())
    
    print("✓ Created logging configuration: config/logging_config.py")

def create_launch_script():
    """Create convenient launch script"""
    if sys.platform == "win32":
        script_content = """@echo off
echo Starting Metin2 Okey Bot...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Launch the bot
python main.py

pause
"""
        with open('start_bot.bat', 'w') as f:
            f.write(script_content)
        print("✓ Created Windows launch script: start_bot.bat")
    
    else:
        script_content = """#!/bin/bash
echo "Starting Metin2 Okey Bot..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Launch the bot
python3 main.py
"""
        with open('start_bot.sh', 'w') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod('start_bot.sh', 0o755)
        print("✓ Created Linux launch script: start_bot.sh")

def run_setup():
    """Run complete setup process"""
    print("="*60)
    print("METIN2 OKEY BOT - SETUP AND CONFIGURATION")
    print("="*60)
    
    print("\n1. Creating directories...")
    create_directories()
    
    print("\n2. Creating configuration files...")
    create_config_file()
    setup_logging()
    
    print("\n3. Creating launch scripts...")
    create_launch_script()
    
    print("\n4. Checking dependencies...")
    deps_ok = check_dependencies()
    
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    
    if deps_ok:
        print("✓ All dependencies are available")
        print("✓ Configuration files created")
        print("✓ Directory structure ready")
        print("\nYou can now run the bot:")
        print("  • GUI Mode: python main.py")
        print("  • Debug Mode: python main.py and click 'Debug Mode'")
        if sys.platform == "win32":
            print("  • Quick Start: Double-click start_bot.bat")
        else:
            print("  • Quick Start: ./start_bot.sh")
    else:
        print("⚠ Some dependencies are missing")
        print("Please install them with: pip install -r requirements.txt")
    
    print("\nNext Steps:")
    print("1. Install Tesseract OCR for text recognition")
    print("2. Configure game window settings in config/bot_config.json")
    print("3. Use debug mode to calibrate tile recognition") 
    print("4. Capture template images if needed")
    print("5. Start playing!")
    
    print("\nFor help and troubleshooting, see README.md")
    print("="*60)

if __name__ == "__main__":
    run_setup()