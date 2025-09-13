import logging
import logging.handlers
import os

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure main logger
logger = logging.getLogger('okey_bot')
logger.setLevel(logging.INFO)

# File handler with rotation
file_handler = logging.handlers.RotatingFileHandler(
    'logs/okey_bot.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Performance logger
perf_logger = logging.getLogger('performance')
perf_handler = logging.FileHandler('logs/performance.log')
perf_handler.setFormatter(formatter)
perf_logger.addHandler(perf_handler)
perf_logger.setLevel(logging.DEBUG)