# -*- encoding: utf-8 -*-


from mod_log import logger

LOG_INFO = True
LOG_WARNING = True
LOG_ERR = True


def loginfo(msg, *args, **kwargs):
    global LOG_INFO
    if LOG_INFO:
        logger.info(msg, *args, **kwargs)


def logwarning(msg, *args, **kwargs):
    global LOG_WARNING
    if LOG_WARNING:
        logger.warning(msg, *args, **kwargs)


def logerror(msg, *args, **kwargs):
    global LOG_ERR
    if LOG_ERR:
        logger.error(msg, *args, **kwargs)
