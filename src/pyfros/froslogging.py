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


def __args_to_str(*args):
    return ",".join(map(str, args))


def info(*args):
    if VERBOSITY > 1:
        LOGGER.info(__args_to_str(*args))


def warn(*args):
    if VERBOSITY > 0:
        LOGGER.warn(__args_to_str(*args))


def error(*args):
    LOGGER.error(__args_to_str(*args))
