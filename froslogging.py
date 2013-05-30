import logging

VERBOSITY = 0


def set_verbosity(verbosity):
    global VERBOSITY
    VERBOSITY = verbosity


def getLogger():
    logger = logging.getLogger('abrt-screencast')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    #ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(ch)

    return logger

LOGGER = getLogger()


def info(*args):
    if VERBOSITY:
        LOGGER.info(",".join(map(str, args)))


def warn(msg):
    if VERBOSITY:
        LOGGER.warn(msg)


def error(msg):
    LOGGER.error(msg)
