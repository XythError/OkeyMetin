# Bot Logs Directory

This directory contains log files from bot operation.

## Log Files

### Automatic Logs
- `okey_bot.log` - Main bot activity log
- `performance.log` - Performance metrics and timing
- `errors.log` - Error messages and exceptions
- `games_YYYYMMDD.log` - Daily game results

### Statistics Files
- `game_stats.json` - Game statistics in JSON format
- `strategy_analysis.txt` - Strategy performance analysis

## Log Levels

- **DEBUG**: Detailed operational information
- **INFO**: General bot activities
- **WARNING**: Issues that don't stop operation
- **ERROR**: Serious problems requiring attention

## Configuration

Logging can be configured in the main bot settings:

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    filename='logs/okey_bot.log',
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

## Rotation

Logs are automatically rotated to prevent excessive disk usage. Old log files are compressed and archived.