"""
Simple test without external dependencies
"""
import sys
import os

# Add the current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test only the core logic without OpenCV dependencies
def test_core_logic():
    """Test core game logic without external dependencies"""
    print("Testing core Okey game logic...")
    
    # Test card creation
    from okey_card import OkeyCard, OkeyHand
    
    red_5 = OkeyCard('RED', 5)
    blue_10 = OkeyCard('BLUE', 10)
    joker = OkeyCard('YELLOW', 1, is_joker=True)
    
    print(f"Created cards: {red_5}, {blue_10}, {joker}")
    
    # Test hand operations
    hand = OkeyHand()
    hand.add_card(red_5)
    hand.add_card(blue_10)
    hand.add_card(joker)
    
    print(f"Hand with {len(hand)} cards: {hand}")
    
    # Test game state
    from okey_game import OkeyGameState, OkeyStrategy
    
    game_state = OkeyGameState()
    game_state.add_card_to_hand(red_5)
    game_state.add_card_to_hand(blue_10)
    game_state.set_joker(joker)
    
    print(f"Game state: {game_state}")
    
    # Test strategy
    strategy = OkeyStrategy()
    discard = strategy.choose_discard_card(game_state)
    print(f"Strategy recommends discarding: {discard}")
    
    print("Core logic tests passed!")


def test_file_structure():
    """Test that all required files exist"""
    print("Testing file structure...")
    
    required_files = [
        'okey_card.py',
        'okey_game.py', 
        'constants.py',
        'requirements.txt',
        'README.md',
        '.gitignore'
    ]
    
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✓ {filename} exists")
        else:
            print(f"✗ {filename} missing")
            return False
    
    print("File structure tests passed!")
    return True


if __name__ == "__main__":
    print("=" * 50)
    print("Running Basic OkeyBot Tests")
    print("=" * 50)
    
    try:
        test_file_structure()
        print()
        
        test_core_logic()
        print()
        
        print("=" * 50)
        print("Basic tests completed successfully!")
        print("Note: Full tests require Windows environment with game dependencies")
        print("=" * 50)
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()