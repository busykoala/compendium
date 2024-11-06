import logging
import sys

from pythonjsonlogger import jsonlogger

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to desired log level

# Create handler for stdout
stream_handler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(name)s %(levelname)s %(message)s"
)
stream_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(stream_handler)
logger.propagate = False

# Test log (optional)
logger.info("Logger initialized successfully.")
