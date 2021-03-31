import json
# import logging
import logging.config

"""
로깅 수준
CRITICAL; 50
ERROR; 40
WARNING; 30
INFO; 20
DEBUG; 10
NOTSET; 0
"""

with open('logging.json', 'rt') as f:
    logging.config.dictConfig(json.load(f))
logger = logging.getLogger('file')
# logger.setLevel(logging.CRITICAL)
# logger.setLevel(logging.ERROR)
# logger.setLevel(logging.WARNING)
# logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)
