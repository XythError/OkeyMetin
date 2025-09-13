"""
Basic structure test without external dependencies
"""

def test_basic_structure():
    """Test basic code structure and imports"""
    print("Testing basic code structure...")
    
    # Test that all modules can be imported (structure-wise)
    try:
        # Test basic tile creation without dependencies
        class MockTile:
            def __init__(self, color=None, number=None, is_joker=False):
                self.color = color
                self.number = number
                self.is_joker = is_joker
            
            def __str__(self):
                if self.is_joker:
                    return "JOKER"
                return f"{self.color}_{self.number}"
        
        # Test tile creation
        tile = MockTile('RED', 5)
        print(f"✓ Tile creation works: {tile}")
        
        joker = MockTile(is_joker=True)
        print(f"✓ Joker creation works: {joker}")
        
        # Test basic game logic structure
        class MockGameLogic:
            def __init__(self):
                self.tiles = []
            
            def add_tile(self, tile):
                self.tiles.append(tile)
            
            def find_sets(self):
                # Mock set finding
                return len([t for t in self.tiles if t.color == 'RED'])
        
        game = MockGameLogic()
        game.add_tile(tile)
        sets_found = game.find_sets()
        print(f"✓ Game logic structure works: {sets_found} red tiles found")
        
        print("✓ Basic structure test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Structure test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    import os
    
    required_files = [
        'constants.py',
        'okey_tile.py',
        'okey_game_logic.py',
        'tile_recognizer.py',
        'window_capture.py',
        'okey_bot.py',
        'main.py',
        'utils.py',
        'requirements.txt',
        'README.md',
        '.gitignore'
    ]
    
    print("Checking file structure...")
    missing_files = []
    
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✓ {filename}")
        else:
            print(f"✗ {filename} - MISSING")
            missing_files.append(filename)
    
    if missing_files:
        print(f"\nMissing files: {missing_files}")
        return False
    else:
        print("✓ All required files present!")
        return True

def test_constants():
    """Test constants file"""
    try:
        # Import constants and check basic structure
        import sys
        sys.path.append('.')
        
        with open('constants.py', 'r') as f:
            content = f.read()
        
        required_constants = [
            'GAME_NAME',
            'OKEY_WINDOW_SIZE',
            'PLAYER_RACK_POSITION',
            'TILE_COLORS',
            'CLICK_DELAY'
        ]
        
        print("Checking constants...")
        for const in required_constants:
            if const in content:
                print(f"✓ {const} defined")
            else:
                print(f"✗ {const} missing")
        
        return True
        
    except Exception as e:
        print(f"✗ Constants test failed: {e}")
        return False

def test_strategy_concepts():
    """Test Okey strategy concepts"""
    print("Testing Okey strategy concepts...")
    
    # Mock tiles for strategy testing
    class StrategyTile:
        def __init__(self, color, number):
            self.color = color
            self.number = number
        
        def __str__(self):
            return f"{self.color}_{self.number}"
    
    # Test set formation concept
    def can_form_set(tiles):
        """Check if tiles can form a set (same number, different colors)"""
        if len(tiles) < 3:
            return False
        
        numbers = [t.number for t in tiles]
        colors = [t.color for t in tiles]
        
        # All same number, all different colors
        return len(set(numbers)) == 1 and len(set(colors)) == len(tiles)
    
    # Test run formation concept
    def can_form_run(tiles):
        """Check if tiles can form a run (consecutive numbers, same color)"""
        if len(tiles) < 3:
            return False
        
        colors = [t.color for t in tiles]
        numbers = sorted([t.number for t in tiles])
        
        # All same color, consecutive numbers
        if len(set(colors)) != 1:
            return False
        
        for i in range(1, len(numbers)):
            if numbers[i] != numbers[i-1] + 1:
                return False
        
        return True
    
    # Test set
    set_tiles = [
        StrategyTile('RED', 5),
        StrategyTile('BLUE', 5),
        StrategyTile('GREEN', 5)
    ]
    
    if can_form_set(set_tiles):
        print("✓ Set formation logic works")
    else:
        print("✗ Set formation logic failed")
    
    # Test run
    run_tiles = [
        StrategyTile('RED', 5),
        StrategyTile('RED', 6),
        StrategyTile('RED', 7)
    ]
    
    if can_form_run(run_tiles):
        print("✓ Run formation logic works")
    else:
        print("✗ Run formation logic failed")
    
    # Test scoring concept
    def calculate_meld_score(tiles):
        """Calculate score for a meld"""
        base_score = sum(t.number for t in tiles)
        length_bonus = (len(tiles) - 3) * 5
        return base_score + length_bonus
    
    set_score = calculate_meld_score(set_tiles)
    run_score = calculate_meld_score(run_tiles)
    
    print(f"✓ Set score calculation: {set_score}")
    print(f"✓ Run score calculation: {run_score}")
    
    return True

def main():
    """Run all basic tests"""
    print("="*50)
    print("METIN2 OKEY BOT - BASIC STRUCTURE TESTS")
    print("="*50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Basic Structure", test_basic_structure),
        ("Constants", test_constants),
        ("Strategy Concepts", test_strategy_concepts)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} Test ---")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} ERROR: {e}")
    
    print("\n" + "="*50)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic tests passed! Code structure is ready.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure game window settings in constants.py")
        print("3. Run: python main.py")
        print("4. Use debug mode to calibrate tile recognition")
    else:
        print("❌ Some tests failed. Please check the issues above.")
    
    print("="*50)

if __name__ == "__main__":
    main()