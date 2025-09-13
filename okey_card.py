"""
Okey Card representation for Metin2 Okey game
"""

class OkeyCard:
    """Represents a single Okey card with color and number"""
    
    def __init__(self, color, number, is_joker=False):
        self.color = color  # 'RED', 'BLACK', 'BLUE', 'YELLOW'
        self.number = number  # 1-13
        self.is_joker = is_joker
        
    def __str__(self):
        if self.is_joker:
            return f"JOKER({self.color}{self.number})"
        return f"{self.color}{self.number}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if not isinstance(other, OkeyCard):
            return False
        return (self.color == other.color and 
                self.number == other.number and 
                self.is_joker == other.is_joker)
    
    def __hash__(self):
        return hash((self.color, self.number, self.is_joker))
    
    def can_substitute(self, target_card):
        """Check if this joker can substitute for target card"""
        if not self.is_joker:
            return False
        return True
    
    def get_actual_value(self, joker_color, joker_number):
        """Get the actual card this represents (for jokers)"""
        if self.is_joker:
            return OkeyCard(joker_color, joker_number)
        return self


class OkeyHand:
    """Represents a player's hand of Okey cards"""
    
    def __init__(self):
        self.cards = []
        
    def add_card(self, card):
        """Add a card to the hand"""
        self.cards.append(card)
        
    def remove_card(self, card):
        """Remove a card from the hand"""
        if card in self.cards:
            self.cards.remove(card)
            return True
        return False
    
    def get_cards_by_color(self, color):
        """Get all cards of a specific color"""
        return [card for card in self.cards if card.color == color]
    
    def get_cards_by_number(self, number):
        """Get all cards with a specific number"""
        return [card for card in self.cards if card.number == number]
    
    def get_jokers(self):
        """Get all joker cards"""
        return [card for card in self.cards if card.is_joker]
    
    def sort_cards(self):
        """Sort cards by color and number"""
        color_order = {'RED': 0, 'BLACK': 1, 'BLUE': 2, 'YELLOW': 3}
        self.cards.sort(key=lambda x: (color_order.get(x.color, 4), x.number))
    
    def find_sets(self):
        """Find all possible sets (3+ cards of same number, different colors)"""
        sets = []
        for number in range(1, 14):
            same_number_cards = self.get_cards_by_number(number)
            if len(same_number_cards) >= 3:
                # Check for different colors
                colors_used = set(card.color for card in same_number_cards)
                if len(colors_used) >= 3:
                    sets.append(same_number_cards[:4])  # Max 4 cards in a set
        return sets
    
    def find_runs(self):
        """Find all possible runs (3+ consecutive cards of same color)"""
        runs = []
        for color in ['RED', 'BLACK', 'BLUE', 'YELLOW']:
            color_cards = self.get_cards_by_color(color)
            color_cards.sort(key=lambda x: x.number)
            
            current_run = []
            for card in color_cards:
                if not current_run:
                    current_run.append(card)
                elif card.number == current_run[-1].number + 1:
                    current_run.append(card)
                else:
                    if len(current_run) >= 3:
                        runs.append(current_run.copy())
                    current_run = [card]
            
            if len(current_run) >= 3:
                runs.append(current_run)
        
        return runs
    
    def calculate_deadwood(self):
        """Calculate deadwood (unmatched cards) value"""
        # This is a simplified version - real algorithm would be more complex
        sets = self.find_sets()
        runs = self.find_runs()
        
        matched_cards = set()
        for group in sets + runs:
            for card in group:
                matched_cards.add(card)
        
        deadwood_value = 0
        for card in self.cards:
            if card not in matched_cards:
                deadwood_value += min(card.number, 10)  # Face cards worth 10
        
        return deadwood_value
    
    def __len__(self):
        return len(self.cards)
    
    def __str__(self):
        return f"Hand({len(self.cards)} cards): {self.cards}"