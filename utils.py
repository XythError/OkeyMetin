"""
Utility functions for the Okey Bot
"""
import cv2 as cv
import numpy as np
import time
from typing import Tuple, List

def calculate_color_histogram(image):
    """Calculate color histogram for image analysis"""
    hist_b = cv.calcHist([image], [0], None, [256], [0, 256])
    hist_g = cv.calcHist([image], [1], None, [256], [0, 256])
    hist_r = cv.calcHist([image], [2], None, [256], [0, 256])
    return hist_b, hist_g, hist_r

def find_template_matches(image, template, threshold=0.8):
    """Find all matches of a template in an image"""
    result = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    
    matches = []
    for pt in zip(*locations[::-1]):
        matches.append(pt)
    
    return matches

def draw_bounding_boxes(image, boxes, color=(0, 255, 0), thickness=2):
    """Draw bounding boxes on an image"""
    for box in boxes:
        x, y, w, h = box
        cv.rectangle(image, (x, y), (x + w, y + h), color, thickness)
    
    return image

def preprocess_image_for_ocr(image):
    """Preprocess image for better OCR results"""
    # Convert to grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv.GaussianBlur(gray, (3, 3), 0)
    
    # Apply threshold to get binary image
    _, binary = cv.threshold(blurred, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    
    # Apply morphological operations to clean up
    kernel = np.ones((2, 2), np.uint8)
    cleaned = cv.morphologyEx(binary, cv.MORPH_CLOSE, kernel)
    
    return cleaned

def calculate_image_similarity(img1, img2):
    """Calculate similarity between two images using histogram comparison"""
    if img1.shape != img2.shape:
        return 0.0
    
    # Convert to HSV for better comparison
    hsv1 = cv.cvtColor(img1, cv.COLOR_BGR2HSV)
    hsv2 = cv.cvtColor(img2, cv.COLOR_BGR2HSV)
    
    # Calculate histograms
    hist1 = cv.calcHist([hsv1], [0, 1, 2], None, [50, 60, 60], [0, 180, 0, 256, 0, 256])
    hist2 = cv.calcHist([hsv2], [0, 1, 2], None, [50, 60, 60], [0, 180, 0, 256, 0, 256])
    
    # Compare histograms
    similarity = cv.compareHist(hist1, hist2, cv.HISTCMP_CORREL)
    
    return max(0.0, similarity)

def create_debug_overlay(image, tiles, melds=None):
    """Create debug overlay showing detected tiles and melds"""
    overlay = image.copy()
    
    # Draw detected tiles
    for i, tile in enumerate(tiles):
        if tile.position:
            x, y = tile.position
            
            # Draw circle for tile position
            cv.circle(overlay, (x, y), 15, (0, 255, 0), 2)
            
            # Draw tile info
            tile_text = str(tile)
            cv.putText(overlay, tile_text, (x - 20, y - 20), 
                      cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
            
            # Draw tile number
            cv.putText(overlay, str(i), (x - 5, y + 5), 
                      cv.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
    
    # Draw melds if provided
    if melds:
        colors = [(255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
        for i, meld in enumerate(melds):
            color = colors[i % len(colors)]
            
            # Draw lines connecting meld tiles
            meld_positions = [tile.position for tile in meld.tiles if tile.position]
            if len(meld_positions) > 1:
                for j in range(len(meld_positions) - 1):
                    pt1 = meld_positions[j]
                    pt2 = meld_positions[j + 1]
                    cv.line(overlay, pt1, pt2, color, 2)
    
    return overlay

def timer_decorator(func):
    """Decorator to time function execution"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def safe_divide(a, b, default=0):
    """Safely divide two numbers, returning default if division by zero"""
    try:
        return a / b if b != 0 else default
    except (TypeError, ZeroDivisionError):
        return default

def clamp(value, min_value, max_value):
    """Clamp a value between min and max"""
    return max(min_value, min(value, max_value))

def point_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    """Calculate Euclidean distance between two points"""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def is_point_in_rect(point: Tuple[int, int], rect: Tuple[int, int, int, int]) -> bool:
    """Check if a point is inside a rectangle"""
    x, y = point
    rect_x, rect_y, rect_w, rect_h = rect
    
    return (rect_x <= x <= rect_x + rect_w and 
            rect_y <= y <= rect_y + rect_h)

class PerformanceMonitor:
    """Monitor performance of different bot components"""
    
    def __init__(self):
        self.timings = {}
        self.call_counts = {}
    
    def start_timer(self, name: str):
        """Start timing an operation"""
        if name not in self.timings:
            self.timings[name] = []
            self.call_counts[name] = 0
        
        return time.time()
    
    def end_timer(self, name: str, start_time: float):
        """End timing an operation"""
        if name in self.timings:
            duration = time.time() - start_time
            self.timings[name].append(duration)
            self.call_counts[name] += 1
    
    def get_average_time(self, name: str) -> float:
        """Get average execution time for an operation"""
        if name in self.timings and self.timings[name]:
            return sum(self.timings[name]) / len(self.timings[name])
        return 0.0
    
    def print_stats(self):
        """Print performance statistics"""
        print("\n=== Performance Statistics ===")
        for name in self.timings:
            avg_time = self.get_average_time(name)
            count = self.call_counts[name]
            total_time = sum(self.timings[name])
            
            print(f"{name}:")
            print(f"  Calls: {count}")
            print(f"  Average time: {avg_time:.4f}s")
            print(f"  Total time: {total_time:.4f}s")
            print()

# Global performance monitor instance
performance_monitor = PerformanceMonitor()