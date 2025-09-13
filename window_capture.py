"""
Window capture utility for Metin2 Okey Bot
Based on WindowCapture from Metin2FishBot with modifications for Okey game
"""
import numpy as np
import win32gui, win32ui, win32con
import cv2 as cv

class WindowCapture:
    """
    Handles capturing screenshots from the Metin2 game window
    """
    
    def __init__(self, window_name=None):
        # Window properties
        self.w = 0
        self.h = 0
        self.hwnd = None
        self.cropped_x = 0
        self.cropped_y = 0
        self.offset_x = 0
        self.offset_y = 0
        
        if window_name:
            self.set_window(window_name)
    
    def set_window(self, window_name):
        """Set the target window for capture"""
        # Find the handle for the window we want to capture
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception(f'Window not found: {window_name}')
        
        # Get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]
        
        # Account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels
        
        # Set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y
    
    def get_screenshot(self):
        """Capture a screenshot of the game window"""
        if not self.hwnd:
            raise Exception("No window set for capture")
        
        # Get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
        
        # Convert the raw data into a format opencv can read
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)
        
        # Free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        
        # Drop the alpha channel
        img = img[...,:3]
        
        # Make image C_CONTIGUOUS to avoid errors
        img = np.ascontiguousarray(img)
        
        return img
    
    def get_cropped_screenshot(self, x, y, width, height):
        """Get a cropped portion of the screenshot"""
        full_screenshot = self.get_screenshot()
        return full_screenshot[y:y+height, x:x+width]
    
    def get_screen_position(self, pos):
        """
        Translate a pixel position on a screenshot image to a pixel position on the screen.
        pos = (x, y)
        """
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)
    
    @staticmethod
    def list_window_names():
        """List all visible window names"""
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)
    
    def is_window_active(self):
        """Check if the target window is active/visible"""
        if not self.hwnd:
            return False
        return win32gui.IsWindowVisible(self.hwnd)