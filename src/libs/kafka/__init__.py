import logging

logging.getLogger('kafka').setLevel(logging.WARNING)

# imports
from .producer import Producer
