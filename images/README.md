# Debug Images Directory

This directory stores debug images and screenshots for development and troubleshooting.

## Contents

### Automatic Screenshots
- `debug_tile_*.jpg` - Individual detected tiles
- `game_state_*.png` - Full game state screenshots
- `recognition_*.png` - Tile recognition debug images

### Manual Captures
- Place your own screenshots here for testing
- Use for template creation
- Compare recognition results

## Usage

Debug images are automatically saved when:
- Running in debug mode
- Tile recognition fails
- Using the `debug_save_tiles()` function

To enable debug image saving, set debug flags in the bot configuration.

## Cleanup

These files can be safely deleted to free up space. The bot will recreate them as needed during operation.