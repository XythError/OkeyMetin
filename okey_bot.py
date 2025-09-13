"""
Main Okey Bot for automated Metin2 Okey gameplay
"""
import numpy as np
import pydirectinput
import cv2 as cv
import time
from windowcapture import WindowCapture
from okey_detection import OkeyDetection
from okey_game import OkeyGameState, OkeyStrategy
from okey_card import OkeyCard
import constants


class OkeyBot:
    """Main bot class for automated Okey gameplay"""
    
    def __init__(self):
        # Core components
        self.wincap = None
        self.detector = OkeyDetection()
        self.game_state = OkeyGameState()
        self.strategy = OkeyStrategy()
        
        # Bot state
        self.botting = False
        self.auto_start = True
        
        # Timing parameters
        self.action_delay = 1.0  # Delay between actions
        self.click_delay = 0.3   # Delay between clicks
        self.game_start_delay = 5.0  # Delay before starting new game
        
        # Timers
        self.last_action_time = time.time()
        self.last_click_time = time.time()
        self.game_start_time = None
        
        # Game statistics
        self.games_played = 0
        self.games_won = 0
        self.current_round_time = 0
        
        # Debug settings
        self.debug_mode = False
        self.show_detection = False
        
    def initialize(self, settings):
        """Initialize the bot with user settings"""
        try:
            self.wincap = WindowCapture(constants.GAME_NAME)
        except Exception as e:
            raise Exception(f"Could not find Metin2 game window: {e}")
        
        # Apply user settings
        self.action_delay = settings.get('action_delay', 1.0)
        self.click_delay = settings.get('click_delay', 0.3)
        self.auto_start = settings.get('auto_start', True)
        self.debug_mode = settings.get('debug_mode', False)
        
        self.botting = True
        self.game_start_time = time.time()
        
        print("OkeyBot initialized successfully")
        
    def run_cycle(self):
        """Run one cycle of the bot"""
        if not self.botting:
            return None
            
        try:
            # Capture screenshot
            screenshot = self.wincap.get_screenshot()
            
            # Update game state from screenshot
            self._update_game_state(screenshot)
            
            # Decide on next action
            action = self._decide_action()
            
            # Execute action
            self._execute_action(action, screenshot)
            
            # Return debug image if requested
            if self.show_detection:
                return self._create_debug_image(screenshot)
                
        except Exception as e:
            print(f"Error in bot cycle: {e}")
            if self.debug_mode:
                raise
                
        return None
        
    def _update_game_state(self, screenshot):
        """Update game state based on current screenshot"""
        # Detect current game state
        detected_state = self.detector.detect_game_state(screenshot)
        
        if detected_state != self.game_state.game_state:
            print(f"Game state changed: {self.game_state.game_state} -> {detected_state}")
            self.game_state.game_state = detected_state
            
            # Handle state transitions
            if detected_state == constants.GAME_STATE_PLAYING:
                self._on_game_started()
            elif detected_state == constants.GAME_STATE_FINISHED:
                self._on_game_finished()
        
        # Update player turn status
        self.game_state.is_player_turn = (detected_state == constants.GAME_STATE_TURN)
        
        # Detect cards in hand
        if detected_state in [constants.GAME_STATE_PLAYING, constants.GAME_STATE_TURN]:
            detected_cards = self.detector.detect_cards_in_hand(screenshot)
            self._update_hand(detected_cards)
            
            # Detect center card
            center_card = self.detector.detect_center_card(screenshot)
            self.game_state.set_center_card(center_card)
            
            # Detect joker
            joker_card = self.detector.detect_joker_card(screenshot)
            if joker_card and not self.game_state.joker_card:
                self.game_state.set_joker(joker_card)
                
    def _update_hand(self, detected_cards):
        """Update the game state hand with detected cards"""
        # Clear current hand and rebuild
        self.game_state.player_hand.cards.clear()
        for card in detected_cards:
            self.game_state.add_card_to_hand(card)
            
    def _decide_action(self):
        """Decide what action to take next"""
        current_time = time.time()
        
        # Respect action delay
        if current_time - self.last_action_time < self.action_delay:
            return "WAIT"
            
        # Handle different game states
        if self.game_state.game_state == constants.GAME_STATE_WAITING:
            if self.auto_start:
                return "START_GAME"
            return "WAIT"
            
        elif self.game_state.game_state == constants.GAME_STATE_FINISHED:
            if self.auto_start:
                return "START_NEW_GAME"
            return "WAIT"
            
        elif self.game_state.game_state == constants.GAME_STATE_TURN:
            # Use strategy to decide action
            return self.strategy.get_next_action(self.game_state)
            
        return "WAIT"
        
    def _execute_action(self, action, screenshot):
        """Execute the decided action"""
        current_time = time.time()
        
        if action == "WAIT":
            return
            
        # Respect click delay
        if current_time - self.last_click_time < self.click_delay:
            return
            
        print(f"Executing action: {action}")
        
        # Detect available buttons
        buttons = self.detector.detect_game_buttons(screenshot)
        
        if action == "START_GAME":
            self._click_button(buttons, 'start_game')
            
        elif action == "START_NEW_GAME":
            time.sleep(self.game_start_delay)  # Wait before starting new game
            self._click_button(buttons, 'start_game')
            
        elif action == "DRAW_CARD":
            self._click_button(buttons, 'draw_card')
            
        elif action == "TAKE_CENTER":
            center_card = self.game_state.center_card
            if center_card:
                self._click_center_card()
                
        elif action.startswith("DISCARD_"):
            card_str = action.replace("DISCARD_", "")
            self._discard_card(card_str)
            
        elif action == "DECLARE_WIN":
            self._click_button(buttons, 'declare_win')
            
        self.last_action_time = current_time
        self.last_click_time = current_time
        
    def _click_button(self, buttons, button_name):
        """Click a specific button"""
        if button_name in buttons:
            x, y = buttons[button_name]
            screen_x, screen_y = self.wincap.get_screen_position((x, y))
            pydirectinput.click(x=screen_x, y=screen_y)
            print(f"Clicked {button_name} at ({screen_x}, {screen_y})")
        else:
            print(f"Button {button_name} not found")
            
    def _click_center_card(self):
        """Click the center card to take it"""
        x, y, w, h = self.detector.center_area
        center_x = x + w // 2
        center_y = y + h // 2
        screen_x, screen_y = self.wincap.get_screen_position((center_x, center_y))
        pydirectinput.click(x=screen_x, y=screen_y)
        print(f"Clicked center card at ({screen_x}, {screen_y})")
        
    def _discard_card(self, card_str):
        """Discard a specific card"""
        # Find the card in hand and click it
        # This would need to map card_str to screen position
        hand_x, hand_y, hand_w, hand_h = self.detector.hand_area
        
        # Simplified: click middle of hand area
        discard_x = hand_x + hand_w // 2
        discard_y = hand_y + hand_h // 2
        screen_x, screen_y = self.wincap.get_screen_position((discard_x, discard_y))
        pydirectinput.click(x=screen_x, y=screen_y)
        print(f"Discarded card at ({screen_x}, {screen_y})")
        
    def _on_game_started(self):
        """Handle game start event"""
        print("New game started!")
        self.games_played += 1
        self.game_state.reset_for_new_round()
        
    def _on_game_finished(self):
        """Handle game finish event"""
        print("Game finished!")
        # Could detect if we won/lost here
        self.current_round_time = time.time() - self.game_start_time
        
    def _create_debug_image(self, screenshot):
        """Create debug visualization of detections"""
        debug_img = screenshot.copy()
        
        # Draw detection areas
        areas = [
            (self.detector.hand_area, (0, 255, 0), "Hand"),
            (self.detector.center_area, (255, 0, 0), "Center"),
            (self.detector.joker_area, (0, 0, 255), "Joker")
        ]
        
        for (x, y, w, h), color, label in areas:
            cv.rectangle(debug_img, (x, y), (x + w, y + h), color, 2)
            cv.putText(debug_img, label, (x, y - 10), 
                      cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        # Add game state info
        info_text = [
            f"State: {self.game_state.game_state}",
            f"Turn: {self.game_state.is_player_turn}",
            f"Hand: {len(self.game_state.player_hand)} cards",
            f"Games: {self.games_played}"
        ]
        
        for i, text in enumerate(info_text):
            cv.putText(debug_img, text, (10, 30 + i * 20), 
                      cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return debug_img
        
    def stop(self):
        """Stop the bot"""
        self.botting = False
        print("OkeyBot stopped")
        
    def get_statistics(self):
        """Get bot performance statistics"""
        return {
            'games_played': self.games_played,
            'games_won': self.games_won,
            'win_rate': self.games_won / max(self.games_played, 1),
            'current_round_time': self.current_round_time
        }