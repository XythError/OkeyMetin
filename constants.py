"""
Constants for Metin2 Okey Bot
"""

# Game window name
GAME_NAME = "Metin2"

# Okey game window dimensions and positions
# These values may need adjustment based on screen resolution and game window size
OKEY_WINDOW_SIZE = (800, 600)
OKEY_WINDOW_POSITION = (200, 100)

# Player rack position (where player's cards are displayed)
PLAYER_RACK_POSITION = (220, 480)
PLAYER_RACK_SIZE = (560, 80)

# Game board position (where tiles are placed during game)
GAME_BOARD_POSITION = (220, 200)
GAME_BOARD_SIZE = (560, 280)

# Control buttons positions
START_GAME_BUTTON = (400, 550)
FINISH_TURN_BUTTON = (500, 550)
SORT_TILES_BUTTON = (350, 550)

# Card/tile dimensions
TILE_WIDTH = 35
TILE_HEIGHT = 50

# Colors for tile recognition (HSV values)
TILE_COLORS = {
    'RED': {'lower': (0, 50, 50), 'upper': (10, 255, 255)},
    'BLUE': {'lower': (100, 50, 50), 'upper': (130, 255, 255)},
    'GREEN': {'lower': (40, 50, 50), 'upper': (80, 255, 255)},
    'BLACK': {'lower': (0, 0, 0), 'upper': (180, 255, 50)},
    'YELLOW': {'lower': (20, 50, 50), 'upper': (40, 255, 255)}
}

# OCR settings for number recognition
OCR_CONFIG = '--psm 8 -c tessedit_char_whitelist=0123456789'

# Game timing constants
CLICK_DELAY = 0.3
ACTION_DELAY = 1.0
GAME_START_DELAY = 2.0

# Scoring values for strategy
MELD_SCORES = {
    'SET_3': 10,
    'SET_4': 15,
    'RUN_3': 12,
    'RUN_4': 18,
    'RUN_5': 25,
    'RUN_6': 32,
    'RUN_7': 40
}

# Joker identification
JOKER_VALUE = 0  # Special value for joker tiles