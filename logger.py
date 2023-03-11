import logging

logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

# create file handler which logs even debug messages
fh = logging.FileHandler('bot.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger.addHandler(fh)


def get_logger():
    return logger
