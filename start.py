"""
Startup script for OkeyBot
"""
import sys
import os

def check_dependencies():
    """Check if all required dependencies are available"""
    try:
        import numpy
        print("✓ NumPy available")
    except ImportError:
        print("✗ NumPy not found")
        return False
        
    try:
        import cv2
        print("✓ OpenCV available")
    except ImportError:
        print("✗ OpenCV not found - install with: pip install opencv-python")
        return False
        
    try:
        import win32gui
        print("✓ Win32 API available")
    except ImportError:
        print("✗ Win32 API not found - install with: pip install pywin32")
        print("  Note: This is required on Windows only")
        return False
        
    try:
        import PySimpleGUI
        print("✓ PySimpleGUI available")
    except ImportError:
        print("✗ PySimpleGUI not found - install with: pip install PySimpleGUI")
        return False
        
    try:
        import pydirectinput
        print("✓ PyDirectInput available")
    except ImportError:
        print("✗ PyDirectInput not found - install with: pip install PyDirectInput")
        return False
        
    return True


def main():
    """Main startup function"""
    print("OkeyBot - Metin2 Okey Game Helper")
    print("=" * 40)
    
    print("Checking dependencies...")
    if not check_dependencies():
        print("\nSome dependencies are missing.")
        print("Install them with: pip install -r requirements.txt")
        print("\nNote: This bot requires Windows for game interaction.")
        return False
    
    print("\nAll dependencies found!")
    print("Starting OkeyBot GUI...")
    
    try:
        from main import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error importing main GUI: {e}")
        return False
    except Exception as e:
        print(f"Error starting GUI: {e}")
        return False
        
    return True


if __name__ == "__main__":
    success = main()
    if not success:
        print("\nOkeyBot failed to start. Please check the error messages above.")
        sys.exit(1)