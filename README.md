# OkeyMetin - Metin2 Okey Game Bot

An intelligent game helper for automatically playing the Okey card game in Metin2. This bot can interactively play the game, start new rounds automatically, and implements strategic algorithms adapted to Okey game mechanics.

## Features

- **Automated Gameplay**: Automatically plays Okey card games in Metin2
- **Intelligent Strategy**: Uses strategic algorithms to make optimal card decisions
- **Game Detection**: Recognizes game state, cards, and interface elements
- **Auto-Start**: Automatically starts new games and rounds
- **GUI Interface**: User-friendly interface for bot control and monitoring
- **Statistics Tracking**: Tracks games played, win rate, and performance metrics

## Installation

1. Clone this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start Metin2 and navigate to the Okey game
2. Run the bot:
   ```bash
   python main.py
   ```
3. Configure bot settings in the GUI
4. Click "Start Bot" to begin automated gameplay

## Bot Components

- **OkeyCard & OkeyHand**: Card representation and hand management
- **OkeyGameState**: Tracks current game state and player information
- **OkeyStrategy**: Strategic decision making for optimal gameplay
- **OkeyDetection**: Image recognition for game interface elements
- **OkeyBot**: Main automation controller
- **WindowCapture**: Screen capture from Metin2 game window

## Game Rules

This bot implements the Metin2 Okey card game rules as described in:
https://de-wiki.metin2.gameforge.com/index.php/Okey-Karten-Spiel

## Configuration

The bot supports various configuration options:
- Action delays and timing parameters
- Risk tolerance for strategic decisions
- Auto-start behavior
- Debug and detection visualization modes

## Requirements

- Python 3.7+
- Windows OS (for Win32 API)
- Metin2 game client
- Required Python packages (see requirements.txt)

## Disclaimer

This bot is for educational purposes. Please ensure compliance with game terms of service and local regulations when using automation tools.
