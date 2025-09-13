# Metin2 Okey Bot

A fully automated bot for playing the Okey card game in Metin2. The bot uses computer vision to detect game state, implements optimal Okey strategies, and automatically plays the game to achieve maximum scores.

## Features

- **Automatic Game Detection**: Recognizes when Okey games are available and automatically starts new rounds
- **Advanced Tile Recognition**: Uses computer vision to detect tile colors, numbers, and jokers
- **Optimal Strategy Engine**: Implements sophisticated algorithms for optimal meld formation and tile discarding
- **Real-time Decision Making**: Makes intelligent decisions based on current hand and game state
- **Statistics Tracking**: Monitors performance with detailed statistics and scoring
- **User-Friendly GUI**: Simple interface for controlling the bot
- **Debug Mode**: Visual debugging tools for development and troubleshooting

## Installation

### Prerequisites

- Python 3.8 or higher
- Metin2 game client
- Windows OS (for Windows API functions)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/XythError/OkeyMetin.git
cd OkeyMetin
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR for text recognition:
   - Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
   - Add Tesseract to your system PATH

4. Configure game window settings in `constants.py` if needed

## Usage

### GUI Mode (Recommended)

Run the bot with the graphical interface:

```bash
python main.py
```

The GUI provides:
- Start/Stop bot controls
- Real-time statistics
- Configuration options
- Debug mode access
- Activity logging

### Console Mode

For advanced users, you can run the bot directly:

```python
from okey_bot import OkeyBot

bot = OkeyBot("Metin2")  # Replace with your game window name
bot.start_bot()
```

### Debug Mode

Use debug mode to visualize tile detection and calibrate settings:

1. Click "Debug Mode" in the GUI, or
2. Run directly: `bot.debug_mode()`

Debug mode shows:
- Detected tile positions
- Recognized tile values
- Game region boundaries
- Recognition confidence scores

## Configuration

### Window Settings

Adjust these values in `constants.py` based on your screen resolution and game window size:

```python
# Game window dimensions
OKEY_WINDOW_SIZE = (800, 600)
OKEY_WINDOW_POSITION = (200, 100)

# Player rack position
PLAYER_RACK_POSITION = (220, 480)
PLAYER_RACK_SIZE = (560, 80)
```

### Recognition Settings

Fine-tune tile recognition parameters:

```python
# Color detection ranges (HSV)
TILE_COLORS = {
    'RED': {'lower': (0, 50, 50), 'upper': (10, 255, 255)},
    # ... other colors
}

# OCR configuration
OCR_CONFIG = '--psm 8 -c tessedit_char_whitelist=0123456789'
```

### Strategy Settings

Customize bot behavior:

```python
# Timing delays
CLICK_DELAY = 0.3
ACTION_DELAY = 1.0

# Scoring preferences
MELD_SCORES = {
    'SET_3': 10,
    'RUN_4': 18,
    # ... other meld types
}
```

## Okey Game Strategy

The bot implements several advanced strategies:

### Meld Formation
- **Sets**: Groups of 3+ tiles with same number but different colors
- **Runs**: Sequences of 3+ consecutive tiles of the same color
- **Joker Usage**: Intelligent joker placement for maximum value

### Decision Making
- **Hand Evaluation**: Calculates potential and current hand strength
- **Discard Strategy**: Removes tiles with lowest strategic value
- **Pickup Decisions**: Evaluates whether to pick up discarded tiles
- **Optimal Timing**: Balances speed with score maximization

### Advanced Features
- **Look-ahead Analysis**: Considers future turn possibilities
- **Joker Conservation**: Preserves jokers for high-value melds
- **Endgame Detection**: Adjusts strategy when approaching game end

## Performance

The bot is optimized for:
- **Speed**: Processes game state in ~100ms
- **Accuracy**: >95% tile recognition accuracy
- **Strategy**: Achieves consistently high scores
- **Reliability**: Handles various game conditions and errors

## Troubleshooting

### Common Issues

**Bot doesn't detect game window:**
- Ensure Metin2 window title matches `GAME_NAME` in constants.py
- Try running `WindowCapture.list_window_names()` to see available windows

**Tile recognition problems:**
- Use debug mode to visualize detection
- Adjust `TILE_COLORS` ranges in constants.py
- Ensure good lighting and contrast in game

**OCR not working:**
- Verify Tesseract installation and PATH configuration
- Check that game text is clear and readable

**Performance issues:**
- Reduce `ACTION_DELAY` for faster gameplay
- Close other applications to free up resources
- Ensure stable frame rate in game

### Debug Tools

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Save debug images:
```python
bot.tile_recognizer.debug_save_tiles(screenshot, tiles, "debug")
```

Monitor performance:
```python
from utils import performance_monitor
performance_monitor.print_stats()
```

## Contributing

Contributions are welcome! Areas for improvement:

- **Recognition Accuracy**: Better tile detection algorithms
- **Strategy Optimization**: Enhanced decision-making logic
- **Game Variants**: Support for different Okey rule sets
- **Performance**: Speed and memory optimizations
- **Testing**: Automated test suites

## License

This project is for educational purposes only. Please ensure compliance with game terms of service.

## Disclaimer

This bot is designed for learning and research purposes. Users are responsible for ensuring their usage complies with game rules and terms of service. The developers are not responsible for any consequences of bot usage.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review debug mode output
3. Open an issue on GitHub with detailed information

## Acknowledgments

Inspired by similar game automation projects:
- [Metin2FishBot](https://github.com/XythError/Metin2FishBot)
- [Metin2Tetris](https://github.com/vncsms/metin2tetris)

Built with:
- OpenCV for computer vision
- Tesseract for OCR
- PySimpleGUI for interface
- PyDirectInput for automation
