"""
Main Okey Bot class that coordinates all components
"""
import time
import cv2 as cv
import pydirectinput
import numpy as np
from typing import List, Optional, Tuple

from window_capture import WindowCapture
from tile_recognizer import TileRecognizer
from okey_game_logic import OkeyGameLogic, OkeyMeld
from okey_tile import OkeyTile
import constants

class OkeyBot:
    """
    Main bot class that handles automatic Okey gameplay
    """
    
    def __init__(self, game_window_name: str = constants.GAME_NAME):
        # Initialize components
        self.window_capture = WindowCapture()
        self.tile_recognizer = TileRecognizer()
        self.game_logic = OkeyGameLogic()
        
        # Game state
        self.is_running = False
        self.game_active = False
        self.player_tiles = []
        self.joker_tile = None
        
        # Timing
        self.last_action_time = 0
        self.action_delay = constants.ACTION_DELAY
        self.click_delay = constants.CLICK_DELAY
        
        # Statistics
        self.games_played = 0
        self.total_score = 0
        self.start_time = None
        
        # Set up window capture
        try:
            self.window_capture.set_window(game_window_name)
            print(f"Successfully attached to window: {game_window_name}")
        except Exception as e:
            print(f"Failed to attach to window '{game_window_name}': {e}")
            print("Available windows:")
            WindowCapture.list_window_names()
    
    def start_bot(self):
        """Start the bot main loop"""
        print("Starting Okey Bot...")
        self.is_running = True
        self.start_time = time.time()
        
        while self.is_running:
            try:
                self._main_loop_iteration()
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
            except KeyboardInterrupt:
                print("\nBot stopped by user")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(1)  # Wait before retrying
        
        self._print_statistics()
    
    def stop_bot(self):
        """Stop the bot"""
        self.is_running = False
    
    def _main_loop_iteration(self):
        """Single iteration of the main bot loop"""
        # Capture current game state
        screenshot = self.window_capture.get_screenshot()
        
        if screenshot is None:
            return
        
        # Check if game is active
        if not self._is_game_active(screenshot):
            if self._should_start_new_game():
                self._start_new_game()
            return
        
        # Update game state
        self._update_game_state(screenshot)
        
        # Make optimal play decision
        if self._can_make_action():
            self._make_optimal_play()
    
    def _is_game_active(self, screenshot) -> bool:
        """Check if an Okey game is currently active"""
        # Look for game UI elements to determine if game is active
        # This would need to be implemented based on actual game UI
        
        # For now, check if there are tiles in the player area
        player_tiles = self._detect_player_tiles(screenshot)
        return len(player_tiles) > 0
    
    def _should_start_new_game(self) -> bool:
        """Determine if we should start a new game"""
        # Don't start too frequently
        if time.time() - self.last_action_time < constants.GAME_START_DELAY:
            return False
        
        return True
    
    def _start_new_game(self):
        """Start a new Okey game"""
        print("Starting new Okey game...")
        
        # Click start game button
        start_pos = self.window_capture.get_screen_position(constants.START_GAME_BUTTON)
        self._safe_click(start_pos)
        
        self.last_action_time = time.time()
        self.game_active = True
    
    def _update_game_state(self, screenshot):
        """Update the current game state from screenshot"""
        # Detect player tiles
        self.player_tiles = self._detect_player_tiles(screenshot)
        
        # Detect joker tile if visible
        joker = self._detect_joker_tile(screenshot)
        if joker:
            self.joker_tile = joker
            self.game_logic.set_joker_tile(joker)
        
        # Update game logic with current tiles
        self.game_logic.update_player_tiles(self.player_tiles)
    
    def _detect_player_tiles(self, screenshot) -> List[OkeyTile]:
        """Detect tiles in player's rack"""
        rack_x, rack_y = constants.PLAYER_RACK_POSITION
        rack_w, rack_h = constants.PLAYER_RACK_SIZE
        
        tiles = self.tile_recognizer.detect_tiles_in_region(
            screenshot, rack_x, rack_y, rack_w, rack_h
        )
        
        return tiles
    
    def _detect_joker_tile(self, screenshot) -> Optional[OkeyTile]:
        """Detect the current joker tile"""
        # Look in the joker display area (would need to be implemented based on UI)
        # For now, return None - joker detection needs UI analysis
        return None
    
    def _can_make_action(self) -> bool:
        """Check if enough time has passed to make an action"""
        return time.time() - self.last_action_time >= self.action_delay
    
    def _make_optimal_play(self):
        """Make the optimal play based on current game state"""
        if not self.player_tiles:
            return
        
        # Get optimal play decision from game logic
        melds_to_play, tile_to_discard = self.game_logic.find_optimal_play(self.player_tiles)
        
        # Execute the play
        if melds_to_play:
            self._play_melds(melds_to_play)
        
        if tile_to_discard:
            self._discard_tile(tile_to_discard)
        
        # Finish turn
        self._finish_turn()
        
        self.last_action_time = time.time()
    
    def _play_melds(self, melds: List[OkeyMeld]):
        """Play melds to the table"""
        print(f"Playing {len(melds)} melds:")
        for meld in melds:
            print(f"  {meld}")
            
            # For each meld, click and drag tiles to table
            for tile in meld.tiles:
                if tile.position:
                    tile_screen_pos = self.window_capture.get_screen_position(tile.position)
                    table_pos = self.window_capture.get_screen_position(constants.GAME_BOARD_POSITION)
                    
                    # Drag tile from rack to table
                    self._drag_tile(tile_screen_pos, table_pos)
                    time.sleep(self.click_delay)
    
    def _discard_tile(self, tile: OkeyTile):
        """Discard a tile"""
        if tile.position:
            print(f"Discarding tile: {tile}")
            tile_screen_pos = self.window_capture.get_screen_position(tile.position)
            
            # Right-click to discard (this might vary based on game UI)
            pydirectinput.click(tile_screen_pos[0], tile_screen_pos[1], button='right')
            time.sleep(self.click_delay)
    
    def _finish_turn(self):
        """Click finish turn button"""
        finish_pos = self.window_capture.get_screen_position(constants.FINISH_TURN_BUTTON)
        self._safe_click(finish_pos)
    
    def _safe_click(self, position: Tuple[int, int]):
        """Safely click at a position"""
        try:
            pydirectinput.click(position[0], position[1])
            time.sleep(self.click_delay)
        except Exception as e:
            print(f"Click error at {position}: {e}")
    
    def _drag_tile(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]):
        """Drag a tile from one position to another"""
        try:
            pydirectinput.mouseDown(from_pos[0], from_pos[1])
            time.sleep(0.1)
            pydirectinput.mouseUp(to_pos[0], to_pos[1])
            time.sleep(self.click_delay)
        except Exception as e:
            print(f"Drag error from {from_pos} to {to_pos}: {e}")
    
    def _print_statistics(self):
        """Print bot performance statistics"""
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            print("\n=== Bot Statistics ===")
            print(f"Games played: {self.games_played}")
            print(f"Total score: {self.total_score}")
            if self.games_played > 0:
                print(f"Average score: {self.total_score / self.games_played:.2f}")
            print(f"Runtime: {elapsed_time:.2f} seconds")
    
    def debug_mode(self):
        """Run in debug mode to visualize detection"""
        print("Starting debug mode...")
        
        while True:
            try:
                screenshot = self.window_capture.get_screenshot()
                if screenshot is None:
                    continue
                
                # Detect tiles and draw debug information
                debug_image = screenshot.copy()
                
                # Detect player tiles
                player_tiles = self._detect_player_tiles(screenshot)
                
                # Draw detected tiles
                for tile in player_tiles:
                    if tile.position:
                        x, y = tile.position
                        cv.circle(debug_image, (x, y), 20, (0, 255, 0), 2)
                        cv.putText(debug_image, str(tile), (x-20, y-25), 
                                 cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                
                # Draw UI regions
                self._draw_debug_regions(debug_image)
                
                # Show debug image
                cv.imshow('Okey Bot Debug', debug_image)
                
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Debug mode error: {e}")
                time.sleep(1)
        
        cv.destroyAllWindows()
    
    def _draw_debug_regions(self, image):
        """Draw debug rectangles for important regions"""
        # Player rack
        rack_x, rack_y = constants.PLAYER_RACK_POSITION
        rack_w, rack_h = constants.PLAYER_RACK_SIZE
        cv.rectangle(image, (rack_x, rack_y), (rack_x + rack_w, rack_y + rack_h), (255, 0, 0), 2)
        cv.putText(image, "Player Rack", (rack_x, rack_y - 10), 
                  cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        # Game board
        board_x, board_y = constants.GAME_BOARD_POSITION
        board_w, board_h = constants.GAME_BOARD_SIZE
        cv.rectangle(image, (board_x, board_y), (board_x + board_w, board_y + board_h), (0, 0, 255), 2)
        cv.putText(image, "Game Board", (board_x, board_y - 10), 
                  cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)