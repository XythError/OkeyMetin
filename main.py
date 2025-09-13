"""
Main entry point for the Metin2 Okey Bot
"""
import PySimpleGUI as sg
import threading
import time
from okey_bot import OkeyBot

class OkeyBotGUI:
    """Simple GUI for the Okey Bot"""
    
    def __init__(self):
        self.bot = None
        self.bot_thread = None
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI layout"""
        sg.theme('DarkBlue3')
        
        layout = [
            [sg.Text('Metin2 Okey Bot', font=('Helvetica', 16), justification='center')],
            [sg.Text('_' * 50)],
            
            [sg.Text('Bot Status:'), sg.Text('Stopped', key='STATUS', text_color='red')],
            [sg.Text('Games Played:'), sg.Text('0', key='GAMES')],
            [sg.Text('Total Score:'), sg.Text('0', key='SCORE')],
            [sg.Text('Average Score:'), sg.Text('0.00', key='AVG_SCORE')],
            
            [sg.Text('_' * 50)],
            
            [sg.Button('Start Bot', key='START', button_color=('white', 'green')),
             sg.Button('Stop Bot', key='STOP', button_color=('white', 'red'), disabled=True),
             sg.Button('Debug Mode', key='DEBUG', button_color=('white', 'orange'))],
            
            [sg.Text('_' * 50)],
            
            [sg.Text('Game Window Name:'), sg.Input('Metin2', key='WINDOW_NAME', size=(20, 1))],
            [sg.Text('Action Delay (s):'), sg.Input('1.0', key='ACTION_DELAY', size=(10, 1))],
            [sg.Checkbox('Auto Start New Games', key='AUTO_START', default=True)],
            
            [sg.Text('_' * 50)],
            
            [sg.Multiline('Bot ready to start...\n', key='LOG', size=(60, 10), disabled=True, autoscroll=True)],
            
            [sg.Button('Exit', button_color=('white', 'darkred'))]
        ]
        
        self.window = sg.Window('Metin2 Okey Bot', layout, finalize=True)
    
    def run(self):
        """Run the GUI main loop"""
        while True:
            event, values = self.window.read(timeout=1000)
            
            if event in (sg.WIN_CLOSED, 'Exit'):
                self._cleanup()
                break
            
            elif event == 'START':
                self._start_bot(values)
            
            elif event == 'STOP':
                self._stop_bot()
            
            elif event == 'DEBUG':
                self._start_debug_mode(values)
            
            # Update status display
            self._update_status_display()
        
        self.window.close()
    
    def _start_bot(self, values):
        """Start the bot in a separate thread"""
        if self.bot_thread and self.bot_thread.is_alive():
            self._log("Bot is already running!")
            return
        
        try:
            # Create bot instance
            window_name = values['WINDOW_NAME'] or 'Metin2'
            self.bot = OkeyBot(window_name)
            
            # Configure bot settings
            try:
                self.bot.action_delay = float(values['ACTION_DELAY'])
            except ValueError:
                self.bot.action_delay = 1.0
            
            # Start bot in separate thread
            self.bot_thread = threading.Thread(target=self.bot.start_bot, daemon=True)
            self.bot_thread.start()
            
            # Update UI
            self.window['START'].update(disabled=True)
            self.window['STOP'].update(disabled=False)
            self.window['STATUS'].update('Running', text_color='green')
            
            self._log(f"Bot started with window: {window_name}")
            
        except Exception as e:
            self._log(f"Failed to start bot: {e}")
    
    def _stop_bot(self):
        """Stop the bot"""
        if self.bot:
            self.bot.stop_bot()
            self._log("Stopping bot...")
        
        # Update UI
        self.window['START'].update(disabled=False)
        self.window['STOP'].update(disabled=True)
        self.window['STATUS'].update('Stopped', text_color='red')
    
    def _start_debug_mode(self, values):
        """Start debug mode"""
        try:
            window_name = values['WINDOW_NAME'] or 'Metin2'
            debug_bot = OkeyBot(window_name)
            
            self._log("Starting debug mode... Press 'q' in the debug window to exit.")
            
            # Run debug mode in separate thread
            debug_thread = threading.Thread(target=debug_bot.debug_mode, daemon=True)
            debug_thread.start()
            
        except Exception as e:
            self._log(f"Failed to start debug mode: {e}")
    
    def _update_status_display(self):
        """Update the status display with current bot statistics"""
        if self.bot:
            self.window['GAMES'].update(str(self.bot.games_played))
            self.window['SCORE'].update(str(self.bot.total_score))
            
            if self.bot.games_played > 0:
                avg_score = self.bot.total_score / self.bot.games_played
                self.window['AVG_SCORE'].update(f"{avg_score:.2f}")
    
    def _log(self, message):
        """Add a message to the log"""
        timestamp = time.strftime('%H:%M:%S')
        log_message = f"[{timestamp}] {message}\n"
        self.window['LOG'].print(log_message, end='')
    
    def _cleanup(self):
        """Clean up resources"""
        if self.bot:
            self.bot.stop_bot()
        
        if self.bot_thread and self.bot_thread.is_alive():
            self.bot_thread.join(timeout=2)

def main():
    """Main entry point"""
    print("Starting Metin2 Okey Bot...")
    
    try:
        gui = OkeyBotGUI()
        gui.run()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        
        # Fallback: run bot without GUI
        print("Starting bot in console mode...")
        bot = OkeyBot()
        try:
            bot.start_bot()
        except KeyboardInterrupt:
            print("Bot stopped by user")

if __name__ == "__main__":
    main()