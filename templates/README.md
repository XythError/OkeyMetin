# Template Images Directory

This directory should contain template images for better tile recognition:

## Required Templates

### Game UI Elements
- `start_button.png` - Start game button
- `finish_turn_button.png` - Finish turn button  
- `sort_tiles_button.png` - Sort tiles button
- `joker_indicator.png` - Joker indicator symbol

### Tile Templates (Optional)
If using template matching for tile recognition:

#### Numbers
- `number_1.png` through `number_13.png` - Individual number templates

#### Colors  
- `red_tile.png` - Red tile background
- `blue_tile.png` - Blue tile background
- `green_tile.png` - Green tile background
- `black_tile.png` - Black tile background

#### Special
- `joker_tile.png` - Joker tile template
- `empty_slot.png` - Empty tile slot

## Usage

Templates are used by the `TileRecognizer` class for more accurate detection when color/OCR recognition fails.

To capture templates:
1. Run the bot in debug mode
2. Take screenshots of the game elements
3. Crop and save the relevant parts as templates
4. Place them in this directory with the correct names

## Format

- **Format**: PNG recommended (supports transparency)
- **Size**: Match the actual game element size
- **Quality**: High quality, clear images work best
- **Background**: Crop tightly around the element