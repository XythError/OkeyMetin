"""
Test script for Okey Bot functionality
"""
import unittest
import numpy as np
import cv2 as cv
from okey_tile import OkeyTile
from okey_game_logic import OkeyGameLogic, OkeyMeld
from tile_recognizer import TileRecognizer
from utils import calculate_image_similarity, point_distance

class TestOkeyTile(unittest.TestCase):
    """Test OkeyTile functionality"""
    
    def test_tile_creation(self):
        """Test basic tile creation"""
        tile = OkeyTile('RED', 5)
        self.assertEqual(tile.color, 'RED')
        self.assertEqual(tile.number, 5)
        self.assertFalse(tile.is_joker)
        self.assertTrue(tile.is_valid())
    
    def test_joker_tile(self):
        """Test joker tile"""
        joker = OkeyTile(is_joker=True)
        self.assertTrue(joker.is_joker)
        self.assertTrue(joker.is_valid())
        self.assertEqual(str(joker), "JOKER")
    
    def test_tile_equality(self):
        """Test tile equality comparison"""
        tile1 = OkeyTile('BLUE', 3)
        tile2 = OkeyTile('BLUE', 3)
        tile3 = OkeyTile('RED', 3)
        
        self.assertEqual(tile1, tile2)
        self.assertNotEqual(tile1, tile3)
    
    def test_set_formation(self):
        """Test set formation logic"""
        red_5 = OkeyTile('RED', 5)
        blue_5 = OkeyTile('BLUE', 5)
        green_5 = OkeyTile('GREEN', 5)
        
        self.assertTrue(red_5.can_form_set_with(blue_5, green_5))
    
    def test_run_formation(self):
        """Test run formation logic"""
        red_5 = OkeyTile('RED', 5)
        red_6 = OkeyTile('RED', 6)
        red_7 = OkeyTile('RED', 7)
        
        self.assertTrue(red_5.can_form_run_with(red_6, red_7))

class TestOkeyGameLogic(unittest.TestCase):
    """Test game logic functionality"""
    
    def setUp(self):
        """Set up test game logic"""
        self.game_logic = OkeyGameLogic()
    
    def test_set_detection(self):
        """Test set detection"""
        tiles = [
            OkeyTile('RED', 5),
            OkeyTile('BLUE', 5),
            OkeyTile('GREEN', 5),
            OkeyTile('RED', 3)
        ]
        
        melds = self.game_logic.find_all_possible_melds(tiles)
        sets = [meld for meld in melds if meld.meld_type == 'SET']
        
        self.assertGreater(len(sets), 0)
    
    def test_run_detection(self):
        """Test run detection"""
        tiles = [
            OkeyTile('RED', 5),
            OkeyTile('RED', 6),
            OkeyTile('RED', 7),
            OkeyTile('BLUE', 3)
        ]
        
        melds = self.game_logic.find_all_possible_melds(tiles)
        runs = [meld for meld in melds if meld.meld_type == 'RUN']
        
        self.assertGreater(len(runs), 0)
    
    def test_optimal_play(self):
        """Test optimal play decision"""
        tiles = [
            OkeyTile('RED', 5),
            OkeyTile('BLUE', 5),
            OkeyTile('GREEN', 5),
            OkeyTile('RED', 1),
            OkeyTile('BLACK', 13)
        ]
        
        melds, discard = self.game_logic.find_optimal_play(tiles)
        
        # Should form the set and discard a low-value tile
        self.assertGreater(len(melds), 0)
        self.assertIsNotNone(discard)
    
    def test_hand_strength_calculation(self):
        """Test hand strength calculation"""
        strong_hand = [
            OkeyTile('RED', 5),
            OkeyTile('BLUE', 5),
            OkeyTile('GREEN', 5),
            OkeyTile('RED', 6),
            OkeyTile('RED', 7)
        ]
        
        weak_hand = [
            OkeyTile('RED', 1),
            OkeyTile('BLUE', 13),
            OkeyTile('GREEN', 3),
            OkeyTile('BLACK', 8),
            OkeyTile('RED', 11)
        ]
        
        strong_strength = self.game_logic.calculate_hand_strength(strong_hand)
        weak_strength = self.game_logic.calculate_hand_strength(weak_hand)
        
        self.assertGreater(strong_strength, weak_strength)

class TestTileRecognizer(unittest.TestCase):
    """Test tile recognition functionality"""
    
    def setUp(self):
        """Set up test recognizer"""
        self.recognizer = TileRecognizer()
    
    def test_recognizer_initialization(self):
        """Test recognizer initialization"""
        self.assertIsNotNone(self.recognizer.ocr_config)
        self.assertGreater(self.recognizer.template_threshold, 0)
    
    def test_color_detection_ranges(self):
        """Test color detection ranges are valid"""
        import constants
        
        for color_name, color_range in constants.TILE_COLORS.items():
            self.assertIn('lower', color_range)
            self.assertIn('upper', color_range)
            
            lower = color_range['lower']
            upper = color_range['upper']
            
            # Check HSV ranges are valid
            self.assertGreaterEqual(lower[0], 0)  # Hue
            self.assertLessEqual(upper[0], 180)
            self.assertGreaterEqual(lower[1], 0)  # Saturation
            self.assertLessEqual(upper[1], 255)
            self.assertGreaterEqual(lower[2], 0)  # Value
            self.assertLessEqual(upper[2], 255)

class TestUtils(unittest.TestCase):
    """Test utility functions"""
    
    def test_point_distance(self):
        """Test point distance calculation"""
        p1 = (0, 0)
        p2 = (3, 4)
        
        distance = point_distance(p1, p2)
        self.assertAlmostEqual(distance, 5.0, places=1)
    
    def test_image_similarity(self):
        """Test image similarity calculation"""
        # Create two identical test images
        img1 = np.zeros((100, 100, 3), dtype=np.uint8)
        img2 = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Add some pattern
        cv.rectangle(img1, (20, 20), (80, 80), (255, 255, 255), -1)
        cv.rectangle(img2, (20, 20), (80, 80), (255, 255, 255), -1)
        
        similarity = calculate_image_similarity(img1, img2)
        self.assertGreater(similarity, 0.9)  # Should be very similar
    
    def test_performance_monitor(self):
        """Test performance monitoring"""
        from utils import PerformanceMonitor
        
        monitor = PerformanceMonitor()
        
        start_time = monitor.start_timer("test_operation")
        # Simulate some work
        import time
        time.sleep(0.01)
        monitor.end_timer("test_operation", start_time)
        
        avg_time = monitor.get_average_time("test_operation")
        self.assertGreater(avg_time, 0)
        self.assertEqual(monitor.call_counts["test_operation"], 1)

def run_basic_tests():
    """Run basic functionality tests"""
    print("Running Okey Bot Tests...")
    
    # Test tile creation
    print("Testing tile creation...")
    tile = OkeyTile('RED', 5)
    print(f"Created tile: {tile}")
    
    # Test game logic
    print("Testing game logic...")
    game_logic = OkeyGameLogic()
    tiles = [
        OkeyTile('RED', 5),
        OkeyTile('BLUE', 5),
        OkeyTile('GREEN', 5)
    ]
    melds = game_logic.find_all_possible_melds(tiles)
    print(f"Found {len(melds)} possible melds")
    
    # Test tile recognizer
    print("Testing tile recognizer...")
    recognizer = TileRecognizer()
    print(f"Recognizer initialized with threshold: {recognizer.template_threshold}")
    
    print("Basic tests completed successfully!")

def run_installation_check():
    """Check if all required packages are installed"""
    print("Checking installation...")
    
    required_packages = [
        ('cv2', 'OpenCV'),
        ('numpy', 'NumPy'),
        ('pytesseract', 'Tesseract OCR'),
        ('win32gui', 'PyWin32'),
        ('pydirectinput', 'PyDirectInput'),
        ('PySimpleGUI', 'PySimpleGUI')
    ]
    
    missing_packages = []
    
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✓ {name} is installed")
        except ImportError:
            print(f"✗ {name} is missing")
            missing_packages.append(name)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please install missing packages using: pip install -r requirements.txt")
        return False
    else:
        print("\nAll required packages are installed!")
        return True

if __name__ == "__main__":
    # Run installation check
    if run_installation_check():
        print("\n" + "="*50)
        
        # Run basic tests
        run_basic_tests()
        
        print("\n" + "="*50)
        
        # Run unit tests
        print("Running unit tests...")
        unittest.main(verbosity=2, exit=False)
        
        print("\n" + "="*50)
        print("Test suite completed!")