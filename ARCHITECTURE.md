# OkeyBot Architecture

## System Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Main GUI      │    │   OkeyBot       │    │  WindowCapture  │
│   (main.py)     │◄──►│  (okey_bot.py)  │◄──►│(windowcapture.py)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
     ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
     │ OkeyDetection   │ │  OkeyGameState  │ │  OkeyStrategy   │
     │(okey_detection.py│ │ (okey_game.py)  │ │ (okey_game.py)  │
     └─────────────────┘ └─────────────────┘ └─────────────────┘
              │                │                
              ▼                ▼                
     ┌─────────────────────────────────────────┐
     │         OkeyCard & OkeyHand             │
     │           (okey_card.py)                │
     └─────────────────────────────────────────┘
```

## Core Components

### 1. Main GUI (`main.py`)
- **Purpose**: User interface and control
- **Features**: 
  - Bot configuration (timing, strategy)
  - Real-time statistics display
  - Debug visualization
  - Start/stop controls

### 2. OkeyBot (`okey_bot.py`)  
- **Purpose**: Main automation controller
- **Responsibilities**:
  - Game cycle management
  - Action decision and execution
  - State synchronization
  - Error handling

### 3. WindowCapture (`windowcapture.py`)
- **Purpose**: Screen capture from Metin2 window
- **Features**:
  - Real-time screenshot capture
  - Window position tracking
  - Screen coordinate translation

### 4. OkeyDetection (`okey_detection.py`)
- **Purpose**: Computer vision for game elements
- **Detects**:
  - Player hand cards
  - Center table card
  - Joker indicator
  - Game buttons and state

### 5. Game Logic (`okey_game.py`, `okey_card.py`)
- **OkeyGameState**: Current game state tracking
- **OkeyStrategy**: Strategic decision making
- **OkeyCard/OkeyHand**: Card representation and management

## Data Flow

### 1. Perception Phase
```
Metin2 Game → WindowCapture → Screenshot → OkeyDetection → Game Elements
```

### 2. Processing Phase  
```
Game Elements → OkeyGameState → OkeyStrategy → Action Decision
```

### 3. Action Phase
```
Action Decision → OkeyBot → Mouse/Keyboard → Metin2 Game
```

## Key Algorithms

### Card Detection
1. **Template Matching**: Compare screen regions to card templates
2. **Color Analysis**: Identify card colors using HSV thresholds  
3. **OCR/Pattern Recognition**: Read card numbers
4. **Position Mapping**: Convert screen coordinates to game positions

### Strategic Decision Making
1. **Hand Evaluation**: Assess current card combinations
2. **Value Scoring**: Rate each card's strategic worth
3. **Risk Assessment**: Balance conservative vs aggressive play
4. **Optimal Selection**: Choose best discard/keep decisions

### Game State Management
1. **State Detection**: Identify current game phase
2. **Turn Recognition**: Detect when it's player's turn
3. **Event Handling**: Respond to game state changes
4. **Memory Management**: Track game history and patterns

## Extension Points

### Custom Strategies
Implement `OkeyStrategy` subclasses for different playing styles:
- Conservative: Minimize risk, slow but steady
- Aggressive: Fast wins, higher risk tolerance  
- Adaptive: Adjust based on opponent behavior

### Enhanced Detection
Improve `OkeyDetection` with:
- Machine learning models for card recognition
- Adaptive thresholds for different lighting
- Multi-resolution template matching
- OCR integration for text detection

### Additional Features
- Multi-table support
- Tournament mode
- Performance analytics
- Player modeling
- Automated training

## Performance Considerations

### Optimization Targets
- **Latency**: Minimize response time for real-time play
- **Accuracy**: Maximize detection and decision quality  
- **CPU Usage**: Efficient image processing and algorithms
- **Memory**: Minimize footprint for long-running sessions

### Bottlenecks
1. **Image Processing**: Screenshot capture and analysis
2. **Template Matching**: Computationally expensive
3. **Strategy Calculation**: Complex decision algorithms
4. **I/O Operations**: Mouse/keyboard input timing

### Solutions
- **Caching**: Store processed templates and regions
- **Optimization**: Use efficient OpenCV operations
- **Threading**: Separate detection and action threads
- **Profiling**: Monitor and optimize hot paths

## Error Handling

### Recovery Strategies
1. **Detection Failures**: Retry with different thresholds
2. **Action Timeouts**: Fall back to safe defaults
3. **Game State Errors**: Reset and resynchronize
4. **System Errors**: Graceful degradation and logging

### Monitoring
- Performance metrics collection
- Error rate tracking  
- Success/failure analysis
- Debug visualization and logging