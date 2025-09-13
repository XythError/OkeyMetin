"""
Okey Tile class - represents individual tiles in the game
"""

class OkeyTile:
    """
    Represents a single Okey tile with color, number, and position information
    """
    
    COLORS = ['RED', 'BLUE', 'GREEN', 'BLACK']
    NUMBERS = list(range(1, 14))  # 1-13
    
    def __init__(self, color=None, number=None, is_joker=False, position=None):
        self.color = color
        self.number = number
        self.is_joker = is_joker
        self.position = position  # (x, y) coordinates on screen
        self.confidence = 0.0  # Recognition confidence score
    
    def __str__(self):
        if self.is_joker:
            return "JOKER"
        if self.color and self.number:
            return f"{self.color}_{self.number}"
        return "UNKNOWN"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if not isinstance(other, OkeyTile):
            return False
        return (self.color == other.color and 
                self.number == other.number and 
                self.is_joker == other.is_joker)
    
    def __hash__(self):
        return hash((self.color, self.number, self.is_joker))
    
    def is_valid(self):
        """Check if the tile has valid color and number"""
        if self.is_joker:
            return True
        return (self.color in self.COLORS and 
                self.number in self.NUMBERS)
    
    def can_form_set_with(self, other1, other2):
        """Check if this tile can form a set with two other tiles"""
        if self.is_joker or other1.is_joker or other2.is_joker:
            return True  # Jokers can complete any set
        
        tiles = [self, other1, other2]
        numbers = [t.number for t in tiles]
        colors = [t.color for t in tiles]
        
        # All same number, all different colors
        return (len(set(numbers)) == 1 and len(set(colors)) == 3)
    
    def can_form_run_with(self, other1, other2):
        """Check if this tile can form a run with two other tiles"""
        if self.is_joker or other1.is_joker or other2.is_joker:
            return True  # Jokers can complete any run
        
        tiles = [self, other1, other2]
        colors = [t.color for t in tiles]
        numbers = sorted([t.number for t in tiles])
        
        # All same color, consecutive numbers
        return (len(set(colors)) == 1 and 
                numbers[1] == numbers[0] + 1 and 
                numbers[2] == numbers[1] + 1)
    
    def get_value(self):
        """Get the point value of the tile"""
        if self.is_joker:
            return 20  # Jokers are valuable
        return self.number if self.number else 0
    
    def copy(self):
        """Create a copy of this tile"""
        return OkeyTile(
            color=self.color,
            number=self.number,
            is_joker=self.is_joker,
            position=self.position
        )