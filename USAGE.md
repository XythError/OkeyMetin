# OkeyBot Usage Guide

## Quick Start

1. **Prerequisites**
   - Windows operating system
   - Python 3.7 or higher  
   - Metin2 game client

2. **Installation**
   ```bash
   git clone https://github.com/XythError/OkeyMetin.git
   cd OkeyMetin
   pip install -r requirements.txt
   ```

3. **Basic Usage**
   ```bash
   python start.py
   ```

## Bot Configuration

### Timing Settings
- **Action Delay**: Time between bot actions (default: 1.0s)
- **Click Delay**: Time between mouse clicks (default: 0.3s)  
- **Game Start Delay**: Wait time before starting new games (default: 5.0s)

### Strategy Settings
- **Risk Tolerance**: 0-100% aggressive vs conservative play
- **Auto Start**: Automatically begin new games
- **Debug Mode**: Enhanced error reporting

### Detection Settings
- **Show Detection**: Visualize card/button detection areas
- Game area calibration (automatic)

## Game Strategy

The bot implements several strategic approaches:

### Card Evaluation
- **Sets**: 3+ cards of same number, different colors
- **Runs**: 3+ consecutive cards of same color
- **Jokers**: High value, versatile for completing groups
- **Deadwood**: Unmatched cards to minimize

### Decision Making
1. **Card Taking**: Evaluates center card value vs hand needs
2. **Discarding**: Removes least valuable cards first
3. **Winning**: Declares when hand strength is optimal
4. **Risk Management**: Adjusts aggression based on game state

## Troubleshooting

### Common Issues

**Bot can't find Metin2 window**
- Ensure Metin2 is running and visible
- Check window title matches "Metin2" exactly
- Try running as administrator

**Card detection not working**
- Calibrate detection areas for your screen resolution
- Ensure good lighting/contrast in game
- Check game window is not minimized or covered

**Bot actions too fast/slow**
- Adjust timing settings in GUI
- Increase delays for slower systems
- Consider network latency for online play

**Dependencies missing**
- Run `pip install -r requirements.txt`
- Ensure all packages installed successfully
- Check Python version compatibility

### Debug Features

**Test Detection**: Validate card/button recognition
**Show Detection**: Visualize detection areas over game
**Debug Mode**: Detailed error logging and stack traces

## Advanced Configuration

### Strategy Tuning
Modify `OkeyStrategy` class for custom decision logic:
- `evaluate_card_value()`: Card scoring algorithm
- `choose_discard_card()`: Discard selection logic
- `should_take_center_card()`: Center card evaluation

### Detection Customization
Adjust `OkeyDetection` areas for different screen sizes:
- `hand_area`: Player card positions
- `center_area`: Table center card location  
- `joker_area`: Joker indicator position

### Performance Optimization
- Reduce image processing resolution
- Optimize detection frequency
- Adjust action timing for smoother gameplay

## Safety Notes

- **Game ToS**: Ensure bot usage complies with game terms
- **Detection**: Bot may be detectable by anti-cheat systems
- **Fairness**: Consider impact on other players
- **Testing**: Test thoroughly in practice modes first

## Support

For issues or improvements:
1. Check existing GitHub issues
2. Create detailed bug reports with logs
3. Include system information and game version
4. Provide screenshots of detection problems

## Contributing

Contributions welcome for:
- Enhanced detection algorithms
- Improved strategy logic
- Additional game features
- Performance optimizations
- Documentation improvements