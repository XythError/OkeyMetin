"""
Tile Recognition System for Okey Bot
Handles detection and identification of tiles using computer vision
"""
import cv2 as cv
import numpy as np
import pytesseract
from okey_tile import OkeyTile
import constants

class TileRecognizer:
    """
    Recognizes Okey tiles from game screenshots using computer vision
    """
    
    def __init__(self):
        # OCR configuration for number recognition
        self.ocr_config = constants.OCR_CONFIG
        
        # Template matching threshold
        self.template_threshold = 0.7
        
        # Tile detection parameters
        self.tile_min_area = 800
        self.tile_max_area = 3000
        
    def detect_tiles_in_region(self, image, region_x, region_y, region_w, region_h):
        """
        Detect all tiles in a specific region of the image
        Returns list of OkeyTile objects
        """
        # Crop the region
        roi = image[region_y:region_y+region_h, region_x:region_x+region_w]
        
        # Find tile contours
        tile_contours = self._find_tile_contours(roi)
        
        tiles = []
        for contour in tile_contours:
            # Get bounding box
            x, y, w, h = cv.boundingRect(contour)
            
            # Extract tile image
            tile_img = roi[y:y+h, x:x+w]
            
            # Recognize the tile
            tile = self._recognize_tile(tile_img)
            if tile and tile.is_valid():
                # Set absolute position
                tile.position = (region_x + x + w//2, region_y + y + h//2)
                tiles.append(tile)
        
        return tiles
    
    def _find_tile_contours(self, image):
        """Find contours that likely represent tiles"""
        # Convert to grayscale
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv.GaussianBlur(gray, (5, 5), 0)
        
        # Apply threshold
        _, thresh = cv.threshold(blurred, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by area and aspect ratio
        valid_contours = []
        for contour in contours:
            area = cv.contourArea(contour)
            if self.tile_min_area <= area <= self.tile_max_area:
                # Check aspect ratio (tiles should be roughly rectangular)
                x, y, w, h = cv.boundingRect(contour)
                aspect_ratio = w / h
                if 0.5 <= aspect_ratio <= 1.5:  # Reasonable aspect ratio for tiles
                    valid_contours.append(contour)
        
        return valid_contours
    
    def _recognize_tile(self, tile_image):
        """Recognize a single tile from its image"""
        if tile_image is None or tile_image.size == 0:
            return None
        
        # Check if it's a joker first
        if self._is_joker(tile_image):
            return OkeyTile(is_joker=True)
        
        # Detect color
        color = self._detect_color(tile_image)
        
        # Detect number
        number = self._detect_number(tile_image)
        
        if color and number:
            tile = OkeyTile(color=color, number=number)
            tile.confidence = 0.8  # Base confidence
            return tile
        
        return None
    
    def _is_joker(self, tile_image):
        """Check if the tile is a joker"""
        # Convert to HSV
        hsv = cv.cvtColor(tile_image, cv.COLOR_BGR2HSV)
        
        # Jokers typically have special patterns or colors
        # This would need to be calibrated based on actual game appearance
        
        # For now, implement basic pattern detection
        # Look for unique characteristics of joker tiles
        gray = cv.cvtColor(tile_image, cv.COLOR_BGR2GRAY)
        edges = cv.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Jokers might have more complex patterns
        return edge_density > 0.3
    
    def _detect_color(self, tile_image):
        """Detect the color of a tile"""
        # Convert to HSV for better color detection
        hsv = cv.cvtColor(tile_image, cv.COLOR_BGR2HSV)
        
        best_color = None
        max_pixels = 0
        
        for color_name, color_range in constants.TILE_COLORS.items():
            # Create mask for this color
            lower = np.array(color_range['lower'])
            upper = np.array(color_range['upper'])
            mask = cv.inRange(hsv, lower, upper)
            
            # Count pixels in this color range
            pixel_count = np.sum(mask > 0)
            
            if pixel_count > max_pixels:
                max_pixels = pixel_count
                best_color = color_name
        
        # Require minimum number of pixels to be confident
        if max_pixels < 100:
            return None
        
        return best_color
    
    def _detect_number(self, tile_image):
        """Detect the number on a tile using OCR"""
        try:
            # Preprocess image for better OCR
            processed = self._preprocess_for_ocr(tile_image)
            
            # Use OCR to detect text
            text = pytesseract.image_to_string(processed, config=self.ocr_config).strip()
            
            # Try to parse as integer
            if text.isdigit():
                number = int(text)
                if 1 <= number <= 13:
                    return number
            
        except Exception as e:
            print(f"OCR error: {e}")
        
        return None
    
    def _preprocess_for_ocr(self, image):
        """Preprocess image for better OCR results"""
        # Convert to grayscale
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
        # Resize image to improve OCR accuracy
        height, width = gray.shape
        scale_factor = max(2, 50 // min(height, width))
        resized = cv.resize(gray, (width * scale_factor, height * scale_factor), 
                           interpolation=cv.INTER_CUBIC)
        
        # Apply threshold
        _, thresh = cv.threshold(resized, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        
        # Apply morphological operations to clean up
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def debug_save_tiles(self, image, tiles, filename_prefix="debug_tile"):
        """Save detected tiles for debugging purposes"""
        for i, tile in enumerate(tiles):
            if tile.position:
                x, y = tile.position
                # Extract tile region for saving
                tile_region = image[y-25:y+25, x-20:x+20]  # Approximate tile size
                if tile_region.size > 0:
                    cv.imwrite(f"/tmp/{filename_prefix}_{i}_{tile}.jpg", tile_region)