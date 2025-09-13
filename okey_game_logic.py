"""
Okey Game Logic and Strategy Engine
Implements the rules and optimal strategies for the Okey card game
"""
from typing import List, Tuple, Set, Optional
from okey_tile import OkeyTile
from itertools import combinations
import copy

class OkeyMeld:
    """Represents a meld (set or run) in Okey"""
    
    def __init__(self, tiles: List[OkeyTile], meld_type: str):
        self.tiles = tiles
        self.meld_type = meld_type  # 'SET' or 'RUN'
        self.score = self._calculate_score()
    
    def _calculate_score(self):
        """Calculate the score value of this meld"""
        base_score = sum(tile.get_value() for tile in self.tiles)
        
        # Bonus for longer melds
        length_bonus = (len(self.tiles) - 3) * 5
        
        # Bonus for pure melds (no jokers)
        joker_count = sum(1 for tile in self.tiles if tile.is_joker)
        purity_bonus = 10 if joker_count == 0 else 0
        
        return base_score + length_bonus + purity_bonus
    
    def __str__(self):
        return f"{self.meld_type}({', '.join(str(tile) for tile in self.tiles)})"

class OkeyGameLogic:
    """
    Implements Okey game rules and optimal playing strategies
    """
    
    def __init__(self):
        self.joker_tile = None  # The current joker for this round
        self.player_tiles = []  # Current player's tiles
        self.table_melds = []   # Melds already on the table
        self.discarded_tiles = []  # Tiles that have been discarded
        
    def set_joker_tile(self, joker_tile: OkeyTile):
        """Set the joker tile for this round"""
        self.joker_tile = joker_tile
    
    def update_player_tiles(self, tiles: List[OkeyTile]):
        """Update the current player's tiles"""
        self.player_tiles = tiles
    
    def find_all_possible_melds(self, tiles: List[OkeyTile]) -> List[OkeyMeld]:
        """Find all possible melds from the given tiles"""
        all_melds = []
        
        # Find all possible sets (3+ tiles of same number, different colors)
        all_melds.extend(self._find_sets(tiles))
        
        # Find all possible runs (3+ consecutive tiles of same color)
        all_melds.extend(self._find_runs(tiles))
        
        return all_melds
    
    def _find_sets(self, tiles: List[OkeyTile]) -> List[OkeyMeld]:
        """Find all possible sets from tiles"""
        sets = []
        
        # Group tiles by number
        number_groups = {}
        jokers = []
        
        for tile in tiles:
            if tile.is_joker:
                jokers.append(tile)
            else:
                if tile.number not in number_groups:
                    number_groups[tile.number] = []
                number_groups[tile.number].append(tile)
        
        # Find sets for each number
        for number, number_tiles in number_groups.items():
            if len(number_tiles) >= 3:
                # Check for valid sets (different colors)
                for r in range(3, min(5, len(number_tiles) + 1)):  # Max 4 colors
                    for combo in combinations(number_tiles, r):
                        colors = set(tile.color for tile in combo)
                        if len(colors) == len(combo):  # All different colors
                            sets.append(OkeyMeld(list(combo), 'SET'))
            
            # Sets with jokers
            if len(number_tiles) >= 2 and jokers:
                needed_jokers = 3 - len(number_tiles)
                if needed_jokers <= len(jokers):
                    colors = set(tile.color for tile in number_tiles)
                    if len(colors) == len(number_tiles):  # Different colors so far
                        meld_tiles = list(number_tiles) + jokers[:needed_jokers]
                        sets.append(OkeyMeld(meld_tiles, 'SET'))
        
        return sets
    
    def _find_runs(self, tiles: List[OkeyTile]) -> List[OkeyMeld]:
        """Find all possible runs from tiles"""
        runs = []
        
        # Group tiles by color
        color_groups = {}
        jokers = []
        
        for tile in tiles:
            if tile.is_joker:
                jokers.append(tile)
            else:
                if tile.color not in color_groups:
                    color_groups[tile.color] = []
                color_groups[tile.color].append(tile)
        
        # Find runs for each color
        for color, color_tiles in color_groups.items():
            # Sort by number
            color_tiles.sort(key=lambda x: x.number)
            
            # Find consecutive sequences
            runs.extend(self._find_consecutive_runs(color_tiles, jokers))
        
        return runs
    
    def _find_consecutive_runs(self, sorted_tiles: List[OkeyTile], jokers: List[OkeyTile]) -> List[OkeyMeld]:
        """Find consecutive runs in sorted tiles of same color"""
        runs = []
        
        for start_idx in range(len(sorted_tiles)):
            current_run = [sorted_tiles[start_idx]]
            last_number = sorted_tiles[start_idx].number
            used_jokers = 0
            
            for i in range(start_idx + 1, len(sorted_tiles)):
                current_tile = sorted_tiles[i]
                gap = current_tile.number - last_number
                
                if gap == 1:
                    # Consecutive
                    current_run.append(current_tile)
                    last_number = current_tile.number
                elif gap == 2 and used_jokers < len(jokers):
                    # Gap of 1, can fill with joker
                    current_run.append(jokers[used_jokers])
                    current_run.append(current_tile)
                    used_jokers += 1
                    last_number = current_tile.number
                else:
                    # Gap too large or no more jokers
                    break
            
            # Add to runs if length >= 3
            if len(current_run) >= 3:
                runs.append(OkeyMeld(current_run, 'RUN'))
        
        return runs
    
    def find_optimal_play(self, tiles: List[OkeyTile]) -> Tuple[List[OkeyMeld], OkeyTile]:
        """
        Find the optimal play: which melds to form and which tile to discard
        Returns (melds_to_play, tile_to_discard)
        """
        all_melds = self.find_all_possible_melds(tiles)
        
        if not all_melds:
            # No melds possible, discard lowest value tile
            discard_tile = min(tiles, key=lambda t: t.get_value())
            return [], discard_tile
        
        # Find the combination of melds that maximizes score
        best_combination = self._find_best_meld_combination(all_melds, tiles)
        
        if best_combination:
            # Remove used tiles from hand
            used_tiles = set()
            for meld in best_combination:
                used_tiles.update(meld.tiles)
            
            remaining_tiles = [t for t in tiles if t not in used_tiles]
            
            if remaining_tiles:
                # Discard the lowest value remaining tile
                discard_tile = min(remaining_tiles, key=lambda t: t.get_value())
            else:
                # All tiles used in melds - this would be a win!
                discard_tile = None
            
            return best_combination, discard_tile
        
        # No optimal combination found, be conservative
        discard_tile = min(tiles, key=lambda t: t.get_value())
        return [], discard_tile
    
    def _find_best_meld_combination(self, melds: List[OkeyMeld], available_tiles: List[OkeyTile]) -> List[OkeyMeld]:
        """Find the best combination of non-overlapping melds"""
        # This is a complex optimization problem
        # For now, use a greedy approach: select highest scoring non-overlapping melds
        
        # Sort melds by score descending
        sorted_melds = sorted(melds, key=lambda m: m.score, reverse=True)
        
        selected_melds = []
        used_tiles = set()
        
        for meld in sorted_melds:
            # Check if any tiles in this meld are already used
            meld_tiles = set(meld.tiles)
            if not meld_tiles.intersection(used_tiles):
                # No overlap, add this meld
                selected_melds.append(meld)
                used_tiles.update(meld_tiles)
        
        return selected_melds
    
    def calculate_hand_strength(self, tiles: List[OkeyTile]) -> float:
        """Calculate the strength/potential of a hand"""
        melds = self.find_all_possible_melds(tiles)
        
        if not melds:
            return 0.0
        
        # Base score from possible melds
        base_score = sum(meld.score for meld in melds)
        
        # Potential for future melds
        potential_score = self._calculate_potential(tiles)
        
        return base_score + potential_score * 0.3
    
    def _calculate_potential(self, tiles: List[OkeyTile]) -> float:
        """Calculate potential for forming melds in the future"""
        potential = 0.0
        
        # Count tiles that are close to forming melds
        # For sets: count tiles with same number
        number_counts = {}
        for tile in tiles:
            if not tile.is_joker:
                number_counts[tile.number] = number_counts.get(tile.number, 0) + 1
        
        for count in number_counts.values():
            if count == 2:
                potential += 5  # Close to forming a set
            elif count == 1:
                potential += 1  # Some potential
        
        # For runs: count consecutive tiles
        color_groups = {}
        for tile in tiles:
            if not tile.is_joker:
                if tile.color not in color_groups:
                    color_groups[tile.color] = []
                color_groups[tile.color].append(tile.number)
        
        for numbers in color_groups.values():
            numbers.sort()
            consecutive_count = 1
            for i in range(1, len(numbers)):
                if numbers[i] == numbers[i-1] + 1:
                    consecutive_count += 1
                else:
                    if consecutive_count == 2:
                        potential += 5  # Close to forming a run
                    consecutive_count = 1
            
            if consecutive_count == 2:
                potential += 5
        
        return potential
    
    def should_pick_discard(self, discard_tile: OkeyTile, current_tiles: List[OkeyTile]) -> bool:
        """Decide whether to pick up a discarded tile"""
        # Create hypothetical hand with the discard tile
        test_hand = current_tiles + [discard_tile]
        
        # Compare hand strength
        current_strength = self.calculate_hand_strength(current_tiles)
        new_strength = self.calculate_hand_strength(test_hand)
        
        # Pick up if it significantly improves hand strength
        return new_strength > current_strength + 10