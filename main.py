"""
Main application entry point for OkeyBot
Provides GUI interface for controlling the bot
"""
import PySimpleGUI as sg
import cv2 as cv
import time
import threading
from okey_bot import OkeyBot
import constants


class OkeyBotGUI:
    """GUI interface for OkeyBot"""
    
    def __init__(self):
        self.bot = OkeyBot()
        self.running = False
        self.bot_thread = None
        
        # GUI theme
        sg.theme('DarkBlue3')
        
        # Create layout
        self.layout = self._create_layout()
        self.window = sg.Window('Metin2 Okey Bot', self.layout, finalize=True)
        
    def _create_layout(self):
        """Create the GUI layout"""
        
        # Settings column
        settings_col = [
            [sg.Text('Bot Settings', font=('Arial', 12, 'bold'))],
            [sg.Text('Action Delay (seconds):'), sg.Input('1.0', key='-ACTION_DELAY-', size=(10, 1))],
            [sg.Text('Click Delay (seconds):'), sg.Input('0.3', key='-CLICK_DELAY-', size=(10, 1))],
            [sg.Text('Game Start Delay (seconds):'), sg.Input('5.0', key='-START_DELAY-', size=(10, 1))],
            [sg.Checkbox('Auto Start Games', default=True, key='-AUTO_START-')],
            [sg.Checkbox('Debug Mode', default=False, key='-DEBUG_MODE-')],
            [sg.Checkbox('Show Detection', default=False, key='-SHOW_DETECTION-')],
            [sg.HSeparator()],
            [sg.Text('Risk Tolerance:'), sg.Slider(range=(0, 100), default_value=50, 
                                                   orientation='h', size=(20, 15), key='-RISK-')],
            [sg.HSeparator()],
            [sg.Button('Start Bot', key='-START-', size=(12, 1), button_color=('white', 'green'))],
            [sg.Button('Stop Bot', key='-STOP-', size=(12, 1), button_color=('white', 'red'), disabled=True)],
            [sg.Button('Test Detection', key='-TEST-', size=(12, 1))],
            [sg.Button('Exit', key='-EXIT-', size=(12, 1))]
        ]
        
        # Statistics column
        stats_col = [
            [sg.Text('Bot Statistics', font=('Arial', 12, 'bold'))],
            [sg.Text('Status: Stopped', key='-STATUS-')],
            [sg.Text('Games Played: 0', key='-GAMES_PLAYED-')],
            [sg.Text('Games Won: 0', key='-GAMES_WON-')],
            [sg.Text('Win Rate: 0%', key='-WIN_RATE-')],
            [sg.Text('Current Round Time: 0s', key='-ROUND_TIME-')],
            [sg.HSeparator()],
            [sg.Text('Current Game State:')],
            [sg.Text('State: Waiting', key='-GAME_STATE-')],
            [sg.Text('Turn: No', key='-PLAYER_TURN-')],
            [sg.Text('Hand Size: 0', key='-HAND_SIZE-')],
            [sg.Text('Center Card: None', key='-CENTER_CARD-')],
            [sg.Text('Joker: None', key='-JOKER_CARD-')]
        ]
        
        # Log column
        log_col = [
            [sg.Text('Bot Log', font=('Arial', 12, 'bold'))],
            [sg.Multiline(size=(50, 15), key='-LOG-', disabled=True, autoscroll=True)]
        ]
        
        # Image display
        image_col = [
            [sg.Text('Game Detection View', font=('Arial', 12, 'bold'))],
            [sg.Image(key='-IMAGE-', size=(400, 300))]
        ]
        
        # Main layout
        layout = [
            [sg.Column(settings_col, vertical_alignment='top'),
             sg.VSeparator(),
             sg.Column(stats_col, vertical_alignment='top'),
             sg.VSeparator(),
             sg.Column(log_col, vertical_alignment='top')],
            [sg.HSeparator()],
            [sg.Column(image_col, justification='center')]
        ]
        
        return layout
        
    def run(self):
        """Run the GUI application"""
        while True:
            event, values = self.window.read(timeout=100)
            
            if event in (sg.WIN_CLOSED, '-EXIT-'):
                break
                
            elif event == '-START-':
                self._start_bot(values)
                
            elif event == '-STOP-':
                self._stop_bot()
                
            elif event == '-TEST-':
                self._test_detection()
                
            # Update displays if bot is running
            if self.running:
                self._update_displays()
                
        self._cleanup()
        
    def _start_bot(self, values):
        """Start the bot with current settings"""
        try:
            # Parse settings
            settings = {
                'action_delay': float(values['-ACTION_DELAY-']),
                'click_delay': float(values['-CLICK_DELAY-']),
                'game_start_delay': float(values['-START_DELAY-']),
                'auto_start': values['-AUTO_START-'],
                'debug_mode': values['-DEBUG_MODE-'],
                'show_detection': values['-SHOW_DETECTION-']
            }
            
            # Set strategy parameters
            self.bot.strategy.risk_tolerance = values['-RISK-'] / 100.0
            
            # Initialize bot
            self.bot.initialize(settings)
            
            # Start bot thread
            self.running = True
            self.bot_thread = threading.Thread(target=self._bot_worker, daemon=True)
            self.bot_thread.start()
            
            # Update GUI
            self.window['-START-'].update(disabled=True)
            self.window['-STOP-'].update(disabled=False)
            self.window['-STATUS-'].update('Status: Running')
            
            self._log("Bot started successfully!")
            
        except Exception as e:
            self._log(f"Error starting bot: {e}")
            sg.popup_error(f"Failed to start bot: {e}")
            
    def _stop_bot(self):
        """Stop the bot"""
        self.running = False
        self.bot.stop()
        
        if self.bot_thread:
            self.bot_thread.join(timeout=2)
            
        # Update GUI
        self.window['-START-'].update(disabled=False)
        self.window['-STOP-'].update(disabled=True)
        self.window['-STATUS-'].update('Status: Stopped')
        
        self._log("Bot stopped")
        
    def _test_detection(self):
        """Test the detection system"""
        try:
            if not self.bot.wincap:
                self.bot.wincap = WindowCapture(constants.GAME_NAME)
                
            screenshot = self.bot.wincap.get_screenshot()
            
            # Test detection
            game_state = self.bot.detector.detect_game_state(screenshot)
            cards = self.bot.detector.detect_cards_in_hand(screenshot)
            buttons = self.bot.detector.detect_game_buttons(screenshot)
            
            self._log(f"Detection test - State: {game_state}, Cards: {len(cards)}, Buttons: {len(buttons)}")
            
            # Show debug image
            debug_img = self.bot._create_debug_image(screenshot)
            self._update_image_display(debug_img)
            
        except Exception as e:
            self._log(f"Detection test failed: {e}")
            sg.popup_error(f"Detection test failed: {e}")
            
    def _bot_worker(self):
        """Worker thread for running the bot"""
        while self.running:
            try:
                debug_img = self.bot.run_cycle()
                
                if debug_img is not None:
                    self._update_image_display(debug_img)
                    
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
            except Exception as e:
                self._log(f"Bot error: {e}")
                if self.bot.debug_mode:
                    break
                    
        self.running = False
        
    def _update_displays(self):
        """Update the GUI displays with current bot state"""
        # Update statistics
        stats = self.bot.get_statistics()
        self.window['-GAMES_PLAYED-'].update(f"Games Played: {stats['games_played']}")
        self.window['-GAMES_WON-'].update(f"Games Won: {stats['games_won']}")
        self.window['-WIN_RATE-'].update(f"Win Rate: {stats['win_rate']:.1%}")
        self.window['-ROUND_TIME-'].update(f"Current Round Time: {stats['current_round_time']:.1f}s")
        
        # Update game state
        game_state = self.bot.game_state
        self.window['-GAME_STATE-'].update(f"State: {game_state.game_state}")
        self.window['-PLAYER_TURN-'].update(f"Turn: {'Yes' if game_state.is_player_turn else 'No'}")
        self.window['-HAND_SIZE-'].update(f"Hand Size: {len(game_state.player_hand)}")
        
        center_card = "None" if not game_state.center_card else str(game_state.center_card)
        self.window['-CENTER_CARD-'].update(f"Center Card: {center_card}")
        
        joker_card = "None" if not game_state.joker_card else str(game_state.joker_card)
        self.window['-JOKER_CARD-'].update(f"Joker: {joker_card}")
        
    def _update_image_display(self, image):
        """Update the image display with detection visualization"""
        try:
            # Resize image to fit display
            height, width = image.shape[:2]
            max_width, max_height = 400, 300
            
            if width > max_width or height > max_height:
                scale = min(max_width / width, max_height / height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                image = cv.resize(image, (new_width, new_height))
            
            # Convert to bytes for display
            imgbytes = cv.imencode('.png', image)[1].tobytes()
            self.window['-IMAGE-'].update(data=imgbytes)
            
        except Exception as e:
            self._log(f"Error updating image display: {e}")
            
    def _log(self, message):
        """Add message to log"""
        timestamp = time.strftime('%H:%M:%S')
        log_message = f"[{timestamp}] {message}\n"
        self.window['-LOG-'].update(log_message, append=True)
        
    def _cleanup(self):
        """Cleanup resources"""
        if self.running:
            self._stop_bot()
        self.window.close()


def main():
    """Main application entry point"""
    print("Starting Metin2 Okey Bot...")
    
    try:
        app = OkeyBotGUI()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        sg.popup_error(f"Application error: {e}")


if __name__ == "__main__":
    main()