"""
Basic tests for OkeyBot functionality
"""
import sys
import os

# Add the current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from okey_card import OkeyCard, OkeyHand
from okey_game import OkeyGameState, OkeyStrategy
from okey_detection import OkeyDetection
import constants


def test_card_creation():
    """Test basic card creation and operations"""
    print("Testing card creation...")
    
    # Create some cards
    red_5 = OkeyCard('RED', 5)
    blue_10 = OkeyCard('BLUE', 10)
    joker = OkeyCard('YELLOW', 1, is_joker=True)
    
    print(f"Created cards: {red_5}, {blue_10}, {joker}")
    
    assert str(red_5) == "RED5"
    assert str(joker) == "JOKER(YELLOW1)"
    assert joker.is_joker == True
    assert red_5.is_joker == False
    
    print("Card creation tests passed!")


def test_hand_operations():
    """Test hand operations"""
    print("Testing hand operations...")
    
    hand = OkeyHand()
    
    # Add some cards
    cards = [
        OkeyCard('RED', 1),
        OkeyCard('RED', 2),
        OkeyCard('RED', 3),
        OkeyCard('BLUE', 1),
        OkeyCard('BLUE', 1),
        OkeyCard('BLUE', 1),
        OkeyCard('YELLOW', 5)
    ]
    
    for card in cards:
        hand.add_card(card)
    
    print(f"Hand: {hand}")
    
    # Test finding runs
    runs = hand.find_runs()
    print(f"Found runs: {runs}")
    
    # Test finding sets
    sets = hand.find_sets()
    print(f"Found sets: {sets}")
    
    # Test sorting
    hand.sort_cards()
    print(f"Sorted hand: {hand}")
    
    print("Hand operations tests passed!")


def test_game_state():
    """Test game state management"""
    print("Testing game state...")
    
    game_state = OkeyGameState()
    
    # Add some cards
    game_state.add_card_to_hand(OkeyCard('RED', 5))
    game_state.add_card_to_hand(OkeyCard('BLUE', 10))
    
    # Set joker
    game_state.set_joker(OkeyCard('YELLOW', 1))
    
    # Set center card
    game_state.set_center_card(OkeyCard('RED', 7))
    
    print(f"Game state: {game_state}")
    print(f"Hand strength: {game_state.get_hand_strength()}")
    
    assert len(game_state.player_hand) == 2
    assert game_state.joker_card is not None
    assert game_state.center_card is not None
    
    print("Game state tests passed!")


def test_strategy():
    """Test strategy decisions"""
    print("Testing strategy...")
    
    strategy = OkeyStrategy()
    game_state = OkeyGameState()
    
    # Create a test hand
    test_cards = [
        OkeyCard('RED', 1),
        OkeyCard('RED', 2),
        OkeyCard('RED', 3),
        OkeyCard('BLUE', 10),
        OkeyCard('YELLOW', 8)
    ]
    
    for card in test_cards:
        game_state.add_card_to_hand(card)
    
    # Test card evaluation
    for card in test_cards:
        value = strategy.evaluate_card_value(card, game_state)
        print(f"Card {card} value: {value}")
    
    # Test discard choice
    discard = strategy.choose_discard_card(game_state)
    print(f"Recommended discard: {discard}")
    
    # Test center card decision
    game_state.set_center_card(OkeyCard('RED', 4))
    game_state.is_player_turn = True
    should_take = strategy.should_take_center_card(game_state)
    print(f"Should take center card: {should_take}")
    
    print("Strategy tests passed!")


def test_detection():
    """Test detection system"""
    print("Testing detection system...")
    
    detector = OkeyDetection()
    
    # Test with dummy image
    import numpy as np
    dummy_image = np.zeros((600, 800, 3), dtype=np.uint8)
    
    # Test game state detection
    state = detector.detect_game_state(dummy_image)
    print(f"Detected game state: {state}")
    
    # Test button detection
    buttons = detector.detect_game_buttons(dummy_image)
    print(f"Detected buttons: {buttons}")
    
    # Test card detection
    cards = detector.detect_cards_in_hand(dummy_image)
    print(f"Detected cards in hand: {len(cards)}")
    
    print("Detection tests passed!")


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("Running OkeyBot Tests")
    print("=" * 50)
    
    try:
        test_card_creation()
        print()
        
        test_hand_operations()
        print()
        
        test_game_state()
        print()
        
        test_strategy()
        print()
        
        test_detection()
        print()
        
        print("=" * 50)
        print("All tests passed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)