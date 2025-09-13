"""
Okey Game State tracking and management
"""
from okey_card import OkeyCard, OkeyHand
import constants


class OkeyGameState:
    """Tracks the current state of an Okey game"""
    
    def __init__(self):
        self.player_hand = OkeyHand()
        self.center_card = None  # Card in the center of the table
        self.joker_card = None   # The designated joker for this round
        self.discarded_cards = []  # Cards that have been discarded
        self.game_state = constants.GAME_STATE_WAITING
        self.is_player_turn = False
        self.round_number = 0
        
    def set_joker(self, card):
        """Set the joker card for this round"""
        self.joker_card = card
        
    def set_center_card(self, card):
        """Set the card in the center of the table"""
        self.center_card = card
        
    def add_card_to_hand(self, card):
        """Add a card to player's hand"""
        self.player_hand.add_card(card)
        
    def remove_card_from_hand(self, card):
        """Remove a card from player's hand"""
        return self.player_hand.remove_card(card)
        
    def discard_card(self, card):
        """Discard a card to the center"""
        if self.remove_card_from_hand(card):
            self.discarded_cards.append(card)
            self.center_card = card
            return True
        return False
        
    def can_take_from_center(self):
        """Check if player can take the center card"""
        return self.center_card is not None and self.is_player_turn
        
    def take_from_center(self):
        """Take the center card"""
        if self.can_take_from_center():
            self.add_card_to_hand(self.center_card)
            self.center_card = None
            return True
        return False
        
    def is_winning_hand(self):
        """Check if current hand is a winning hand"""
        # Simplified winning condition - need at least one set or run
        sets = self.player_hand.find_sets()
        runs = self.player_hand.find_runs()
        
        # Basic winning condition: all cards can be grouped
        total_grouped = 0
        for group in sets + runs:
            total_grouped += len(group)
            
        return total_grouped >= len(self.player_hand) - 1  # -1 for final discard
        
    def get_hand_strength(self):
        """Calculate the strength of current hand (lower is better)"""
        return self.player_hand.calculate_deadwood()
        
    def reset_for_new_round(self):
        """Reset state for a new round"""
        self.player_hand = OkeyHand()
        self.center_card = None
        self.joker_card = None
        self.discarded_cards = []
        self.game_state = constants.GAME_STATE_WAITING
        self.is_player_turn = False
        self.round_number += 1
        
    def __str__(self):
        return (f"GameState(Round {self.round_number}, "
                f"Hand: {len(self.player_hand)} cards, "
                f"State: {self.game_state}, "
                f"Turn: {self.is_player_turn})")


class OkeyStrategy:
    """Strategic decision making for Okey gameplay"""
    
    def __init__(self):
        self.risk_tolerance = 0.5  # 0 = very conservative, 1 = very aggressive
        
    def evaluate_card_value(self, card, game_state):
        """Evaluate the strategic value of a card"""
        hand = game_state.player_hand
        
        # Higher value = more valuable to keep
        value = 0
        
        # Cards that complete sets/runs are very valuable
        for run in hand.find_runs():
            if card in run:
                value += 50
                
        for card_set in hand.find_sets():
            if card in card_set:
                value += 50
        
        # Cards that could extend sets/runs are valuable
        same_color = hand.get_cards_by_color(card.color)
        same_number = hand.get_cards_by_number(card.number)
        
        # Potential for runs
        adjacent_numbers = 0
        for other_card in same_color:
            if abs(other_card.number - card.number) == 1:
                adjacent_numbers += 1
        value += adjacent_numbers * 10
        
        # Potential for sets
        value += (len(same_number) - 1) * 15
        
        # Jokers are always valuable
        if card.is_joker:
            value += 100
            
        # Lower number cards are generally less valuable to hold
        value -= card.number * 2
        
        return value
    
    def choose_discard_card(self, game_state):
        """Choose the best card to discard"""
        hand = game_state.player_hand
        
        if not hand.cards:
            return None
            
        # Calculate value for each card
        card_values = []
        for card in hand.cards:
            value = self.evaluate_card_value(card, game_state)
            card_values.append((card, value))
            
        # Sort by value (lowest first = best to discard)
        card_values.sort(key=lambda x: x[1])
        
        # Return the least valuable card
        return card_values[0][0]
    
    def should_take_center_card(self, game_state):
        """Decide whether to take the center card"""
        if not game_state.can_take_from_center():
            return False
            
        center_card = game_state.center_card
        center_value = self.evaluate_card_value(center_card, game_state)
        
        # Take card if it's valuable enough
        return center_value > 30
    
    def should_declare_win(self, game_state):
        """Decide whether to declare a winning hand"""
        if not game_state.is_winning_hand():
            return False
            
        # Only declare if hand strength is good enough
        hand_strength = game_state.get_hand_strength()
        return hand_strength <= 10  # Low deadwood value
    
    def get_next_action(self, game_state):
        """Get the next recommended action"""
        if not game_state.is_player_turn:
            return "WAIT"
            
        if game_state.should_declare_win(game_state):
            return "DECLARE_WIN"
            
        if game_state.can_take_from_center():
            if self.should_take_center_card(game_state):
                return "TAKE_CENTER"
            else:
                return "DRAW_CARD"
        
        # If we have too many cards, discard one
        if len(game_state.player_hand) > 14:  # Standard hand size
            discard = self.choose_discard_card(game_state)
            return f"DISCARD_{discard}"
            
        return "DRAW_CARD"